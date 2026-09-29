# Mob diagrams

Mermaid sources render on GitHub. PNG copies sit next to each `.mmd` file.

## Mob world map

```mermaid
flowchart LR
  subgraph Guardian_bosses___key_worlds["Guardian bosses · key worlds"]
    direction TB
    prism_sentinel["Prism Sentinel<br/>300 hp"]:::boss
    rift_tyrant["Rift Tyrant<br/>450 hp"]:::boss
    eidolon_captain["Eidolon Captain<br/>400 hp"]:::boss
    dying_star["The Dying Star<br/>900 hp"]:::boss
  end
  subgraph Wastelands___every_galaxy__tinted_["Wastelands · every galaxy (tinted)"]
    direction TB
    dune_burrower["Dune Burrower<br/>40 hp<br/>Desert"]:::hostile
    ash_strider["Ash Strider<br/>30 hp<br/>Volcanic"]:::neutral
    rime_stalker["Rime Stalker<br/>24 hp<br/>Frozen"]:::hostile
    bog_lurker["Bog Lurker<br/>28 hp<br/>Toxic"]:::hostile
    crater_drifter["Crater Drifter<br/>20 hp<br/>Barren"]:::neutral
    deep_eel["Deep Eel<br/>22 hp<br/>Ocean"]:::hostile
    sand_skitter["Sand Skitter<br/>16 hp<br/>Desert"]:::hostile
  end
  subgraph Galaxy_5___Solvane["Galaxy 5 · Solvane"]
    direction TB
    flare_sprite["Flare Sprite<br/>6 hp"]:::hostile
    sun_colossus["Sun Colossus<br/>200 hp"]:::boss
    gildcrab["Gildcrab<br/>12 hp"]:::neutral
  end
  subgraph Galaxy_4___Eidolon["Galaxy 4 · Eidolon"]
    direction TB
    frost_warden["Frost Warden<br/>120 hp"]:::boss
    frost_yak["Frost Yak<br/>30 hp"]:::passive
    ice_leech["Ice Leech<br/>14 hp"]:::hostile
  end
  subgraph Galaxy_3___Skarn["Galaxy 3 · Skarn"]
    direction TB
    cinder_hound["Cinder Hound<br/>18 hp"]:::hostile
    slag_boar["Slag Boar<br/>26 hp"]:::neutral
    scorch_wyrmling["Scorch Wyrmling<br/>16 hp"]:::hostile
  end
  subgraph Galaxy_2___Cerulon["Galaxy 2 · Cerulon"]
    direction TB
    crystal_stag["Crystal Stag<br/>20 hp"]:::passive
    prismling["Prismling<br/>8 hp"]:::hostile
    azure_fowl["Azure Fowl<br/>4 hp"]:::passive
    glimmerfish["Glimmerfish<br/>3 hp"]:::passive
  end
  subgraph Sol___Mars["Sol · Mars"]
    direction TB
    rust_beetle["Rust Beetle<br/>20 hp"]:::neutral
    dust_grazer["Dust Grazer<br/>24 hp"]:::passive
  end
  subgraph Sol___Moon["Sol · Moon"]
    direction TB
    regolith_crawler["Regolith Crawler<br/>14 hp"]:::hostile
    moon_hopper["Moon Hopper<br/>6 hp"]:::passive
  end
  classDef passive fill:#d9f2e3,stroke:#2e7d4f,color:#123
  classDef neutral fill:#fff1cc,stroke:#b8860b,color:#321
  classDef hostile fill:#ffd9d6,stroke:#b3261e,color:#300
  classDef boss fill:#e6dcff,stroke:#5b3fb3,color:#102,stroke-width:2px
```

## Mob drops food chain

