from mobs_data import both, MOBS as OLD
M2={}
def mob(key,name,info,pal,boxes,stats,notes): M2[key]=dict(name=name,info=info,pal=pal,boxes=boxes,stats=stats,notes=notes)
mob('moon_hopper','Moon Hopper','Moon · passive · hitbox 0.5 × 0.6 blocks',
 dict(fluff='#eceef2',fluff_dk='#b8bcc4',ear='#e8a0b0',eye='#6fe0ff',nose='#e89aa0'),
 [('Moon fluff',-3,2,-3,3,8,5,'fluff','fur'),('Head',-2.5,5,-6,2.5,10,-2,'fluff','noise'),('Nose',-.5,7,-6.3,.5,8,-6,'nose','noise'),('Puff tail',-1,5,5,1,8,7,'fluff','fur')]
 +both(('Long ears',-2,10,-4,-1,16,-3,'fluff_dk','noise'),(None,-1.8,11,-4.2,-1.2,15,-4,'ear','noise'),('Springy hind feet',-3,0,1,-1,2,6,'fluff_dk','noise'),
       ('Front paws',-2,0,-3,-1,2,-2,'fluff_dk','noise'),('Eyes',-2,8,-6.3,-1,9,-6,'eye','glow')),
 [('Health','6 (3 hearts)'),('Behavior','Hops up to 4 blocks high in Moon gravity; flees when hit'),('Breeding','Lunar Lichen'),('Spawns','Moon surface, groups of 2–4'),
  ('Drops','Hopper Meat 0–2, Hopper Fluff 1–2')],['Jump animation: hind feet stretch, ears fold back.','Eyes on the emissive layer.'])
mob('dust_grazer','Dust Grazer','Mars · passive · hitbox 1.3 × 1.4 blocks',
 dict(hide='#9a4a2a',hide_dk='#6e2c17',mane='#c4683a',horn='#e8d0b0',hoof='#2a120b',nose='#3a1a10',eye='#ffc28a'),
 [('Shaggy rust hide',-6,10,-9,6,20,9,'hide','fur'),('Dust mane',-7,14,-10,7,22,-4,'mane','fur'),('Head',-4,10,-16,4,17,-9,'hide_dk','noise'),('Snout',-3,10,-18,3,13,-16,'nose','noise'),
  ('Tail',-1,12,9,1,18,10,'mane','fur')]
 +both(('Curved horns',-8,15,-13,-4,17,-11,'horn','noise'),(None,-8,17,-13,-7,20,-11,'horn','noise'),('Eyes',-4.3,14,-15,-4,15,-14,'eye','glow'),
       ('Legs',-5,2,-7,-2,10,-4,'hide_dk','noise'),(None,-5,2,4,-2,10,7,'hide_dk','noise'),('Hooves',-5,0,-7,-2,2,-4,'hoof','noise'),(None,-5,0,4,-2,2,7,'hoof','noise')),
 [('Health','24 (12 hearts)'),('Behavior','Grazes in herds; the whole herd stampedes if one is hit'),('Breeding','Rust Tuber'),('Spawns','Mars plains, herds of 3–6'),
  ('Drops','Grazer Steak 1–3, Grazer Hide 0–2')],['Mane sways in dust storms.'])
mob('azure_fowl','Azure Fowl','Cerulon · passive · hitbox 0.4 × 0.8 blocks',
 dict(feather='#4a8ad0',feather_lt='#8ab8e8',beak='#e8c870',crest='#3fc9e8',leg='#e8c870',eye='#141f3d'),
 [('Azure feathers',-3,4,-4,3,10,4,'feather','fur'),('Head',-2,9,-6,2,14,-2,'feather_lt','noise'),('Beak',-1,10,-8,1,12,-6,'beak','noise'),
  ('Crystal crest (emissive)',-1,14,-5,1,17,-2,'crest','glow'),('Tail',-2,8,4,2,13,6,'feather','fur')]
 +both(('Wings',-4,5,-3,-3,9,3,'feather_lt','fur'),('Legs',-2,0,-1,-1,4,0,'leg','noise'),('Eyes',-2.3,12,-4,-2,13,-3,'eye','noise')),
 [('Health','4 (2 hearts)'),('Behavior','Glides slowly when falling; lays a Blue Egg every 5–10 minutes'),('Breeding','Skyberries'),('Spawns','Cerulon moss plains and Shardwood forests'),
  ('Drops','Raw Fowl 1, Azure Feather 0–2')],['Crest on the emissive layer.'])
