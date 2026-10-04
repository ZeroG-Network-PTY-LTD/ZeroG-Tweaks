package net.zerog.tweaks.genetics;

import java.lang.reflect.Method;
import java.util.LinkedHashMap;
import java.util.Map;
import net.minecraft.core.component.DataComponents;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.CustomData;
import net.neoforged.neoforge.attachment.AttachmentHolder;

/** Optional, verified PB 13.14.0 cage/attachment bridge. Never invents alleles. */
public final class ProductiveBeeGenes {
    public static final String[] GENES={"productivity","endurance","temper","behavior","weather_tolerance"};
    public static final String ATTACHMENT="productivebees:attributes_handler";
    private static final String ROOT="cy.jdkdigital.productivebees.";
    private static final class Api {
        static final Method FILLED=method(ROOT+"common.item.BeeCage","isFilled",ItemStack.class);
        static final Method BY_NAME=method(ROOT+"util.GeneValue","byName",String.class);
        static final Method NAME=method(ROOT+"util.GeneValue","getSerializedName");
        static final Method NUMBER=method(ROOT+"util.GeneValue","getValue");
        private static Method method(String type,String name,Class<?>... args) {
            try{return Class.forName(type).getMethod(name,args);}catch(ReflectiveOperationException|LinkageError ex){return null;}
        }
    }
    public static boolean valid(String gene,String value) {
        if(value.isEmpty()||value.length()>64||Api.BY_NAME==null||Api.NAME==null)return false;
        try {
            Object allele=Api.BY_NAME.invoke(null,value);
            if(allele==null||!value.equals(Api.NAME.invoke(allele)))return false;
            String enumName=((Enum<?>)allele).name();
            return switch(gene) {
                case "productivity"->enumName.startsWith("PRODUCTIVITY_");
                case "endurance"->enumName.startsWith("ENDURANCE_");
                case "temper"->enumName.startsWith("TEMPER_");
                case "behavior"->enumName.startsWith("BEHAVIOR_");
                case "weather_tolerance"->enumName.startsWith("WEATHER_TOLERANCE_");
                default->false;
            };
        }catch(ReflectiveOperationException|ClassCastException ex){return false;}
    }
    public static int numeric(String value) {
        try{return (Integer)Api.NUMBER.invoke(Api.BY_NAME.invoke(null,value));}
        catch(ReflectiveOperationException|NullPointerException ex){return -1;}
    }
    public static Map<String,String> read(ItemStack stack) {
        var result=new LinkedHashMap<String,String>();
        try {
            if(Api.FILLED==null||!(Boolean)Api.FILLED.invoke(null,stack))return result;
            var data=stack.get(DataComponents.CUSTOM_DATA);if(data==null)return result;
            CompoundTag tag=data.copyTag().getCompound(AttachmentHolder.ATTACHMENTS_NBT_KEY).getCompound(ATTACHMENT);
            for(String gene:GENES){String value=tag.getString("bee_"+gene);if(!valid(gene,value))return Map.of();result.put(gene,value);}
        }catch(ReflectiveOperationException|LinkageError ex){return Map.of();}
        return result;
    }
    public static ItemStack analyse(ItemStack source) {
        if(read(source).size()!=5)return ItemStack.EMPTY;
        ItemStack copy=source.copyWithCount(1);
        var tag=copy.get(DataComponents.CUSTOM_DATA).copyTag();
        tag.putBoolean("zerog_tweaks:analysed",true);
        copy.set(DataComponents.CUSTOM_DATA,CustomData.of(tag));return copy;
    }
    public static ItemStack splice(ItemStack source,String gene,String value) {
        if(read(source).size()!=5||!valid(gene,value))return ItemStack.EMPTY;
        ItemStack copy=analyse(source);var tag=copy.get(DataComponents.CUSTOM_DATA).copyTag();
        // CopyTag protects the original; all identity, bee type and other attachments survive.
        tag.getCompound(AttachmentHolder.ATTACHMENTS_NBT_KEY).getCompound(ATTACHMENT).putString("bee_"+gene,value);
        copy.set(DataComponents.CUSTOM_DATA,CustomData.of(tag));return copy;
    }
    private ProductiveBeeGenes(){}
}
