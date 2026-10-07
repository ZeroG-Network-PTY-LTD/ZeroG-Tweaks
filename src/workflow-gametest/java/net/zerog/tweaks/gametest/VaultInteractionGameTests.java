package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.Tag;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.Mirror;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.BlockHitResult;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.arena.ConcordLockBlock;
import net.zerog.tweaks.arena.ConcordPrismBlock;
import net.zerog.tweaks.arena.VaultKeyAltarBlock;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.EntityInit;
import net.zerog.tweaks.registry.ItemInit;

/** Public block interactions in disposable fixtures; not natural encounters or combat approval. */
@GameTestHolder("zerog_galaxy_access") @PrefixGameTestTemplate(false)
public final class VaultInteractionGameTests {
    @GameTest(templateNamespace="zerog_galaxy_access",template="equipment_empty",timeoutTicks=200)
    public static void four_altars_yield_one_key_each_and_do_not_duplicate_guardians(GameTestHelper h) {
        var level=h.getLevel();
        var player=h.makeMockPlayer(GameType.SURVIVAL);
        var base=h.absolutePos(new BlockPos(4,2,4));
        // Separate bounded pads allow the actual guardian-spawn checks to run.
        for(int altar=0;altar<4;altar++) {
            var pos=base.offset(altar*10,0,0);
            for(var at:BlockPos.betweenClosed(pos.offset(-4,0,-4),pos.offset(4,3,4)))
                level.setBlock(at,Blocks.AIR.defaultBlockState(),2);
            for(var at:BlockPos.betweenClosed(pos.offset(-4,-1,-4),pos.offset(4,-1,4)))
                level.setBlock(at,Blocks.STONE.defaultBlockState(),2);
            level.setBlock(pos,BlockInit.VAULT_KEY_ALTAR.get().defaultBlockState(),3);
            player.setPos(pos.getCenter().add(0,0,2));
            var hit=new BlockHitResult(pos.getCenter(),Direction.UP,pos,false);
            level.getBlockState(pos).useWithoutItem(level,player,hit);
            h.assertTrue(!level.getBlockState(pos).getValue(VaultKeyAltarBlock.HAS_KEY),"Claimed altar retained its key");
            int claimed=0;
            for(var stack:player.getInventory().items)if(stack.is(ItemInit.CONCORD_VAULT_KEY.get()))claimed+=stack.getCount();
            h.assertTrue(claimed==altar+1,"Altar failed to award exactly one key");
            var area=new AABB(pos).inflate(4);
            long guardians=level.getEntitiesOfClass(net.minecraft.world.entity.Mob.class,area)
                    .stream().filter(m->m.getType()==EntityInit.PRISMLING_HOLDER.get()).count();
            h.assertTrue(guardians==VaultKeyAltarBlock.GUARDIANS,"Altar did not awaken three room guardians");
            level.getBlockState(pos).useWithoutItem(level,player,hit);
            int repeated=0;
            for(var stack:player.getInventory().items)if(stack.is(ItemInit.CONCORD_VAULT_KEY.get()))repeated+=stack.getCount();
            h.assertTrue(repeated==claimed,"Empty altar duplicated a key");
            h.assertTrue(level.getEntitiesOfClass(net.minecraft.world.entity.Mob.class,area).stream()
                    .filter(m->m.getType()==EntityInit.PRISMLING_HOLDER.get()).count()==guardians,"Empty altar duplicated guardians");
            level.getEntitiesOfClass(net.minecraft.world.entity.Mob.class,area).forEach(net.minecraft.world.entity.Entity::discard);
        }
        h.succeed();
    }

