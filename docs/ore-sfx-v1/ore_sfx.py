"""ZeroG ore block sounds (v1): three families, procedural, seeded, re-runnable.

Owner's call (2026-10-06): the 39 ores get three sound families instead of vanilla stone --
  metal  (Ferrox, Moonsteel, ... and the precious metals): stone crunch + a short metallic ring
  gem    (the main gem sets and gem ores: Nullifite, Cerulite, Selenite, ...): stone crunch + a glassy chime
  dust   (the iron-tier fuel / energy-dust ores): a soft, gritty crumble
Each family has break (3), step (4) and hit (3) sounds; place reuses break and fall reuses step (like vanilla stone).
Reuses the Sentinel generator's helpers (docs/sentinel-sfx-v1/sentinel_sfx.py). Mono 44.1 kHz OGG Vorbis.

usage: python ore_sfx.py <code-branch assets/zerog_tweaks dir> [preview_dir]
"""
import importlib.util
import json
import os
import sys
import numpy as np
import soundfile as sf

_spec = importlib.util.spec_from_file_location('sentinel_sfx', os.path.join(os.path.dirname(__file__), '..', 'sentinel-sfx-v1', 'sentinel_sfx.py'))
S = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(S)
SR, time, tone, band, reverb, finish = S.SR, S.time, S.tone, S.band, S.reverb, S.finish
rng = np.random.default_rng(39)
BAR = [1.0, 2.76, 5.40, 8.93]                  # metal bar/plate partials (inharmonic, shorter than glass)


def grains(t, count, lo, hi, spread, size=.006):
    """Stone crunch: many tiny band-passed noise grains scattered over `spread` seconds."""
    out = np.zeros_like(t)
    for _ in range(count):
        s = int(rng.uniform(0, spread) ** 1.5 * SR)
        n = min(len(t) - s, int(size * 6 * SR))
        if n <= 0: continue
        g = band(rng.standard_normal(n), lo, hi) * np.exp(-np.arange(n) / SR / size) * rng.uniform(.4, 1)
        out[s:s + n] += g
    return out


def ring(t, f0, decay, partials):
    return sum(a * tone(t, f0 * r, rng.uniform(0, 6.28)) * np.exp(-t / (decay / r ** .6))
               for r, a in zip(partials, (1, .5, .3, .18, .1)))


def metal(kind, i):
    t = time({'break': .5, 'step': .22, 'hit': .2}[kind])
    f = (920, 1060, 1210, 990)[i] * (1.15 if kind == 'hit' else 1)
    crunch = grains(t, {'break': 70, 'step': 14, 'hit': 10}[kind], 300, 5000, {'break': .18, 'step': .05, 'hit': .03}[kind])
    tone_ = ring(t, f, {'break': .32, 'step': .09, 'hit': .08}[kind], BAR) * {'break': .5, 'step': .3, 'hit': .45}[kind]
    return reverb(crunch + tone_, .5, .15)


def gem(kind, i):
    t = time({'break': .55, 'step': .22, 'hit': .2}[kind])
    f = (1650, 1960, 2330, 1820)[i] * (1.1 if kind == 'hit' else 1)
    crunch = grains(t, {'break': 60, 'step': 12, 'hit': 9}[kind], 500, 7000, {'break': .16, 'step': .05, 'hit': .03}[kind])
    chime = ring(t, f, {'break': .45, 'step': .12, 'hit': .1}[kind], S.GLASS) * {'break': .45, 'step': .28, 'hit': .4}[kind]
    if kind == 'break':                                        # a couple of extra shards tinkling off
        for _ in range(3):
            s = int(rng.uniform(.04, .2) * SR)
            chime[s:] += .18 * ring(t[:len(t) - s], rng.uniform(2400, 3600), .12, S.GLASS)
    return reverb(crunch + chime, .6, .18)


def dust(kind, i):
    t = time({'break': .45, 'step': .2, 'hit': .16}[kind])
    crumble = grains(t, {'break': 140, 'step': 30, 'hit': 18}[kind], 150, 3200 + 300 * i,
                     {'break': .3, 'step': .1, 'hit': .05}[kind], size=.009)
    return reverb(crumble, .35, .1)


FAMILIES = {'metal': metal, 'gem': gem, 'dust': dust}
COUNTS = {'break': 3, 'step': 4, 'hit': 3}

if __name__ == '__main__':
    assets = sys.argv[1]; preview = sys.argv[2] if len(sys.argv) > 2 else None
    out_dir = os.path.join(assets, 'sounds', 'ore'); os.makedirs(out_dir, exist_ok=True)
    if preview: os.makedirs(preview, exist_ok=True)
    events = {}
    for fam, make in FAMILIES.items():
        for kind, n in COUNTS.items():
            names = []
            for i in range(n):
                name = f'{fam}_{kind}_{i + 1}'
                audio = finish(make(kind, i), peak={'break': .89, 'step': .5, 'hit': .6}[kind]).astype(np.float32)
                sf.write(os.path.join(out_dir, f'{name}.ogg'), audio, SR, format='OGG', subtype='VORBIS')
                if preview: sf.write(os.path.join(preview, f'{name}.wav'), audio, SR, subtype='PCM_16')
                names.append(f'zerog_tweaks:ore/{name}')
            events[f'ore.{fam}.{kind}'] = {'subtitle': f'subtitles.zerog_tweaks.ore.{kind}', 'sounds': names}
    path = os.path.join(assets, 'sounds.json')
    data = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else {}
    data.update(events)
    json.dump(data, open(path, 'w', encoding='utf-8', newline='\n'), indent=2)
    print(f'{sum(len(e["sounds"]) for e in events.values())} files, {len(events)} events')