```mermaid
flowchart LR
  regolith_crawler(["Regolith Crawler"]):::hostile --> zerog_tweaks_crawler_leg["Crawler Leg"]
  zerog_tweaks_crawler_leg -- cook --> zerog_tweaks_roasted_crawler_leg["Roasted Crawler Leg"]:::cooked
  rust_beetle(["Rust Beetle"]):::neutral --> zerog_tweaks_beetle_grub["Beetle Grub"]
  zerog_tweaks_beetle_grub -- cook --> zerog_tweaks_toasted_grub["Toasted Grub"]:::cooked
  crystal_stag(["Crystal Stag"]):::passive --> zerog_tweaks_stag_venison["Stag Venison"]
  zerog_tweaks_stag_venison -- cook --> zerog_tweaks_cooked_venison["Cooked Venison"]:::cooked
  dune_burrower(["Dune Burrower"]):::hostile --> zerog_tweaks_burrower_steak["Burrower Steak"]
  zerog_tweaks_burrower_steak -- cook --> zerog_tweaks_cooked_burrower_steak["Cooked Burrower Steak"]:::cooked
  bog_lurker(["Bog Lurker"]):::hostile --> zerog_tweaks_lurker_leg["Lurker Leg"]
  zerog_tweaks_lurker_leg -- cook --> zerog_tweaks_crispy_lurker_leg["Crispy Lurker Leg"]:::cooked
  crater_drifter(["Crater Drifter"]):::neutral --> zerog_tweaks_stardust["Stardust"]
  zerog_tweaks_stardust --> zerog_tweaks_low_g_jelly["Low-G Jelly"]:::dish
  moon_hopper(["Moon Hopper"]):::passive --> zerog_tweaks_hopper_meat["Hopper Meat"]
  zerog_tweaks_hopper_meat -- cook --> zerog_tweaks_cooked_hopper["Cooked Hopper"]:::cooked
  dust_grazer(["Dust Grazer"]):::passive --> zerog_tweaks_grazer_steak["Grazer Steak"]
  zerog_tweaks_grazer_steak -- cook --> zerog_tweaks_seared_grazer_steak["Seared Grazer Steak"]:::cooked
  zerog_tweaks_seared_grazer_steak --> zerog_tweaks_astronaut_ration["Astronaut Ration"]:::dish
  zerog_tweaks_seared_grazer_steak --> zerog_tweaks_orbit_burger["Orbit Burger"]:::dish
  azure_fowl(["Azure Fowl"]):::passive --> zerog_tweaks_fowl["Raw Fowl"]
  zerog_tweaks_fowl -- cook --> zerog_tweaks_roast_fowl["Roast Fowl"]:::cooked
  glimmerfish(["Glimmerfish"]):::passive --> zerog_tweaks_glimmerfish["Glimmerfish"]
  zerog_tweaks_glimmerfish -- cook --> zerog_tweaks_cooked_glimmerfish["Cooked Glimmerfish"]:::cooked
  slag_boar(["Slag Boar"]):::neutral --> zerog_tweaks_boar_chop["Boar Chop"]
  zerog_tweaks_boar_chop -- cook --> zerog_tweaks_smoked_boar_chop["Smoked Boar Chop"]:::cooked
  zerog_tweaks_smoked_boar_chop --> zerog_tweaks_ember_chili["Ember Chili"]:::dish
  scorch_wyrmling(["Scorch Wyrmling"]):::hostile --> zerog_tweaks_scorch_tail["Scorch Tail"]
  zerog_tweaks_scorch_tail -- cook --> zerog_tweaks_grilled_scorch_tail["Grilled Scorch Tail"]:::cooked
  zerog_tweaks_grilled_scorch_tail --> zerog_tweaks_ember_chili["Ember Chili"]:::dish
  frost_yak(["Frost Yak"]):::passive --> zerog_tweaks_yak_meat["Yak Meat"]
  zerog_tweaks_yak_meat -- cook --> zerog_tweaks_yak_roast["Yak Roast"]:::cooked
  zerog_tweaks_yak_roast --> zerog_tweaks_cryo_chowder["Cryo Chowder"]:::dish
  zerog_tweaks_yak_roast --> zerog_tweaks_ration_pack["Ration Pack"]:::dish
  ice_leech(["Ice Leech"]):::hostile --> zerog_tweaks_leech_gel["Leech Gel"]
  zerog_tweaks_leech_gel --> zerog_tweaks_low_g_jelly["Low-G Jelly"]:::dish
  gildcrab(["Gildcrab"]):::neutral --> zerog_tweaks_gildcrab_meat["Gildcrab Meat"]
  zerog_tweaks_gildcrab_meat -- cook --> zerog_tweaks_cooked_gildcrab["Cooked Gildcrab"]:::cooked
  zerog_tweaks_cooked_gildcrab --> zerog_tweaks_starfall_feast["Starfall Feast"]:::dish
  deep_eel(["Deep Eel"]):::hostile --> zerog_tweaks_eel_fillet["Eel Fillet"]
  zerog_tweaks_eel_fillet -- cook --> zerog_tweaks_cooked_eel["Cooked Eel"]:::cooked
  sand_skitter(["Sand Skitter"]):::hostile --> zerog_tweaks_skitter_leg["Skitter Leg"]
  zerog_tweaks_skitter_leg -- cook --> zerog_tweaks_roasted_skitter_leg["Roasted Skitter Leg"]:::cooked
  classDef passive fill:#d9f2e3,stroke:#2e7d4f,color:#123
  classDef neutral fill:#fff1cc,stroke:#b8860b,color:#321
  classDef hostile fill:#ffd9d6,stroke:#b3261e,color:#300
  classDef boss fill:#e6dcff,stroke:#5b3fb3,color:#102,stroke-width:2px
  classDef cooked fill:#ffe6cc,stroke:#c26a00,color:#310
  classDef dish fill:#e0ecff,stroke:#2458b3,color:#012
```

