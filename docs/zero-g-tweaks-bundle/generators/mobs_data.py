# boxes: (label_or_None, x0,y0,z0,x1,y1,z1, color_key, pattern)  units = model pixels, y up, z negative = front
def mir(b):
    l,x0,y0,z0,x1,y1,z1,c,p=b; return (None,-x1,y0,z0,-x0,y1,z1,c,p)
def both(*bs):
    out=[]
    for b in bs: out+= [b,mir(b)]
    return out
MOBS={}
def mob(key,name,info,pal,boxes,stats,notes): MOBS[key]=dict(name=name,info=info,pal=pal,boxes=boxes,stats=stats,notes=notes)
# ---------------- Moon: Regolith Crawler
mob('regolith_crawler','Regolith Crawler','Moon · hostile ambusher · hitbox 0.9 × 0.5 × 1.1 blocks',
 dict(shell='#9a9aa0',shell_dk='#6e6e74',under='#4a4a50',leg='#34343a',eye='#6fe0ff',dust='#c4c4c8',mand='#2a2a2e'),
 [('Armored shell',-6,2,-8,6,7,8,'shell','stripes'),('Regolith dust plates',-5,7,-6,5,8,6,'dust','noise'),('Belly',-5,1,-7,5,2,7,'under','noise'),
  ('Head',-4,2,-12,4,6,-8,'shell_dk','noise')]
 +both(('Glowing eyes',-3,4,-12.4,-1,5,-12,'eye','glow'),('Mandibles',-4,2,-15,-2,3,-12,'mand','noise'),
       ('Six legs',-9,0,-5.5,-6,3,-4.5,'leg','noise'),(None,-9,0,-.5,-6,3,.5,'leg','noise'),(None,-9,0,4.5,-6,3,5.5,'leg','noise')),
 [('Health','14 (7 hearts)'),('Damage','3, plus Slowness I for 3 s'),('Speed','Slow; fast burst lunge'),('Behavior','Burrows under Regolith and waits; lunges when a player walks within 3 blocks'),
  ('Spawns','Moon surface, groups of 1–3'),('Drops','Regolith Dust 1–3, rare Selenite shard')],
 ['Burrowed state: only the dust plates and eyes show above the block surface.','Eyes on the emissive layer.','Walk cycle: legs alternate in two sets of three.'])
# ---------------- Mars: Rust Beetle
mob('rust_beetle','Rust Beetle','Mars · neutral · hitbox 0.8 × 0.7 × 1.0 blocks',
 dict(shell='#9c4424',shell_hi='#c4683a',spot='#e89a62',body='#3a1a10',leg='#2a120b',horn='#e8d0b0',eye='#ffc28a'),
 [('Rust shell with Ferrox spots',-5,3,-5,5,10,7,'shell','spots'),('Wing seam',-.5,9.9,-5,.5,10.1,7,'body','noise'),('Belly',-4,2,-4,4,3,6,'body','noise'),
  ('Head',-3,3,-9,3,7,-5,'body','noise'),('Horn',-1,6,-11,1,11,-9,'horn','noise')]
 +both(('Eyes',-3,5,-9.3,-2,6,-9,'eye','glow'),('Legs',-7,0,-3.5,-5,4,-2.5,'leg','noise'),(None,-7,0,.5,-5,4,1.5,'leg','noise'),(None,-7,0,4.5,-5,4,5.5,'leg','noise')),
 [('Health','20 (10 hearts)'),('Damage','4 (horn ram) when provoked'),('Speed','Slow'),('Behavior','Grazes on Rust Lichen; rams back when hit; tamed beetles with a Ferrox saddle carry a chest'),
  ('Spawns','Mars plains, herds of 2–4'),('Drops','Ferrox bits 1–2, Rust Shell (armor upgrade)')],
 ['Shell splits open when it flies short hops (low gravity).','Spots use the shell spot color.'])
