"""Overview: all six planet villagers at the same scale, with a vanilla-proportion villager and a door."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vkit import *
from species import ALL
import sheet as SH


def vanilla():
    g = lambda p, P: p.fill('all', P['g'], noise=2, edge=.12)
    bones = [Bone('body', pivot=(0, 12, 0)), Bone('arms', 'body', (0, 21, -1), (-43, 0, 0)), Bone('head', pivot=(0, 24, 0)),
             Bone('nose', 'head', (0, 26, 0)), Bone('right_leg', pivot=(2, 12, 0)), Bone('left_leg', pivot=(-2, 12, 0))]
    cubes = [Cube('right_leg', 'lr', (0, 0, -2), (4, 12, 4), g), Cube('left_leg', 'll', (-4, 0, -2), (4, 12, 4), g),
             Cube('body', 'b', (-4, 12, -3), (8, 12, 6), g), Cube('body', 'robe', (-4, 4, -3), (8, 20, 6), g, inflate=.5),
             Cube('arms', 'ar', (4, 15, -3), (4, 8, 4), g), Cube('arms', 'al', (-8, 15, -3), (4, 8, 4), g), Cube('arms', 'af', (-4, 15, -3), (8, 4, 4), g),
             Cube('head', 'h', (-4, 24, -4), (8, 10, 8), g), Cube('nose', 'n', (-1, 23, -6), (2, 4, 2), g)]
    return Species(id='vanilla', name='Vanilla villager', planet='Overworld', gravity=1.0, bones=bones, cubes=cubes, palette={'g': '#b9b6c4'})


def main(out, built):
    W, H = 2240, 2140
    sh = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(sh)
    d.text((28, 20), 'Planet villagers  —  overview', font=FB(32), fill=INK)
    d.text((28, 64), 'Six species, one per fixed planet. All share the vanilla villager rig (bone names, crossed arms, 0.6 x 1.95 hitbox, 0.9375 render scale) '
                     'so vanilla AI, trades and doors work; gravity shapes the build.', font=FR(14), fill=SUB)
    # lineup
    box = (28, 100, W - 28, 800); panel(d, box, 'LINEUP  (front view, same scale, flat colours)', 'grid = 1 model px; dashed = hitbox; door = 1 x 2 blocks')
    S = 13; gy = box[3] - 110
    sp_list = [vanilla()] + built
    xs = []; x = box[0] + 300
    for sp in sp_list:
        tex = sp.texture(); im, proj = render(sp, tex, Cam(0, 0, S), flat=True)
        g0 = proj((0, 0, 0)); ox = x + 120 - g0[0]; oy = gy - g0[1]
        sh.alpha_composite(im, (int(ox), int(oy))); xs.append((x + 120, sp))
        top = gy - sp.height() * S
        d.text((x + 120 - d.textlength(sp.name, font=FB(15)) / 2, gy + 16), sp.name, font=FB(15), fill=INK)
        sub = f'{sp.planet} · {sp.gravity:g} g'
        d.text((x + 120 - d.textlength(sub, font=FR(12)) / 2, gy + 38), sub, font=FR(12), fill=SUB)
        t = f'{sp.height():g} px'
        d.text((x + 120 - d.textlength(t, font=FR(12)) / 2, top - 26), t, font=FR(12), fill=SUB)
        x += 255
    # door + ground + hitbox reference
    dw, dh = 16 / RENDER_SCALE * S, 32 / RENDER_SCALE * S
    dx = box[0] + 70
    d.rectangle([dx, gy - dh, dx + dw, gy], outline=INK, width=2); d.line([(dx + dw / 2, gy - dh), (dx + dw / 2, gy)], fill=LINE)
    d.text((dx - 6, gy + 16), 'oak door', font=FB(13), fill=INK); d.text((dx - 6, gy + 36), '1 x 2 blocks', font=FR(12), fill=SUB)
    hy = gy - HITBOX[1] * 16 / RENDER_SCALE * S
    for a in range(box[0] + 20, box[2] - 20, 10): d.line([(a, hy), (a + 5, hy)], fill=ACC)
    d.text((box[0] + 20, hy - 34), 'hitbox top (1.95 blocks)', font=FR(11), fill=ACC)
    d.line([(box[0] + 20, gy), (box[2] - 20, gy)], fill=SUB)
    # 3D row
    y2 = 820; box2 = (28, y2, W - 28, y2 + 520); panel(d, box2, '3D', 'front-right view, lit')
    cw = (box2[2] - box2[0] - 32) // len(built)
    for i, sp in enumerate(built):
        im, _ = render(sp, sp.texture(), Cam(-35, 20, 10)); cx = box2[0] + 16 + i * cw
        d.rounded_rectangle([cx, box2[1] + 46, cx + cw - 12, box2[3] - 16], 10, fill=(235, 233, 243))
        sh.alpha_composite(im, (cx + (cw - 12 - im.width) // 2, box2[1] + 64))
        d.text((cx + 12, box2[3] - 62), sp.name, font=FB(15), fill=INK)
        d.text((cx + 12, box2[3] - 40), sp.tag, font=FR(12), fill=SUB)
    # summary table
    y3 = y2 + 540
    d.text((28, y3), 'At a glance', font=FB(18), fill=INK)
    rows = []
    for sp in built:
        legs = max(c.origin[1] + c.size[1] for c in sp.cubes if c.bone == 'right_leg')
        rows.append((sp.name, f'zerog_tweaks:{sp.id}', f'{sp.planet} ({sp.gravity:g} g)', f'{sp.height():g} px', f'{legs:g} px', f'{sp.W} x {sp.H}',
                     sp.signature[0], sp.job, len(sp.cubes)))
    yy = SH.table(d, 28, y3 + 34, [('Species', 140), ('Entity id', 230), ('Planet', 160), ('Height', 80), ('Legs', 70), ('Texture', 90),
                                   ('Signature profession', 190), ('Job site block', 210), ('Cubes', 60)], rows, font=FR(13), rh=26)
    # profession colours
    px0 = 1520
    d.text((px0, y3), 'Profession colours (overlay recolours the accent)', font=FB(18), fill=INK)
    for i, (nm, col) in enumerate(SH.PROF + [(sp.signature[0] + ' (per species)', '#ffffff')]):
        if i == len(SH.PROF): break
        cx = px0 + (i % 2) * 340; cy = y3 + 38 + (i // 2) * 28
        d.rectangle([cx, cy, cx + 20, cy + 20], fill=hexc(col), outline=LINE); d.text((cx + 30, cy + 2), f'{nm}  {col}', font=FR(13), fill=INK)
    yb = max(yy, y3 + 38 + 7 * 28) + 24
    d.text((28, yb), 'How it plugs in', font=FB(18), fill=INK)
    notes = ['Each species is its own EntityType<PlanetVillager> where PlanetVillager extends Villager, so brains, gossip, POIs, trading, beds, '
             'iron golems and raids all work. Override getBreedOffspring() to return the same species, and convert to the vanilla zombie villager (keep '
             'profession data) or add species zombies later.',
             'Rendering: a GeoEntityRenderer with the species .geo.json, main texture by VillagerType (biome variant), an emissive layer from the glowmask and '
             'a profession layer drawing professions/<profession>.png on the same model. Head bone follows the look target in setCustomAnimations.',
             'Professions: the 13 vanilla professions use their vanilla job blocks. Each species adds one signature profession whose PoiType is a ZeroG '
             'machine block (ore_refinery, combustion_generator, crystal_growth_chamber, alloy_forge, salvage_station, solar_array).',
             'Spawning: planet village structures place the matching species; existing clothing overlays (planet-worldgen-overhaul/source/villagers) stay '
             'for vanilla villagers that travel through a gate. No ids are removed.']
    for nt in notes:
        d.text((28, yb + 32), '•', font=FR(13), fill=INK); yb = text_block(d, 44, yb + 32, nt, FR(13), W - 90, gap=4) - 28
    sh.crop((0, 0, W, yb + 70)).convert('RGB').save(f'{out}/sheets/00_overview.png')


if __name__ == '__main__':
    import build_villagers as B
    built = B.main(sys.argv[1])
    main(sys.argv[1], built)