## Boss progression

```mermaid
flowchart LR
  T2["T2 gate<br/>(Sol materials)"] --> G2(("Galaxy 2"))
  G2 --> PS["Prism Sentinel<br/>300 hp · 3 phases"]:::boss
  PS --> K3["Galaxy 3 Gate Key"] & CT["Cerulite template"] & SP["Sentinel Prism<br/>T3 lens upgrade"]
  K3 --> G3(("Galaxy 3")) --> RT["Rift Tyrant<br/>450 hp · 3 phases"]:::boss
  RT --> K4["Galaxy 4 Gate Key"] & ST["Skarnite template"] & RH["Rift Heart"]
  K4 --> G4(("Galaxy 4")) --> EC["Eidolon Captain<br/>400 hp · fight or parley"]:::boss
  EC --> K5["Galaxy 5 Gate Key"] & ET["Eidolite template"] & CL["Captain's Lantern<br/>(if spared)"]
  G4 -.-> FW["Frost Warden<br/>mini-boss · wrecks"]:::boss --> RS["Remnant Shards<br/>(parley needs 16)"] -.-> EC
  K5 --> G5(("Galaxy 5")) --> SC["Sun Colossus<br/>mini-boss · plateaus"]:::boss --> SV["Solvanite template<br/>Colossus Core"]
  G5 --> DS["The Dying Star<br/>900 hp · final boss"]:::boss --> HS["Heart of Solvane<br/>Rekindle or Let it fade"]
  classDef passive fill:#d9f2e3,stroke:#2e7d4f,color:#123
  classDef neutral fill:#fff1cc,stroke:#b8860b,color:#321
  classDef hostile fill:#ffd9d6,stroke:#b3261e,color:#300
  classDef boss fill:#e6dcff,stroke:#5b3fb3,color:#102,stroke-width:2px
```

## Behavior states per mob

### Regolith Crawler

```mermaid
stateDiagram-v2
  direction LR
  state "burrowed" as s0
  state "emerging" as s1
  state "hunting" as s2
  state "lunging" as s3
  state "dead" as s4
  [*] --> s0
  s0 --> s1 : player within 3 blocks, not sneaking
  s1 --> s2 : emerge anim done (20t)
  s2 --> s3 : target in 3 blocks, cooldown ready
  s3 --> s2 : lunge lands
  s2 --> s0 : no target 200t
  s2 --> s4 : health 0
  s4 --> [*]
```

### Rust Beetle