mob('glimmerfish','Glimmerfish','Cerulon · passive (water) · hitbox 0.5 × 0.4 blocks',
 dict(scale='#3fc9e8',scale_dk='#1592b8',fin='#b0f2ff',eye='#e8ffff'),
 [('Glowing scales',-2,4,-5,2,9,5,'scale','crystal'),('Belly',-1.5,3,-4,1.5,4,4,'scale_dk','noise'),('Tail fin',-.5,3,5,.5,10,8,'fin','glow'),('Top fin',-.5,9,-2,.5,11,2,'fin','glow')]
 +both(('Side fins',-3,5,-2,-2,6,1,'fin','glow'),('Eyes',-2.3,7,-4,-2,8,-3,'eye','glow')),
 [('Health','3'),('Behavior','Schools of 4–8; lights the water around it at night'),('Catching','Bucket, or fishing on Cerulon'),('Spawns','Cerulon lakes and oceans'),
  ('Drops','Glimmerfish 1, Glimmer Scale 0–1 (rare)')],['Scales and fins on the emissive layer.'])
mob('slag_boar','Slag Boar','Skarn · neutral · hitbox 0.9 × 0.9 × 1.3 blocks',
 dict(hide='#3e2a20',bristle='#6a4a36',slag='#8a8a8a',tusk='#e6ddd2',ember='#ff8a2a',hoof='#140c0a',eye='#ffd070'),
 [('Bristled hide',-5,6,-8,5,14,8,'hide','fur'),('Slag armor plates',-4,14,-6,4,16,6,'slag','noise'),('Head',-4,6,-14,4,13,-8,'hide','noise'),('Snout',-2,6,-16,2,9,-14,'bristle','noise'),
  ('Ember tail',-1,10,8,1,12,10,'ember','glow')]
 +both(('Tusks',-3,8,-16.5,-2,11,-15.5,'tusk','noise'),('Eyes',-3,11,-14.3,-2,12,-14,'eye','glow'),('Legs',-4,0,-6,-2,6,-3,'hide','noise'),(None,-4,0,3,-2,6,6,'hide','noise')),
 [('Health','26 (13 hearts)'),('Damage','6 charge, only when provoked'),('Behavior','Roots through Slag; charges if hit or if you get too close to its young'),('Breeding','Cinder Caps'),
  ('Spawns','Skarn slag fields'),('Drops','Boar Chop 1–3, Boar Tusk 0–1')],['Ember tail and eyes on the emissive layer.'])
mob('scorch_wyrmling','Scorch Wyrmling','Skarn · hostile · hitbox 0.6 × 0.6 × 1.0 blocks',
 dict(scale='#e8661e',scale_dk='#8a3a14',belly='#ffd070',wing='#b0380c',horn='#2a1a14',eye='#fff0a0',flame='#ffb040'),
 [('Scorched scales',-3,4,-6,3,9,4,'scale','spots'),('Belly',-2.5,3,-5,2.5,4,3,'belly','noise'),('Head',-2.5,5,-10,2.5,10,-6,'scale_dk','noise'),
  ('Tail (Scorch Tail drop)',-1,4,4,1,7,14,'scale','stripes'),('Flame tip',-1,4,14,1,7,16,'flame','glow')]
 +both(('Horns',-2,10,-8,-1,12,-7,'horn','noise'),('Stubby wings',-8,8,-3,-3,10,2,'wing','noise'),('Eyes',-2.8,8,-9,-2.5,9,-8,'eye','glow'),
       ('Legs',-3,0,-5,-2,4,-3,'scale_dk','noise'),(None,-3,0,1,-2,4,3,'scale_dk','noise')),
 [('Health','16 (8 hearts)'),('Damage','3 bite; spits a fire bolt (3 + fire)'),('Behavior','Glides between ledges; guards Emberite veins'),('Spawns','Skarn lava contact zones'),
  ('Drops','Scorch Tail 1, Scorch Scale 0–2')],['Flame tip and eyes on the emissive layer.','Wings flap only when gliding.'])
