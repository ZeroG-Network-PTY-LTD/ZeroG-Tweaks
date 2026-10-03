"""Build the planet villager species: sheets, GeckoLib models, textures, glowmasks, animations, overlays.
Usage: python3 build_villagers.py <out_dir>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vkit import *
from species import ALL
import sheet as SH

SIG = {'lunari': '#58e1ff', 'rustborn': '#c9a24a', 'glintfolk': '#1592b8', 'ashwright': '#ff7a2e', 'hollow_kin': '#d9b44a', 'sunwarden': '#ffd25a'}


def anims(sp):
    A = {}
    legs = {'right_leg': {'rotation': {'0.0': [40, 0, 0], '0.5': [-40, 0, 0], '1.0': [40, 0, 0]}},
            'left_leg': {'rotation': {'0.0': [-40, 0, 0], '0.5': [40, 0, 0], '1.0': [-40, 0, 0]}}}
    amp = {'ashwright': 30, 'sunwarden': 25}.get(sp.id, 40)
    for b in legs.values():
        for k, v in b['rotation'].items(): v[0] = amp if v[0] > 0 else -amp
    idle = {'body': {'position': {'0.0': [0, 0, 0], '2.0': [0, -0.25 if sp.id == 'ashwright' else -0.15, 0], '4.0': [0, 0, 0]}},
            'head': {'rotation': {'0.0': [0, 0, 0], '2.0': [-2, 0, 0], '4.0': [0, 0, 0]}}}
    walk = dict(legs)
    extra = {}
    if sp.id == 'lunari':
        idle['crest'] = {'position': {'0.0': [0, 0, 0], '1.5': [0, 0.4, 0], '3.0': [0, 0, 0], '4.0': [0, 0, 0]}}
    if sp.id == 'rustborn':
        extra['goggles_down'] = {'loop': 'hold_on_last_frame', 'animation_length': 0.25, 'bones': {'goggles': {'position': {'0.0': [0, 0, 0], '0.25': [0, -2, -0.2]}}}}
    if sp.id == 'glintfolk':
        walk['pick'] = {'rotation': {'0.0': [0, 0, 4], '0.5': [0, 0, -4], '1.0': [0, 0, 4]}}
    if sp.id == 'ashwright':
        extra['work'] = {'loop': False, 'animation_length': 1.5, 'bones': {'arms': {'rotation': {'0.0': [0, 0, 0], '0.2': [15, 0, 0], '0.4': [0, 0, 0], '0.6': [15, 0, 0], '0.8': [0, 0, 0], '1.0': [15, 0, 0], '1.2': [0, 0, 0]}}}}
    if sp.id == 'hollow_kin':
        idle['lantern'] = {'rotation': {'0.0': [0, 0, -6], '2.0': [0, 0, 6], '4.0': [0, 0, -6]}}
        walk['lantern'] = {'rotation': {'0.0': [12, 0, 0], '0.5': [-12, 0, 0], '1.0': [12, 0, 0]}}
    if sp.id == 'sunwarden':
        extra['dawn_hymn'] = {'loop': False, 'animation_length': 3.0, 'bones': {'arms': {'rotation': {'0.0': [0, 0, 0], '0.5': [25, 0, 0], '2.5': [25, 0, 0], '3.0': [0, 0, 0]}},
                              'head': {'rotation': {'0.0': [0, 0, 0], '0.5': [-20, 0, 0], '2.5': [-20, 0, 0], '3.0': [0, 0, 0]}}}}
    A[f'animation.{sp.id}.idle'] = {'loop': True, 'animation_length': 4.0, 'bones': idle}
    if sp.id == 'sunwarden':
        A[f'animation.{sp.id}.halo_spin'] = {'loop': True, 'animation_length': 12.0, 'bones': {'halo': {'rotation': {'0.0': [0, 0, 0], '12.0': [0, 0, 360]}}}}
    A[f'animation.{sp.id}.walk'] = {'loop': True, 'animation_length': 1.0, 'bones': walk}
    A[f'animation.{sp.id}.no'] = {'loop': True, 'animation_length': 0.7, 'bones': {'head': {'rotation': {
        '0.0': [23, 0, 0], '0.175': [23, 0, 17], '0.35': [23, 0, 0], '0.525': [23, 0, -17], '0.7': [23, 0, 0]}}}}
    for k, v in extra.items(): A[f'animation.{sp.id}.{k}'] = v
    return {'format_version': '1.8.0', 'animations': A, 'geckolib_format_version': 2}


def main(out):
    os.makedirs(f'{out}/sheets', exist_ok=True)
    built = []
    for i, f in enumerate(ALL):
        sp = f(); sp.sig_colour = SIG[sp.id]
        d = f'{out}/blockbench/{sp.id}'; os.makedirs(f'{d}/professions', exist_ok=True)
        json.dump(sp.geo(), open(f'{d}/{sp.id}.geo.json', 'w'), indent=1)
        json.dump(anims(sp), open(f'{d}/{sp.id}.animation.json', 'w'), indent=1)
        tex = sp.texture(); tex.img.save(f'{d}/{sp.id}.png'); tex.glowmask().save(f'{d}/{sp.id}_glowmask.png')
        for vid, vname, pal in sp.variants[1:]:
            sp.texture(pal).img.save(f'{d}/{sp.id}_{vid}.png')
        for pname, col in SH.PROF + [(sp.signature[0], sp.sig_colour)]:
            SH.overlay(tex, col).save(f'{d}/professions/{pname.lower().replace(" ", "_")}.png')
        yy = SH.build(sp, f'{out}/sheets/{i + 1:02d}_{sp.id}.png')
        print(sp.id, sp.W, sp.H, 'text ends at', yy)
        built.append(sp)
    return built


if __name__ == '__main__':
    main(sys.argv[1])