```mermaid
stateDiagram-v2
  direction LR
  state "grazing" as s0
  state "wandering" as s1
  state "angry" as s2
  state "hopping" as s3
  state "tamed" as s4
  state "saddled" as s5
  [*] --> s0
  s0 --> s1 : grazed / random
  s1 --> s0 : finds rust_lichen
  s0 --> s3 : random hop (low gravity)
  s1 --> s3 : random hop
  s3 --> s1 : lands
  s0 --> s2 : hurt
  s1 --> s2 : hurt
  s2 --> s1 : anger timer ends
  s1 --> s4 : fed rust_lichen (tame roll)
  s4 --> s5 : ferrox saddle + chest
```

### Crystal Stag

```mermaid
stateDiagram-v2
  direction LR
  state "antlered" as s0
  state "sheared (regrowing 6000t)" as s1
  state "fleeing" as s2
  [*] --> s0
  s0 --> s1 : sheared - drop starlite
  s1 --> s0 : 6000t regrow
  s0 --> s2 : hurt
  s1 --> s2 : hurt
  s2 --> s0 : panic ends, antlers intact
  s2 --> s1 : panic ends, sheared
```

### Prismling

```mermaid
stateDiagram-v2
  direction LR
  state "idle" as s0
  state "swarming" as s1
  state "shattering" as s2
  [*] --> s0
  s0 --> s1 : player seen / ally hurt
  s1 --> s0 : target lost
  s1 --> s2 : health 0 - burst 2-3 shards
  s2 --> [*]
```

### Cinder Hound

```mermaid
stateDiagram-v2
  direction LR
  state "roaming" as s0
  state "circling" as s1
  state "lunging" as s2
  state "attacking" as s3
  [*] --> s0
  s0 --> s1 : target found
  s1 --> s2 : 3+ pack members circling
  s2 --> s3 : lands next to target
  s3 --> s1 : target retreats
  s3 --> s0 : target lost
```

### Frost Warden

```mermaid
stateDiagram-v2
  direction LR
  state "guarding" as s0
  state "phase1" as s1
  state "phase2 (<50% hp)" as s2
  state "dead" as s3
  [*] --> s0
  s0 --> s1 : player enters wreck (16 blocks)
  s1 --> s2 : health < 50% - summon 2 rime_stalker + ice ring
  s2 --> s3 : health 0
  s1 --> s0 : no players 600t (heal)
  s3 --> [*]
```

### Flare Sprite

```mermaid
stateDiagram-v2
  direction LR
  state "orbiting" as s0
  state "flaring (vent eruption)" as s1
  state "attacking" as s2
  state "extinguished" as s3
  [*] --> s0
  s0 --> s1 : nearby flare_vent erupts
  s1 --> s0 : 100t
  s0 --> s2 : target in 10 blocks
  s1 --> s2 : target in 10 blocks
  s2 --> s0 : target lost
  s0 --> s3 : water or rain
  s2 --> s3 : water or rain
  s3 --> [*] : instant death
```

### Sun Colossus

```mermaid
stateDiagram-v2
  direction LR
  state "dormant" as s0
  state "awake" as s1
  state "slamming" as s2
  state "core_open" as s3
  state "dead" as s4
  [*] --> s0
  s0 --> s1 : player on plateau
  s1 --> s2 : target in 6 blocks
  s2 --> s3 : slam done
  s3 --> s1 : 60t window closes
  s1 --> s4 : health 0
  s3 --> s4 : health 0
  s4 --> [*]
```

### Dune Burrower

```mermaid
stateDiagram-v2
  direction LR
  state "burrowed_travel" as s0
  state "bursting" as s1
  state "swallowing" as s2
  state "surface_fight" as s3
  state "reburrow" as s4
  [*] --> s0
  s0 --> s1 : target still 40t above it
  s1 --> s2 : catches target
  s1 --> s3 : misses
  s2 --> s3 : 40t, spit out
  s3 --> s4 : 200t or target lost
  s4 --> s0 : under sand
```

### Ash Strider