# ---------------- Cerulon: Crystal Stag
mob('crystal_stag','Crystal Stag','Cerulon · passive · hitbox 0.9 × 1.8 × 1.3 blocks',
 dict(fur='#2c3d57',fur_lt='#4c6588',belly='#8fa6c2',hoof='#141f3d',antler='#3fc9e8',antler_hi='#b0f2ff',eye='#e8ffff',nose='#0d1426'),
 [('Blue fur',-4,12,-7,4,20,7,'fur','fur'),('Neck',-2,18,-9,2,25,-5,'fur','fur'),('Head',-2.5,22,-14,2.5,27,-8,'fur_lt','noise'),('Nose',-1.5,22,-15,1.5,24,-14,'nose','noise'),
  ('Pale tail',-1,17,7,1,20,8,'belly','noise'),('Belly',-3,11,-6,3,12,6,'belly','noise')]
 +both(('Legs',-4,2,-6,-2,12,-4,'fur','fur'),(None,-4,2,4,-2,12,6,'fur','fur'),('Hooves',-4,0,-6,-2,2,-4,'hoof','noise'),(None,-4,0,4,-2,2,6,'hoof','noise'),
       ('Eyes',-2.6,25,-12,-2.4,26,-11,'eye','glow'),('Crystal antlers (emissive, shearable)',-3,27,-10,-2,33,-9,'antler','crystal'),(None,-6,31,-10,-3,32,-9,'antler','crystal'),
       (None,-6,32,-10,-5,35,-9,'antler_hi','glow'),(None,-3,33,-10,-2,36,-9,'antler_hi','glow')),
 [('Health','20 (10 hearts)'),('Damage','None'),('Speed','Fast; flees when hit'),('Behavior','Shear the antlers for 1–2 Starlite; they regrow over 5 minutes. Breeds with Starbloom'),
  ('Spawns','Cerulon Azure Moss plains, herds of 3–5'),('Drops','Crystal Hide 0–2, raw venison')],
 ['Sheared state: antlers shrink to stubs; glow turns off.','Antlers, eyes on the emissive layer.'])
# ---------------- Cerulon: Prismling (renamed from Shardling)
mob('prismling','Prismling','Cerulon · hostile (small) · hitbox 0.5 × 0.75 blocks · renamed from Shardling',
 dict(crystal='#1592b8',crystal_hi='#3fc9e8',core='#e8ffff',base='#2c3d57',leg='#141f3d'),
 [('Stone body',-3,2,-3,3,6,3,'base','noise'),('Crystal spikes',-1,6,-1,1,12,1,'crystal','crystal'),(None,-3,6,-2,-1,10,0,'crystal_hi','crystal'),(None,1,6,0,3,9,2,'crystal','crystal'),
  (None,-2,6,1,0,8,3,'crystal_hi','crystal'),('Glowing core',-1,3,-3.3,1,5,-3,'core','glow')]
 +both(('Stubby legs',-3,0,-3,-2,2,-2,'leg','noise'),(None,-3,0,2,-2,2,3,'leg','noise')),
 [('Health','8 (4 hearts)'),('Damage','2'),('Speed','Fast, skittering'),('Behavior','Swarms in groups; shatters into 2–3 crystal shards on death that deal 1 damage nearby'),
  ('Spawns','Cerulean geodes and crystal caves'),('Drops','Crystal shard 1–3 (smelts to Cerulite dust)')],
 ['Name changed: "Shardling" is already the minion line in Shattered Skies.','Core pulses on the emissive layer.'])
