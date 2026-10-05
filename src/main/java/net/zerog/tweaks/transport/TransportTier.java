package net.zerog.tweaks.transport;

public record TransportTier(String name,int energy,int fluid,int items,int interval,int capacity) {
    public static final TransportTier[] ALL={new TransportTier("copper",1000,250,4,20,400000),new TransportTier("nullifite",8000,1000,8,10,2000000),new TransportTier("cyrrium",64000,4000,16,5,10000000),new TransportTier("tectium",512000,16000,32,3,50000000),new TransportTier("wraithsteel",4096000,64000,64,2,250000000),new TransportTier("astrium",32768000,256000,64,1,1250000000)};
    public static int minimumFluidTier(String id){if(id.contains("solar_plasma"))return 5;if(id.contains("cryo"))return 4;if(id.contains("magma_slag"))return 3;if(id.contains("acid"))return 2;if(id.contains("null_fluid"))return 1;return 0;}
}
