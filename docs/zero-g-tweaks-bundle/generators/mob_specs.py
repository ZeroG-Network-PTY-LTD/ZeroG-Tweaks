"""Implementation specs for the 28 ZeroG Tweaks mobs, written for coding agents.

Design text (health, damage, behavior, spawns, drops, visual notes) comes from mobs_data.py /
mobs_food.py, the same source as the reference sheets. This file adds what an implementer needs:
Java base class, MobCategory, attribute values, AI goals, states, animations and mechanics.
"""

SPEED = {'very_slow': 0.15, 'slow': 0.2, 'medium': 0.25, 'fast': 0.33, 'very_fast': 0.4}

# key: (galaxy, world, dimension ids, role, java_base, category, speed, follow, armor, kb_resist,
#       goals, states, animations, mechanics, breed_item, interactions)
S = {}
def spec(key, galaxy, world, dims, role, base, cat, speed, *, follow=16, armor=0, kb=0.0, fly=None,
         goals, states, anims, mech, breed=None, interact=None, immune=None, boss=None):
    S[key] = dict(galaxy=galaxy, world=world, dimensions=dims, role=role, java_base=base, mob_category=cat,
                  movement_speed=SPEED[speed], speed_class=speed, follow_range=follow, armor=armor,
                  knockback_resistance=kb, flying_speed=fly, goals=goals, states=states, animations=anims,
                  mechanics=mech, breeding_item=breed, interactions=interact or [], immunities=immune or [], boss=boss)

WL = lambda t: [f'zerog_tweaks:g{g}_p{p}' for g in range(2, 6) for p in range(1, 7)] + [f'(any slot rolled as {t})']

# ------------------------------------------------------------------ Sol
spec('regolith_crawler', 1, 'Moon', ['zerog_tweaks:moon'], 'hostile', 'Monster', 'MONSTER', 'slow',
     goals=['FloatGoal', 'BurrowAmbushGoal (custom): burrow when no target, wait', 'LungeAtTargetGoal (custom, range 3, cooldown 60t)',
            'MeleeAttackGoal', 'WaterAvoidingRandomStrollGoal', 'NearestAttackableTargetGoal<Player>'],
     states=['burrowed', 'emerging', 'hunting', 'lunging', 'dead'],
     anims=['idle', 'walk', 'burrow', 'emerge', 'lunge', 'death'],
     mech=['While burrowed: invisible except dust plates + eyes (model bone visibility), no collision push, takes 50% less damage',
           'Emerges when a player is within 3 blocks and not sneaking', 'Hit applies Slowness I 60 ticks'])
spec('rust_beetle', 1, 'Mars', ['zerog_tweaks:mars'], 'neutral', 'Animal + NeutralMob (tameable, saddle + chest like a llama)', 'CREATURE', 'slow',
     goals=['FloatGoal', 'MeleeAttackGoal (only when angry)', 'HurtByTargetGoal', 'EatBlockGoal-style: graze Rust Lichen',
            'BreedGoal', 'TemptGoal(rust_lichen)', 'FollowParentGoal', 'WaterAvoidingRandomStrollGoal', 'LookAtPlayerGoal', 'ResetUniversalAngerTargetGoal'],
     states=['grazing', 'wandering', 'angry', 'hopping', 'tamed', 'saddled'],
     anims=['idle', 'walk', 'ram', 'hop (shell opens)', 'graze'],
     mech=['Low-gravity hop: occasional jump with shell-open animation', 'Tame with Rust Lichen; Ferrox saddle (new item) + chest gives 15-slot storage'],
     breed='rust_lichen')
# ------------------------------------------------------------------ Cerulon
spec('crystal_stag', 2, 'Cerulon', ['zerog_tweaks:cerulon'], 'passive', 'Animal + Shearable', 'CREATURE', 'fast',
     goals=['FloatGoal', 'PanicGoal(1.8)', 'BreedGoal', 'TemptGoal(starbloom)', 'FollowParentGoal', 'WaterAvoidingRandomStrollGoal', 'LookAtPlayerGoal', 'RandomLookAroundGoal'],
     states=['antlered', 'sheared (regrowing 6000t)', 'fleeing'],
     anims=['idle', 'walk', 'run', 'graze'],
     mech=['Shears: drop 1-2 starlite, set SHEARED synced data, regrow after 6000 ticks', 'Sheared: antler bones hidden, glowmask off'],
     breed='starbloom', interact=['shears -> starlite x1-2'])
spec('prismling', 2, 'Cerulon', ['zerog_tweaks:cerulon'], 'hostile', 'Monster', 'MONSTER', 'fast',
     goals=['FloatGoal', 'MeleeAttackGoal', 'WaterAvoidingRandomStrollGoal', 'NearestAttackableTargetGoal<Player>', 'HurtByTargetGoal (alert others)'],
     states=['idle', 'swarming', 'shattering'],
     anims=['idle', 'walk', 'attack', 'shatter'],
     mech=['On death: spawn 2-3 shard particles/projectiles dealing 1 damage within 2 blocks', 'Spawns in geodes and crystal caves (low light)'])
spec('azure_fowl', 2, 'Cerulon', ['zerog_tweaks:cerulon'], 'passive', 'Animal (Chicken-like)', 'CREATURE', 'medium',
     goals=['FloatGoal', 'PanicGoal(1.4)', 'BreedGoal', 'TemptGoal(skyberries)', 'FollowParentGoal', 'WaterAvoidingRandomStrollGoal', 'LookAtPlayerGoal'],
     states=['walking', 'gliding', 'laying'],
     anims=['idle', 'walk', 'glide', 'flap'],
     mech=['Slow fall like a chicken (cap downward velocity at -0.1 while not on ground)', 'Lays blue_egg every 6000-12000 ticks (Chicken eggTime pattern)'],
     breed='skyberries')
