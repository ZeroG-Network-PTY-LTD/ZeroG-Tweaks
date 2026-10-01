"""Explicit anatomical eye placements. No width-from-height or visor heuristics.

The two supplied face references define crisp rectangular eye pixels; existing
creature references define whether those eyes belong on the sides or front.
All coordinates are in the unchanged model space, facing north (-Z).
"""

def front(spread,y0,y1,z,width):
    return [(s*spread-width/2,y0,z,s*spread+width/2,y1,z) for s in (-1,1)]

def side(x,y0,y1,z0,z1):
    return [(s*x,y0,z0,s*x,y1,z1) for s in (-1,1)]

def single(width,y0,y1,z):
    return [(-width/2,y0,z,width/2,y1,z)]

# Every base species is named explicitly. Grazers, fowl, fish and selected small
# animals retain lateral eyes; predators/humanoids retain frontal eye pairs.
PROFILES={
 'regolith_crawler':('front',front(2,4,5,-12.035,2),'eye'),
 'rust_beetle':('front',front(1.9,5.1,5.85,-9.035,1.5),'eye'),
 'crystal_stag':('side',side(2.535,25,25.75,-12.1,-10.6),'eye'),
 'prismling':('ender_eye',single(4,2.8,6,-3.335),'crystal_hi'),
 'cinder_hound':('front',front(1.8,13,13.75,-12.035,1.5),'eye'),
 'frost_warden':('front',front(1.2,31,31.75,-3.535,1.5),'glow'),
 'flare_sprite':('ender_eye',single(4.5,11.9,16.1,-3.335),'flame'),
 'sun_colossus':('front',front(2.5,41,42,-5.035,3),'eye'),
 'dune_burrower':('front',front(1.35,3.375,4.125,-10.035,1.125),'teeth'),
 'ash_strider':('ender_eye',single(3.5,24.25,27.75,-8.035),'vent'),
 'rime_stalker':('front',front(1.8,12,12.75,-12.035,1.5),'eye'),
 'bog_lurker':('stalk',front(4,11,12.5,-12.035,1.5),'eye'),
 'crater_drifter':('ender_eye',single(6,15.5,21,-5.335),'rock_lt'),
 'prism_sentinel':('ender_eye',single(5,24.75,29.5,-5.035),'crystal_hi'),
 'rift_tyrant':('front',front(3.5,25,26,-20.035,3),'eye'),
 'eidolon_captain':('front',front(2,31,32,-4.035,2.25),'glow'),
 'dying_star':('ender_eye',single(6,41,47,-19.035),'vael'),
 'moon_hopper':('front',front(1.375,8,8.75,-6.035,1.5),'eye'),
 'dust_grazer':('side',side(4.035,14,14.75,-13.75,-12.25),'eye'),
 'azure_fowl':('side',side(2.035,12,12.75,-4.3,-2.8),'eye'),
 'glimmerfish':('side',side(2.035,7,7.75,-4.5,-3),'eye'),
 'slag_boar':('side',side(4.035,11,11.75,-13.1,-11.6),'eye'),
 'scorch_wyrmling':('side',side(2.535,8,8.75,-9.25,-7.75),'eye'),
 'frost_yak':('side',side(4.035,15,15.75,-13.9,-12.4),'eye'),
 'ice_leech':('front',front(1.375,4.125,4.75,-8.035,1.25),'ice'),
 'gildcrab':('stalk',front(1.5,11.125,11.875,-5.035,.875),'eye'),
 'deep_eel':('side',side(2.535,7,7.75,-12.25,-10.75),'fin'),
 'sand_skitter':('front',front(1.5,6,6.75,-8.035,1.5),'eye'),
 'amethyst_stalker':('side',side(6.035,20.5,21.5,-25.5,-22.5),'glow'),
 'hollow_sentinel':('front',front(2.5,38,39,-5.035,2.5),'glow'),
 'mossback':('side',side(10.035,20.5,21.5,-29.5,-26.5),'glow'),
 'slagjaw':('front',front(4.5,40,41.5,-22.035,3),'glow'),
 'splinter_mite':('ender_eye',single(4,3,6,-6.035),'glow'),
 'splinter_wisp':('ender_eye',single(3.5,11.75,15.25,-2.335),'glow'),
 'stormbitten_wyvern':('front',front(3.5,45,46,-44.035,2.5),'glow'),
 'tidewraith':('side',side(3.535,23,24,-11.5,-9.5),'glow'),
 'meteor_maw':('side',side(16.035,33,35,-10,-7),'glow'),
 'shardmother':('stalk',front(5,23,25,-25.035,2),'glow'),
}

NATURAL={'crystal_stag','moon_hopper','dust_grazer','azure_fowl','slag_boar','frost_yak','rust_beetle','gildcrab','dune_burrower'}

def is_optical(entry):
    name=entry['label'].lower()
    return entry['color_key']=='eye' or ('eye' in name and 'stalk' not in name and 'socket' not in name) or 'visor' in name

def refine_face(key,spec,entries):
    base=spec.get('base_rig',key)
    old=[e for e in entries if is_optical(e)]
    remaining=[e for e in entries if not is_optical(e)]
    assert base in PROFILES,f'{key}: missing explicit anatomical face profile'
    orientation,boxes,colour=PROFILES[base]
    assert colour in spec['pal'],(key,colour)
    pattern='ender_eye_'+base if orientation=='ender_eye' else 'noise' if base in NATURAL else 'glow'
    parent='helm' if base=='hollow_sentinel' else 'core' if base=='splinter_wisp' else 'body' if base=='meteor_maw' else 'head'
    if base=='splinter_wisp':spec['parents']['head']='core';parent='head'
    else:spec['parents'].setdefault('head','body')
    if orientation=='stalk':
        # Replace the old six-eye cluster/bulges with exactly two articulated
        # mounts. Keep the optical planes in front of the socket, never buried.
        remaining=[e for e in remaining if 'eye stalk' not in e['label'].lower() or base!='gildcrab']
        skin={'bog_lurker':'skin_dk','gildcrab':'body','shardmother':'shell'}[base]
        floor={'bog_lurker':9,'gildcrab':9,'shardmother':20}[base]
        for i,box in enumerate(boxes):
            cx=(box[0]+box[3])/2;cy=(box[1]+box[4])/2;z=box[2]+.035
            stalk='stalk_l' if cx<0 else 'stalk_r'
            spec['parents'][stalk]=parent
            spec.setdefault('pivots',{})[stalk]=[cx,floor,z+.5]
            remaining.append(dict(label='Eye stalk',box=(cx-.25,floor,z+.25,cx+.25,box[1],z+.75),color_key=skin,pattern='noise',group=stalk,plane_axis=None))
            remaining.append(dict(label='Eye socket',box=(box[0]-.15,box[1]-.15,z,box[3]+.15,box[4]+.15,z+1),color_key=skin,pattern='noise',group=stalk,plane_axis=None))
    for i,box in enumerate(boxes):
        eye_parent=('stalk_l' if box[0]+box[3]<0 else 'stalk_r') if orientation=='stalk' else parent
        remaining.append({'label':'Eyes','box':box,'color_key':colour,'pattern':pattern,
                          'group':eye_parent,'plane_axis':0 if orientation=='side' else 2})
    return remaining
