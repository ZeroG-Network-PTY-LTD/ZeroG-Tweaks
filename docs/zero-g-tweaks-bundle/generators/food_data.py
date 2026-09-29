# masks: letters map to colors per item; '.' empty
MASK={
'steak':["................","................",".....HHHHH......","...HHHHHHHHH....","..HHHAHHHHHHH...","..HHHHHHHHHHHH..",".HHHHHHHAHHHHH..",".HHHHHHHHHHHHH..",".HHHAHHHHHHHHH..","..HHHHHHHHHHHH..","...HHHHHHHHHH...",".....HHHHHHH...."],
'cooked_steak':["................","................",".....HHHHH......","...HHGHHHGHH....","..HHGHHHGHHHH...","..HGHHHGHHHGHH..",".HGHHHGHHHGHHH..",".HHHHGHHHGHHHH..",".HHHGHHHGHHHHH..","..HGHHHGHHHHHH..","...HHHGHHHHH....",".....HHHHHHH...."],
'drumstick':["................","......HHHH......","....HHHHHHH.....","...HHHAHHHHH....","...HHHHHHHHH....","...HHHHHHHAH....","....HHHHHHH.....",".....HHHHH......","......WWW.......","......WW........",".....WWW........","....WWWW........","....WW.........."],
'fish':["................","................","................",".....HHHHH......","...HHHHHHHHH..G.","..HAHHHHHHHHHGG.",".HHHHHHHHHHHHGG.","..HHHHHHHHHHHGG.","...HHHHHHHHH..G.",".....HHHHH......"],
'fillet':["................","................","................","................","..HHHHHHHHHHH...",".HHAHHHHHHHHHH..",".HHHHHHHHHAHHH..","..HHHHHHHHHHH..."],
'egg':["................","................","......HHH.......",".....HHHHH......","....HHHHHHH.....","....HHAHHHH.....","...HHHHHHHHH....","...HHHHHHAHH....","...HHHHHHHHH....","....HHHHHHH.....",".....HHHHH......"],
'berries':["................",".......GG.......","......GG........","....HH..HH......","...HHHH.HHHH....","...HAHH.HAHH....","....HH.HHHHH....","......HHHH......","......HAHH......",".......HH......."],
'tuber':["................","................","................",".....HHHH.......","...HHHHHHHH.....","..HHAHHHHHHH....","..HHHHHHHAHHH...","...HHHHHHHHHH...","....HHAHHHHH....",".....HHHHHH....."],
'seeds':["................","...HH......HH...","..HHH.....HHH...","..HH..HH..HH....",".....HHH........",".....HH...HH....","..HH.....HHH....",".HHH.....HH.....",".HH............."],
'crisps':["................","................","................","....HHHHH.......","..HHHHHHHH......","..HHAHHHHHHHH...","...HHHHHHHHHHH..",".....HHHHAHHHH..","......HHHHHHH..."],
'bowl':["................","................","................","................","..HHHHHHHHHHHH..",".WHHHAHHHHAHHHW.",".WWWWWWWWWWWWWW.","..WWWWWWWWWWWW..","...WWWWWWWWWW...",".....WWWWWW....."],
'mug':["................","................","...WWWWWWW......","...WHHHHHW......","...WHHHHHWWW....","...WHHAHHW.W....","...WHHHHHW.W....","...WHHHHHWWW....","...WHHHHHW......","....WWWWW......."],
'bottle':["................","......GG........","......WW........",".....WWWW.......","....WHHHHW......","...WHHHHHHW.....","...WHHAHHHW.....","...WHHHHHHW.....","...WHHHHHHW.....","....WWWWWW......"],
'pie':["................","................","................","....GGGGGGGG....","..GGAGGGGGAGGG..",".GGGGGGAGGGGGGG.",".HHHHHHHHHHHHHH.",".WWWWWWWWWWWWWW.","..WWWWWWWWWWWW.."],
'burger':["................","................","....GGGGGGG.....","..GGAGGGAGGGG...","..GGGGGGGGGGG...","..AAAAAAAAAAA...","..HHHHHHHHHHH...","..HHHHHHHHHHH...","..GGGGGGGGGGG...","...GGGGGGGGG...."],
'jelly':["................","................",".....HHHHH......","...HHHHHHHHH....","..HHHHHAHHHHH...","..HHHHAAAHHHH...","..HHHHHAHHHHH...","..HHHHHHHHHHH...",".WWWWWWWWWWWWW.."],
'ration':["................","................","..WWWWWWWWWW....","..WHHHHHHHHW....","..WHAAAAAAHW....","..WHHHHHHHHW....","..WHHGGGGHHW....","..WHHHHHHHHW....","..WHHHHHHHHW....","..WWWWWWWWWW...."],
'fruit':["................",".......G........","......GGG.......","....HHHHHH......","...HHAHHHHH.....","..HHHHHHHHHH....","..HHHHHHHHHH....","..HHHHHHHAHH....","...HHHHHHHH.....","....HHHHHH......"],
'tail':["................","............HH..","...........HHH..",".........HHHH...",".......HHHHH....",".....HHHHHA.....","...HHHHHHH......","..HHHHHH........",".HHHHH..........",".HHH............"],
'claw':["................","......HHH.......",".....HHHHH..HH..","....HHHAHH.HHH..","....HHHHHHHHHH..",".....HHHHHHHH...","......HHHHHH....",".......HHH......","......WW........",".....WW........."],
'leg':[".............HH.","............HHH.","...........HHH..","..........HHH...",".........HHHH...","........WWWW....",".......HHH......","......HHH.......",".....HHH........","....HHH.........","...HHH..........","..HHH..........."],
'chop':["................","................","....HHHHHH......","..HHHHHHHHHH....",".HHHAHHHHHHHH...",".HHHHHHHHHHHH...",".HHHHHHHAHHHH...","..HHHHHHHHHHW...","...HHHHHHHHWWW..",".....HHHHHHWWWW.","..........WW.WW."],
'ribs':["................","................","...HHHHHHHHHH...","..HHHHHHHHHHHH..","..HHHAHHHHAHHH..","..HHHHHHHHHHHH..","..HHHHHHHHHHHH..","..WHWHWHWHWHWH..","..W.W.W.W.W.W..."],
'loin':["................","................","................","...HHHHHHHHH....",".HHHHAHHHHHHHH..",".HHHHHHHHHAHHHH.",".HHHHHHHHHHHHHH.","..HHHHHHHHHHHH..","....HHHHHHHH...."],
'slab':["................","................","....HHHHHHH.....","..HHHHHHHHHHH...","..HAHHHHHHHHH...","..HHHHHHHAHHH...","..HHHHHHHHHHH...","..HHHHHHHHHHH...","...HHHHHHHHH...."],
'frogleg':["................",".........HH.....","........HHHH....",".......HHAHH....","......HHHHH.....",".....HHHH.......","....HHH.........","....HH..........","....HHH.........","...HHHHH........","..HH.H.HH......."],
'fluff':["................","................","................","......HHH.......","....HHHHHHH.....","..HHHHHAHHHHH...",".HHHHHHHHHHHHH..",".HHHAHHHHHHAHH..","..HHHHHHHHHHH...","....HHHHHHH....."],
'hide':["................","................","..HH......HH....","..HHHHHHHHHHH...","...HHHHHHHHH....","..HHHAHHHHHHH...","..HHHHHHHAHHH...","...HHHHHHHHH....","..HHHHHHHHHHH...","..HH......HH...."],
'feather':["................","............HH..","..........HHHH..",".........HHAHH..","........HHAHH...",".......HHAHH....","......HHAHH.....",".....HHAHH......","....HHAHH.......","....HAHH........","...WW...........","..WW............"],
'scale':["................","................","....HHHHHHH.....","...HHHHHHHHH....","...HHAAAAAHH....","...HHHHHHHHH....","....HHAAAHH.....",".....HHHHH......","......HHH.......",".......H........"],
'tusk':["................","..HH............","..HHH...........","...HHH..........","...HHHH.........","....HHHH........",".....HHHHH......","......HHHHHH....","........HHHHH...","..........HHH..."],
'shell':["................","................","................",".....HHHHHH.....","...HHAHHHHAHH...","..HHHHHAHHHHHH..","..HHAHHHHHAHHH..",".HHHHHHAHHHHHHH.",".WWWWWWWWWWWWWW."],
'gel':["................","................","......HHHH......","....HHHHHHHH....","...HHAAHHHHHH...","...HAHHHHHHHH...","...HHHHHHHHHH...","....HHHHHHHH....","......HHHH......"],
'skin':["................","................","......HHHHHH....","....HHAHHAHHH...","...HHHHHHHHH....","..HHHAHHAHH.....","..HHHHHHHH......","...HHAHHAHHH....","....HHHHHHHHH...","......HHHHH....."],
'gland':["................","................",".......WW.......","......HHHH......","....HHHHHHHH....","...HHHAAHHHHH...","...HHAAHHHHHH...","...HHHHHHHHHH...","....HHHHHHHH....","......HHHH......"],
}
# ---------- foods: key, name, mask, colors(H,G,A,W), source, hunger, sat, effect, world
F=[]
def f(k,n,mask,H,A='#ffffff',G=None,W='#e8e0cc',src='',hun=0,sat=0.0,eff='',world='',kind='food'):
    F.append(dict(k=k,n=n,mask=mask,H=H,A=A,G=G or H,W=W,src=src,hun=hun,sat=sat,eff=eff,world=world,kind=kind))