```mermaid
stateDiagram-v2
  direction LR
  state "wading" as s0
  state "walking" as s1
  state "saddled" as s2
  state "ridden" as s3
  state "angry" as s4
  [*] --> s0
  s0 --> s1 : leaves lava
  s1 --> s0 : enters lava
  s0 --> s2 : saddle
  s1 --> s2 : saddle
  s2 --> s3 : player mounts
  s3 --> s2 : dismount
  s0 --> s4 : hurt
  s1 --> s4 : hurt
  s4 --> s1 : anger timer ends
```

### Rime Stalker

```mermaid
stateDiagram-v2
  direction LR
  state "stalking" as s0
  state "hidden_in_blizzard" as s1
  state "attacking" as s2
  [*] --> s0
  s0 --> s1 : snowfall and player > 8 blocks
  s1 --> s0 : player within 8 / weather clears
  s0 --> s2 : behind target, in range
  s1 --> s2 : behind target, in range
  s2 --> s0 : target turns to face it
```

### Bog Lurker

```mermaid
stateDiagram-v2
  direction LR
  state "submerged" as s0
  state "surfacing" as s1
  state "spitting" as s2
  state "crawling" as s3
  [*] --> s0
  s0 --> s1 : target near acid edge
  s1 --> s2 : target in 10 blocks
  s2 --> s3 : target on land, close
  s3 --> s0 : back in acid
  s2 --> s0 : target lost
```

### Crater Drifter

```mermaid
stateDiagram-v2
  direction LR
  state "drifting" as s0
  state "swarming" as s1
  [*] --> s0
  s0 --> s1 : this or nearby drifter hurt
  s1 --> s0 : anger timer ends
```

### Prism Sentinel

```mermaid
stateDiagram-v2
  direction LR
  state "dialogue ('Are you Concord?')" as s0
  state "phase1 beams" as s1
  state "phase2 shards loose" as s2
  state "phase3 core open (x2 damage to heart)" as s3
  state "defeated (names you heir)" as s4
  [*] --> s0
  s0 --> s1 : player answers / attacks
  s1 --> s2 : health < 66%
  s2 --> s3 : health < 33%
  s3 --> s4 : health 0
  s4 --> [*] : heir granted
```

### Rift Tyrant

```mermaid
stateDiagram-v2
  direction LR
  state "phase1 charge/claw" as s0
  state "phase2 rift pull (arena crumbles)" as s1
  state "phase3 void shards" as s2
  state "defeated" as s3
  [*] --> s0
  s0 --> s1 : health < 66%
  s1 --> s2 : health < 33%
  s2 --> s3 : health 0
  s3 --> [*]
```

### Eidolon Captain

```mermaid
stateDiagram-v2
  direction LR
  state "waiting" as s0
  state "parley (holding enough remnant_shard)" as s1
  state "phase1 duel" as s2
  state "phase2 crew" as s3
  state "phase3 lantern" as s4
  state "yielded" as s5
  state "defeated" as s6
  [*] --> s0
  s0 --> s1 : player right-clicks holding 16 remnant_shard
  s0 --> s2 : player attacks / enters deck without shards
  s1 --> s5 : reads final log
  s2 --> s3 : health < 66%
  s3 --> s4 : health < 33%
  s4 --> s6 : health 0
  s5 --> [*] : key + captains_lantern
  s6 --> [*] : key
```

### The Dying Star

```mermaid
stateDiagram-v2
  direction LR
  state "phase1 Vael on surface" as s0
  state "phase2 corona rays" as s1
  state "phase3 collapse" as s2
  state "defeated (ending choice)" as s3
  [*] --> s0
  s0 --> s1 : health < 66%
  s1 --> s2 : health < 33%
  s2 --> s3 : health 0
  s3 --> [*] : Heart of Solvane - choose ending
```

### Moon Hopper

```mermaid
stateDiagram-v2
  direction LR
  state "hopping" as s0
  state "grazing" as s1
  state "fleeing" as s2
  [*] --> s0
  s0 --> s1 : finds lunar_lichen
  s1 --> s0 : random
  s0 --> s2 : hurt / player close
  s1 --> s2 : hurt
  s2 --> s0 : safe
```

