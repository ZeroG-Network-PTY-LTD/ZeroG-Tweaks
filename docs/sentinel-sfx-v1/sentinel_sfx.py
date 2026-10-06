"""Prism Sentinel sound set (v1): procedural, seeded, re-runnable.

The Sentinel is a Concord crystal construct that fights in light-refracting phases (design doc, The Quiet Mines), so
every sound is glassy and resonant: inharmonic glass-bell partials, filtered-noise cracks, pitch sweeps and a short
crystal-hall reverb. Output is mono 44.1 kHz (Minecraft plays positional sounds in mono only).

usage: python sentinel_sfx.py <code-branch assets/zerog_tweaks dir> [preview_dir]
  writes <assets>/sounds/sentinel/<name>.ogg (OGG Vorbis), merges the sentinel.* events into <assets>/sounds.json,
  and optionally writes 16-bit WAV previews. Needs numpy and soundfile (libsndfile with Vorbis).
"""
import json
import os
import sys
import numpy as np
import soundfile as sf

SR = 44100
rng = np.random.default_rng(2026_10_06)
GLASS = [1.0, 2.32, 4.25, 6.63, 9.38]          # struck-glass partial ratios (inharmonic, bell-like)
GLASS_AMP = [1.0, .55, .35, .22, .12]


def time(seconds): return np.arange(int(seconds * SR)) / SR


def env(t, attack=.005, decay=.5, sustain=0.0, release=None):
    """Exponential AR/ADSR-ish envelope over t."""
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    d = sustain + (1 - sustain) * np.exp(-np.maximum(t - attack, 0) / max(decay, 1e-4))
    e = a * d
    if release:
        e *= np.clip((t[-1] - t) / release, 0, 1)
    return e


def tone(t, freq, phase=0.0):
    """Sine whose frequency may be an array (pitch sweep) -- integrates phase."""
    f = np.broadcast_to(freq, t.shape).astype(float)
    return np.sin(2 * np.pi * np.cumsum(f) / SR + phase)


def glass(t, f0, decay=.6, bright=1.0, detune=.003):
    """Struck crystal: inharmonic partials, higher ones decaying faster, slight detune shimmer."""
    out = np.zeros_like(t)
    for r, a in zip(GLASS, GLASS_AMP):
        for d in (-detune, detune):
            out += a * bright ** (r > 1) * tone(t, f0 * r * (1 + d), rng.uniform(0, 6.28)) * np.exp(-t / (decay / r ** .55))
    return out / 2


def noise(n): return rng.standard_normal(n)


def band(x, lo, hi):
    """Band-pass via FFT with soft edges."""
    spec = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    mask = 1 / (1 + (lo / np.maximum(f, 1)) ** 4) / (1 + (f / hi) ** 4)
    return np.fft.irfft(spec * mask, len(x))


def crack(t, lo=1500, hi=9000, length=.02):
    """Sharp crystal crack: a very short band-passed noise burst."""
    return band(noise(len(t)), lo, hi) * np.exp(-t / length)


def reverb(x, size=1.1, mix=.3):
    """Crystal-hall reverb: convolve with band-passed, exponentially decaying noise."""
    n = int(size * SR); tt = np.arange(n) / SR
    ir = band(noise(n), 200, 7000) * np.exp(-tt / (size / 5)); ir /= np.sqrt(np.sum(ir ** 2))
    m = len(x) + n
    wet = np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)
    dry = np.concatenate([x, np.zeros(n)])
    return (1 - mix) * dry + mix * wet


def finish(x, peak=.89, fade=.01):
    """Normalise to about -1 dBFS and fade the edges so nothing clicks."""
    x = x - np.mean(x)
    f = int(fade * SR); w = np.ones_like(x); w[:f] = np.linspace(0, 1, f); w[-f:] = np.linspace(1, 0, f)
    x = x * w
    return x / (np.max(np.abs(x)) + 1e-9) * peak