# ---------------- Skarn: Cinder Hound
mob('cinder_hound','Cinder Hound','Skarn · hostile pack hunter · hitbox 0.7 × 0.9 × 1.2 blocks',
 dict(coat='#221c1a',coat_lt='#3a302c',ember='#ff8a2a',eye='#ffd070',jaw='#161211',claw='#0c0908'),
 [('Charred coat with ember cracks',-3,7,-6,3,13,6,'coat','cracks'),('Ash mane',-4,8,-7,4,15,-3,'coat_lt','fur'),('Head',-3,9,-12,3,15,-7,'coat','noise'),
  ('Snout',-2,9,-15,2,12,-12,'coat_lt','noise'),('Glowing jaw',-2,8,-15,2,9,-12,'ember','glow'),('Ember tail',-1,11,6,1,13,13,'ember','glow')]
 +both(('Eyes',-2.5,13,-12.3,-1.5,14,-12,'eye','glow'),('Ears',-3,15,-9,-2,17,-8,'coat','noise'),('Legs',-3,0,-5,-1,7,-3,'coat','noise'),(None,-3,0,3,-1,7,5,'coat','noise')),
 [('Health','18 (9 hearts)'),('Damage','4, sets target on fire for 2 s'),('Speed','Fast'),('Behavior','Hunts in packs of 3–5; circles, then lunges together. Immune to fire'),
  ('Spawns','Skarn Ember Crust fields'),('Drops','Cinder pelt, Emberite 0–2')],
 ['Ember cracks and tail on the emissive layer.','Leaves a short ember particle trail when running.'])
# ---------------- Eidolon: Frost Warden
mob('frost_warden','Frost Warden','Eidolon · mini-boss · hitbox 1.0 × 2.4 blocks',
 dict(ice='#8ab0c0',ice_hi='#d8ecf6',armor='#5e6e74',armor_dk='#3a464c',glow='#9ff0f0',cloth='#2a3a46',glaive='#c4e0ec'),
 [('Tattered cloak',-5,8,3,5,28,4,'cloth','fur'),('Wraithsteel plate',-5,14,-3,5,28,3,'armor','rivets'),('Frozen core',-1,22,-3.3,1,24,-3,'glow','glow'),
  ('Ice helm',-3.5,28,-3.5,3.5,36,3.5,'ice','crystal'),('Visor glow',-2,31,-3.8,2,32,-3.5,'glow','glow'),
  ('Ice glaive',6,2,-5,7,40,-4,'armor_dk','noise'),(None,5,36,-5,8,46,-4,'glaive','crystal')]
 +both(('Legs',-4,0,-2,-1,14,2,'armor','noise'),('Arms',-8,15,-2,-5,28,2,'armor_dk','noise'),('Ice pauldrons',-9,28,-3,-5,31,3,'ice_hi','crystal'),(None,-8,31,-1,-7,35,1,'ice_hi','glow')),
 [('Health','120 (60 hearts)'),('Damage','9; glaive sweep 12 and Slowness II'),('Speed','Slow, heavy'),('Behavior','Guards the largest wrecks. Phase 2 at half health: summons 2 Rime Stalkers and an ice wall ring'),
  ('Spawns','One per large wreck on Eidolon; does not respawn'),('Drops','Wraithsteel Ingots 3–5, Frost Warden Helm (trophy), Remnant Shard')],
 ['Visor, core, antler-like pauldron tips and glaive edge on the emissive layer.','Boss bar in pale cyan.'])
# ---------------- Solvane: Flare Sprite
mob('flare_sprite','Flare Sprite','Solvane · hostile flyer · hitbox 0.5 × 0.5 blocks',
 dict(core='#fff0a0',flame='#ffa030',flame_dk='#e06010',ember='#ff7030',eye='#ffffff'),
 [('Flame shell',-3,11,-3,3,17,3,'flame','cracks'),('White-hot core',-2,12,-3.3,2,16,-3,'core','glow'),('Flame crest',-1,17,-1,1,21,1,'flame_dk','glow'),
  ('Ember trail',-1,7,1,1,11,3,'flame_dk','glow')]
 +both(('Fire wings',-8,13,0,-3,16,1,'ember','glow'),('Eyes',-2,14,-3.6,-1,15,-3.3,'eye','glow')),
 [('Health','6 (3 hearts)'),('Damage','3 fire, or a small fireball at range'),('Speed','Fast flyer'),('Behavior','Swarms around Flare Vents; bursts into flame when a vent erupts. Water puts it out instantly'),
  ('Spawns','Solvane near Flare Vents, swarms of 4–8'),('Drops','Fusion Dust 0–1, Solar Spark')],
 ['Whole mob is emissive; no shadow.','Animated wing flicker (4 frames).'])
