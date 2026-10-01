"""Inventory mapped 1.21.1 animation code without redistributing Mojang sources."""
import hashlib, json, re, zipfile
from pathlib import Path
from build_mob_models import ROOT, write_json

CLIENT=Path('/mnt/c/Users/jakem/.gradle/caches/neoformruntime/artifacts/minecraft_1.21.1_client.jar')
SOURCES=ROOT.parent/'ZeroG_Tweaks/build/moddev/artifacts/neoforge-21.1.252-sources.jar'
OUT=ROOT/'docs/zero-g-tweaks-bundle/blockbench/references'
GROUPS={
 'Passive':'allay armadillo axolotl bat camel cat chicken cod cow donkey fox frog glow_squid horse mooshroom mule ocelot parrot pig pufferfish rabbit salmon sheep skeleton_horse sniffer snow_golem squid strider tadpole tropical_fish turtle villager wandering_trader zombie_horse',
 'Neutral':'bee cave_spider dolphin enderman goat iron_golem llama panda piglin polar_bear spider trader_llama wolf zombified_piglin',
 'Hostile':'blaze bogged breeze creeper drowned elder_guardian endermite evoker ghast giant guardian hoglin husk illusioner magma_cube phantom piglin_brute pillager ravager shulker silverfish skeleton slime stray vex vindicator warden witch wither_skeleton zoglin zombie zombie_villager',
 'Boss':'ender_dragon wither'}