# ------------------------------------------------------------------------------------------------ sounds
def ambient(f0):
    """Low crystalline hum with a slowly drifting high shimmer."""
    t = time(3.2)
    hum = sum(a * tone(t, f0 * h * (1 + .002 * np.sin(2 * np.pi * .3 * t + h))) for h, a in ((1, 1), (2, .45), (3, .25), (5, .12)))
    shimmer = sum(.08 * tone(t, f0 * r) * (.5 + .5 * np.sin(2 * np.pi * rng.uniform(.4, 1.2) * t + rng.uniform(0, 6)))
                  for r in (8, 9.38, 11.2, 12.6))
    return reverb((hum + shimmer) * env(t, attack=.6, decay=99, sustain=1, release=1.0), 1.4, .35)


def hurt(f0):
    """Glass-bell impact with a crack and a slight downward bend."""
    t = time(.7)
    bend = f0 * (1 - .04 * (1 - np.exp(-t / .08)))
    out = crack(t) * .9 + sum(a * tone(t, bend * r) * np.exp(-t / (.35 / r ** .5)) for r, a in zip(GLASS, GLASS_AMP))
    return reverb(out, .8, .25)


def death():
    """Shatter cascade (a burst of splinter pings), then a descending resonant chord that fades: it accepts you."""
    t = time(4.5); out = np.zeros_like(t)
    for _ in range(26):                                      # shatter: 26 shards over ~1.1 s
        s = int(rng.uniform(0, 1.1) ** 1.6 * SR); n = len(t) - s
        out[s:] += .35 * (glass(t[:n], rng.uniform(900, 3200), decay=rng.uniform(.15, .4)) + crack(t[:n]) * .6)
    chord_t = t - .5; on = chord_t > 0
    slide = np.where(on, np.exp(-np.maximum(chord_t, 0) / 2.2), 1)        # glide down about an octave
    for f in (329.6, 415.3, 493.9, 659.3):                    # E major: the test is passed
        out += on * .45 * tone(t, f * (.5 + .5 * slide)) * np.exp(-np.maximum(chord_t, 0) / 1.6) * np.clip(chord_t / .4, 0, 1)
    return reverb(out, 1.8, .45)


def core(opening):
    """Resonant sweep: rising when the core opens, falling when it seals."""
    t = time(1.1)
    sweep = 180 * (4 ** (t / t[-1])) if opening else 720 * (4 ** (-t / t[-1]))
    body = sum(a * tone(t, sweep * h) for h, a in ((1, 1), (2, .4), (3, .2), (4.25, .15)))
    air = band(noise(len(t)), 600, 6000) * .25
    shape = env(t, attack=.25 if opening else .02, decay=.45 if opening else .3, sustain=.15 if opening else 0, release=.2)
    return reverb((body + air) * shape, 1.0, .3)


def phase_change():
    """Deep crack and thump, then a minor chord swelling in: the construct changes refraction."""
    t = time(2.4)
    thump = tone(t, 55 * (1 + np.exp(-t / .05))) * np.exp(-t / .35)
    cracks = crack(t, 400, 6000, .06) * 1.2
    swell = sum(.35 * tone(t, f) for f in (220, 261.6, 329.6, 440)) * np.clip((t - .25) / .8, 0, 1) * np.exp(-np.maximum(t - 1.05, 0) / .6)
    shimmer = .4 * glass(t, 1320, decay=1.2)
    return reverb(thump + cracks + swell + shimmer * np.clip((t - .2) * 4, 0, 1), 1.6, .4)


def shard_hit():
    """Sharp crystal splinter striking a player."""
    t = time(.45)
    return reverb(crack(t, 2500, 12000, .012) * 1.3 + glass(t, 1850, decay=.18, detune=.006), .6, .2)