# ---------------- Solvane: Sun Colossus
mob('sun_colossus','Sun Colossus','Solvane · mini-boss · hitbox 2.6 × 2.9 blocks',
 dict(stone='#7a3c1a',stone_dk='#5a2a14',crust='#e08018',core='#fff0a0',eye='#ffd060'),
 [('Solar Stone body (glowing cracks)',-12,16,-7,12,38,7,'stone','cracks'),('Sun core (weak point)',-4,26,-7.4,4,34,-7,'core','glow'),('Head',-5,38,-5,5,46,5,'stone_dk','noise'),
  ('Flare vents',-8,30,7,8,40,9,'crust','glow')]
 +both(('Eyes',-4,41,-5.3,-1,42,-5,'eye','glow'),('Legs',-9,0,-4,-3,16,4,'stone','noise'),('Corona Crust shoulders',-17,32,-6,-12,40,6,'crust','cracks'),
       ('Arms',-17,10,-5,-12,32,5,'stone','noise'),('Heavy fists',-18,4,-6,-11,10,6,'stone_dk','noise')),
 [('Health','200 (100 hearts)'),('Damage','14 slam; ground wave sets fire in a line'),('Speed','Very slow'),('Behavior','Wakes when a player steps on its Sunspot Rock plateau. Core opens to take damage after each slam'),
  ('Spawns','One per Solvane plateau structure'),('Drops','Astrium 4–6, Coronite 6–10, Colossus Core (Fusion Reactor upgrade)')],
 ['Core only takes damage while open (animated plates).','Cracks, core, vents on the emissive layer.'])
# ---------------- wasteland mobs
mob('dune_burrower','Dune Burrower','Desert wasteland · hostile · hitbox 1.2 × 1.9 blocks',
 dict(seg='#c8a868',seg_dk='#9a7a48',maw='#3a1a10',teeth='#f0e6d0',sand='#d8c090'),
 [('Sand mound',-10,0,-4,10,2,12,'sand','noise'),('Segmented body',-6,0,-2,6,8,10,'seg','stripes'),(None,-5,8,-4,5,16,6,'seg_dk','stripes'),(None,-5,16,-8,5,24,2,'seg','stripes'),
  ('Head',-6,22,-14,6,30,-4,'seg_dk','noise'),('Ringed maw',-4,23,-14.3,4,29,-14,'maw','noise'),('Teeth',-5,29,-14.5,5,30,-14,'teeth','noise'),(None,-5,22,-14.5,5,23,-14,'teeth','noise')],
 [('Health','40 (20 hearts)'),('Damage','8; can swallow and hold a player for 2 s'),('Speed','Fast underground'),('Behavior','Travels under sand shown as a moving ripple; bursts up under players who stand still'),
  ('Spawns','Desert wastelands in every galaxy'),('Drops','Burrower Scale, Star Map Fragment (rare)')],['Colors tinted per galaxy like the terrain.','Underground: only a sand ripple particle trail.'])
mob('ash_strider','Ash Strider','Volcanic wasteland · neutral · hitbox 1.0 × 1.9 blocks',
 dict(body='#3a3a3a',ash='#6a6a6a',vent='#ff8a2a',leg='#1a1a1a',eye='#ffd070'),
 [('Ash-plated body',-5,22,-5,5,28,5,'body','rivets'),('Heat vents',-3,28,-3,3,29,3,'vent','glow'),('Head',-2,24,-8,2,28,-5,'ash','noise')]
 +both(('Eyes',-2,26,-8.3,-1,27,-8,'eye','glow'),('Stilt legs',-5.5,0,-4.5,-4,22,-3,'leg','noise'),(None,-5.5,0,3,-4,22,4.5,'leg','noise')),
 [('Health','30 (15 hearts)'),('Damage','6 stomp'),('Speed','Medium; walks over lava'),('Behavior','Wades across lava lakes; rideable with a saddle, making it the lava crossing mount'),
  ('Spawns','Volcanic wastelands'),('Drops','Heatproof Plating (rare), ash 1–3')],['Vents on the emissive layer.'])
