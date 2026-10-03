"""Six planet villager species for ZeroG Tweaks. Geometry is in Blockbench space (+X = model's right)."""
from vkit import Bone, Cube, Species, shade, mix

ARM_ROT = (-43, 0, 0)          # vanilla villager crossed arms (-0.75 rad)


# ---------------------------------------------------------------- shared paint helpers
def skin_hands(p, P, skin, sleeve, cuff=None, hand_rows=2):
    p.fill('all', P[sleeve], edge=.12)
    for f in ('north', 'south', 'east', 'west'):
        h = p.size(f)[1]
        p.rect(f, 0, h - hand_rows, 9, h - 1, P[skin], noise=3)
        if cuff: p.row(f, h - hand_rows - 1, P[cuff])
    p.fill('bottom', P[skin])


def eyes(p, r, cols, white, iris, glow=False, brow=None, glint=None):
    for c0 in cols:
        p.px('north', c0, r, white, glow=glow); p.px('north', c0 + 1, r, iris, glow=glow)
        if glint: p.px('north', c0, r, glint, glow=True)
        if brow: p.px('north', c0, r - 1, brow); p.px('north', c0 + 1, r - 1, brow)


# ==================================================================== 1. LUNARI (Moon)
def lunari():
    def boot(p, P):
        p.fill('all', P['boot'], edge=.15)
        for f in ('north', 'south', 'east', 'west'):
            p.row(f, 3, P['sole']); p.row(f, 0, shade(P['boot'], 1.25))
            p.row(f, 1, P['stripe'], mask='accent')
        p.fill('bottom', P['sole'])
        for _ in range(6): p.px(p.faces('all')[p.rng.randrange(6)], p.rng.randrange(4), p.rng.randrange(3), P['dust'])

    def leg(p, P):
        p.fill('all', P['suit'], edge=.10)
        for f in ('north', 'south', 'east', 'west'): p.row(f, 4, P['suit_d']); p.row(f, 5, P['suit_s'])   # knee pad

    def torso(p, P):
        p.fill('all', P['suit'], edge=.10)
        p.col('north', 2, P['suit_s']); p.col('north', 3, P['suit_s'])                          # zipper seam
        p.row(('north', 'south', 'east', 'west'), 2, P['stripe'], mask='accent')
        p.rect('north', 4, 4, 5, 5, P['screen'], glow=True); p.px('north', 4, 4, P['screen_hi'], glow=True)
        p.row(('north', 'south', 'east', 'west'), 9, P['suit_d'])                               # belt line
        p.px('north', 1, 9, P['metal_hi']); p.px('north', 4, 9, P['metal_hi'])

    def belt(p, P):
        p.fill('all', P['metal']); p.fill(('top', 'bottom'), (0, 0, 0, 0))
        p.px('north', 1, 0, P['metal_hi']); p.px('north', 4, 0, P['metal_hi'])
        p.px('east', 1, 0, P['stripe']); p.px('west', 1, 0, P['stripe'])

    def collar(p, P):
        p.fill('all', P['metal'], edge=.18)
        p.row(('north', 'south', 'east', 'west'), 0, P['metal_hi'])
        for f, cs in (('north', (1, 8)), ('south', (1, 8)), ('east', (1, 6)), ('west', (1, 6))):
            for c in cs: p.px(f, c, 1, P['bolt'])
        p.fill('top', P['metal_hi'], grad=0)
        p.rect('top', 1, 1, 8, 6, P['metal_d'])                                                    # inner rim (head sits here)
        p.fill('bottom', P['metal_d'])

    def tank(p, P):
        p.fill('all', P['suit_s'], edge=.18)
        p.row(('south', 'east', 'west', 'north'), 1, P['stripe'], mask='accent')
        p.rect('south', 1, 3, 3, 5, P['metal_d']); p.px('south', 2, 4, P['screen'], glow=True)      # gauge
        p.fill('top', P['metal']); p.rect('top', 2, 1, 2, 1, P['bolt'])

    def arm(p, P):
        p.fill('all', P['suit'], edge=.12)
        for f in ('north', 'south', 'east', 'west'):
            p.row(f, 1, P['stripe'], mask='accent')
            h = p.size(f)[1]; p.rect(f, 0, h - 3, 9, h - 1, P['glove']); p.row(f, h - 4, P['glove_cuff'])
        p.fill('bottom', P['glove'])

    def forearms(p, P):
        p.fill('all', P['suit'], edge=.12)
        for f in ('north', 'south', 'top', 'bottom'):
            w = p.size(f)[0]; p.col(f, 0, P['glove']); p.col(f, w - 1, P['glove'])
        p.fill(('east', 'west'), P['glove'])

    def head(p, P):
        p.fill('all', P['skin'], noise=3, grad=.08)
        eyes(p, 3, (1, 5), P['eye'], P['eye'], glint=P['eye_glint'])
        for c0 in (1, 5): p.px('north', c0, 4, P['eye']); p.px('north', c0 + 1, 4, P['eye'])        # tall 2x2 night eyes
        p.px('north', 3, 6, P['skin_d']); p.px('north', 4, 6, P['skin_d'])                         # small mouth
        p.px('north', 0, 5, P['skin_blush']); p.px('north', 7, 5, P['skin_blush'])

    def hood(p, P):
        p.fill('all', P['suit'], edge=.10)
        p.clear('north', 1, 1, 6, 7)                                                                # face opening
        for c in range(1, 7): p.px('north', c, 0, P['stripe'], mask='accent')                      # piping over the brow
        p.col('south', 3, P['suit_s']); p.col('south', 4, P['suit_s'])                              # back seam
        p.rect('top', 2, 2, 5, 5, P['suit_s'])
        p.fill('bottom', (0, 0, 0, 0))

    def nose(p, P):
        p.fill('all', P['skin_d'], noise=2)

    def socket(p, P):
        p.fill('all', P['metal'], edge=.2); p.fill('top', P['metal_d'])

    def crystal(p, P):
        p.fill('all', P['selenite'], noise=4, grad=.2)
        for f in ('north', 'south', 'east', 'west'): p.px(f, 0, 0, P['selenite_hi']); p.px(f, 1, 1, P['selenite_core'])
        p.fill('top', P['selenite_hi']); p.glow_all()

    bones = [Bone('body', pivot=(0, 14, 0)), Bone('arms', 'body', (0, 22, -1), ARM_ROT),
             Bone('head', pivot=(0, 25, 0)), Bone('hood', 'head', (0, 25, 0)), Bone('nose', 'head', (0, 28, 0)),
             Bone('crest', 'head', (0, 34, 0)), Bone('right_leg', pivot=(2, 14, 0)), Bone('left_leg', pivot=(-2, 14, 0))]
    cubes = [
        Cube('right_leg', 'leg_r', (0.5, 4, -1.5), (3, 10, 3), leg), Cube('right_leg', 'boot_r', (0, 0, -3), (4, 4, 5), boot, label='Moon boots'),
        Cube('left_leg', 'leg_l', (-3.5, 4, -1.5), (3, 10, 3), leg), Cube('left_leg', 'boot_l', (-4, 0, -3), (4, 4, 5), boot),
        Cube('body', 'torso', (-3, 14, -2), (6, 11, 4), torso, label='Suit (orange stripe = profession colour)'),
        Cube('body', 'belt', (-3, 16, -2), (6, 1, 4), belt, inflate=0.3),
        Cube('body', 'collar', (-5, 24, -4), (10, 2, 8), collar, label='Pressure-suit collar ring'),
        Cube('body', 'tank', (-2.5, 15, 2), (5, 8, 3), tank, label='Air tank'),
        Cube('arms', 'arm_r', (3, 15, -3), (2, 8, 3), arm), Cube('arms', 'arm_l', (-5, 15, -3), (2, 8, 3), arm, label='Crossed arms, gloves'),
        Cube('arms', 'forearms', (-3, 15, -3), (6, 3, 3), forearms),
        Cube('head', 'head', (-4, 25, -4), (8, 8, 8), head, label='Large night eyes'),
        Cube('hood', 'hood', (-4, 25, -4), (8, 8, 8), hood, inflate=0.5, label='Suit hood (open face)'),
        Cube('nose', 'nose', (-1, 27, -5), (2, 2, 1), nose),
        Cube('crest', 'socket', (-1.5, 33.5, -1.5), (3, 1, 3), socket),
        Cube('crest', 'crystal', (-1, 34.5, -1), (2, 2, 2), crystal, label='Selenite crest (glows)'),
    ]
    return Species(
        id='lunari', name='Lunari', planet='Moon', gravity=0.5, bones=bones, cubes=cubes, job='ore_refinery',
        tag='Dustwalkers of the Moon',
        palette=dict(suit='#d9dce3', suit_s='#b4b9c6', suit_d='#8e95a6', stripe='#e0873a', metal='#7d8494', metal_hi='#aeb4c2',
                     metal_d='#4c5160', bolt='#e0873a', boot='#4a4e5c', sole='#2c2f38', dust='#a7a7ab', glove='#5a5f6e',
                     glove_cuff='#3c404b', skin='#c9c6d9', skin_d='#a8a3bd', skin_blush='#d8c3d6', eye='#1c1d33',
                     eye_glint='#9ff3ff', screen='#58e1ff', screen_hi='#d9fbff', selenite='#bfefff', selenite_hi='#ecfdff',
                     selenite_core='#ffffff'),
        variants=[('lunar_highlands', 'Highlands (default)', {}),
                  ('lunar_mare', 'Mare', dict(suit='#5d6270', suit_s='#4a4e5a', suit_d='#383b45', stripe='#58d0e8', bolt='#58d0e8')),
                  ('shadowed_craters', 'Shadowed Craters', dict(suit='#3b3a5c', suit_s='#2f2e4a', suit_d='#24233a', stripe='#a487ff', bolt='#a487ff', screen='#a487ff'))],
        lore=('The Lunari are the oldest of the Concord\'s stay-behinds: a crew left to watch the Moon relay when the migration ships '
              'went on. Generations of half gravity made them tall and light on their feet, with long legs and wide, dark eyes '
              'for the two-week lunar night. They still wear the old pressure suits even though their domes hold air, and every '
              'Lunari grows a sliver of selenite on their hood as a sign of coming of age.'),
        behaviour=('Low-gravity walkers: they take longer, floatier steps (walk animation at 0.8x speed, legs swing wider). '
                   'At night their crest glows, so a village reads as a field of pale lights from the crater rim. '
                   'Shy: they stare at a player in a gate-tier armour set for a few seconds before trading.'),
        signature=('Regolith Refiner', 'ore_refinery', [
            ('Novice', '16 Regolith -> 1 Emerald', '1 Emerald -> 4 Lunar Lichen'),
            ('Apprentice', '10 Crater Ice -> 1 Emerald', '2 Emeralds -> 2 Selenite Lamps'),
            ('Journeyman', '6 Meteorite Fragments -> 1 Emerald', '4 Emeralds -> 3 Moonsteel Nuggets'),
            ('Expert', '2 Raw Moonsteel -> 1 Emerald', '6 Emeralds -> 1 Raw Moonsteel'),
            ('Master', '-', '18 Emeralds -> 1 Crater trim template (copy)')]),
        anims=[('idle', 'breathing; crest bobs 0.4 px every 3 s'), ('walk', 'legs +/-40 deg, played at 0.8x (floaty)'),
               ('no', 'head shake when a trade is refused (vanilla: z +/-17 deg, 0.7 s)'), ('crest_glow', 'emissive crest pulses at night (code)')],
        notes=['Arms bone keeps vanilla\'s crossed pose (-43 deg X) and pivot height so held items line up.',
               'Hood is an inflated copy of the head (+0.5) with the face cut out; the head shows through.',
               'Hitbox stays 0.6 x 1.95 so Lunari fit 1 x 2 doors; the crest is cosmetic and clips door tops.',
               'Glowmask: crest crystal, chest screen, tank gauge, eye glints.'],
        badge='the orange suit stripes and boot straps')