spec('glimmerfish', 2, 'Cerulon', ['zerog_tweaks:cerulon'], 'passive', 'AbstractSchoolingFish', 'WATER_AMBIENT', 'fast',
     goals=['PanicGoal', 'AvoidEntityGoal<Player>', 'FollowFlockLeaderGoal', 'RandomSwimmingGoal'],
     states=['schooling', 'fleeing', 'flopping (out of water)'],
     anims=['swim', 'flop'],
     mech=['Bucketable: glimmerfish_bucket (new item)', 'At night: emits light via client dynamic light is not vanilla; approximate with glowmask + particles'],
     interact=['water bucket -> glimmerfish_bucket (new)'])
# ------------------------------------------------------------------ Skarn
spec('cinder_hound', 3, 'Skarn', ['zerog_tweaks:skarn'], 'hostile', 'Monster', 'MONSTER', 'fast', follow=24,
     goals=['FloatGoal', 'PackCircleGoal (custom): circle target at 5 blocks until 3+ pack members ready', 'LeapAtTargetGoal(0.4)',
            'MeleeAttackGoal', 'WaterAvoidingRandomStrollGoal', 'HurtByTargetGoal (alert pack)', 'NearestAttackableTargetGoal<Player>'],
     states=['roaming', 'circling', 'lunging', 'attacking'],
     anims=['idle', 'walk', 'run', 'lunge', 'bite'],
     mech=['fireImmune() in EntityType builder', 'Bite: target.igniteForSeconds(2)', 'Ember particle trail while sprinting'],
     immune=['fire', 'lava'])
spec('slag_boar', 3, 'Skarn', ['zerog_tweaks:skarn'], 'neutral', 'Animal + NeutralMob', 'CREATURE', 'medium',
     goals=['FloatGoal', 'ChargeGoal (custom, when angry)', 'HurtByTargetGoal', 'ProtectBabiesGoal (custom, range 4)', 'BreedGoal',
            'TemptGoal(cinder_cap)', 'FollowParentGoal', 'WaterAvoidingRandomStrollGoal', 'LookAtPlayerGoal'],
     states=['rooting', 'wandering', 'charging'],
     anims=['idle', 'walk', 'charge', 'root'],
     mech=['Charge deals 6 + knockback 1.5', 'Angers when a player comes within 4 blocks of its baby'],
     breed='cinder_cap', immune=['fire'])
spec('scorch_wyrmling', 3, 'Skarn', ['zerog_tweaks:skarn'], 'hostile', 'Monster (glides, not full flight)', 'MONSTER', 'medium',
     goals=['FloatGoal', 'RangedAttackGoal (fire bolt, 40t cooldown, range 12)', 'MeleeAttackGoal', 'GuardOreGoal (custom: stay near emberite_ore)',
            'WaterAvoidingRandomStrollGoal', 'NearestAttackableTargetGoal<Player>'],
     states=['perched', 'gliding', 'spitting', 'biting'],
     anims=['idle', 'walk', 'glide', 'spit', 'bite'],
     mech=['Fire bolt: SmallFireball-like projectile (3 dmg + fire)', 'Glide: slow fall + forward motion when jumping off ledges'],
     immune=['fire'])
# ------------------------------------------------------------------ Eidolon
spec('frost_yak', 4, 'Eidolon', ['zerog_tweaks:eidolon'], 'passive', 'Animal + Shearable (Sheep + Cow pattern)', 'CREATURE', 'slow',
     goals=['FloatGoal', 'PanicGoal', 'BreedGoal', 'TemptGoal(frostfern)', 'FollowParentGoal', 'ShelterCalvesGoal (custom, during snow)',
            'WaterAvoidingRandomStrollGoal', 'LookAtPlayerGoal'],
     states=['woolly', 'sheared (regrow by grazing)', 'sheltering'],
     anims=['idle', 'walk', 'graze'],
     mech=['Shears -> yak_wool 1-2; regrows after eating a snowpack/frozen_regolith block', 'Glass bottle -> frost_milk (see ZGInteractions)'],
     breed='frostfern', interact=['shears -> yak_wool', 'glass_bottle -> frost_milk'], immune=['freezing'])
spec('ice_leech', 4, 'Eidolon', ['zerog_tweaks:eidolon'], 'hostile', 'Monster', 'MONSTER', 'medium',
     goals=['FloatGoal', 'HideUnderSnowGoal (custom)', 'LatchOnGoal (custom: ride target)', 'MeleeAttackGoal', 'NearestAttackableTargetGoal<Player>'],
     states=['hidden', 'crawling', 'latched'],
     anims=['idle', 'crawl', 'latch'],
     mech=['Latch: startRiding(player), apply Hunger II while attached', 'Detach when rider sprints 20 ticks or leech is hit'],
     immune=['freezing'])
spec('frost_warden', 4, 'Eidolon', ['zerog_tweaks:eidolon'], 'mini_boss', 'Monster + ServerBossEvent (pale cyan)', 'MONSTER', 'slow', follow=32, armor=10, kb=0.8,
     goals=['FloatGoal', 'GlaiveSweepGoal (custom: 12 dmg arc, Slowness II)', 'MeleeAttackGoal', 'SummonAddsGoal (phase 2: 2 rime_stalker)',
            'IceWallRingGoal (phase 2: ring of glacial_ice radius 6, melts after 200t)', 'StayNearHomeGoal (wreck)', 'NearestAttackableTargetGoal<Player>'],
     states=['guarding', 'phase1', 'phase2 (<50% hp)', 'dead'],
     anims=['idle', 'walk', 'sweep', 'summon', 'death'],
     mech=['Placed by wreck structure; persistenceRequired, no natural respawn', 'Boss bar only within 32 blocks'],
     immune=['freezing'], boss={'bar_color': 'BLUE', 'phases': 2})
# ------------------------------------------------------------------ Solvane
spec('flare_sprite', 5, 'Solvane', ['zerog_tweaks:solvane'], 'hostile', 'FlyingMob / Monster with FlyingMoveControl (Blaze/Vex pattern)', 'MONSTER', 'fast', fly=0.6,
     goals=['FloatGoal', 'RangedAttackGoal (small fireball, range 10)', 'OrbitVentGoal (custom: circle nearest flare_vent)', 'MeleeAttackGoal',
            'WaterAvoidingRandomFlyingGoal', 'NearestAttackableTargetGoal<Player>'],
     states=['orbiting', 'flaring (vent eruption)', 'attacking', 'extinguished'],
     anims=['fly (4-frame wing flicker)', 'attack'],
     mech=['Dies instantly in water or rain (isInWaterRainOrBubble -> kill)', 'Whole model fullbright, no shadow (shadowRadius 0)', 'Near erupting vent: +50% damage for 100t'],
     immune=['fire', 'lava'])