mob('rime_stalker','Rime Stalker','Frozen wasteland · hostile · hitbox 0.8 × 1.0 blocks',
 dict(fur='#dce6ec',fur_dk='#a6b6c0',ice='#9ff0ff',eye='#7ae8ff',claw='#3a5a66'),
 [('Frost fur',-3,7,-7,3,13,7,'fur','fur'),('Ice spines',-1,13,-5,1,17,-3,'ice','crystal'),(None,-1,13,-1,1,18,1,'ice','crystal'),(None,-1,13,3,1,16,5,'ice','crystal'),
  ('Head',-3,9,-12,3,15,-7,'fur','fur'),('Long tail',-1,10,7,1,12,17,'fur_dk','fur')]
 +both(('Eyes',-2.5,12,-12.3,-1.5,13,-12,'eye','glow'),('Ears',-3,15,-9,-2,17,-8,'fur_dk','noise'),('Legs',-3,0,-6,-1,7,-4,'fur_dk','noise'),(None,-3,0,4,-1,7,6,'fur_dk','noise')),
 [('Health','24 (12 hearts)'),('Damage','5, plus Freezing'),('Speed','Fast; invisible in snowstorms'),('Behavior','Stalks from behind; only visible within 8 blocks during blizzards'),
  ('Spawns','Frozen wastelands; summoned by the Frost Warden'),('Drops','Cryo Core (rare), Frost pelt')],['Spines on the emissive layer.'])
mob('bog_lurker','Bog Lurker','Toxic wasteland · hostile · hitbox 1.0 × 0.7 × 1.4 blocks',
 dict(skin='#4a5a3a',skin_dk='#34402a',moss='#6a8a3a',sac='#b8f040',eye='#e8ff80',mouth='#1a2010'),
 [('Slick hide',-7,2,-8,7,9,8,'skin','spots'),('Blightmoss back',-6,9,-6,6,10,6,'moss','fur'),('Head',-6,3,-14,6,9,-8,'skin_dk','noise'),('Mouth',-5,4,-14.3,5,5,-14,'mouth','noise')]
 +both(('Bulging eyes',-5,9,-12,-3,11,-10,'eye','glow'),('Acid sacs (emissive)',-8,4,-2,-7,7,2,'sac','glow'),('Legs',-7,0,-7,-4,3,-4,'skin_dk','noise'),(None,-7,0,4,-4,3,7,'skin_dk','noise')),
 [('Health','28 (14 hearts)'),('Damage','5, and spits acid (Poison II, 4 s)'),('Speed','Slow on land, fast in Acid'),('Behavior','Lies submerged in Acid with only eyes showing'),
  ('Spawns','Toxic wastelands'),('Drops','Neutralizer (rare), acid gland')],['Sacs and eyes on the emissive layer.'])
mob('crater_drifter','Crater Drifter','Barren wasteland · neutral flyer · hitbox 0.8 × 1.4 blocks',
 dict(rock='#3a3a3a',rock_lt='#5a5a5a',ore='#cfcfcf',glow='#e0f4ff',tend='#262626'),
 [('Meteorite shell',-5,14,-5,5,22,5,'rock','spots'),('Crater top',-3,22,-3,3,23,3,'rock_lt','noise'),('Glowing fissure',-3,17,-5.3,3,18,-5,'glow','glow')]
 +both(('Stone tendrils',-4,4,-1,-3,14,0,'tend','noise'),(None,-2,6,2,-1,14,3,'tend','noise'),(None,-4,8,3,-3,14,4,'tend','noise')),
 [('Health','20 (10 hearts)'),('Damage','None unless hit, then 4'),('Speed','Slow drift'),('Behavior','Floats over craters; drops Meteorite Fragments as it drifts. Attacking one makes nearby drifters swarm'),
  ('Spawns','Barren wastelands'),('Drops','Stardust 1–2, Meteorite Fragment')],['Fissure on the emissive layer.','Bobs up and down (2 s cycle).'])