# ==================================================================== 2. RUSTBORN (Mars)
def rustborn():
    def leg(p, P):
        p.fill('all', P['cloth'], edge=.12)
        p.rows_from_bottom(('north', 'south', 'east', 'west'), 3, P['boot'])
        p.fill('bottom', P['boot'])
        for f in ('north', 'east', 'west'): p.row(f, 8, mix(P['boot'], P['dust'], .35))

    def torso(p, P):
        p.fill('all', P['cloth'], edge=.1)

    def poncho(p, P):
        p.fill('all', P['poncho'], edge=.12, grad=.14)
        for f in ('north', 'south', 'east', 'west'):
            h = p.size(f)[1]
            for r in range(2, h, 4): p.row(f, r, P['poncho_s'])
            p.row(f, h - 4, P['band'], mask='band'); p.row(f, h - 3, P['band_d'])
            for c in range(p.size(f)[0]):
                if c % 2: p.px(f, c, h - 4, P['band_d'])
            for c in range(0, p.size(f)[0], 2): p.px(f, c, h - 1, (0, 0, 0, 0))                    # fringe
        p.fill(('top', 'bottom'), (0, 0, 0, 0))

    def mantle(p, P):
        p.fill('all', P['scarf'], edge=.15, grad=.2)
        for f in ('north', 'south', 'east', 'west'):
            for c in range(0, p.size(f)[0], 3): p.px(f, c, 1, P['scarf_s'], mask='accent')
            p.row(f, 0, shade(P['scarf'], 1.12), mask='accent'); p.row(f, 2, P['scarf_s'], mask='accent')
            for c in range(p.size(f)[0]):
                if (c + 1) % 3: p.px(f, c, 1, P['scarf'], mask='accent')
        p.fill('top', P['scarf'], grad=0); p.rect('top', 1, 1, 8, 6, P['scarf_s']); p.fill('bottom', P['scarf_s'])

    def drape(p, P):
        p.fill('all', P['poncho_d'], edge=.15)
        p.rect('south', 1, 0, 4, 2, P['lining']); p.row('south', 4, P['poncho_s'])

    def arm(p, P):
        skin_hands(p, P, 'skin', 'poncho', cuff='poncho_d')
        for f in ('north', 'south', 'east', 'west'): p.row(f, 2, P['poncho_s'])

    def forearms(p, P):
        p.fill('all', P['poncho'], edge=.12)
        for f in ('north', 'south', 'top', 'bottom'):
            w = p.size(f)[0]; p.col(f, 0, P['skin']); p.col(f, w - 1, P['skin'])
        p.fill(('east', 'west'), P['skin'])

    def head(p, P):
        p.fill('all', P['skin'], noise=3, grad=.08)
        p.fill('top', P['hair']); p.rect('south', 0, 0, 7, 4, P['hair'], noise=6)
        for f in ('east', 'west'): p.rect(f, 0, 0, 7, 1, P['hair'], noise=6); p.rect(f, 0 if f == 'east' else 5, 2, 2 if f == 'east' else 7, 3, P['hair'])
        p.row('north', 0, P['hair'])
        eyes(p, 3, (1, 5), P['eye_w'], P['eye'], brow=P['brow'])
        p.px('north', 3, 2, P['brow']); p.px('north', 4, 2, P['brow'])                              # the unibrow, a villager tradition
        for c, r in ((0, 4), (7, 4), (2, 5), (6, 5)): p.px('north', c, r, P['freckle'])

    def strap(p, P):
        p.fill('all', P['leather'], noise=3); p.fill(('top', 'bottom'), (0, 0, 0, 0))
        p.px('east', 4, 0, P['brass']); p.px('west', 4, 0, P['brass'])

    def lens(p, P):
        p.fill('all', P['brass'], edge=.2); p.px('north', 1, 0, P['lens'], glow=True); p.px('north', 1, 1, P['lens_d'], glow=True)
        p.px('north', 0, 0, P['brass_hi'])

    def mask(p, P):
        p.fill('all', P['metal'], edge=.2)
        p.row('north', 0, P['metal_hi']); p.row('north', 1, P['metal_d']); p.px('north', 1, 2, P['metal_d']); p.px('north', 2, 2, P['metal_d'])
        p.px('north', 0, 1, P['metal']); p.px('north', 3, 1, P['metal'])

    def filt(p, P):
        p.fill('all', P['brass'], edge=.2)
        p.rect('north', 0, 0, 1, 1, P['brass_d']); p.px('north', 0, 0, P['brass_hi'])
        p.rect('east', 0, 0, 1, 1, P['brass_d']); p.rect('west', 0, 0, 1, 1, P['brass_d'])

    bones = [Bone('body', pivot=(0, 11, 0)), Bone('arms', 'body', (0, 20, -1), ARM_ROT),
             Bone('head', pivot=(0, 23, 0)), Bone('goggles', 'head', (0, 30, 0)), Bone('respirator', 'head', (0, 25, -4)),
             Bone('right_leg', pivot=(2, 11, 0)), Bone('left_leg', pivot=(-2, 11, 0))]
    cubes = [
        Cube('right_leg', 'leg_r', (0, 0, -2), (4, 11, 4), leg), Cube('left_leg', 'leg_l', (-4, 0, -2), (4, 11, 4), leg, label='Dust boots'),
        Cube('body', 'torso', (-4, 11, -3), (8, 12, 6), torso),
        Cube('body', 'poncho', (-4, 5, -3), (8, 18, 6), poncho, inflate=0.5, label='Dust poncho, fringed hem'),
        Cube('body', 'mantle', (-5, 20, -4), (10, 3, 8), mantle, label='Scarf (profession colour)'),
        Cube('body', 'drape', (-3, 15, 3.5), (6, 5, 1), drape, label='Hood, down'),
        Cube('arms', 'arm_r', (4, 14, -3), (4, 8, 4), arm), Cube('arms', 'arm_l', (-8, 14, -3), (4, 8, 4), arm),
        Cube('arms', 'forearms', (-4, 14, -3), (8, 4, 4), forearms),
        Cube('head', 'head', (-4, 23, -4), (8, 9, 8), head, label='Unibrow, freckles'),
        Cube('goggles', 'strap', (-4, 29, -4), (8, 2, 8), strap, inflate=0.3),
        Cube('goggles', 'lens_r', (0.5, 29, -5), (3, 2, 1), lens, label='Dust goggles, pushed up'), Cube('goggles', 'lens_l', (-3.5, 29, -5), (3, 2, 1), lens),
        Cube('respirator', 'mask', (-2, 23.5, -6), (4, 3, 2), mask, label='Respirator (replaces the nose)'),
        Cube('respirator', 'filter_r', (2, 23.5, -5.5), (2, 2, 2), filt), Cube('respirator', 'filter_l', (-4, 23.5, -5.5), (2, 2, 2), filt),
    ]
    return Species(
        id='rustborn', name='Rustborn', planet='Mars', gravity=0.7, bones=bones, cubes=cubes, job='combustion_generator',
        tag='Dust-wrapped wanderers of Mars',
        palette=dict(skin='#a8735a', hair='#5a2a1e', brow='#3b1d16', freckle='#8e5a44', eye_w='#e9dccb', eye='#3a6b4a',
                     cloth='#9c8a6a', boot='#3b2a22', dust='#c98a62', poncho='#b5523a', poncho_s='#9b4230', poncho_d='#6e2e22',
                     lining='#d9b48a', band='#e3c38f', band_d='#8a3a2a', scarf='#d8a35a', scarf_s='#b07f3e',
                     leather='#3b2a22', brass='#c9a24a', brass_hi='#f0d27a', brass_d='#7a5f26', lens='#ffb347', lens_d='#d9771f',
                     metal='#7f8a94', metal_hi='#aab4bd', metal_d='#3f474f'),
        variants=[('rust_plains', 'Rust Plains (default)', {}),
                  ('oxide_badlands', 'Oxide Badlands', dict(poncho='#c98a2e', poncho_s='#a8701f', poncho_d='#7a4f14', scarf='#8a3a2a', scarf_s='#6b2a1e')),
                  ('polar_caps', 'Polar Caps', dict(poncho='#d9dde3', poncho_s='#b9bfc8', poncho_d='#8e95a0', scarf='#4f7fb0', scarf_s='#3a6290', band='#4f7fb0'))],
        lore=('Mars was the Concord\'s first stop out of Sol, and the Rustborn are the families who stayed to work the Olympium '
              'seams. The dust gets into everything, so they live wrapped in heavy ponchos and never take off their respirators '
              'outdoors; a Rustborn\'s goggles are pushed up only to show trust. They are the first people a player meets who '
              'remember the Concord by name, and they still keep a hand-cut Aresite core in every village as a shrine.'),
        behaviour=('Normal villager pace. During dust storms (rain on Mars) they pull their goggles down and stop gossiping. '
                   'Fond of machines: the job site is a Combustion Generator, and a Rustborn standing next to a running one '
                   'gets a small happy-particle burst.'),
        signature=('Rust Mechanic', 'combustion_generator', [
            ('Novice', '20 Rustsand -> 1 Emerald', '1 Emerald -> 6 Rust Lichen'),
            ('Apprentice', '12 Oxide Crust -> 1 Emerald', '3 Emeralds -> 4 Olympium Nuggets'),
            ('Journeyman', '4 Olympium Nuggets -> 1 Emerald', '5 Emeralds -> 1 Olympium Ingot'),
            ('Expert', '1 Aresite -> 3 Emeralds', '8 Emeralds -> 2 Olympium Plating'),
            ('Master', '-', '20 Emeralds -> 1 Olympus trim template (copy)')]),
        anims=[('idle', 'breathing; poncho hood drape sways 3 deg'), ('walk', 'legs +/-40 deg (vanilla)'),
               ('no', 'head shake (vanilla)'), ('goggles_down', 'goggles bone drops 2 px over the eyes during rain (0.25 s)')],
        notes=['The respirator bone replaces the vanilla nose; keep it parented to the head so head-shake moves it.',
               'Poncho is the vanilla robe idea (inflate 0.5 over the body) with a transparent fringe on the bottom row.',
               'Goggles are a separate bone so the rain animation can slide them down without touching the head.',
               'Glowmask: goggle lenses only.'],
        badge='the scarf')