mob('frost_yak','Frost Yak','Eidolon · passive · hitbox 1.4 × 1.7 blocks',
 dict(wool='#d8e0e6',wool_dk='#a6b6c0',face='#3a464c',horn='#c4e0ec',hoof='#1c2226',eye='#7ae8ff'),
 [('Thick Yak Wool (shearable)',-7,10,-10,7,24,10,'wool','fur'),('Hump',-5,24,-8,5,27,-2,'wool','fur'),('Wool skirt',-7.5,7,-10,7.5,11,10,'wool_dk','fur'),
  ('Dark face',-4,10,-16,4,18,-10,'face','noise')]
 +both(('Ice-tipped horns',-8,16,-14,-4,18,-12,'wool_dk','noise'),(None,-8,18,-14,-7,22,-12,'horn','crystal'),('Eyes',-3,15,-16.3,-2,16,-16,'eye','glow'),
       ('Legs',-6,2,-8,-3,8,-5,'face','noise'),(None,-6,2,5,-3,8,8,'face','noise'),('Hooves',-6,0,-8,-3,2,-5,'hoof','noise'),(None,-6,0,5,-3,2,8,'hoof','noise')),
 [('Health','30 (15 hearts)'),('Behavior','Shear for Yak Wool; milk with a glass bottle for Frost Milk. Shelters calves in blizzards'),('Breeding','Frostfern'),
  ('Spawns','Eidolon glaciers, herds of 2–4'),('Drops','Yak Meat 1–3, Yak Wool 1–2')],['Sheared state: wool shrinks to a thin coat.'])
mob('ice_leech','Ice Leech','Eidolon · hostile · hitbox 0.6 × 0.4 × 1.2 blocks',
 dict(gel='#6ad0c0',gel_dk='#3a9a8a',ice='#d0fbfb',mouth='#1a3a3a'),
 [('Translucent gel body',-3,0,-8,3,5,-3,'gel','noise'),(None,-3.5,0,-3,3.5,6,3,'gel','noise'),(None,-3,0,3,3,5,8,'gel_dk','noise'),(None,-2,0,8,2,4,11,'gel_dk','noise'),
  ('Frost crystals',-1,6,-2,1,8,2,'ice','glow'),('Sucker mouth',-2,1,-8.3,2,4,-8,'mouth','noise')],
 [('Health','14 (7 hearts)'),('Damage','2 and latches on: Hunger II while attached'),('Behavior','Hides under Snowpack; shake it off by sprinting or hitting it'),('Spawns','Eidolon snowfields and wreck interiors'),
  ('Drops','Leech Gel 1–3')],['Body at 75% opacity.','Crystals on the emissive layer.'])
mob('gildcrab','Gildcrab','Solvane · passive · hitbox 0.9 × 0.5 blocks',
 dict(shell='#e0a010',shell_hi='#fff4a8',body='#a86a00',claw='#f0a060',leg='#6a3a10',eye='#ffffff'),
 [('Golden shell',-6,3,-5,6,8,5,'shell','rivets'),('Sun-polished dome',-5,8,-4,5,9,4,'shell_hi','noise'),('Underside',-5,2,-4,5,3,4,'body','noise')]
 +both(('Eye stalks',-2,8,-5,-1,11,-4,'body','noise'),(None,-2,11,-5,-1,12,-4,'eye','glow'),('Pincers',-10,4,-10,-6,8,-5,'claw','noise'),
       ('Legs',-9,0,-3,-6,4,-2,'leg','noise'),(None,-9,0,0,-6,4,1,'leg','noise'),(None,-9,0,3,-6,4,4,'leg','noise')),
 [('Health','12 (6 hearts)'),('Damage','3 pinch, only when attacked'),('Behavior','Walks sideways; basks on Sunspot Rock and is immune to heat'),('Breeding','Pyrefruit'),
  ('Spawns','Solvane Sunspot Rock shores'),('Drops','Gildcrab Meat 1–2, Gildcrab Shell 0–1')],['Eyes on the emissive layer.'])