spec('gildcrab', 5, 'Solvane', ['zerog_tweaks:solvane'], 'neutral', 'Animal + NeutralMob', 'CREATURE', 'medium',
     goals=['FloatGoal', 'MeleeAttackGoal (only when angry)', 'HurtByTargetGoal', 'BaskGoal (custom: rest on sunspot_rock)', 'BreedGoal',
            'TemptGoal(pyrefruit)', 'FollowParentGoal', 'SidewaysStrollGoal (custom)', 'LookAtPlayerGoal'],
     states=['basking', 'scuttling', 'pinching'],
     anims=['idle', 'walk_sideways', 'pinch', 'bask'],
     mech=['Moves sideways: rotate body 90 degrees from travel direction', 'Immune to corona_crust/ember_crust damage types'],
     breed='pyrefruit', immune=['fire', 'zerog_tweaks:corona_crust'])
spec('sun_colossus', 5, 'Solvane', ['zerog_tweaks:solvane'], 'mini_boss', 'Monster + ServerBossEvent (yellow)', 'MONSTER', 'very_slow', follow=32, armor=20, kb=1.0,
     goals=['FloatGoal', 'SlamGoal (custom: 14 dmg AoE + fire line ground wave)', 'CoreOpenWindowGoal (custom: 60t vulnerable after slam)',
            'DormantUntilTriggeredGoal (custom: wake when player on plateau)', 'NearestAttackableTargetGoal<Player>'],
     states=['dormant', 'awake', 'slamming', 'core_open', 'dead'],
     anims=['dormant', 'wake', 'walk', 'slam', 'core_open', 'death'],
     mech=['Invulnerable except during core_open window (hurt() returns false otherwise)', 'Drops colossus_core (fusion_reactor upgrade)'],
     immune=['fire', 'lava'], boss={'bar_color': 'YELLOW', 'phases': 1})
# ------------------------------------------------------------------ wastelands
spec('dune_burrower', 0, 'Desert wasteland', WL('desert'), 'hostile', 'Monster', 'MONSTER', 'fast', follow=24, armor=4,
     goals=['FloatGoal', 'BurrowTravelGoal (custom: move under sand, ripple particles)', 'BurstAmbushGoal (custom: target still for 40t)',
            'SwallowGoal (custom: hold player 40t)', 'MeleeAttackGoal', 'NearestAttackableTargetGoal<Player>'],
     states=['burrowed_travel', 'bursting', 'swallowing', 'surface_fight', 'reburrow'],
     anims=['burrow', 'burst', 'swallow', 'walk', 'attack'],
     mech=['While burrowed: noPhysics through sand-tagged blocks, invisible, ripple particles', 'Swallow: player riding mob, invisible, 2 dmg/s for 2 s'],
     )
spec('ash_strider', 0, 'Volcanic wasteland', WL('volcanic'), 'neutral', 'Animal + NeutralMob + ItemSteerable (Strider pattern)', 'CREATURE', 'medium',
     goals=['FloatGoal', 'MeleeAttackGoal (angry)', 'HurtByTargetGoal', 'BreedGoal', 'TemptGoal(cinder_cap)', 'StriderGoToLavaGoal-like',
            'WaterAvoidingRandomStrollGoal', 'LookAtPlayerGoal'],
     states=['wading', 'walking', 'saddled', 'ridden', 'angry'],
     anims=['idle', 'walk', 'stomp'],
     mech=['Walks on lava: canStandOnFluid(lava) = true (copy Strider)', 'Rideable with saddle; steer with a cinder_cap on a stick is optional'],
     breed='cinder_cap', immune=['fire', 'lava'])
spec('rime_stalker', 0, 'Frozen wasteland', WL('frozen'), 'hostile', 'Monster', 'MONSTER', 'fast', follow=24,
     goals=['FloatGoal', 'StalkFromBehindGoal (custom: approach outside player view cone)', 'MeleeAttackGoal', 'WaterAvoidingRandomStrollGoal',
            'NearestAttackableTargetGoal<Player>'],
     states=['stalking', 'hidden_in_blizzard', 'attacking'],
     anims=['idle', 'walk', 'pounce', 'attack'],
     mech=['During snowfall: invisible to players more than 8 blocks away (client-side render check)', 'Hit adds 100 frozen ticks (setTicksFrozen)'],
     immune=['freezing'])
spec('bog_lurker', 0, 'Toxic wasteland', WL('toxic'), 'hostile', 'Monster (amphibious, Drowned-like navigation)', 'MONSTER', 'slow',
     goals=['FloatGoal (not in acid)', 'SubmergeGoal (custom: sit in acid with eyes above surface)', 'RangedAttackGoal (acid spit, Poison II 80t)',
            'MeleeAttackGoal', 'NearestAttackableTargetGoal<Player>'],
     states=['submerged', 'surfacing', 'spitting', 'crawling'],
     anims=['idle', 'walk', 'swim', 'spit'],
     mech=['Speed x2.5 while in zerog_tweaks:acid fluid', 'Immune to acid damage type'],
     immune=['zerog_tweaks:acid', 'poison'])
spec('crater_drifter', 0, 'Barren wasteland', WL('barren') + ['zerog_tweaks:g2_moons', 'zerog_tweaks:g3_moons', 'zerog_tweaks:g4_moons', 'zerog_tweaks:g5_moons'],
     'neutral', 'FlyingMob + NeutralMob (Ghast-like drift, small)', 'CREATURE', 'slow', fly=0.3,
     goals=['FloatGoal', 'DriftGoal (custom: random float 4-10 blocks above ground)', 'MeleeAttackGoal (angry)', 'HurtByTargetGoal (alert others in 16)',
            'DropFragmentGoal (custom: drop meteorite_fragment item every 6000t)'],
     states=['drifting', 'swarming'],
     anims=['float (2 s bob)', 'attack'],
     mech=['No gravity (setNoGravity); bob 2 s cycle in animation only'])