# ---------------- bosses
mob('prism_sentinel','Prism Sentinel','Galaxy 2 guardian boss · hitbox 2.0 × 2.4 blocks',
 dict(crystal='#1592b8',crystal_hi='#3fc9e8',core='#e8ffff',stone='#2c3d57',stone_dk='#1b2638',gold='#e0dcb8'),
 [('Keeper plinth',-12,0,-12,12,4,12,'stone','noise'),('Lower body',-6,4,-6,6,12,6,'stone_dk','rivets'),('Concord rune band',-6.2,10,-6.2,6.2,12,6.2,'gold','noise'),
  ('Prism core',-5,14,-5,5,30,5,'crystal','crystal'),('Heart light (weak point)',-2,20,-5.4,2,24,-5,'core','glow'),('Crown shard',-2,30,-2,2,38,2,'crystal_hi','crystal'),
  ('Orbiting shards (reflect beams)',-16,16,-2,-12,32,2,'crystal_hi','crystal'),(None,12,16,-2,16,32,2,'crystal_hi','crystal'),(None,-2,16,-16,2,32,-12,'crystal_hi','crystal'),(None,-2,16,12,2,32,16,'crystal_hi','crystal')],
 [('Health','300 (150 hearts)'),('Damage','Light beams 10; shard spin 8'),('Phases','1: beams bounce off the orbiting shards. 2: shards break loose and circle the arena. 3: core cracks open, and hits to the heart light deal double'),
  ('Test, not a hunt','Opens by asking "Are you Concord?" in the chat; beaten, it names you an heir'),('Arena','Crystal amphitheater on Galaxy 2\'s key world'),('Drops','Galaxy 3 gate key, Cerulite 4–6, Sentinel Prism (T3 lens upgrade)')],
 ['Shards orbit on a 4 s loop around the core.','Core and shards on the emissive layer; boss bar cyan.'])
mob('rift_tyrant','Rift Tyrant','Galaxy 3 guardian boss · hitbox 2.4 × 2.4 × 3.2 blocks',
 dict(hide='#2e2624',hide_dk='#1a1412',rift='#b48cff',horn='#e6ddd2',claw='#cfc2b6',eye='#e6dcff'),
 [('Hide split by rift cracks',-12,12,-10,12,30,14,'hide','cracks'),('Rift crystal spines',-2,30,-4,2,38,0,'rift','glow'),(None,-2,30,4,2,36,8,'rift','glow'),
  ('Head',-7,18,-20,7,30,-10,'hide_dk','noise'),('Jaw',-6,16,-22,6,20,-12,'hide','noise'),('Rift tail',-3,14,14,3,20,28,'hide_dk','noise'),(None,-3,14,28,3,20,32,'rift','glow')]
 +both(('Eyes',-5,25,-20.3,-2,27,-20,'eye','glow'),('Horns',-11,28,-16,-7,32,-12,'horn','noise'),(None,-12,32,-15,-10,38,-13,'horn','noise'),
       ('Arms',-17,4,-12,-12,26,-4,'hide','noise'),('Rift claws',-18,0,-16,-11,4,-6,'claw','noise'),('Hind legs',-12,0,6,-6,12,14,'hide','noise')),
 [('Health','450 (225 hearts)'),('Damage','Claw 16; rift pull drags you toward the rift'),('Phases','1: charges and claws. 2: rift pulls chunks of the arena into the void. 3: spines fire void shards'),
  ('Lore','Vael\'s lieutenant, fused into the rift he helped tear open'),('Arena','Fractured island over the void on Galaxy 3\'s key world'),('Drops','Galaxy 4 gate key, Skarnite 4–6, Rift Heart')],
 ['Arena blocks near the rift fall away over the fight.','Cracks, spines and eyes on the emissive layer; boss bar violet.'])