def refract():
    """Refract-teleport: a reversed shimmer swelling into a whoosh."""
    t = time(1.0)
    cluster = sum(glass(t, f, decay=.35) for f in (880, 1175, 1568))
    rev = cluster[::-1] * np.clip(t / .05, 0, 1)
    whoosh = band(noise(len(t)), 300, 5000) * np.sin(np.pi * t / t[-1]) ** 2 * .6
    return reverb(rev + whoosh, .9, .3)


def beam_charge():
    """Rising prismatic whine with quickening tremolo: the beam is coming."""
    t = time(1.05)
    f = 260 * (5 ** (t / t[-1]))
    trem = .65 + .35 * np.sin(2 * np.pi * np.cumsum(4 + 22 * t / t[-1]) / SR)
    body = sum(a * tone(t, f * h) for h, a in ((1, 1), (2, .5), (3, .3), (6.63, .15)))
    return reverb(body * trem * env(t, attack=.3, decay=99, sustain=1, release=.04), .7, .25)


def beam_fire():
    """Bright refracting zap: fast falling FM sweep over a noise burst and a crystal ring."""
    t = time(.75)
    f = 400 + 2200 * np.exp(-t / .07)
    mod = 1 + .5 * tone(t, f * 1.5)
    zap = tone(t, f * mod) * np.exp(-t / .2)
    return reverb(zap + crack(t, 1000, 10000, .03) * .8 + .5 * glass(t, 990, decay=.4), .8, .25)


def beam_deflect():
    """The beam hits a refracting block: a clear, ringing ping."""
    t = time(.9)
    return reverb(glass(t, 1320, decay=.7, detune=.002) + crack(t, 3000, 12000, .008) * .5, 1.2, .35)


SOUNDS = {
    'ambient_1': lambda: ambient(98), 'ambient_2': lambda: ambient(110), 'ambient_3': lambda: ambient(123.5),
    'hurt_1': lambda: hurt(620), 'hurt_2': lambda: hurt(700), 'hurt_3': lambda: hurt(560),
    'death': death, 'core_open': lambda: core(True), 'core_close': lambda: core(False), 'phase': phase_change,
    'shard_hit': shard_hit, 'refract': refract, 'beam_charge': beam_charge, 'beam_fire': beam_fire,
    'beam_deflect': beam_deflect,
}
# sounds.json events (zerog_tweaks:sentinel.<event>) -> files
EVENTS = {'ambient': ['ambient_1', 'ambient_2', 'ambient_3'], 'hurt': ['hurt_1', 'hurt_2', 'hurt_3'], 'death': ['death'],
          'core_open': ['core_open'], 'core_close': ['core_close'], 'phase': ['phase'], 'shard_hit': ['shard_hit'],
          'refract': ['refract'], 'beam_charge': ['beam_charge'], 'beam_fire': ['beam_fire'], 'beam_deflect': ['beam_deflect']}

if __name__ == '__main__':
    assets = sys.argv[1]; preview = sys.argv[2] if len(sys.argv) > 2 else None
    out_dir = os.path.join(assets, 'sounds', 'sentinel'); os.makedirs(out_dir, exist_ok=True)
    if preview: os.makedirs(preview, exist_ok=True)
    for name, make in SOUNDS.items():
        audio = finish(make()).astype(np.float32)
        sf.write(os.path.join(out_dir, f'{name}.ogg'), audio, SR, format='OGG', subtype='VORBIS')
        if preview: sf.write(os.path.join(preview, f'{name}.wav'), audio, SR, subtype='PCM_16')
        print(f'{name:13} {len(audio) / SR:4.2f} s')
    path = os.path.join(assets, 'sounds.json')
    data = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else {}
    for event, files in EVENTS.items():
        data[f'sentinel.{event}'] = {'subtitle': f'subtitles.zerog_tweaks.sentinel.{event}',
                                     'sounds': [f'zerog_tweaks:sentinel/{f}' for f in files]}
    json.dump(data, open(path, 'w', encoding='utf-8', newline='\n'), indent=2)
    print(f'{len(EVENTS)} events in sounds.json')