spec('deep_eel', 0, 'Ocean wasteland', WL('ocean'), 'hostile', 'WaterAnimal/Monster with SmoothSwimmingMoveControl (Guardian/Drowned nav)', 'MONSTER', 'fast',
     goals=['FollowLightSourceGoal (custom: move toward block light > 10 or player holding light)', 'MeleeAttackGoal', 'RandomSwimmingGoal',
            'NearestAttackableTargetGoal<Player> (in water only)'],
     states=['lurking', 'following_light', 'biting'],
     anims=['swim', 'bite'],
     mech=['Bite pulls target down: target.push(0,-0.6,0)', 'Out of water: flop and take suffocation damage like fish'])
spec('sand_skitter', 0, 'Desert wasteland', WL('desert'), 'hostile', 'Monster (Spider-like)', 'MONSTER', 'fast',
     goals=['FloatGoal', 'BuriedAmbushGoal (custom: bury in dunesand, burst in 2-3)', 'LeapAtTargetGoal(0.4)', 'MeleeAttackGoal',
            'NearestAttackableTargetGoal<Player>'],
     states=['buried', 'bursting', 'attacking'],
     anims=['idle', 'walk', 'burst', 'sting'],
     mech=['Sting: Poison I 80t', 'Wake one buried skitter triggers the group within 8 blocks'],
     immune=['poison'])
# ------------------------------------------------------------------ guardian bosses
spec('prism_sentinel', 2, 'Galaxy 2 key world', ['(Galaxy 2 key world arena)'], 'boss', 'Monster + ServerBossEvent (cyan) ; no natural spawn', 'MONSTER', 'slow', follow=48, armor=15, kb=1.0,
     goals=['BeamAttackGoal (custom: 10 dmg beams reflecting off orbiting shards)', 'ShardSpinGoal (8 dmg, phase 2)', 'StayInArenaGoal'],
     states=['dialogue ("Are you Concord?")', 'phase1 beams', 'phase2 shards loose', 'phase3 core open (x2 damage to heart)', 'defeated (names you heir)'],
     anims=['idle (shard orbit 4 s)', 'beam', 'shard_spin', 'core_open', 'death'],
     mech=['Phase thresholds 66% / 33%', 'Chat line on start and on defeat (translatable)', 'Drops galaxy_3_gate_key, cerulite 4-6, sentinel_prism, cerulite template'],
     boss={'bar_color': 'BLUE', 'phases': 3})
spec('rift_tyrant', 3, 'Galaxy 3 key world', ['(Galaxy 3 key world arena)'], 'boss', 'Monster + ServerBossEvent (purple) ; no natural spawn', 'MONSTER', 'medium', follow=48, armor=18, kb=1.0,
     goals=['ChargeGoal', 'ClawGoal (16 dmg)', 'RiftPullGoal (pull players toward rift, remove arena blocks)', 'VoidShardVolleyGoal (phase 3)'],
     states=['phase1 charge/claw', 'phase2 rift pull (arena crumbles)', 'phase3 void shards', 'defeated'],
     anims=['idle', 'walk', 'charge', 'claw', 'roar', 'shard_volley', 'death'],
     mech=['Arena block removal: only blocks tagged zerog_tweaks:rift_arena (new tag), restore on reset', 'Void damage type zerog_tweaks:void_rift for pull-into-void'],
     boss={'bar_color': 'PURPLE', 'phases': 3})
spec('eidolon_captain', 4, 'Galaxy 4 key world', ['(Galaxy 4 key world arena)'], 'boss', 'Monster + ServerBossEvent (white) ; no natural spawn', 'MONSTER', 'medium', follow=48, armor=14, kb=0.9,
     goals=['DuelGoal (cutlass 13)', 'SummonCrewGoal (phase 2: Hollow Crewmen = new entity or Shattered Skies Hollow Sentinel)', 'LanternFreezeGoal (phase 3: freeze deck)'],
     states=['waiting', 'parley (holding enough remnant_shard)', 'phase1 duel', 'phase2 crew', 'phase3 lantern', 'yielded', 'defeated'],
     anims=['idle', 'walk', 'slash', 'summon', 'lantern', 'yield', 'death'],
     mech=['Right-click with >= 16 remnant_shard before combat: peaceful path, drops key + captains_lantern', 'Render at 80% alpha, legs 40% (translucent render type)'],
     boss={'bar_color': 'WHITE', 'phases': 3})
spec('dying_star', 5, 'Solvane (orbit arena)', ['(Solvane orbital ring arena)'], 'final_boss', 'FlyingMob + ServerBossEvent (yellow->white) ; no natural spawn', 'MONSTER', 'slow', follow=64, armor=20, kb=1.0, fly=0.4,
     goals=['SolarFlareGoal (20 dmg)', 'CoronaRaySweepGoal (phase 2)', 'FallingStarsGoal (12 dmg)', 'CollapseGoal (phase 3: arena shrink)'],
     states=['phase1 Vael on surface', 'phase2 corona rays', 'phase3 collapse', 'defeated (ending choice)'],
     anims=['idle (ray rotation)', 'flare', 'sweep', 'collapse', 'death'],
     mech=['Drops heart_of_solvane; each player chooses Rekindle / Let it fade (Codex screen)', 'Brightness pulse scales with missing health'],
     boss={'bar_color': 'YELLOW', 'phases': 3})
# ------------------------------------------------------------------ Sol food mobs
spec('moon_hopper', 1, 'Moon', ['zerog_tweaks:moon'], 'passive', 'Animal (Rabbit pattern: JumpControl + RabbitMoveControl)', 'CREATURE', 'medium',
     goals=['FloatGoal', 'PanicGoal(2.2)', 'BreedGoal', 'TemptGoal(lunar_lichen)', 'AvoidEntityGoal<Player> (when not tempted)',
            'WaterAvoidingRandomStrollGoal', 'LookAtPlayerGoal'],
     states=['hopping', 'grazing', 'fleeing'],
     anims=['idle', 'hop', 'graze'],
     mech=['Jump power scaled so it clears ~4 blocks at Moon gravity (0.5x)', 'No fall damage (causeFallDamage returns false)'],
     breed='lunar_lichen')