# ==================================================================== 3. GLINTFOLK (Cerulon)
def glintfolk():
    def leg(p, P):
        p.fill('all', P['overall'], edge=.12)
        p.rows_from_bottom(('north', 'south', 'east', 'west'), 3, P['boot']); p.fill('bottom', P['boot'])
        p.rect('north', 1, 4, 2, 5, P['overall_s'])

    def torso(p, P):
        p.fill('all', P['shirt'], edge=.1)
        p.rect('north', 0, 2, 7, 11, P['overall']); p.rect('south', 0, 3, 7, 11, P['overall'])
        for f in ('east', 'west'): p.rect(f, 0, 5, 5, 11, P['overall'])
        for c in (1, 6): p.rect('north', c, 0, c, 1, P['overall']); p.px('north', c, 2, P['brass'])
        for r in range(3): p.px('south', 1 + r, r, P['overall']); p.px('south', 6 - r, r, P['overall'])
        p.rect('north', 2, 5, 5, 7, P['overall_s']); p.row('north', 5, P['overall_d'])               # bib pocket
        for f in ('north', 'south', 'east', 'west'): p.row(f, 9, P['belt'])
        p.px('north', 3, 9, P['brass']); p.px('north', 4, 9, P['brass'])
        for f in ('north', 'south', 'east', 'west'):
            w, h = p.size(f)
            for r in range(h):
                for c in range(w):
                    if p.t.img.getpixel((p.R[f][0] + c, p.R[f][1] + r))[:3] == P['shirt'][:3]: p.t.masks.setdefault('accent', set()).add((p.R[f][0] + c, p.R[f][1] + r))
        p.fill('top', P['shirt'])

    def arm(p, P):
        skin_hands(p, P, 'skin', 'shirt', cuff='shirt_d')
        for f in ('north', 'south', 'east', 'west'):
            for r in range(p.size(f)[1] - 3): p.t.masks.setdefault('accent', set()).update((p.R[f][0] + c, p.R[f][1] + r) for c in range(p.size(f)[0]))

    def forearms(p, P):
        p.fill('all', P['shirt'], edge=.12)
        for f in ('north', 'south', 'top', 'bottom'):
            w = p.size(f)[0]; p.col(f, 0, P['skin']); p.col(f, w - 1, P['skin'])
        p.fill(('east', 'west'), P['skin'])

    def head(p, P):
        p.fill('all', P['skin'], noise=3, grad=.08)
        p.rect('south', 0, 0, 7, 5, P['hair'], noise=5)
        for f in ('east', 'west'): p.rect(f, 0, 2, 7, 4, P['hair'], noise=5)
        eyes(p, 4, (1, 5), P['eye'], P['eye_hi'], glow=True, brow=P['brow'])
        for r in (7, 8, 9):
            for c in range(8):
                if (r > 7 or c in (0, 1, 6, 7)) and p.rng.random() < .75: p.px('north', c, r, P['beard'])
        for f in ('east', 'west'): p.rect(f, 0, 7, 7, 9, P['beard'], noise=4)

    def helmet(p, P):
        p.fill('all', P['hat'], edge=.15, grad=.18)
        p.row(('north', 'south', 'east', 'west'), 3, P['hat_d']); p.row(('north', 'south', 'east', 'west'), 2, P['hat_band'])
        p.fill('top', P['hat'], grad=0); p.rect('top', 4, 0, 4, 8, P['hat_hi'])                     # ridge
        p.fill('bottom', (0, 0, 0, 0))

    def brim(p, P):
        p.fill('all', P['hat_d'], edge=.1); p.fill('top', P['hat'])

    def lamp(p, P):
        p.fill('all', P['hat_d'], edge=.2)
        p.rect('north', 0, 0, 1, 1, P['lamp'], glow=True); p.px('north', 0, 0, P['lamp_hi'], glow=True)

    def nose(p, P):
        p.fill('all', P['skin_d'], noise=2); p.row('north', 3, P['skin'])

    def crystal(p, P):
        p.fill('all', P['cry'], noise=5, grad=.25)
        for f in ('north', 'south', 'east', 'west'):
            p.col(f, 0, P['cry_hi']); p.px(f, 0, 0, P['cry_core'])
        p.fill('top', P['cry_hi']); p.fill('bottom', P['cry_d']); p.glow_all()

    def handle(p, P):
        p.fill('all', P['wood'], edge=.15); p.row(('north', 'south', 'east', 'west'), 0, P['wood_d'])
        for r in (3, 4): p.row(('north', 'south', 'east', 'west'), r, P['leather'])

    def pickhead(p, P):
        p.fill('all', P['steel'], edge=.2); p.px('north', 0, 0, P['steel_d']); p.px('north', 5, 0, P['steel_d'])
        p.px('south', 0, 0, P['steel_d']); p.px('south', 5, 0, P['steel_d']); p.px('north', 2, 0, P['steel_hi'])

    bones = [Bone('body', pivot=(0, 12, 0)), Bone('arms', 'body', (0, 21, -1), ARM_ROT),
             Bone('head', pivot=(0, 24, 0)), Bone('helmet', 'head', (0, 31, 0)), Bone('nose', 'head', (0, 26, 0)),
             Bone('crystals', 'body', (0, 24, 0)), Bone('pick', 'body', (1.5, 17, 3.5)),
             Bone('right_leg', pivot=(2, 12, 0)), Bone('left_leg', pivot=(-2, 12, 0))]
    cubes = [
        Cube('right_leg', 'leg_r', (0, 0, -2), (4, 12, 4), leg), Cube('left_leg', 'leg_l', (-4, 0, -2), (4, 12, 4), leg),
        Cube('body', 'torso', (-4, 12, -3), (8, 12, 6), torso, label='Overalls over a teal shirt (profession colour)'),
        Cube('arms', 'arm_r', (4, 15, -3), (4, 8, 4), arm), Cube('arms', 'arm_l', (-8, 15, -3), (4, 8, 4), arm),
        Cube('arms', 'forearms', (-4, 15, -3), (8, 4, 4), forearms),
        Cube('head', 'head', (-4, 24, -4), (8, 10, 8), head, label='Glowing cyan eyes, stubble beard'),
        Cube('helmet', 'helmet', (-4.5, 31, -4.5), (9, 4, 9), helmet, label='Concord hard hat'),
        Cube('helmet', 'brim', (-4.5, 31, -6.5), (9, 1, 2), brim),
        Cube('helmet', 'lamp', (-1, 32, -5.5), (2, 2, 1), lamp, label='Headlamp (glows)'),
        Cube('nose', 'nose', (-1, 25, -6), (2, 4, 2), nose),
        Cube('crystals', 'cry_r1', (4, 22, -1.5), (2, 4, 2), crystal, label='Cerulite growing from the shoulders'),
        Cube('crystals', 'cry_r2', (5.5, 22, 0.5), (1, 3, 1), crystal),
        Cube('crystals', 'cry_l1', (-6, 22, -0.5), (2, 3, 2), crystal), Cube('crystals', 'cry_l2', (-4.5, 23, 1.5), (1, 2, 1), crystal),
        Cube('crystals', 'cry_back', (-4, 17, 3), (2, 4, 2), crystal, label='Crystal on the back'),
        Cube('pick', 'pick_handle', (1, 12, 3), (1, 10, 1), handle, label='Pick slung on the back'),
        Cube('pick', 'pick_head', (-1.5, 21, 3), (6, 1, 1), pickhead),
    ]
    return Species(
        id='glintfolk', name='Glintfolk', planet='Cerulon', gravity=0.9, bones=bones, cubes=cubes, job='crystal_growth_chamber',
        tag='Heirs of the Quiet Mines',
        palette=dict(skin='#8fb3c4', skin_d='#6a8fa3', hair='#22324a', brow='#1b2738', beard='#5d7f93', eye='#7ff6ff', eye_hi='#e8ffff',
                     overall='#2c3d57', overall_s='#24334a', overall_d='#1d2a40', shirt='#3ba9bc', shirt_d='#2a8798', belt='#3b2a22',
                     brass='#c9a24a', boot='#3a2c24', hat='#d6a93f', hat_hi='#f2cf6a', hat_d='#9c7522', hat_band='#2c3d57',
                     lamp='#fff3b0', lamp_hi='#ffffff', cry='#1592b8', cry_hi='#3fc9e8', cry_core='#e8ffff', cry_d='#0e6f8e',
                     wood='#9b8a72', wood_d='#6e604e', leather='#3b2a22', steel='#7d8b99', steel_hi='#b7c3cf', steel_d='#4a5562'),
        variants=[('azure_plains', 'Azure Plains (default)', {}),
                  ('crystal_shores', 'Crystal Shores', dict(overall='#c9b98f', overall_s='#b3a37a', overall_d='#968862', shirt='#e07a5f', shirt_d='#b85c44')),
                  ('shardwood_grove', 'Shardwood Grove', dict(overall='#3f5a3a', overall_s='#34492f', overall_d='#283a25', shirt='#b48ae0', shirt_d='#8f68b8'))],
        lore=('Cerulon was the Concord\'s peaceful mining world, the Quiet Mines. When the Concord splintered, the miners stayed '
              'with the Sentinel and the crystal, and the crystal stayed with them: older Glintfolk grow little Cerulite spurs '
              'on their shoulders, which they file down for luck and grow back in a season. They still wear the Concord\'s '
              'hard hats. Once the player beats the Prism Sentinel, Glintfolk call them "heir" in their trade titles.'),
        behaviour=('They work at night as well as by day: their job site is the Crystal Growth Chamber, and they can visit it at any '
                   'time. Headlamps switch on below light 7. After the Prism Sentinel is beaten, every Glintfolk gives a '
                   'permanent 10% Hero discount to that player.'),
        signature=('Crystal Tender', 'crystal_growth_chamber', [
            ('Novice', '24 Crystal Sand -> 1 Emerald', '1 Emerald -> 4 Starblooms'),
            ('Apprentice', '16 Azure Moss -> 1 Emerald', '2 Emeralds -> 1 Shardwood Sapling'),
            ('Journeyman', '6 Pulsar Dust -> 1 Emerald', '4 Emeralds -> 4 Pulsar Lamps'),
            ('Expert', '2 Cerulite -> 3 Emeralds', '8 Emeralds -> 4 Cyrrium Nuggets'),
            ('Master', '-', '22 Emeralds -> 1 Geode trim template (copy)')]),
        anims=[('idle', 'breathing; occasional glance down at the shoulder crystals'), ('walk', 'legs +/-40 deg; pick swings 4 deg'),
               ('no', 'head shake (vanilla)'), ('lamp', 'headlamp emissive turns on below light 7 (code)')],
        notes=['Shoulder crystals sit on their own bone (crystals) so a baby model can hide them.',
               'The pick bone pivots where it is strapped ([-1.5, 17, 3.5] in the file) for a small walk swing.',
               'Profession overlays recolour the teal shirt pixels; the overalls stay the biome colour.',
               'Glowmask: eyes, headlamp, all five crystals.'],
        badge='the teal shirt and sleeves')