BONE='#e8e0cc'
# meats
pairs=[('crawler_leg','Crawler Leg','leg','#a8a0a0','#6fe0ff','Regolith Crawler','Moon','roasted','Roasted Crawler Leg','#c89a6a'),
('hopper_meat','Hopper Meat','drumstick','#e89aa0','#ffd0d4','Moon Hopper','Moon','cooked','Cooked Hopper','#b8744a'),
('grazer_steak','Grazer Steak','steak','#c8483a','#f4c0b0','Dust Grazer','Mars','seared','Seared Grazer Steak','#8a4a28'),
('beetle_grub','Beetle Grub','tuber','#e8d0a0','#fff0d0','Rust Beetle','Mars','toasted','Toasted Grub','#c08a40'),
('stag_venison','Stag Venison','loin','#b04050','#e8a0b0','Crystal Stag','Cerulon','cooked','Cooked Venison','#7a4a30'),
('fowl','Raw Fowl','drumstick','#8ab0e0','#d8ecff','Azure Fowl','Cerulon','roast','Roast Fowl','#c08040'),
('glimmerfish','Glimmerfish','fish','#3fc9e8','#ffffff','Glimmerfish','Cerulon','cooked','Cooked Glimmerfish','#c8904a'),
('boar_chop','Boar Chop','chop','#d05848','#ffc0a8','Slag Boar','Skarn','smoked','Smoked Boar Chop','#6a3a20'),
('scorch_tail','Scorch Tail','tail','#e8661e','#ffd070','Scorch Wyrmling','Skarn','grilled','Grilled Scorch Tail','#8a3a14'),
('yak_meat','Yak Meat','ribs','#c05060','#f0c8d0','Frost Yak','Eidolon','roast','Yak Roast','#7a5030'),
('gildcrab_meat','Gildcrab Meat','claw','#f0a060','#fff0d0','Gildcrab','Solvane','cooked','Cooked Gildcrab','#e07a30'),
('eel_fillet','Eel Fillet','fillet','#9aa0a8','#e0e8f0','Deep Eel','Ocean wasteland','cooked','Cooked Eel','#b88a50'),
('burrower_steak','Burrower Steak','slab','#c8a060','#f0e0b0','Dune Burrower','Desert wasteland','cooked','Cooked Burrower Steak','#8a6a30'),
('lurker_leg','Lurker Leg','frogleg','#8aa060','#d0e0a0','Bog Lurker','Toxic wasteland','crispy','Crispy Lurker Leg','#a07a30'),
('skitter_leg','Skitter Leg','leg','#c8b080','#fff0c0','Sand Skitter','Desert wasteland','roasted','Roasted Skitter Leg','#a06a30')]
NUT={'drumstick':(2,.3,6,.6),'steak':(3,.3,8,.8),'loin':(3,.3,8,.8),'chop':(3,.3,8,.8),'ribs':(3,.3,8,.8),'slab':(3,.2,7,.7),'frogleg':(2,.2,5,.6),'leg':(2,.2,5,.6),'fish':(2,.1,5,.6),'fillet':(2,.1,6,.8),'tuber':(1,.3,4,.6),'tail':(2,.3,6,.6),'claw':(2,.3,7,.8)}
RAW_EFF={'lurker_leg':'Poison I, 4 s (60%)','scorch_tail':'On fire 2 s','beetle_grub':'Nausea 4 s (30%)','crawler_leg':'Hunger 10 s (30%)'}
COOK_EFF={'grilled_scorch_tail':'Fire Resistance 30 s','cooked_glimmerfish':'Night Vision 30 s','cooked_hopper':'Jump Boost I 20 s','cooked_gildcrab':'Absorption I 20 s'}
for (k,n,m,H,A,src,w,pre,cn,CH) in pairs:
    r1,s1,r2,s2=NUT[m]
    f(k,n,m,H,A,W=BONE,src=f'Drops from {src}',hun=r1,sat=s1,eff=RAW_EFF.get(k,''),world=w,kind='raw')
    ck=cn.lower().replace(' ','_')
    f(ck,cn,m,CH,'#f0d0a0',G='GRILL',W=BONE,src=f'Cook {n}',hun=r2,sat=s2,eff=COOK_EFF.get(ck,''),world=w,kind='cooked')