spec('dust_grazer', 1, 'Mars', ['zerog_tweaks:mars'], 'passive', 'Animal (Cow pattern)', 'CREATURE', 'medium',
     goals=['FloatGoal', 'StampedeGoal (custom: when one is hurt, herd within 12 panics in the same direction)', 'PanicGoal(2.0)', 'BreedGoal',
            'TemptGoal(rust_tuber)', 'FollowParentGoal', 'EatBlockGoal-style graze', 'WaterAvoidingRandomStrollGoal', 'LookAtPlayerGoal'],
     states=['grazing', 'wandering', 'stampeding'],
     anims=['idle', 'walk', 'run', 'graze'],
     mech=['Stampede: entities in the herd trample (1 dmg) anything they run through', 'Mane sway animation driven by dust-storm weather flag'],
     breed='rust_tuber')

# ------------------------------------------------------------------ state transitions (index into states list, trigger)
# [*] start is always state 0. -1 as target = entity removed/dead.
T = {
 'regolith_crawler': [(0, 1, 'player within 3 blocks, not sneaking'), (1, 2, 'emerge anim done (20t)'), (2, 3, 'target in 3 blocks, cooldown ready'),
                      (3, 2, 'lunge lands'), (2, 0, 'no target 200t'), (2, 4, 'health 0'), (4, -1, '')],
 'rust_beetle': [(0, 1, 'grazed / random'), (1, 0, 'finds rust_lichen'), (0, 3, 'random hop (low gravity)'), (1, 3, 'random hop'), (3, 1, 'lands'),
                 (0, 2, 'hurt'), (1, 2, 'hurt'), (2, 1, 'anger timer ends'), (1, 4, 'fed rust_lichen (tame roll)'), (4, 5, 'ferrox saddle + chest')],
 'crystal_stag': [(0, 1, 'sheared: drop starlite'), (1, 0, '6000t regrow'), (0, 2, 'hurt'), (1, 2, 'hurt'), (2, 0, 'panic ends, antlers intact'), (2, 1, 'panic ends, sheared')],
 'prismling': [(0, 1, 'player seen / ally hurt'), (1, 0, 'target lost'), (1, 2, 'health 0: burst 2-3 shards'), (2, -1, '')],
 'azure_fowl': [(0, 1, 'falling (not on ground)'), (1, 0, 'lands'), (0, 2, 'egg timer 6000-12000t'), (2, 0, 'blue_egg dropped')],
 'glimmerfish': [(0, 1, 'hurt / player close'), (1, 0, 'safe'), (0, 2, 'out of water'), (1, 2, 'out of water'), (2, 0, 'back in water')],
 'cinder_hound': [(0, 1, 'target found'), (1, 2, '3+ pack members circling'), (2, 3, 'lands next to target'), (3, 1, 'target retreats'), (3, 0, 'target lost')],
 'slag_boar': [(0, 1, 'random'), (1, 0, 'finds slag'), (0, 2, 'hurt / player near baby'), (1, 2, 'hurt / player near baby'), (2, 1, 'anger timer ends')],
 'scorch_wyrmling': [(0, 1, 'jumps off ledge'), (1, 0, 'lands'), (0, 2, 'target in 12 blocks'), (1, 2, 'target in 12 blocks'), (2, 3, 'target in melee range'),
                     (3, 2, 'target backs off'), (2, 0, 'target lost')],
 'frost_yak': [(0, 1, 'sheared: yak_wool'), (1, 0, 'eats snowpack / frozen_regolith'), (0, 2, 'snowfall + calf nearby'), (1, 2, 'snowfall + calf nearby'), (2, 0, 'weather clears')],
 'ice_leech': [(0, 1, 'player steps within 2 blocks'), (1, 2, 'touches target: ride'), (2, 1, 'player sprints 20t / leech hit'), (1, 0, 'no target 200t')],
 'frost_warden': [(0, 1, 'player enters wreck (16 blocks)'), (1, 2, 'health < 50%: summon 2 rime_stalker + ice ring'), (2, 3, 'health 0'), (1, 0, 'no players 600t (heal)'), (3, -1, '')],
 'flare_sprite': [(0, 1, 'nearby flare_vent erupts'), (1, 0, '100t'), (0, 2, 'target in 10 blocks'), (1, 2, 'target in 10 blocks'), (2, 0, 'target lost'),
                  (0, 3, 'water or rain'), (2, 3, 'water or rain'), (3, -1, 'instant death')],
 'gildcrab': [(0, 1, 'random / disturbed'), (1, 0, 'on sunspot_rock'), (0, 2, 'hurt'), (1, 2, 'hurt'), (2, 1, 'anger timer ends')],
 'sun_colossus': [(0, 1, 'player on plateau'), (1, 2, 'target in 6 blocks'), (2, 3, 'slam done'), (3, 1, '60t window closes'), (1, 4, 'health 0'), (3, 4, 'health 0'), (4, -1, '')],
 'dune_burrower': [(0, 1, 'target still 40t above it'), (1, 2, 'catches target'), (1, 3, 'misses'), (2, 3, '40t, spit out'), (3, 4, '200t or target lost'), (4, 0, 'under sand')],
 'ash_strider': [(0, 1, 'leaves lava'), (1, 0, 'enters lava'), (0, 2, 'saddle'), (1, 2, 'saddle'), (2, 3, 'player mounts'), (3, 2, 'dismount'),
                 (0, 4, 'hurt'), (1, 4, 'hurt'), (4, 1, 'anger timer ends')],
 'rime_stalker': [(0, 1, 'snowfall and player > 8 blocks'), (1, 0, 'player within 8 / weather clears'), (0, 2, 'behind target, in range'), (1, 2, 'behind target, in range'),
                  (2, 0, 'target turns to face it')],
 'bog_lurker': [(0, 1, 'target near acid edge'), (1, 2, 'target in 10 blocks'), (2, 3, 'target on land, close'), (3, 0, 'back in acid'), (2, 0, 'target lost')],
 'crater_drifter': [(0, 1, 'this or nearby drifter hurt'), (1, 0, 'anger timer ends')],
 'deep_eel': [(0, 1, 'light source > 10 or player with light'), (1, 2, 'target in water, in range'), (2, 0, 'target leaves water'), (1, 0, 'light gone')],
 'sand_skitter': [(0, 1, 'player within 4 or group member bursts'), (1, 2, 'out of sand'), (2, 0, 'target lost 200t (re-bury)')],
 'prism_sentinel': [(0, 1, 'player answers / attacks'), (1, 2, 'health < 66%'), (2, 3, 'health < 33%'), (3, 4, 'health 0'), (4, -1, 'heir granted')],
 'rift_tyrant': [(0, 1, 'health < 66%'), (1, 2, 'health < 33%'), (2, 3, 'health 0'), (3, -1, '')],
 'eidolon_captain': [(0, 1, 'player right-clicks holding 16 remnant_shard'), (0, 2, 'player attacks / enters deck without shards'), (1, 5, 'reads final log'),
                     (2, 3, 'health < 66%'), (3, 4, 'health < 33%'), (4, 6, 'health 0'), (5, -1, 'key + captains_lantern'), (6, -1, 'key')],
 'dying_star': [(0, 1, 'health < 66%'), (1, 2, 'health < 33%'), (2, 3, 'health 0'), (3, -1, 'Heart of Solvane: choose ending')],
 'moon_hopper': [(0, 1, 'finds lunar_lichen'), (1, 0, 'random'), (0, 2, 'hurt / player close'), (1, 2, 'hurt'), (2, 0, 'safe')],
 'dust_grazer': [(0, 1, 'random'), (1, 0, 'finds grass-like block'), (0, 2, 'any herd member within 12 hurt'), (1, 2, 'herd member hurt'), (2, 1, 'panic ends (100t)')],
}
for _k, _v in T.items():
    n = len(S[_k]['states'])
    assert all(0 <= a < n and (-1 <= b < n) for a, b, _ in _v), _k
    S[_k]['transitions'] = [dict(frm=S[_k]['states'][a], to=('[removed]' if b == -1 else S[_k]['states'][b]), trigger=t) for a, b, t in _v]
    S[_k]['_T'] = _v