SHARED={
 'donkey':'ChestedHorseModel','horse':'HorseModel','mule':'ChestedHorseModel',
 'skeleton_horse':'HorseModel','zombie_horse':'HorseModel','mooshroom':'CowModel',
 'glow_squid':'SquidModel','ocelot':'OcelotModel','snow_golem':'SnowGolemModel',
 'wandering_trader':'VillagerModel','trader_llama':'LlamaModel','cave_spider':'SpiderModel',
 'zombified_piglin':'PiglinModel','piglin_brute':'PiglinModel','elder_guardian':'GuardianModel',
 'evoker':'IllagerModel','illusioner':'IllagerModel','pillager':'IllagerModel',
 'vindicator':'IllagerModel','giant':'GiantZombieModel','husk':'ZombieModel',
 'stray':'SkeletonModel','wither_skeleton':'SkeletonModel','zoglin':'HoglinModel',
 'ender_dragon':'EnderDragonRenderer','tropical_fish':'TropicalFishModelA',
 'pufferfish':'PufferfishBigModel','magma_cube':'LavaSlimeModel','wither':'WitherBossModel'}

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(CLIENT) as jar:
        version=json.loads(jar.read('version.json'))
    assert version['id']=='1.21.1'
    with zipfile.ZipFile(SOURCES) as jar:
        paths=[p for p in jar.namelist() if p.endswith('.java') and
               (p.startswith('net/minecraft/client/model/') or p.startswith('net/minecraft/client/animation/definitions/') or p.endswith('/EnderDragonRenderer.java'))]
        code={Path(p).stem:(p,jar.read(p).decode()) for p in paths}
    records=[]
    for category,ids in GROUPS.items():
        for mob in ids.split():
            name=SHARED.get(mob,''.join(s.title() for s in mob.split('_'))+'Model')
            assert name in code,(mob,name)
            path,source=code[name]
            records.append({'id':'minecraft:'+mob,'category':category,'source':path,
                'sha256':hashlib.sha256(source.encode()).hexdigest(),
                'animation_methods':sorted(set(re.findall(r'\b(setupAnim|prepareMobModel|animateWalk|animate|applyStatic)\s*\(',source))),
                'animation_definitions':sorted(set(re.findall(r'([A-Z][A-Za-z]+Animation)\.',source))),
                'inherits':re.findall(r'extends\s+([A-Za-z]+)',source)[:1]})
    definitions=[{'source':p,'sha256':hashlib.sha256(s.encode()).hexdigest()}
                 for p,s in code.values() if '/animation/definitions/' in p]
    write_json(OUT/'vanilla_animation_inventory.json',{'minecraft':'1.21.1',
        'client_version':version,'source_archive':str(SOURCES),
        'source_archive_sha256':hashlib.sha256(SOURCES.read_bytes()).hexdigest(),
        'mobs':records,'definition_files':definitions,
        'scope':'Static code inventory; no vanilla mob models or source code redistributed; no client test.'})
    lines=['# Minecraft 1.21.1 animation references','',
        f'Checked the local client version metadata (`1.21.1`) and mapped NeoForge Minecraft sources for all {len(records)} mob IDs supplied by the user. These are references, not additional ZeroG entity registrations.', '',
        '## Applied to the original ZeroG rigs','',
        '- QuadrupedModel: diagonal leg pairs move together; opposite pairs counter-swing. Child shins/feet inherit the phase of their own upper leg.',
        '- RabbitModel: left/right hind limbs push together while forelegs tuck; Moon Hopper now has limb motion in its hop clip instead of root bob alone.',
        '- ChickenModel: opposite leg phases, mirrored wing movement and head-linked facial parts. Azure Fowl retains its original anatomy.',
        '- SpiderModel: mirrored lateral leg movement and staggered phases. The Shardmother lower-leg phase now matches its corresponding numbered upper leg.',
        '- PhantomModel: mirrored wing chains; its tail flex runs at twice wing frequency. Tidewraith fly/glide drafts now use this relationship.',
        '- SilverfishModel: low articulated segments with phase-offset lateral sway; Dune Burrower is now an original low sand-coloured arthropod with segment movement, replacing the upright worm concept.',
        '- BatModel / BatAnimation: distinct resting and flight states and articulated wings; reference only, not copied as universal animation for every flyer.',
        '- Armadillo, Camel, Sniffer, Frog, Warden and Breeze use authored state/animation definitions. Bogged uses its skeleton-family locomotion. These demonstrate why separate runtime state controllers are required.', '',
        'The current assets contain editable, original animation drafts. Locomotion speed, head tracking, randomized blinking, attack transitions, aura/emissive layers and particle/sound events still need Java/GeckoLib controllers and client testing. The vanilla code does not make these custom clips run automatically.', '',
        '## Inventory','', '| Mob ID | Model / renderer source | Animation entry points |', '| --- | --- | --- |']
    lines.extend(f'| `{r["id"]}` | `{Path(r["source"]).name}` | {", ".join(r["animation_methods"]) or "Inherited / renderer-driven"} |' for r in records)
    lines += ['', '## Guides inspected','',
        '- [Minecraft style guide](https://blockbench.net/wiki/guides/minecraft-style-guide/): deliberate pixel clusters, restrained palettes, planes and consistent UV density.',
        '- [Overview and tips](https://blockbench.net/wiki/guides/blockbench-overview-tips/): proximal-to-distal parenting and pivots at anatomical joints.',
        '- [Animation expressions](https://blockbench.net/wiki/guides/animation-expressions/): expression exports and GeckoLib support; implementation still requires matching controllers.',
        '- [Emissive renders](https://blockbench.net/wiki/guides/emissive-textures-renders/): Blender/Sketchfab rendering workflow, not automatic Minecraft lighting.',
        '- [Particles and sounds](https://blockbench.net/wiki/guides/minecraft-particles-sounds/): Bedrock-specific effects; Java needs its own registration and event handling.', '',
        'The two purple-eyed face images were inspected directly. Optical decals use a deliberate rectangular three-cell design, darker centres and lighter ends, adapted to each creature. Natural and emissive eyes keep different colour treatments. The project remains custom HD art rather than strict vanilla texel density.']
    (OUT/'vanilla_animation_reference.md').write_text('\n'.join(lines)+'\n')
    print('Inventoried',len(records),'Minecraft 1.21.1 mobs and',len(definitions),'animation definition files')

if __name__=='__main__':main()
