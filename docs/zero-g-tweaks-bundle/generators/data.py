# palettes: outline, dark, mid, light, highlight, accent
STONES={
 'deepslate':['#1e1e24','#2c2c34','#3a3a44','#4a4a56'],
 'lunar_stone':['#6c6c70','#86868a','#9e9ea2','#b6b6b8'],
 'martian_stone':['#4a1e12','#6a2c1a','#843a22','#9c4c2e'],
 'cerulean_stone':['#1b2638','#2c3d57','#3b5170','#4c6588'],
 'skarn_rock':['#141010','#211b19','#2e2624','#3d3330'],
 'permafrost':['#6a7a86','#86969f','#a2b1b8','#c0ccd2'],
 'solar_stone':['#3a1a0e','#5a2a14','#7a3c1a','#9a5222'],
}
M={}
def mat(k,name,pal,role,stone,desc,src,use,glow=False): M[k]=dict(name=name,pal=pal,role=role,stone=stone,desc=desc,src=src,use=use,glow=glow)
# ---- Sol
mat('nullifite','Nullifite',['#0b0712','#1a1226','#2e2240','#4a3a66','#d9c8ff','#b48cff'],'metal','deepslate',
 'Near-black metal split by violet-white fracture lines.','Deepslate ore, Y -64 to -40; more in the Deep Dark','T1 teleporter, Nullifite gear',True)
mat('regolith','Regolith Dust',['#2a2a2e','#6e6e74','#9a9aa0','#c4c4c8','#ecece8','#ffffff'],'dust','lunar_stone',
 'Fine grey moon dust.','Moon surface','Smelts into Lunar Glass')
mat('moonsteel','Moonsteel',['#1d2126','#5b6470','#8a95a3','#b8c3cf','#eef4fa','#a8d8ff'],'metal','lunar_stone',
 'Pale blue-grey steel with a cold sheen.','Moon ore, mid-depth','T2 frames, Olympium gear alloy')
mat('selenite','Selenite',['#3a3f52','#8f9ab8','#c2cbe6','#e2e8f7','#ffffff','#d8e4ff'],'crystal','lunar_stone',
 'Milky pale crystal that catches light.','Moon deep geodes','T2 focus lens, Selenite Lamp')
mat('ferrox','Ferrox',['#2a120b','#6e2c17','#9c4424','#c4683a','#e89a62','#ffc28a'],'metal','martian_stone',
 'Rust-red iron-oxide metal.','Mars ore, common','Basic Mars parts')
mat('olympium','Olympium',['#1f1413','#553531','#7f5048','#a8766a','#d8b0a0','#ffd8c8'],'metal','martian_stone',
 'Dense bronze-red heavy metal.','Mars ore, deep','Olympium gear, Olympium Plating')
mat('aresite','Aresite',['#2b0508','#7a1016','#b01e24','#e0443c','#ff9a8a','#ffd0c8'],'diamond','martian_stone',
 'Deep red cut gem with a bright core.','Mars ore, rare and deep','T2 core')