assert set(T) == set(S)

# ------------------------------------------------------------------ vanilla base per mob (for rigging and animating)
# base: the vanilla mob whose skeleton and motion ours copies. also: extra vanilla refs for specific moves.
# rig: how our bones line up with the vanilla model parts. anims: our animation -> the vanilla motion to copy.
VANILLA = {
 'regolith_crawler': dict(base='minecraft:spider', also=['minecraft:silverfish'],
    rig='Spider layout: low body, head in front, legs in pairs splayed sideways (we have 3 pairs instead of 4).',
    anims={'idle': 'spider idle (legs still, slight body sway)', 'walk': 'spider walk (alternating leg pairs)', 'burrow': 'silverfish hiding in a block: sink down in 20 ticks',
           'emerge': 'reverse of burrow, then spider-style rear-up', 'lunge': 'spider leap (LeapAtTargetGoal arc)', 'death': 'vanilla death tip-over'}),
 'rust_beetle': dict(base='minecraft:armadillo', also=['minecraft:llama', 'minecraft:goat'],
    rig='Armadillo layout: domed shell over a small body, short legs, head low at the front. Horn on the head bone.',
    anims={'idle': 'armadillo idle', 'walk': 'armadillo walk', 'ram': 'goat ram (head down, charge)', 'hop': 'rabbit hop timing, with the shell split open like elytra',
           'graze': 'sheep eat-grass head dip'}),
 'crystal_stag': dict(base='minecraft:horse', also=['minecraft:goat'],
    rig='Horse layout: long legs, neck and head raised in front, tail at the back. Antlers sit on the head bone.',
    anims={'idle': 'horse idle (tail swish, head bob)', 'walk': 'horse walk', 'run': 'horse gallop', 'graze': 'horse eating (neck down)'}),
 'prismling': dict(base='minecraft:endermite', also=['minecraft:silverfish'],
    rig='Endermite layout: small body segments close to the ground; crystal spikes ride the body bone.',
    anims={'idle': 'endermite idle wiggle', 'walk': 'endermite skitter', 'attack': 'silverfish lunge bite', 'shatter': 'custom: scale to 0 with shard particles'}),
 'azure_fowl': dict(base='minecraft:chicken', also=['minecraft:parrot'],
    rig='Chicken layout exactly: body, head, beak, wings, two legs. Crest on the head bone.',
    anims={'idle': 'chicken idle (head peck)', 'walk': 'chicken walk', 'glide': 'chicken falling (wings flap slowly, fall slowed)', 'flap': 'chicken wing flap'}),
 'glimmerfish': dict(base='minecraft:tropical_fish', also=['minecraft:salmon'],
    rig='Tropical fish layout: body, tail fin, top and side fins.',
    anims={'swim': 'tropical fish tail wave', 'flop': 'fish flopping on land'}),
 'cinder_hound': dict(base='minecraft:wolf',
    rig='Wolf layout exactly: body, mane, head with snout and ears, 4 legs, tail.',
    anims={'idle': 'wolf idle (tail wag)', 'walk': 'wolf walk', 'run': 'wolf run', 'lunge': 'wolf LeapAtTarget pounce', 'bite': 'wolf attack snap'}),
 'slag_boar': dict(base='minecraft:hoglin',
    rig='Hoglin layout exactly: big head with tusks, body, 4 legs. Our tail is an extra bone.',
    anims={'idle': 'hoglin idle', 'walk': 'hoglin walk', 'charge': 'hoglin head-toss attack while running', 'root': 'hoglin head down, swinging side to side'}),
 'scorch_wyrmling': dict(base='minecraft:parrot', also=['minecraft:phantom', 'minecraft:blaze'],
    rig='Parrot layout: small body that walks and glides, two wings, tail; head on a short neck.',
    anims={'idle': 'parrot idle', 'walk': 'parrot walk', 'glide': 'phantom glide (wings out, slow flap)', 'spit': 'llama spit head jerk (projectile like a blaze fireball)',
           'bite': 'parrot peck, scaled up'}),
 'frost_yak': dict(base='minecraft:cow', also=['minecraft:sheep', 'minecraft:llama'],
    rig='Cow layout: big body, head with horns, 4 legs. Wool is an extra layer on the body, like the sheep wool layer.',
    anims={'idle': 'cow idle', 'walk': 'cow walk', 'graze': 'sheep eat-grass'}),
 'ice_leech': dict(base='minecraft:silverfish',
    rig='Silverfish layout: a chain of body segments, each its own bone.',
    anims={'idle': 'silverfish idle', 'crawl': 'silverfish crawl (segment wave)', 'latch': 'custom: curl around, ride the player like a chicken jockey'}),
 'frost_warden': dict(base='minecraft:vindicator', also=['minecraft:warden', 'minecraft:iron_golem'],
    rig='Vindicator (illager) layout: head, body, 2 arms, 2 legs; the glaive is held in the right arm like the vindicator axe. Walk weight from the warden.',
    anims={'idle': 'vindicator idle, arms crossed or weapon held', 'walk': 'warden heavy walk', 'sweep': 'vindicator axe swing, widened into a sweep',
           'summon': 'evoker spell-cast (arms raised)', 'death': 'vanilla death tip-over'}),
 'flare_sprite': dict(base='minecraft:vex', also=['minecraft:blaze'],
    rig='Vex layout: small flying humanoid with two wings, no legs used.',
    anims={'fly': 'vex flying (wing flicker, hover bob)', 'attack': 'blaze fireball charge (glow up, then shoot)'}),
 'gildcrab': dict(base='minecraft:spider', also=['minecraft:armadillo'],
    rig='Spider layout turned sideways: body wider than long, legs splayed left and right; pincers are extra front arm bones.',
    anims={'idle': 'spider idle', 'walk_sideways': 'spider walk played on the X axis', 'pinch': 'custom pincer snap', 'bask': 'armadillo settled pose'}),
 'sun_colossus': dict(base='minecraft:iron_golem', also=['minecraft:warden'],
    rig='Iron golem layout: big body, small head, long arms, 2 legs.',
    anims={'dormant': 'custom: crouched, still', 'wake': 'warden emerge (rising out of the ground)', 'walk': 'iron golem walk',
           'slam': 'iron golem attack (both arms swing down)', 'core_open': 'custom: chest plates swing open', 'death': 'vanilla death tip-over'}),
 'dune_burrower': dict(base='minecraft:silverfish', also=['minecraft:sniffer', 'minecraft:warden'],
    rig='Silverfish layout scaled up: a chain of segments with a big head segment.',
    anims={'burrow': 'warden dig (sinking)', 'burst': 'warden emerge, fast', 'swallow': 'custom: head segment opens and closes',
           'walk': 'silverfish crawl', 'attack': 'silverfish lunge'}),
 'ash_strider': dict(base='minecraft:strider',
    rig='Strider layout exactly: body block on two long legs, bristles on the body.',
    anims={'idle': 'strider idle', 'walk': 'strider walk (also on lava)', 'stomp': 'strider leg stamp, emphasized'}),
 'rime_stalker': dict(base='minecraft:ocelot', also=['minecraft:wolf'],
    rig='Ocelot/cat layout: long body, 4 legs, long tail, head with ears. Spines on the body bone.',
    anims={'idle': 'ocelot idle', 'walk': 'ocelot sneak-walk (crouched stalk)', 'pounce': 'ocelot/cat pounce', 'attack': 'wolf bite'}),
 'bog_lurker': dict(base='minecraft:axolotl', also=['minecraft:frog'],
    rig='Axolotl layout scaled up: long flat body, 4 short legs, tail, wide head.',
    anims={'idle': 'axolotl idle (lying still)', 'walk': 'axolotl walk on land', 'swim': 'axolotl swim', 'spit': 'llama spit head jerk'}),
 'crater_drifter': dict(base='minecraft:ghast', also=['minecraft:allay'],
    rig='Ghast layout, small: floating body with hanging tendrils.',
    anims={'float': 'ghast idle (tendril sway, bob)', 'attack': 'ghast shoot (body flinch forward)'}),
 'deep_eel': dict(base='minecraft:dolphin', also=['minecraft:guardian', 'minecraft:drowned'],
    rig='Dolphin layout stretched into an eel: head, body segments, tail.',
    anims={'swim': 'dolphin swim wave, carried down each segment', 'bite': 'guardian snap, with a pull-down'}),
 'sand_skitter': dict(base='minecraft:spider', also=['minecraft:silverfish'],
    rig='Spider layout: body and head low, 6-8 splayed legs; the stinger tail is an extra bone chain arched over the back.',
    anims={'idle': 'spider idle', 'walk': 'spider walk', 'burst': 'silverfish popping out of a block', 'sting': 'custom: tail arcs over and forward'}),
 'prism_sentinel': dict(base='minecraft:blaze', also=['minecraft:guardian', 'minecraft:elder_guardian'],
    rig='Blaze layout: floating core with an orbit bone for the shards (like the blaze rods), no legs.',
    anims={'idle': 'blaze idle (rods orbit), 4 s loop', 'beam': 'guardian laser charge and fire', 'shard_spin': 'blaze rods spinning fast',
           'core_open': 'custom: core plates open', 'death': 'custom: shards fall, core cracks'}),
 'rift_tyrant': dict(base='minecraft:ravager', also=['minecraft:warden'],
    rig='Ravager layout: huge body, heavy head with jaw, 4 legs. Spines on the body bone.',
    anims={'idle': 'ravager idle', 'walk': 'ravager walk', 'charge': 'ravager charge', 'claw': 'ravager bite, turned into a swipe',
           'roar': 'ravager roar', 'shard_volley': 'warden sonic boom wind-up', 'death': 'vanilla death tip-over'}),
 'eidolon_captain': dict(base='minecraft:vindicator', also=['minecraft:evoker', 'minecraft:vex'],
    rig='Vindicator (illager) layout: the cutlass in the right arm, the lantern in the left. Rendered see-through like a vex.',
    anims={'idle': 'vindicator idle', 'walk': 'vindicator walk', 'slash': 'vindicator axe swing', 'summon': 'evoker summon (arms raised)',
           'lantern': 'evoker spell-cast holding the lantern high', 'yield': 'custom: kneels, sword down', 'death': 'custom: fades out'}),
 'dying_star': dict(base='minecraft:wither', also=['minecraft:blaze', 'minecraft:ender_dragon'],
    rig='Wither-style floating boss: core body with ray bones orbiting like blaze rods; Vael is a bone on top.',
    anims={'idle': 'wither hover and blaze-rod rotation', 'flare': 'wither charge-up and blast', 'sweep': 'ender dragon breath sweep',
           'collapse': 'wither spawn in reverse (shrinks)', 'death': 'ender dragon death beams'}),
 'moon_hopper': dict(base='minecraft:rabbit',
    rig='Rabbit layout exactly: body, head, long ears, big hind feet.',
    anims={'idle': 'rabbit idle (nose twitch)', 'hop': 'rabbit jump (scale the height ×2 for Moon gravity)', 'graze': 'rabbit eating'}),
 'dust_grazer': dict(base='minecraft:cow', also=['minecraft:goat'],
    rig='Cow layout: body, head with curved horns, 4 legs; the mane is an extra layer on the body.',
    anims={'idle': 'cow idle', 'walk': 'cow walk', 'run': 'cow panic run', 'graze': 'sheep eat-grass'}),
}
assert set(VANILLA) == set(S), set(VANILLA) ^ set(S)
for _k, _v in VANILLA.items():
    need = [a.split(' ')[0] for a in S[_k]['animations']]
    assert set(_v['anims']) == set(need), (_k, set(_v['anims']) ^ set(need))
    S[_k]['vanilla'] = _v