# forage / crops
f('rust_tuber','Rust Tuber','tuber','#a8502a','#e08a5a',src='Mars crop (plant on Rustsand)',hun=1,sat=.3,world='Mars',kind='crop')
f('baked_tuber','Baked Tuber','tuber','#d8a060','#fff0c0',src='Cook Rust Tuber',hun=5,sat=.6,world='Mars',kind='cooked')
f('lichen_crisps','Lichen Crisps','crisps','#b8c0b0','#e8f0e0',src='Cook Lunar Lichen',hun=2,sat=.3,world='Moon',kind='cooked')
f('skyberries','Skyberries','berries','#5a8ad0','#d8ecff',G='#2e7a4a',src='Skyberry bushes on Cerulon',hun=2,sat=.1,world='Cerulon',kind='crop')
f('shardwood_syrup','Shardwood Syrup','bottle','#3fc9e8','#e8ffff',G='#6a4a30',W='#d8ecf6',src='Tap a Shardwood log with a bottle',hun=4,sat=.3,eff='Speed I 10 s',world='Cerulon',kind='drink')
f('cinder_cap_stew','Cinder Cap Stew','bowl','#e07a2a','#ffd070',W='#6a4a30',src='2 Cinder Caps + bowl',hun=6,sat=.6,eff='Fire Resistance 60 s',world='Skarn',kind='dish')
f('frostfern_tea','Frostfern Tea','mug','#9ad0c0','#e8fff8',W='#c8d8e0',src='2 Frostfern + glass bottle + snowball',hun=2,sat=.4,eff='Freeze immunity 60 s',world='Eidolon',kind='drink')
f('frost_milk','Frost Milk','bottle','#eef8ff','#9ff0ff',G='#c8d8e0',W='#c8d8e0',src='Milk a Frost Yak with a bottle',hun=2,sat=.2,eff='Clears effects; Slowness immunity 30 s',world='Eidolon',kind='drink')
f('blue_egg','Blue Egg','egg','#8ab8e8','#d8ecff',src='Laid by Azure Fowl',hun=0,sat=0,eff='Throw like an egg; baking ingredient',world='Cerulon',kind='ingredient')
f('pyrefruit','Pyrefruit','fruit','#ff7a30','#fff0a0',G='#6a8a30',src='Drops from Pyrevine',hun=4,sat=.4,eff='Glowing 10 s',world='Solvane',kind='crop')
f('solflower_seeds','Solflower Seeds','seeds','#6a4a20','#e8c870',src='Break Solflowers',hun=0,sat=0,eff='Plant to grow Solflowers',world='Solvane',kind='ingredient')
f('roasted_solflower_seeds','Roasted Solflower Seeds','seeds','#a87a40','#fff0c0',src='Cook Solflower Seeds',hun=2,sat=.2,world='Solvane',kind='cooked')
# dishes
f('astronaut_ration','Astronaut Ration','ration','#c8ccd4','#e8661e',G='#5a6070',W='#8a929e',src='Baked Tuber + Seared Grazer Steak + Lichen Crisps',hun=10,sat=1.0,eff='Stacks to 16; eaten twice as fast',world='Sol',kind='dish')
f('orbit_burger','Orbit Burger','burger','#6a3a20','#6ab04a',G='#d8a060',src='Bread + Seared Grazer Steak + Skyberries',hun=10,sat=.9,world='Sol',kind='dish')
f('nebula_pie','Nebula Pie','pie','#5a3a9a','#9ff0ff',G='#d8a060',W='#8a929e',src='Skyberries + Blue Egg + Shardwood Syrup + sugar',hun=8,sat=.5,eff='Night Vision 60 s',world='Cerulon',kind='dish')
f('ember_chili','Ember Chili','bowl','#c02a10','#ffb040',W='#3a2a24',src='Smoked Boar Chop + Grilled Scorch Tail + Cinder Cap + bowl',hun=10,sat=.9,eff='Fire Resistance 3 min, Strength I 30 s',world='Skarn',kind='dish')
f('cryo_chowder','Cryo Chowder','bowl','#e0eef4','#7ae8ff',W='#8a9aa6',src='Yak Roast + Frost Milk + Frostfern + bowl',hun=10,sat=.9,eff='Freeze immunity 3 min, Resistance I 30 s',world='Eidolon',kind='dish')
f('ration_pack','Ration Pack','ration','#6a7a86','#d49a5a',G='#3a464c',W='#4a525a',src='Eidolon wreck loot and Cryo Pods',hun=6,sat=.8,eff='Never spoils; fast to eat',world='Eidolon',kind='dish')
f('starfall_feast','Starfall Feast','bowl','#ffb040','#fff4a8',W='#e0a010',src='Cooked Gildcrab + Pyrefruit + Roasted Solflower Seeds + bowl',hun=12,sat=1.2,eff='Regeneration II 10 s, Absorption II 2 min',world='Solvane',kind='dish')
f('low_g_jelly','Low-G Jelly','jelly','#b48cff','#fff6c0',W='#8a929e',src='Leech Gel + Stardust + sugar',hun=3,sat=.3,eff='Slow Falling 60 s, Jump Boost II 60 s',world='Any',kind='dish')
# materials
M_=[('hopper_fluff','Hopper Fluff','fluff','#eceef2','#ffffff','Moon Hopper','Craft into Moon Wool; string'),
('grazer_hide','Grazer Hide','hide','#9a4a2a','#c47a4a','Dust Grazer','Leather; Ferrox saddles'),
('azure_feather','Azure Feather','feather','#4a8ad0','#d8ecff','Azure Fowl','Arrows; Aurelion gear repair bonus'),
('glimmer_scale','Glimmer Scale','scale','#3fc9e8','#e8ffff','Glimmerfish','Water breathing potion ingredient'),
('boar_tusk','Boar Tusk','tusk','#e6ddd2','#ffffff','Slag Boar','Bone meal x3; Tectium tool upgrade'),
('scorch_scale','Scorch Scale','scale','#e8661e','#ffd070','Scorch Wyrmling','Heatproof Plating ingredient'),
('yak_wool','Yak Wool','fluff','#d8e0e6','#ffffff','Frost Yak','Frost wool blocks; warm cloak'),
('leech_gel','Leech Gel','gel','#6ad0c0','#e8fff8','Ice Leech','Slime ball substitute; Low-G Jelly'),
('gildcrab_shell','Gildcrab Shell','shell','#e0a010','#fff4a8','Gildcrab','Radiantine armor trim; shields'),
('eel_skin','Eel Skin','skin','#5a6a7a','#9ff0f0','Deep Eel','Waterproof leather; Abyssal Pearl'),
('skitter_carapace','Skitter Carapace','shell','#c8a868','#fff0c0','Sand Skitter','Light armor plating'),
('venom_gland','Venom Gland','gland','#8ac040','#e8ff80','Sand Skitter, Bog Lurker','Poison arrows; Neutralizer')]
MAT=[dict(k=a,n=b,mask=c,H=d,A=e,G=d,W='#e8e0cc',src=f'Drops from {g}',use=h) for a,b,c,d,e,g,h in M_]
MASK.update({
'map':["................","................","..HHHHHHHHH.....","..HAAHHHHHHH....","..HHHAHHHGHHH...","..HHHHAAHHHHH...","...HHHHHAHHH....","...HHGHHHAHHH...","..HHHHHHHHHH....","..HHH..HHHH....."],
'plate':["................","................","..WWWWWWWWWWWW..","..WHHHHHHHHHHW..","..WHAHHHHHHAHW..","..WHHHHHHHHHHW..","..WHHHHHHHHHHW..","..WHAHHHHHHAHW..","..WHHHHHHHHHHW..","..WWWWWWWWWWWW.."],
'lens':["................","......WWWW......","....WWHHHHWW....","...WHHAAHHHHW...","...WHAHHHHHHW...","..WHHHHHHHHHHW..","..WHHHHHHHHHHW..","...WHHHHHHHHW...","...WHHHHHHHHW...","....WWHHHHWW....","......WWWW......"],
'dust':["................","..A.........A...","........A.......","....A...........","................","........HH......",".......HHHH.....","......HHHHHH....","....HHHHAHHHHH..","..HHHHHHHHHHHHH.","..HHHHHHHHHHHHH."],
'spark':["................",".......H........",".......H........","......HAH.......","...HHHAAAHHH....","......HAH.......",".......H........",".......H........"],
'core':["................","................",".......HH.......","......HHHH......",".....HHAAHH.....","....HHAAAAHH....","....HHAAAAHH....",".....HHAAHH.....","......HHHH......",".......HH......."],
'lantern':["................","......WWWW......",".......WW.......",".....WWWWWW.....",".....WHHHHW.....",".....WHAAHW.....",".....WHAAHW.....",".....WHHHHW.....",".....WWWWWW....."],
'key':["................","................","..HHHH..........",".HHAAHH.........",".HAAAAHHHHHHHHH.",".HHAAHH....H.H..","..HHHH.....H.H.."],
'orb':["................","................",".....HHHHHH.....","....HHHHHHHH....","...HHAAHHHHHH...","...HAHHHHHHHH...","...HHHHHHHHHH...","...HHHHHHHHHH...","....HHHHHHHH....",".....HHHHHH....."],
})
R_=[('abyssal_pearl','Abyssal Pearl','orb','#1a4a66','#9ff0ff','Sunken Relay (ocean wasteland)','Helmet upgrade: water breathing'),
('star_map_fragment','Star Map Fragment','map','#e0d6b8','#3c3c9a','Buried Observatory, Dune Burrower (rare)','Reveals hidden planets on the star chart'),
('heatproof_plating','Heatproof Plating','plate','#b86a2a','#ffd070','Collapsed Forge, Ash Strider (rare)','Chestplate upgrade: fire resistance'),
('cryo_core','Cryo Core','core','#5cb4d0','#e8ffff','Frozen Outpost, Rime Stalker (rare)','Machine speed upgrade'),
('neutralizer','Neutralizer','bottle','#8ac040','#e8ff80','Sunken Lab, Bog Lurker (rare)','Leggings upgrade: poison immunity'),
('refracting_lens','Refracting Lens','lens','#d8e4ff','#ffffff','Prism Spire (crystal wasteland)','Teleporter upgrade: lower FE cost'),
('stardust','Stardust','dust','#c8c8e0','#fff6c0','Impact Site, Crater Drifter','Universal crafting catalyst; Grav Boots'),
('capacity_coil','Capacity Coil','spark','#3fc9e8','#ffffff','Crafted: Cyrrium + Pulsar Dust','Teleporter upgrade: +2 passengers'),
('rust_shell','Rust Shell','shell','#9c4424','#e89a62','Rust Beetle','Armor upgrade: dust resistance'),
('crystal_hide','Crystal Hide','hide','#2c3d57','#3fc9e8','Crystal Stag','Crystal leather; Cerulon saddles'),
('cinder_pelt','Cinder Pelt','hide','#221c1a','#ff8a2a','Cinder Hound','Fire-proof leather'),
('frost_pelt','Frost Pelt','hide','#dce6ec','#9ff0ff','Rime Stalker','Warm leather; freeze resistance lining'),
('burrower_scale','Burrower Scale','scale','#c8a868','#fff0d0','Dune Burrower','Sand-proof armor plating'),
('solar_spark','Solar Spark','spark','#ffb040','#fff0a0','Flare Sprite','Fuel additive; Fusion Dust crafting'),
('colossus_core','Colossus Core','core','#e08018','#fff0a0','Sun Colossus','Fusion Reactor upgrade'),
('sentinel_prism','Sentinel Prism','core','#1592b8','#e8ffff','Prism Sentinel','T3 teleporter lens upgrade'),
('rift_heart','Rift Heart','core','#5e3a80','#e6dcff','Rift Tyrant','Void-tier crafting; Skarnite gear infusion'),
('captains_lantern','Captain’s Lantern','lantern','#fff0a0','#ffffff','Eidolon Captain (if spared)','Light that reveals Remnant Shards'),
('heart_of_solvane','Heart of Solvane','core','#ff7030','#fff4a8','The Dying Star','Ending choice: Rekindle or Let it fade'),
('galaxy_3_gate_key','Galaxy 3 Gate Key','key','#3fc9e8','#ffffff','Prism Sentinel','Unlocks Galaxy 3 destinations'),
('galaxy_4_gate_key','Galaxy 4 Gate Key','key','#e8661e','#ffffff','Rift Tyrant','Unlocks Galaxy 4 destinations'),
('galaxy_5_gate_key','Galaxy 5 Gate Key','key','#9ff0f0','#ffffff','Eidolon Captain','Unlocks Galaxy 5 destinations')]
REW=[dict(k=a,n=b,mask=c,H=d,A=e,G=d,W='#8a929e',src=g,use=h) for a,b,c,d,e,g,h in R_]