# ---- planets: (key,name,pal,role,desc,src,use)
PL={
'cerulon':('Cerulon','Galaxy 2','cerulean_stone',[
 ('nebulite','Nebulite',['#070b1c','#141f3d','#22335e','#34508a','#5a7cc0','#6fe0ff'],'fuel','Dark blue coal with glowing cyan specks.','Cerulon ore, Y 0 to 192','Fuel, burns twice as long as coal',True),
 ('cobaltium','Cobaltium',['#0f1b33','#2b4a7c','#3f68a8','#6a95d1','#b5d4f5','#d8ecff'],'metal','Bright cobalt-blue common metal.','Cerulon ore, common','Basic parts and wiring',False),
 ('cyrrium','Cyrrium',['#141c24','#3e5566','#5f7f94','#8fb0c2','#d5eaf2','#9ff0ff'],'metal','Blue-tinted steel.','Cerulon ore, Y -24 to 56','Frames, T1 machine casings',False),
 ('aurelion','Aurelion',['#2a2a1c','#8a8a6a','#bdbb94','#e0dcb8','#fbf8e6','#ffffff'],'metal','Pale champagne precious metal.','Cerulon ore, deep','Circuits and upgrades',False),
 ('pulsar_dust','Pulsar Dust',['#0d1d33','#1c4f8a','#2f7fd0','#5fb6ff','#b8e6ff','#ffffff'],'dust','Blue dust that pulses with light.','Cerulon ore, drops 4–5','Teleporter coils, Pulsar Lamp',True),
 ('starlite','Starlite',['#16163a','#3c3c9a','#5f5fd0','#9696f0','#dcdcff','#fff4a0'],'orb','Indigo orb holding a tiny star.','Cerulon ore, drops 4–8','Star charts, enchanting, Codex',True),
 ('cerulite','Cerulite',['#062431','#0d5f7c','#1592b8','#3fc9e8','#b0f2ff','#ffffff'],'diamond','Cyan cut gem; the key to T3.','Cerulean geodes, rare','T3 teleporter, Cerulite gear',False),
 ('lumenite','Lumenite',['#0b2a2a','#1a7a6e','#2fb39e','#6fe0c8','#d0fff2','#ffffff'],'crystal','Sea-green trade crystal.','Crystal-field terrain only','Alien trader currency',False)]),
'skarn':('Skarn','Galaxy 3','skarn_rock',[
 ('emberite','Emberite',['#0c0908','#1e1715','#302522','#45352f','#5a4740','#ff8a2a'],'fuel','Charcoal lump with ember seams.','Skarn ore, lava contact zones','Hot fuel',True),
 ('ruskite','Ruskite',['#260e08','#6a2a18','#9a3f22','#c25d34','#e89060','#ffc090'],'metal','Rust-red basic metal.','Skarn ore, common','Basic parts',False),
 ('tectium','Tectium',['#151312','#3e3834','#5c5550','#827a73','#b5ada5','#ffb070'],'metal','Heavy grey plate metal.','Skarn ore, mid-depth','Frames, T2 machine casings, Skarnite gear',False),
 ('pyrium','Pyrium',['#2c1604','#8a4a0a','#c67514','#f0a52a','#ffe07a','#fff4c8'],'metal','Fire-gold precious metal.','Skarn ore, deep','High-tier circuits',False),
 ('tremor_dust','Tremor Dust',['#2a1206','#7a3208','#c05a10','#f08a28','#ffd08a','#fff0c0'],'dust','Crackling orange spark dust.','Skarn ore, drops 4–5','Energy efficiency, Tremor Lamp',True),
 ('rift_opal','Rift Opal',['#140a1e','#3a1f52','#5e3a80','#8c6ab0','#d8c4ff','#7af0ff'],'orb','Violet opal with a void swirl.','Skarn ore, drops 4–8','Lore, enchanting',True),
 ('skarnite','Skarnite',['#1e0802','#6e1e06','#b0380c','#e8661e','#ffb070','#fff0d0'],'diamond','Molten-orange cut gem; the key to T4.','Skarn ore, rare, near lava','T4 teleporter, Skarnite gear',False),
 ('cinnabrite','Cinnabrite',['#2a0508','#8a0e1e','#c42032','#ee4c56','#ffa8a8','#ffffff'],'crystal','Blood-red trade crystal.','Scorched Marble zones only','Alien trader currency',False)]),
'eidolon':('Eidolon','Galaxy 4','permafrost',[
 ('cryocite','Cryocite',['#0a1a24','#1c4a60','#2e7a96','#5cb4d0','#bff0ff','#e8ffff'],'fuel','Frozen fuel that burns cold blue.','Eidolon ore','Cold fuel',True),
 ('salvium','Salvium',['#1a1c1e','#4a4e52','#6e7378','#9aa0a6','#cfd4d8','#d49a5a'],'metal','Scrap metal flecked with rust.','Wrecks; small veins','Basic parts, Salvage Station',False),
 ('wraithsteel','Wraithsteel',['#1c2226','#5e6e74','#8ea2a8','#c0d2d6','#f0fbfc','#9ff0f0'],'metal','Pale ghostly steel.','Eidolon ore, mid-depth','Frames, T3 machine casings, Eidolite gear',False),
 ('palladine','Palladine',['#26282c','#8a8e96','#bfc3cb','#e2e5ea','#ffffff','#e8f4ff'],'metal','Bright white precious metal.','Eidolon ore, deep','Circuits and upgrades',False),
 ('spectral_dust','Spectral Dust',['#0c2226','#1e6068','#3aa4ac','#78dde0','#d0fbfb','#ffffff'],'dust','Faintly glowing ghost dust.','Eidolon ore, drops 4–5','Energy efficiency, Spectral Lantern',True),
 ('remnant_shard','Remnant Shard',['#101820','#2a4050','#46687e','#7aa2b8','#d0e8f4','#7ae8ff'],'orb','Memory fragment of the lost fleet.','Eidolon ore, Broken Consoles','Crew logs, Codex',True),
 ('eidolite','Eidolite',['#062028','#0e5a66','#1a98a4','#56d8dc','#d0ffff','#ffffff'],'diamond','Ice-cyan cut gem; the key to T5.','Eidolon ore, rare','T5 teleporter, Eidolite gear',False),
 ('rimeglass','Rimeglass',['#1a2a34','#5a7a8c','#90b4c4','#c4e0ec','#f4fcff','#ffffff'],'crystal','Frosted trade crystal.','Glacier terrain only','Alien trader currency',False)]),
'solvane':('Solvane','Galaxy 5','solar_stone',[
 ('coronite','Coronite',['#2a0a02','#7a1e02','#c44a06','#f08a14','#ffd060','#ffffff'],'fuel','Solar plasma frozen into rock.','Solvane ore, near molten flows','Strongest fuel in the mod',True),
 ('photium','Photium',['#3a3424','#a09a78','#d4cfa8','#f0ecc8','#fffef0','#fff6b0'],'metal','Light metal with a faint glow.','Solvane ore, common','Basic endgame parts',True),
 ('astrium','Astrium',['#1a1420','#4e4258','#7a6c88','#aa9cba','#e6dcf4','#ffd070'],'metal','Star-forged violet steel.','Solvane ore, mid-depth','Endgame frames, T4 machine casings, Solvanite gear',False),
 ('radiantine','Radiantine',['#3a2200','#a86a00','#e0a010','#ffd040','#fff4a8','#ffffff'],'metal','Gold that gives off light.','Solvane ore, deep','Top-tier circuits, Radiant Bricks',True),
 ('fusion_dust','Fusion Dust',['#3a0a04','#a02a08','#e06010','#ffa030','#fff0a0','#ffffff'],'dust','White-hot energy dust.','Solvane ore, drops 4–5','Fusion Reactor, T6 power',True),
 ('nova_pearl','Nova Pearl',['#2a1426','#7a3a6e','#b86aa4','#e8a8d4','#fff0fa','#ffffff'],'orb','Rose pearl holding the last chapter.','Solvane ore, drops 4–8','Final Codex chapter',True),
 ('solvanite','Solvanite',['#2a0204','#8a0a10','#d02818','#ff7030','#ffe0a0','#ffffff'],'diamond','Crimson-gold cut gem; the key to T6.','Solvane ore, rare','T6 teleporter, Solvanite gear',False),
 ('dawnstone','Dawnstone',['#2a1a08','#a0602a','#e09a50','#ffc890','#fff2e0','#ffffff'],'crystal','Peach-gold dawn crystal.','Sunspot Rock terrain only','Rarest trader currency',False)]),
}
for pk,(pn,gal,st,lst) in PL.items():
    for (k,n,p,r,d,s,u,g) in lst: mat(k,n,p,r,st,d,s,u,g)