# ------------------------------------------------------------------ eye styles + boss scale (art direction)
# side      : prey/grazer eyes, one on each side of the head (like vanilla cow, horse, fish); never both visible from straight ahead
# front     : predator/humanoid eyes, both on the front face (like wolf, spider, illagers)
# ender_eye : one central eye drawn in the style of the vanilla Eye of Ender (round orb, ringed iris, dark slit pupil,
#             one highlight pixel), recoloured to the mob's palette and placed on the glowmask
# stalk     : eyes raised on short stalks above the head (crab/snail style), each stalk its own bone so it can swivel
EYE_STYLES = {
    'side': 'One eye on each side of the head, set back from the snout; read from the side view, not the front.',
    'front': 'Both eyes on the front face, level and close together; read from the front view.',
    'ender_eye': 'A single central eye modelled on the vanilla Eye of Ender: round orb, ringed iris, dark vertical slit pupil, one highlight pixel. Recoloured per mob, emissive.',
    'stalk': 'Two eyes on short stalks rising above the head; each stalk is its own bone and swivels in idle.',
}
# source: 'team' = decided by the art team, 'proposed' = filled in to match the vanilla base, confirm before modelling
EYES = {
    'crystal_stag': ('side', 'team'), 'azure_fowl': ('side', 'team'), 'glimmerfish': ('side', 'team'),
    'scorch_wyrmling': ('side', 'team'), 'dust_grazer': ('side', 'team'),
    'regolith_crawler': ('front', 'team'), 'rift_tyrant': ('front', 'team'), 'rust_beetle': ('front', 'team'),
    'sand_skitter': ('front', 'team'), 'rime_stalker': ('front', 'team'), 'frost_warden': ('front', 'team'),
    'dune_burrower': ('front', 'team'), 'moon_hopper': ('front', 'team'),
    'prismling': ('ender_eye', 'team'), 'flare_sprite': ('ender_eye', 'team'), 'dying_star': ('ender_eye', 'team'),
    'crater_drifter': ('ender_eye', 'team'), 'ash_strider': ('ender_eye', 'team'),
    'bog_lurker': ('stalk', 'team'), 'gildcrab': ('stalk', 'team'),
    # not covered by the team list yet
    'cinder_hound': ('front', 'proposed'), 'eidolon_captain': ('front', 'proposed'), 'sun_colossus': ('front', 'proposed'),
    'ice_leech': ('front', 'proposed'), 'slag_boar': ('side', 'proposed'), 'frost_yak': ('side', 'proposed'),
    'deep_eel': ('side', 'proposed'), 'prism_sentinel': ('ender_eye', 'proposed'),
}
# Shattered Skies creatures (their models live in docs/shattered-skies/models; listed here so one table covers every mob)
SS_EYES = {
    'mossback': ('side', 'team', ''), 'amethyst_stalker': ('side', 'team', ''), 'meteor_maw': ('side', 'team', ''),
    'tidewraith': ('side', 'team', 'Build it on the vanilla Phantom model: same rig and flight animations, retextured with pixel scales and manta-ray gill slits on the underside.'),
    'hollow_sentinel': ('front', 'team', ''), 'stormbitten_wyvern': ('front', 'team', ''),
    'splinter_mite': ('ender_eye', 'team', 'Listed as "Splinter": applied to both Splinter adds.'),
    'splinter_wisp': ('ender_eye', 'team', 'Listed as "Splinter": applied to both Splinter adds.'),
    'shardmother': ('stalk', 'team', ''), 'slagjaw': ('front', 'proposed', ''),
}
# Guardian bosses are built at six times the player's size (player 0.6 x 1.8 -> 3.6 wide, 10.8 tall)
BOSS_SCALE = 6.0
PLAYER = (0.6, 1.8)
assert set(EYES) == set(S), set(EYES) ^ set(S)
for _k, (_e, _src) in EYES.items():
    S[_k]['eye_style'] = _e; S[_k]['eye_source'] = _src
    if S[_k]['role'] in ('boss', 'final_boss'):
        S[_k]['scale_rule'] = f'{BOSS_SCALE:g}x player size: {PLAYER[0]*BOSS_SCALE:g} wide, {PLAYER[1]*BOSS_SCALE:g} tall'
        S[_k]['hitbox_override'] = (PLAYER[0] * BOSS_SCALE, PLAYER[1] * BOSS_SCALE)