    @GameTest(templateNamespace="zerog_galaxy_access",template="equipment_empty",timeoutTicks=1200)
    public static void four_consumed_keys_construct_authored_stages_in_all_facings(GameTestHelper h) {
        var level=h.getLevel();var player=h.makeMockPlayer(GameType.SURVIVAL);
        int orientation=0;
        for(var facing:new Direction[]{Direction.SOUTH,Direction.WEST,Direction.NORTH,Direction.EAST}) {
            // Large authored chamber templates must not overwrite other GameTest fixtures.
            var pos=new BlockPos(16000+orientation++*96,128,16000);
            level.setBlock(pos,BlockInit.CONCORD_LOCK.get().defaultBlockState().setValue(ConcordLockBlock.FACING,facing),3);
            player.setPos(pos.getCenter().add(0,0,2));
            var hit=new BlockHitResult(pos.getCenter(),Direction.UP,pos,false);
            player.setItemInHand(InteractionHand.MAIN_HAND,new ItemStack(Items.DIAMOND,4));
            level.getBlockState(pos).useItemOn(player.getMainHandItem(),level,player,InteractionHand.MAIN_HAND,hit);
            h.assertTrue(level.getBlockState(pos).getValue(ConcordLockBlock.STAGE)==0
                    &&player.getMainHandItem().getCount()==4,"Non-key item changed the lock or was consumed");
            player.setItemInHand(InteractionHand.MAIN_HAND,new ItemStack(ItemInit.CONCORD_VAULT_KEY.get(),4));
            for(int key=1;key<=4;key++) {
                level.getBlockState(pos).useItemOn(player.getMainHandItem(),level,player,InteractionHand.MAIN_HAND,hit);
                h.assertTrue(player.getMainHandItem().getCount()==4-key,"Lock did not consume precisely one survival key");
                if(key<4) {
                    h.assertTrue(level.getBlockState(pos).is(BlockInit.CONCORD_LOCK.get())
                            &&level.getBlockState(pos).getValue(ConcordLockBlock.STAGE)==key,"Lock advanced incorrectly");
                    var template=level.getStructureManager().get(ResourceLocation.parse("zerog_tweaks:concord_vault/chamber_stage_"+key)).orElseThrow();
                    var data=template.save(new CompoundTag());var palette=data.getList("palette",Tag.TAG_COMPOUND);
                    int checked=0;
                    for(var entry:data.getList("blocks",Tag.TAG_COMPOUND)) {
                        var block=(CompoundTag)entry;
                        var id=ResourceLocation.parse(palette.getCompound(block.getInt("state")).getString("Name"));
                        if(!id.getNamespace().equals("zerog_tweaks")||id.getPath().equals("concord_lock"))continue;
                        var xyz=block.getList("pos",Tag.TAG_INT);
                        var relative=new BlockPos(xyz.getInt(0),xyz.getInt(1),xyz.getInt(2));
                        var at=pos.subtract(ConcordLockBlock.TEMPLATE_PIVOT).offset(StructureTemplate.transform(
                                relative,Mirror.NONE,ConcordLockBlock.rotationOf(facing),ConcordLockBlock.TEMPLATE_PIVOT));
                        h.assertTrue(level.getBlockState(at).is(BuiltInRegistries.BLOCK.get(id)),
                                "Authored stage "+key+" missing "+id+" at "+at+" facing "+facing);
                        checked++;
                    }
                    h.assertTrue(checked>0,"Stage test inspected no authored blocks");
                }else {
                    h.assertTrue(level.getBlockState(pos).is(BlockInit.CONCORD_PRISM.get())
                            &&level.getBlockState(pos).getValue(ConcordPrismBlock.STATE)==ConcordPrismBlock.State.IDLE,
                            "Fourth key did not create an idle Concord Prism");
                    h.assertTrue(level.getBlockEntity(pos) instanceof net.zerog.tweaks.arena.ConcordPrismBlockEntity,
                            "Fourth key created a decorative block without encounter backend");
                    var prism=(net.zerog.tweaks.arena.ConcordPrismBlockEntity)level.getBlockEntity(pos);
                    level.getBlockState(pos).useWithoutItem(level,player,hit);
                    h.assertTrue(prism.state()==ConcordPrismBlock.State.ACTIVE,"Prism click did not start the test");
                    h.assertTrue(!prism.start(level),"Active Prism accepted a second start");
                    // Exercise the registered ticker's work without certifying real-time combat.
                    for(int tick=0;tick<net.zerog.tweaks.arena.ConcordPrismBlockEntity.SUMMON_DELAY;tick++)
                        net.zerog.tweaks.arena.ConcordPrismBlockEntity.serverTick(level,pos,level.getBlockState(pos),prism);
                    h.assertTrue(prism.sentinelId()!=null&&level.getEntity(prism.sentinelId())
                            instanceof net.zerog.tweaks.entity.PrismSentinel,"Completed Prism did not summon its Sentinel");
                    h.assertTrue(!prism.isRematch(),"First challenge was incorrectly marked a rematch");
                    level.getEntity(prism.sentinelId()).discard();
                }
            }
        }
        h.succeed();
    }
}