mob('deep_eel','Deep Eel','Ocean wasteland · hostile (water) · hitbox 0.6 × 0.6 × 1.8 blocks',
 dict(skin='#5a6a7a',skin_dk='#3a4450',fin='#9ff0f0',mouth='#1a1e24',teeth='#e8f0f0'),
 [('Head',-2.5,4,-14,2.5,9,-6,'skin_dk','noise'),('Jaw',-2,3,-15,2,5,-9,'mouth','noise'),('Teeth',-2,5,-15.3,2,6,-15,'teeth','noise'),
  ('Eel body',-2,4,-6,2,8,6,'skin','stripes'),(None,-1.5,4.5,6,1.5,7.5,14,'skin','stripes'),('Glowing fin ridge',-.5,8,-6,.5,10,12,'fin','glow')]
 +both(('Eyes',-2.8,7,-12,-2.5,8,-11,'fin','glow')),
 [('Health','22 (11 hearts)'),('Damage','6 bite; pulls you down 2 blocks'),('Behavior','Lurks in trenches; follows light sources'),('Spawns','Ocean wastelands in every galaxy (tinted)'),
  ('Drops','Eel Fillet 1–2, Eel Skin 0–1')],['Fin ridge and eyes on the emissive layer.'])
mob('sand_skitter','Sand Skitter','Desert wasteland · hostile · hitbox 1.0 × 0.6 blocks',
 dict(carapace='#c8a868',carapace_dk='#8a6a38',leg='#6a4a20',stinger='#8ac040',eye='#ff5a3a'),
 [('Sandy carapace',-4,4,-4,4,8,6,'carapace','rivets'),('Head',-3,4,-8,3,7,-4,'carapace_dk','noise'),('Curled tail',-1,8,5,1,14,7,'carapace','stripes'),(None,-1,12,1,1,14,5,'carapace','stripes'),
  ('Venom stinger',-1,10,0,1,12,1,'stinger','glow')]
 +both(('Eyes',-2,6,-8.3,-1,7,-8,'eye','glow'),('Eight legs',-9,0,-3.5,-4,5,-2.5,'leg','noise'),(None,-9,0,-.5,-4,5,.5,'leg','noise'),(None,-9,0,2.5,-4,5,3.5,'leg','noise'),(None,-9,0,4.5,-4,5,5.5,'leg','noise')),
 [('Health','16 (8 hearts)'),('Damage','3 and Poison I for 4 s'),('Behavior','Buries itself in Dunesand; bursts out in groups of 2–3'),('Spawns','Desert wastelands (tinted)'),
  ('Drops','Skitter Leg 1–2, Skitter Carapace 0–1, Venom Gland 0–1')],['Stinger and eyes on the emissive layer.'])
# add food drops to earlier mobs
def setdrop(k,txt):
    OLD[k]['stats']=[(a,txt if a=='Drops' else b) for a,b in OLD[k]['stats']]
setdrop('regolith_crawler','Crawler Leg 0–2, Regolith Dust 1–3, rare Selenite shard')
setdrop('rust_beetle','Beetle Grub 0–1, Ferrox bits 1–2, Rust Shell (armor upgrade)')
setdrop('crystal_stag','Stag Venison 1–3, Crystal Hide 0–2')
setdrop('dune_burrower','Burrower Steak 1–3, Burrower Scale, Star Map Fragment (rare)')
setdrop('bog_lurker','Lurker Leg 1–2, Venom Gland 0–1, Neutralizer (rare)')