# ==================================================================== 4. ASHWRIGHTS (Skarn)
def ashwright():
    def cracks(p, P, f, n):
        w, h = p.size(f)
        for _ in range(n):
            c, r = p.rng.randrange(w), p.rng.randrange(h)
            for _ in range(p.rng.randint(2, 4)):
                p.px(f, c, r, P['ember'], glow=True)
                c += p.rng.choice((-1, 0, 1)); r += 1
                if not (0 <= c < w and 0 <= r < h): break

    def rock(p, P, n=2):
        p.fill('all', P['rock'], noise=6, edge=.1)
        for f in ('north', 'south', 'east', 'west'): cracks(p, P, f, n)

    def leg(p, P):
        p.fill('all', P['trouser'], edge=.12)
        p.rows_from_bottom(('north', 'south', 'east', 'west'), 3, P['boot']); p.fill('bottom', P['boot'])
        p.row(('north', 'south', 'east', 'west'), 5, P['boot']); p.px('north', 1, 3, P['brass']); p.px('north', 2, 3, P['brass'])

    def torso(p, P):
        rock(p, P, 3)
        for r in range(11): p.px('north', min(9, r), r, P['leather']); p.px('north', min(9, r + 1), r, P['leather'])   # harness strap
        p.px('north', 5, 5, P['brass'])

    def apron(p, P):
        p.fill('all', P['apron'], edge=.1, grad=.15)
        for f in ('north',):
            w, h = p.size(f)
            for r in range(h): p.px(f, 0, r, P['trim'], mask='accent'); p.px(f, w - 1, r, P['trim'], mask='accent')
            p.row(f, h - 1, P['trim'], mask='accent')
            for c, r in ((1, 1), (6, 1), (1, h - 3), (6, h - 3)): p.px(f, c, r, P['brass'])
            for _ in range(5): p.px(f, p.rng.randrange(1, w - 1), p.rng.randrange(h - 1), P['scorch'])
        p.fill('south', P['apron_d'])

    def pauldron(p, P):
        p.fill('all', P['marble'], noise=4, edge=.12)
        p.fill('top', P['marble_hi'], noise=3)
        for f in ('north', 'south', 'east', 'west', 'top'):
            w, h = p.size(f); c = p.rng.randrange(w)
            for r in range(h): p.px(f, max(0, min(w - 1, c)), r, P['vein']); c += p.rng.choice((-1, 0, 1))
        p.row(('north', 'south', 'east', 'west'), 2, P['marble_s'])

    def arm(p, P):
        rock(p, P, 1)
        for f in ('north', 'south', 'east', 'west'):
            h = p.size(f)[1]; p.row(f, h - 3, P['wrap']); p.row(f, h - 2, P['wrap_d'])
        p.fill('bottom', P['rock'])

    def forearms(p, P):
        rock(p, P, 1)
        for f in ('north', 'south', 'top', 'bottom'):
            w = p.size(f)[0]
            for c in (2, w - 3): p.col(f, c, P['wrap'])

    def head(p, P):
        rock(p, P, 2)

    def mask(p, P):
        p.fill('all', P['marble'], noise=3, edge=.15)
        for c0 in (1, 5):
            p.px('north', c0, 2, P['slit']); p.px('north', c0 + 1, 2, P['eye'], glow=True)
        p.px('north', 1, 2, P['eye_d'], glow=True)
        for r in range(1, 5): p.px('north', 3, r, P['marble_hi']); p.px('north', 4, r, P['marble_hi'])
        for c in (2, 3, 4, 5): p.px('north', c, 5, P['slit'] if c % 2 == 0 else P['marble_s'])
        c = 6
        for r in range(7): p.px('north', c, r, P['vein']); c += p.rng.choice((-1, 0, 0, 1))
        p.px('north', 0, 4, P['vein']); p.px('north', 1, 5, P['vein'])

    def crest(p, P):
        p.fill('all', P['rock_d'], noise=5, edge=.15)
        p.fill('top', P['ember'], noise=8); p.px('top', 1, 1, P['ember_hi'])
        p.row(('north', 'south', 'east', 'west'), 0, P['ember'], glow=True)
        p.glow_all('top')

    bones = [Bone('body', pivot=(0, 9, 0)), Bone('arms', 'body', (0, 17, -1.5), (-40, 0, 0)),
             Bone('head', pivot=(0, 20, 0)), Bone('mask', 'head', (0, 24, -4)), Bone('crest', 'head', (0, 28, 0)),
             Bone('right_leg', pivot=(2.5, 9, 0)), Bone('left_leg', pivot=(-2.5, 9, 0))]
    cubes = [
        Cube('right_leg', 'leg_r', (0.5, 0, -2.5), (4, 9, 5), leg), Cube('left_leg', 'leg_l', (-4.5, 0, -2.5), (4, 9, 5), leg, label='Short, thick legs (1.2 g)'),
        Cube('body', 'torso', (-5, 9, -3.5), (10, 11, 7), torso, label='Rock skin with ember cracks'),
        Cube('body', 'apron', (-4, 3, -4.5), (8, 14, 1), apron, label='Forge apron (trim = profession colour)'),
        Cube('body', 'pauldron_r', (3.5, 18, -4), (4, 3, 8), pauldron), Cube('body', 'pauldron_l', (-7.5, 18, -4), (4, 3, 8), pauldron, label='Scorched-marble pauldrons'),
        Cube('arms', 'arm_r', (5, 11, -3.5), (3, 8, 4), arm), Cube('arms', 'arm_l', (-8, 11, -3.5), (3, 8, 4), arm),
        Cube('arms', 'forearms', (-5, 11, -3.5), (10, 4, 4), forearms, label='Wrapped forearms'),
        Cube('head', 'head', (-4, 20, -4), (8, 8, 8), head),
        Cube('mask', 'mask', (-4, 20.5, -4.75), (8, 7, 1), mask, label='Marble mask, ember eye slits'),
        Cube('crest', 'crest', (-1.5, 28, -1.5), (3, 3, 3), crest, label='Chimney crest (smokes)'),
    ]
    return Species(
        id='ashwright', name='Ashwrights', planet='Skarn', gravity=1.2, bones=bones, cubes=cubes, job='alloy_forge',
        tag='Smiths of the Wound',
        palette=dict(rock='#3a3134', rock_d='#2a2326', ember='#ff7a2e', ember_hi='#ffc061', marble='#e6ddd0', marble_hi='#f5efe6',
                     marble_s='#b8ad9f', vein='#d9772f', slit='#1a1416', eye='#ffb347', eye_d='#ff7a2e', trouser='#3a3236',
                     boot='#221c1e', brass='#c9a24a', leather='#6b4a32', apron='#6b4a32', apron_d='#4a3222', trim='#c9a24a',
                     scorch='#2a1d16', wrap='#8a6a4a', wrap_d='#5e4630'),
        variants=[('ember_fields', 'Ember Fields (default)', {}),
                  ('marble_contact_zone', 'Marble Contact Zone', dict(apron='#b8ad9f', apron_d='#8e8478', rock='#5a4e4f', trim='#d9772f')),
                  ('charwood_barrens', 'Charwood Barrens', dict(apron='#2a2326', apron_d='#1a1416', trim='#ff7a2e', ember='#ff4f2e'))],
        lore=('Skarn is the Wound, where Archon Vael tore space open. The Ashwrights descend from the Concord smiths who were '
              'caught at the forges when it happened; the heat and the rift changed them until their skin set like skarn rock, '
              'still glowing in the cracks. They wear masks of scorched marble, because a face that shows its fire is thought '
              'rude. Heavy gravity keeps them short and broad. They forged the first gate parts, and they know it.'),
        behaviour=('Slow (0.85x walk speed), very knockback resistant (0.6), and immune to fire and Ember Crust, so their villages '
                   'can sit on hot ground. The crest puffs a smoke particle every few seconds; more when they work their '
                   'Alloy Forge. They do not panic from fire, only from raiders and the Rift Tyrant.'),
        signature=('Ashwright Smith', 'alloy_forge', [
            ('Novice', '12 Slag -> 1 Emerald', '1 Emerald -> 3 Cinder Caps'),
            ('Apprentice', '8 Tremor Dust -> 1 Emerald', '3 Emeralds -> 2 Tremor Lamps'),
            ('Journeyman', '4 Ruskite Nuggets -> 1 Emerald', '4 Emeralds -> 1 Charwood Sapling'),
            ('Expert', '6 Rift Glass -> 2 Emeralds', '9 Emeralds -> 4 Pyrium Nuggets'),
            ('Master', '-', '24 Emeralds -> 1 Rift trim template (copy)')]),
        anims=[('idle', 'heavy breathing: body bobs 0.3 px; crest smoke particles (code)'), ('walk', 'legs +/-30 deg, 0.85x speed'),
               ('no', 'head shake (vanilla); the mask moves with the head'), ('work', 'at the forge: arms bone lifts 15 deg, three taps')],
        notes=['Arms rotate -40 deg (slightly less than vanilla) because the forearms are a wider 10 px bar.',
               'The mask is its own cube in front of the head (z -4.75), so the head front is never seen and needs no face.',
               'Ember cracks are randomised per cube by the generator seed; re-running keeps them stable.',
               'Glowmask: ember cracks, eye slits, crest top. Use an emissive layer so the cracks show in the dark.'],
        badge='the brass apron trim')