mob('eidolon_captain','Eidolon Captain','Galaxy 4 guardian boss · hitbox 0.9 × 2.6 blocks',
 dict(ghost='#c4e0ec',coat='#2a4050',trim='#d0e8f4',glow='#7ae8ff',hat='#1a2a34',blade='#e8f4ff',lantern='#fff0a0'),
 [('Fading legs (translucent)',-4,0,-3,4,10,3,'ghost','fur'),("Captain's coat",-6,10,-4,6,28,4,'coat','noise'),('Lapels',-1,14,-4.3,1,28,-4,'trim','noise'),
  ('Head',-4,28,-4,4,36,4,'ghost','noise'),("Captain's hat",-7,36,-6,7,38,6,'hat','noise'),(None,-4,38,-4,4,42,4,'hat','noise'),
  ('Spectral cutlass',-10,4,-6,-9,16,-5,'blade','glow'),('Fleet lantern',7,10,-2,10,15,1,'lantern','glow')]
 +both(('Hollow eyes',-3,31,-4.3,-1,32,-4,'glow','glow'),('Epaulettes',-8,26,-3,-5,28,3,'trim','noise'),('Arms',-8,14,-2,-6,26,2,'coat','noise')),
 [('Health','400 (200 hearts)'),('Damage','Cutlass 13; lantern beam chills'),('Phases','1: duels with the cutlass. 2: calls Hollow Crewmen. 3: fleet lantern freezes the deck'),
  ('Peaceful ending','Show him the crew\'s final log (enough Remnant Shards) and he yields without a fight'),('Arena','Flagship deck on Galaxy 4\'s key world'),('Drops','Galaxy 5 gate key, Eidolite 4–6; Captain\'s Lantern if spared')],
 ['Whole body at 80% opacity; legs fade to 40%.','Eyes, lantern and blade on the emissive layer; boss bar pale blue.'])
mob('dying_star','The Dying Star','Final boss · Archon Vael fused with Solvane\'s sun · hitbox 3.6 × 3.6 blocks (flies)',
 dict(plasma='#f08a14',plasma_hi='#ffd060',core='#fff0a0',crust='#7a1e02',ray='#ffb040',vael='#2a1426',crown='#ffd070',eye='#ffffff'),
 [('Molten star body',-16,16,-16,16,40,16,'plasma','cracks'),(None,-12,12,-12,12,44,12,'plasma','cracks'),(None,-18,20,-10,18,36,10,'plasma_hi','cracks'),
  ('Cooling crust',-14,38,-8,-4,41,4,'crust','noise'),('Core (weak point, phase 3)',-4,20,-16.4,4,26,-16,'core','glow'),
  ('Corona rays (rotate)',-2,44,-2,2,54,2,'ray','glow'),(None,-2,2,-2,2,12,2,'ray','glow'),(None,18,26,-2,28,30,2,'ray','glow'),(None,-28,26,-2,-18,30,2,'ray','glow'),
  ('Archon Vael',-6,26,-20,6,40,-14,'vael','noise'),(None,-4,40,-19,4,48,-13,'vael','noise'),('Crown',-5,48,-19.5,5,51,-12.5,'crown','glow')]
 +both(('Vael\'s eyes',-3,43,-19.3,-1,44,-19,'eye','glow'),('Reaching arms',-12,28,-20,-6,40,-16,'vael','noise')),
 [('Health','900 (450 hearts)'),('Damage','Solar flare 20; falling stars 12'),('Phases','1: Vael fights from the surface. 2: corona rays sweep the arena. 3: the star collapses, the core opens and the arena shrinks'),
  ('Ending','Heart of Solvane drops; each player chooses Rekindle or Let it fade'),('Arena','Floating ring platform above Solvane'),('Drops','Heart of Solvane, Solvanite 6–8, T6 crown')],
 ['Rays rotate slowly; the body pulses brighter as health drops.','Everything but Vael emissive; boss bar gold to white.'])