### Dust Grazer

```mermaid
stateDiagram-v2
  direction LR
  state "grazing" as s0
  state "wandering" as s1
  state "stampeding" as s2
  [*] --> s0
  s0 --> s1 : random
  s1 --> s0 : finds grass-like block
  s0 --> s2 : any herd member within 12 hurt
  s1 --> s2 : herd member hurt
  s2 --> s1 : panic ends (100t)
```

### Azure Fowl

```mermaid
stateDiagram-v2
  direction LR
  state "walking" as s0
  state "gliding" as s1
  state "laying" as s2
  [*] --> s0
  s0 --> s1 : falling (not on ground)
  s1 --> s0 : lands
  s0 --> s2 : egg timer 6000-12000t
  s2 --> s0 : blue_egg dropped
```

### Glimmerfish

```mermaid
stateDiagram-v2
  direction LR
  state "schooling" as s0
  state "fleeing" as s1
  state "flopping (out of water)" as s2
  [*] --> s0
  s0 --> s1 : hurt / player close
  s1 --> s0 : safe
  s0 --> s2 : out of water
  s1 --> s2 : out of water
  s2 --> s0 : back in water
```

### Slag Boar

```mermaid
stateDiagram-v2
  direction LR
  state "rooting" as s0
  state "wandering" as s1
  state "charging" as s2
  [*] --> s0
  s0 --> s1 : random
  s1 --> s0 : finds slag
  s0 --> s2 : hurt / player near baby
  s1 --> s2 : hurt / player near baby
  s2 --> s1 : anger timer ends
```

### Scorch Wyrmling

```mermaid
stateDiagram-v2
  direction LR
  state "perched" as s0
  state "gliding" as s1
  state "spitting" as s2
  state "biting" as s3
  [*] --> s0
  s0 --> s1 : jumps off ledge
  s1 --> s0 : lands
  s0 --> s2 : target in 12 blocks
  s1 --> s2 : target in 12 blocks
  s2 --> s3 : target in melee range
  s3 --> s2 : target backs off
  s2 --> s0 : target lost
```

### Frost Yak

```mermaid
stateDiagram-v2
  direction LR
  state "woolly" as s0
  state "sheared (regrow by grazing)" as s1
  state "sheltering" as s2
  [*] --> s0
  s0 --> s1 : sheared - yak_wool
  s1 --> s0 : eats snowpack / frozen_regolith
  s0 --> s2 : snowfall + calf nearby
  s1 --> s2 : snowfall + calf nearby
  s2 --> s0 : weather clears
```

### Ice Leech

```mermaid
stateDiagram-v2
  direction LR
  state "hidden" as s0
  state "crawling" as s1
  state "latched" as s2
  [*] --> s0
  s0 --> s1 : player steps within 2 blocks
  s1 --> s2 : touches target - ride
  s2 --> s1 : player sprints 20t / leech hit
  s1 --> s0 : no target 200t
```

### Gildcrab

```mermaid
stateDiagram-v2
  direction LR
  state "basking" as s0
  state "scuttling" as s1
  state "pinching" as s2
  [*] --> s0
  s0 --> s1 : random / disturbed
  s1 --> s0 : on sunspot_rock
  s0 --> s2 : hurt
  s1 --> s2 : hurt
  s2 --> s1 : anger timer ends
```

### Deep Eel

```mermaid
stateDiagram-v2
  direction LR
  state "lurking" as s0
  state "following_light" as s1
  state "biting" as s2
  [*] --> s0
  s0 --> s1 : light source > 10 or player with light
  s1 --> s2 : target in water, in range
  s2 --> s0 : target leaves water
  s1 --> s0 : light gone
```

### Sand Skitter

```mermaid
stateDiagram-v2
  direction LR
  state "buried" as s0
  state "bursting" as s1
  state "attacking" as s2
  [*] --> s0
  s0 --> s1 : player within 4 or group member bursts
  s1 --> s2 : out of sand
  s2 --> s0 : target lost 200t (re-bury)
```