# ==================================================================== 5. HOLLOW KIN (Eidolon)
def hollowkin():
    def leg(p, P):
        p.fill('all', P['coat'], edge=.12)
        for f in ('north', 'south', 'east', 'west'):
            for r in range(1, p.size(f)[1], 3): p.row(f, r, P['coat_s'])

    def cuff(p, P):
        p.fill('all', P['fur'], noise=10, edge=.08); p.fill('bottom', P['boot'])
        for f in ('north', 'south', 'east', 'west'): p.row(f, 2, P['fur_s'], noise=8)

    def torso(p, P):
        p.fill('all', P['coat'], edge=.1)

    def coat(p, P):
        p.fill('all', P['coat'], edge=.12, grad=.12)
        for f in ('north', 'south', 'east', 'west'):
            w, h = p.size(f)
            p.rect(f, 0, h - 2, w - 1, h - 1, P['fur'], noise=10)
            p.row(f, 9, P['sash'], mask='accent'); p.row(f, 10, shade(P['sash'], .75), mask='accent')
        for r in range(0, p.size('north')[1] - 2): p.px('north', 3, r, P['coat_d']); p.px('north', 4, r, P['coat_s'])
        for r in (13, 15): p.px('north', 3, r, P['toggle']); p.px('north', 4, r, P['toggle'])
        p.fill(('top', 'bottom'), (0, 0, 0, 0))

    def pauldron(p, P):
        p.fill('all', P['hull'], noise=4, edge=.18)
        for f in ('north', 'south', 'east', 'west', 'top'):
            w, h = p.size(f)
            for c, r in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)): p.px(f, c, r, P['rivet'])
        w, h = p.size('east')
        for c in range(w):
            for r in range(h):
                if (c + r) % 4 < 2 and 1 <= r <= 2: p.px('east', c, r, P['hazard'])
                elif 1 <= r <= 2: p.px('east', c, r, P['hazard_d'])
        p.rect('top', 1, 1, 2, 5, P['hull_hi'])

    def arm(p, P):
        p.fill('all', P['coat'], edge=.12)
        for f in ('north', 'south', 'east', 'west'):
            h = p.size(f)[1]; p.rect(f, 0, h - 3, 9, h - 2, P['fur'], noise=8); p.row(f, h - 1, P['mitten'])
        p.fill('bottom', P['mitten'])

    def forearms(p, P):
        p.fill('all', P['coat'], edge=.12)
        for f in ('north', 'south', 'top', 'bottom'):
            w = p.size(f)[0]; p.col(f, 0, P['mitten']); p.col(f, w - 1, P['mitten'])
        p.fill(('east', 'west'), P['mitten'])

    def head(p, P):
        p.fill('all', P['skin'], noise=3, grad=.08)
        for c0 in (1, 5):
            p.rect('north', c0 - 0, 2, c0 + 1, 4, P['socket'])
            p.px('north', c0, 3, P['eye'], glow=True); p.px('north', c0 + 1, 3, P['eye_hi'], glow=True)
            p.px('north', c0, 2, P['frost']); p.px('north', c0 + 1, 2, P['frost'])
        p.px('north', 3, 7, P['lip']); p.px('north', 4, 7, P['lip'])

    def hood(p, P):
        p.fill('all', P['fur'], noise=12, edge=.06, grad=.12)
        p.clear('north', 2, 2, 7, 10)
        for c in range(1, 9): p.px('north', c, 1, P['fur_s'])
        for r in range(1, 11): p.px('north', 1, r, P['fur_s']); p.px('north', 8, r, P['fur_s'])
        for f in ('south', 'east', 'west', 'top'):                                                  # fur tufts
            w, h = p.size(f)
            for _ in range(w * h // 6): p.px(f, p.rng.randrange(w), p.rng.randrange(h), p.rng.choice((P['fur_s'], P['frost'])))
        for r in range(11): p.px('south', 4, r, P['fur_s']); p.px('south', 5, r, shade(P['fur_s'], .93))   # back seam
        p.fill('bottom', (0, 0, 0, 0))

    def nose(p, P):
        p.fill('all', P['skin_d'], noise=2); p.px('north', 0, 1, P['frost_nose']); p.px('north', 1, 1, P['frost_nose'])

    def iron(p, P):
        p.fill('all', P['iron'], edge=.2)

    def glass(p, P):
        p.fill('all', P['glass'], noise=6, grad=.2)
        for f in ('north', 'south', 'east', 'west'):
            p.col(f, 0, P['iron']); p.col(f, 2, P['iron']); p.px(f, 1, 1, P['glass_hi'])
        p.fill(('top', 'bottom'), P['iron'])
        for f in ('north', 'south', 'east', 'west'):
            for r in range(4): p.t.glow.add((p.R[f][0] + 1, p.R[f][1] + r))

    bones = [Bone('body', pivot=(0, 12, 0)), Bone('arms', 'body', (0, 21, -1), ARM_ROT),
             Bone('head', pivot=(0, 24, 0)), Bone('hood', 'head', (0, 24, 0)), Bone('nose', 'head', (0, 27, 0)),
             Bone('pauldron', 'body', (5, 23, 0)), Bone('lantern', 'body', (-6, 15, 0)),
             Bone('right_leg', pivot=(2, 12, 0)), Bone('left_leg', pivot=(-2, 12, 0))]
    cubes = [
        Cube('right_leg', 'leg_r', (0, 0, -2), (4, 12, 4), leg), Cube('left_leg', 'leg_l', (-4, 0, -2), (4, 12, 4), leg),
        Cube('right_leg', 'cuff_r', (0, 0, -2), (4, 3, 4), cuff, inflate=0.5), Cube('left_leg', 'cuff_l', (-4, 0, -2), (4, 3, 4), cuff, inflate=0.45, label='Fur boots'),
        Cube('body', 'torso', (-4, 12, -3), (8, 12, 6), torso),
        Cube('body', 'coat', (-4, 4, -3), (8, 20, 6), coat, inflate=0.5, label='Parka, sash = profession colour'),
        Cube('pauldron', 'pauldron', (3.5, 21, -3.5), (4, 4, 7), pauldron, label='Salvaged hull-plate pauldron'),
        Cube('arms', 'arm_r', (4, 15, -3), (4, 8, 4), arm), Cube('arms', 'arm_l', (-8, 15, -3), (4, 8, 4), arm),
        Cube('arms', 'forearms', (-4, 15, -3), (8, 4, 4), forearms),
        Cube('head', 'head', (-4, 24, -4), (8, 9, 8), head, label='Frost-rimmed spectral eyes'),
        Cube('hood', 'hood', (-5, 23.5, -5), (10, 11, 10), hood, label='Fur hood'),
        Cube('nose', 'nose', (-1, 26, -5), (2, 2, 1), nose),
        Cube('lantern', 'hookbar', (-6, 15, -0.5), (2, 1, 1), iron), Cube('lantern', 'chain', (-6.5, 14, -0.5), (1, 1, 1), iron),
        Cube('lantern', 'cap', (-7, 13, -1), (2, 1, 2), iron),
        Cube('lantern', 'glass', (-7.5, 9, -1.5), (3, 4, 3), glass, label='Ghost lantern (glows)'),
        Cube('lantern', 'base', (-7, 8, -1), (2, 1, 2), iron),
    ]
    return Species(
        id='hollow_kin', name='Hollow Kin', planet='Eidolon', gravity=0.8, bones=bones, cubes=cubes, job='salvage_station',
        tag='Children of the Frozen Fleet',
        palette=dict(skin='#cfe3ec', skin_d='#a9c6d4', socket='#7f97a8', eye='#9cfcff', eye_hi='#e6ffff', frost='#f4fbff', lip='#7fa3c4',
                     frost_nose='#8fc3e0', fur='#eef3f5', fur_s='#c3cfd6', coat='#4b5d70', coat_s='#405063', coat_d='#34424f',
                     sash='#c9a24a', toggle='#c9a24a', boot='#34424f', mitten='#2a3540', hull='#6f7b86', hull_hi='#8e9aa5', rivet='#b7c3cd',
                     hazard='#d9b44a', hazard_d='#2a2f36', iron='#2a2f36', glass='#9cfcff', glass_hi='#e6ffff'),
        variants=[('frozen_graveyard', 'Frozen Graveyard (default)', {}),
                  ('phantom_ice_sheets', 'Phantom Ice Sheets', dict(coat='#9fbfd4', coat_s='#8aaabf', coat_d='#6f8fa6', sash='#4b5d70')),
                  ('hoarwood_taiga', 'Hoarwood Taiga', dict(coat='#3c5544', coat_s='#33493a', coat_d='#283a2e', sash='#b0453a', toggle='#b0453a'))],
        lore=('When Vael\'s rift opened, the Concord survivors fled to Eidolon and froze there waiting for a rescue that never came; '
              'their ghosts became the Hollow Fleet. The Hollow Kin are the children who were thawed out first and lived. They '
              'grew up among the wrecks, pale as frost, with eyes that catch the light like phantom ice. Everything they own is '
              'salvaged, from hull-plate armour to the lanterns they carry, lit with the same cold light as the ghosts.'),
        behaviour=('They never freeze in powder snow or on Polar Frost. At night the ghost lantern brightens and Hollow Fleet '
                   'phantoms ignore anyone standing within 8 blocks of a Hollow Kin. Shown a Remnant Shard, they will say '
                   'which wreck it came from (a Codex hint).'),
        signature=('Salvager', 'salvage_station', [
            ('Novice', '10 Permafrost Bricks -> 1 Emerald', '1 Emerald -> 2 Frost Milk'),
            ('Apprentice', '6 Hull Plating -> 1 Emerald', '2 Emeralds -> 1 Hoarwood Sapling'),
            ('Journeyman', '2 Broken Consoles -> 1 Emerald', '5 Emeralds -> 4 Salvium Nuggets'),
            ('Expert', '3 Remnant Shards -> 2 Emeralds', '8 Emeralds -> 2 Frost Crystals'),
            ('Master', '-', '24 Emeralds -> 1 Hull trim template (copy)')]),
        anims=[('idle', 'breath particle every 2 s (code); lantern sways +/-6 deg'), ('walk', 'legs +/-40 deg; lantern swings +/-12 deg'),
               ('no', 'head shake (vanilla); hood moves with the head'), ('lantern_flare', 'when a phantom is near: glass glow flickers (code)')],
        notes=['The hood is bigger than the head (10 x 11 x 10) with the face cut out, so the face sits back inside it.',
               'Use a no-cull render type (GeckoLib default entityCutoutNoCull) so the inside of the hood shows through the opening.',
               'The boot cuffs inflate 0.5 and 0.45 so their touching faces never z-fight.',
               'Lantern bone pivots at the belt hook ([6, 15, 0] in the file) for the sway. Glowmask: eyes and the lantern glass.'],
        badge='the coat sash')


# ==================================================================== 6. SUNWARDENS (Solvane)
def sunwarden():
    def leg(p, P):
        p.fill('all', P['skin'], noise=3)
        p.rows_from_bottom(('north', 'south', 'east', 'west'), 2, P['gold']); p.fill('bottom', P['gold_d'])

    def torso(p, P):
        p.fill('all', P['robe'], edge=.1)

    def robe(p, P):
        p.fill('all', P['robe'], edge=.10, grad=.12)
        for f in ('north', 'south', 'east', 'west'):
            w, h = p.size(f)
            p.rect(f, 0, h - 2, w - 1, h - 1, P['gold']); p.row(f, h - 3, P['gold_d'])
            p.row(f, 9, P['sash'], mask='accent'); p.row(f, 10, shade(P['sash'], .78), mask='accent')
        for r in range(11, p.size('north')[1] - 2): p.px('north', 3, r, P['gold']); p.px('north', 4, r, P['gold'])
        for c, r in ((2, 14), (5, 14), (3, 13), (4, 15)): p.px('north', c, r, P['gold_hi'])
        p.fill(('top', 'bottom'), (0, 0, 0, 0))

    def mantle(p, P):
        p.fill('all', P['gold'], edge=.15, grad=.2)
        for f in ('north', 'south', 'east', 'west'):
            w = p.size(f)[0]; p.row(f, 2, P['robe'])
            for c in range(0, w, 2): p.px(f, c, 1, P['gold_d'])
        p.fill('top', P['gold'], grad=0); p.rect('top', 1, 1, 8, 6, P['gold_d'])
        p.fill('bottom', P['gold_d'])

    def pectoral(p, P):
        p.fill('all', P['gold_d'])
        p.fill('north', P['gold'], noise=0, grad=0); p.px('north', 1, 1, P['sun_core'], glow=True)
        for c, r in ((1, 0), (0, 1), (2, 1), (1, 2)): p.px('north', c, r, P['sun'], glow=True)

    def arm(p, P):
        skin_hands(p, P, 'skin', 'robe', cuff='gold')
        for f in ('north', 'south', 'east', 'west'): p.row(f, 0, P['robe_s'])

    def forearms(p, P):
        p.fill('all', P['robe'], edge=.12)
        for f in ('north', 'south', 'top', 'bottom'):
            w = p.size(f)[0]; p.col(f, 0, P['skin']); p.col(f, w - 1, P['skin']); p.col(f, 1, P['gold']); p.col(f, w - 2, P['gold'])
        p.fill(('east', 'west'), P['skin'])

    def head(p, P):
        p.fill('all', P['skin'], noise=3, grad=.08)
        p.fill('top', P['hair']); p.rect('south', 0, 0, 7, 6, P['hair'], noise=5)
        for f in ('east', 'west'): p.rect(f, 0, 0, 7, 1, P['hair'], noise=5); p.rect(f, 0 if f == 'east' else 4, 2, 3 if f == 'east' else 7, 5, P['hair'], noise=5)
        p.row('north', 0, P['hair']); p.row('north', 1, P['hair_s'])
        eyes(p, 4, (1, 5), P['eye'], P['eye_hi'], glow=True, brow=P['hair'])
        p.px('north', 3, 6, P['skin_d']); p.px('north', 4, 6, P['skin_d'])

    def circlet(p, P):
        p.fill('all', P['gold'], noise=3); p.fill(('top', 'bottom'), (0, 0, 0, 0))
        for f in ('east', 'west', 'south'):
            for c in range(0, p.size(f)[0], 3): p.px(f, c, 0, P['gold_hi'])

    def gem(p, P):
        p.fill('all', P['gem'], noise=4); p.px('north', 0, 0, P['gem_hi'], glow=True); p.glow_all()

    def nose(p, P):
        p.fill('all', P['skin_d'], noise=2); p.row('north', 0, P['skin'])

    def halo(p, P):
        p.fill('all', P['halo_o'], noise=0, grad=0)
        for f in ('north', 'south'):
            w, h = p.size(f)
            for r in range(h):
                for c in range(w):
                    dx, dy = c - (w - 1) / 2, r - (h - 1) / 2; dd = (dx * dx + dy * dy) ** .5
                    ray = (abs(dx) < .6 or abs(dy) < .6 or abs(abs(dx) - abs(dy)) < .6)
                    if dd > 5.9 and not (ray and dd < 6.4): p.px(f, c, r, (0, 0, 0, 0))
                    elif dd > 5.0: p.px(f, c, r, P['halo_o'], glow=True)
                    elif dd > 4.0: p.px(f, c, r, P['halo_m'], glow=True)
                    elif dd > 3.2: p.px(f, c, r, P['halo_i'], glow=True)
                    elif ray and dd > 1.8: p.px(f, c, r, P['halo_m'], glow=True)
                    else: p.px(f, c, r, (0, 0, 0, 0))
        for f in ('east', 'west', 'top', 'bottom'):
            p.fill(f, P['halo_m'], noise=0, grad=0); p.glow_all(f)
        for f in ('east', 'west'):
            for r in (0, 1, 10, 11): p.px(f, 0, r, (0, 0, 0, 0))
        for f in ('top', 'bottom'):
            for c in (0, 1, 10, 11): p.px(f, c, 0, (0, 0, 0, 0))

    bones = [Bone('body', pivot=(0, 10, 0)), Bone('arms', 'body', (0, 19, -1), ARM_ROT),
             Bone('head', pivot=(0, 22, 0)), Bone('circlet', 'head', (0, 27, 0)), Bone('nose', 'head', (0, 25, 0)),
             Bone('halo', 'head', (0, 29, 5)), Bone('right_leg', pivot=(2, 10, 0)), Bone('left_leg', pivot=(-2, 10, 0))]
    cubes = [
        Cube('right_leg', 'leg_r', (0, 0, -2), (4, 10, 4), leg), Cube('left_leg', 'leg_l', (-4, 0, -2), (4, 10, 4), leg),
        Cube('body', 'torso', (-4, 10, -3), (8, 12, 6), torso),
        Cube('body', 'robe', (-4, 2, -3), (8, 20, 6), robe, inflate=0.6, label='Full robe, sash = profession colour'),
        Cube('body', 'mantle', (-5, 19, -4), (10, 3, 8), mantle, label='Gold mantle'),
        Cube('body', 'pectoral', (-1.5, 19, -5), (3, 3, 1), pectoral, label='Sun pectoral (glows)'),
        Cube('arms', 'arm_r', (4, 13, -3), (4, 8, 4), arm), Cube('arms', 'arm_l', (-8, 13, -3), (4, 8, 4), arm),
        Cube('arms', 'forearms', (-4, 13, -3), (8, 4, 4), forearms),
        Cube('head', 'head', (-4, 22, -4), (8, 8, 8), head, label='Molten-gold eyes'),
        Cube('circlet', 'circlet', (-4, 27, -4), (8, 1, 8), circlet, inflate=0.3, label='Circlet'),
        Cube('circlet', 'gem', (-0.5, 27, -4.8), (1, 1, 1), gem),
        Cube('nose', 'nose', (-1, 24, -5.5), (2, 3, 2), nose),
        Cube('halo', 'halo', (-6, 23, 4.5), (12, 12, 1), halo, label='Corona halo (spins, glows)'),
    ]
    return Species(
        id='sunwarden', name='Sunwardens', planet='Solvane', gravity=1.3, bones=bones, cubes=cubes, job='solar_array',
        tag='Keepers of the Last Light',
        palette=dict(skin='#e8c99a', skin_d='#c9a274', hair='#fff3d6', hair_s='#e8d6a8', eye='#ffcf4a', eye_hi='#fff6c4',
                     robe='#f4efe3', robe_s='#d8cfbd', gold='#e9ac42', gold_hi='#ffd77a', gold_d='#b07a22', sash='#8f2d22',
                     sun='#ffd25a', sun_core='#fff3c4', gem='#d6342a', gem_hi='#ff9a8a', halo_o='#ff9a2e', halo_m='#ffd25a', halo_i='#fff3c4'),
        variants=[('corona_flats', 'Corona Flats (default)', {}),
                  ('sunspot_plateaus', 'Sunspot Plateaus', dict(robe='#4a2f2a', robe_s='#3a2420', sash='#e9ac42', gold='#c98a2e', gold_d='#8a5a18')),
                  ('gildwood_oasis', 'Gildwood Oasis', dict(robe='#e7ecd4', robe_s='#c9d2ae', sash='#4f8a3a'))],
        lore=('The Sunwardens tended the great star of Solvane long before it began to die. When Vael fused himself with the sun, '
              'they stayed and kept their oaths, burning the old hymns into gildwood and singing the light back every dusk. The '
              'heaviest gravity of any world keeps them small and steady; their corona halos are not jewellery but grown, a '
              'gift of the star they serve. What they think of the player depends on which ending the player chooses.'),
        behaviour=('Never sleep through a sunrise: they gather at the village bell at dawn. Halos spin faster at noon. After the '
                   'ending choice: "Rekindle" makes them brighten (halos full glow, extra trade XP); "Let it fade" dims their '
                   'halos to embers and unlocks a farewell trade.'),
        signature=('Sun Keeper', 'solar_array', [
            ('Novice', '16 Solar Stone -> 1 Emerald', '1 Emerald -> 1 Gildwood Sapling'),
            ('Apprentice', '4 Coronite -> 1 Emerald', '3 Emeralds -> 4 Photium Nuggets'),
            ('Journeyman', '2 Starlite -> 1 Emerald', '6 Emeralds -> 4 Radiantine Nuggets'),
            ('Expert', '1 Star Map Fragment -> 4 Emeralds', '10 Emeralds -> 1 Star Map Fragment'),
            ('Master', '-', '28 Emeralds -> 1 Corona trim template (copy)')]),
        anims=[('idle', 'halo spins 360 deg every 12 s; breathing'), ('walk', 'legs +/-25 deg under the robe, 0.9x speed'),
               ('no', 'head shake (vanilla); the halo tilts with the head'), ('dawn_hymn', 'arms bone lifts 25 deg, head up, 3 s (at the bell)')],
        notes=['The halo is a flat 12 x 12 x 1 cube with a round cut-out texture; the bone pivots at its centre ([0, 29, 5]) for the spin.',
               'The robe inflates 0.6 to sit just outside the arms\' shoulders; legs show only as gold sandals below the hem.',
               'Ending state lives on the player; the renderer reads it client-side to pick full or ember halo brightness.',
               'Glowmask: halo, eyes, pectoral, circlet gem.'],
        badge='the red sash')


ALL = [lunari, rustborn, glintfolk, ashwright, hollowkin, sunwarden]
