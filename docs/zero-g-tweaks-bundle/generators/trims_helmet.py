"""Trim patterns v2 - helmets. Hand-drawn 8x8 faces per pattern (top, front, side, back), drawn in the 8-step trim key
palette (0 light .. 7 dark). Only the helmet region of <pattern>.png (head UV 0,0-32,16) is replaced.
Rules: the face centre (rows 2-6, cols 2-5 of the front) stays clear so the visor and face read; every helmet gets a
feature on the top (the part you see most in third person); sides mirror; edges line up across faces.
Usage: python3 trims_helmet.py <in_trim_dir> <out_trim_dir>"""
import sys, os
from PIL import Image

KEY = [(236, 236, 236), (212, 212, 212), (188, 188, 188), (164, 164, 164), (140, 140, 140), (116, 116, 116), (92, 92, 92), (68, 68, 68)]
# top: row 0 = back edge, row 7 = front edge. side: drawn as the player's RIGHT side (col 7 = front edge), mirrored for the left.
# back: col 0 = player's left.
H = {
 'fracture': dict(  # a void crack runs from the brow over the crown and down the back
  top=['....3...', '...2....', '...1....', '....2...', '....1...', '...3....', '...2....', '....3...'],
  front=['....3...', '...2....', '...1....', '........', '........', '........', '........', '5......5'],
  side=['........', '........', '.....1..', '....3.2.', '...2....', '..3.....', '........', '555.....'],
  back=['...3....', '....2...', '....1...', '...2.3..', '..3...2.', '........', '........', '55555555']),
 'crater': dict(  # an impact ring on the crown, a dented brow band, small craters on the sides and back
  top=['........', '..3223..', '.3.55.3.', '.2.5..2.', '.2....2.', '.3....3.', '..3223..', '........'],
  front=['55555555', '5......5', '2......2', '........', '........', '3......3', '2......2', '........'],
  side=['55555555', '........', '..232...', '.2.5.2..', '..232...', '........', '........', '........'],
  back=['55555555', '........', '...232..', '..2.5.2.', '...232..', '........', '.32.....', '........']),
 'olympus': dict(  # a mountain ridge crest from brow to nape, peaks on the back, a range along the sides
  top=['...12...', '...12...', '...12...', '...12...', '...12...', '...12...', '...12...', '...12...'],
  front=['...12...', '..2..3..', '.2....3.', '........', '........', '........', '........', '66666666'],
  side=['........', '........', '........', '........', '....2...', '...2.3.2', '..2...3.', '66666666'],
  back=['...12...', '..2..3..', '.2....3.', '2..12..3', '..2..3..', '.2....3.', '........', '66666666']),
 'geode': dict(  # a cut gem on the brow, a faceted diamond on the crown, small facets on the sides
  top=['...11...', '..2..2..', '.2.00.2.', '.2.00.2.', '..2..2..', '...11...', '........', '........'],
  front=['...00...', '..1..1..', '...22...', '........', '........', '........', '........', '5......5'],
  side=['........', '........', '...1....', '..2.2...', '...2....', '........', '........', '........'],
  back=['........', '...11...', '..2..2..', '.2.00.2.', '..2..2..', '...11...', '........', '55555555']),
 'rift': dict(  # three claw tears across the crown and sides, a torn corner on the brow
  top=['........', '.2......', '..2..2..', '...2..2.', '....3..2', '.....3..', '......3.', '........'],
  front=['2.......', '.3......', '........', '........', '........', '........', '........', '55555555'],
  side=['2..2..2.', '.2..2..2', '..3..3..', '...3..3.', '........', '........', '........', '55555555'],
  back=['.2..2...', '..2..2..', '...3..3.', '....3..3', '........', '........', '........', '55555555']),
 'hull': dict(  # a riveted band round the head and a welded seam over the crown
  top=['...55...', '...11...', '...55...', '........', '...55...', '...11...', '...55...', '........'],
  front=['55555555', '1......1', '........', '........', '........', '........', '1......1', '55555555'],
  side=['55555555', '1..1..1.', '........', '....5...', '....5...', '........', '1..1..1.', '55555555'],
  back=['55555555', '1..11..1', '........', '...55...', '...55...', '........', '1..11..1', '55555555']),
 'corona': dict(  # a sun on the crown with rays falling down every side, a sunburst on the brow
  top=['2......2', '.2....2.', '...11...', '..1001..', '..1001..', '...11...', '.2....2.', '2......2'],
  front=['..2112..', '.2.00.2.', '2..11..2', '........', '........', '........', '........', '3......3'],
  side=['2...2...', '2...2...', '3.......', '........', '........', '........', '........', '........'],
  back=['2.2..2.2', '.2.11.2.', '...33...', '........', '........', '........', '........', '33333333']),
 'surge': dict(  # a wave band round the lower helmet and a wave crest over the crown
  top=['..2.....', '...2....', '....2...', '...2....', '..2.....', '...2....', '....2...', '...2....'],
  front=['........', '........', '........', '........', '........', '2..22..2', '.22..22.', '55555555'],
  side=['........', '........', '........', '........', '........', '2..22..2', '.22..22.', '55555555'],
  back=['........', '........', '........', '...2....', '..2.2...', '2..22..2', '.22..22.', '55555555']),
 'prism': dict(  # a triangle crest on the forehead pointing up, a prism arrow on the crown, stacked prisms on the back
  top=['........', '.222222.', '..2..2..', '..2..2..', '...22...', '...11...', '...00...', '........'],
  front=['...11...', '..2..2..', '.222222.', '........', '........', '........', '........', '5......5'],
  side=['........', '........', '...2....', '..2.2...', '.22222..', '........', '........', '........'],
  back=['........', '...11...', '..2..2..', '.222222.', '...11...', '..2..2..', '.222222.', '55555555']),
 'meteor': dict(  # a meteor streaks over the crown and burns in over the brow
  top=['5.......', '.5......', '..3.....', '...3....', '....2...', '.....1..', '......00', '......00'],
  front=['......00', '.....11.', '....2...', '...3....', '........', '........', '........', '5......5'],
  side=['........', '..5.3...', '...3.2..', '........', '........', '........', '........', '........'],
  back=['5.......', '.5......', '..3.....', '........', '........', '........', '........', '55555555']),
}
FACES = {'top': (8, 0), 'right': (0, 8), 'front': (8, 8), 'left': (16, 8), 'back': (24, 8)}

def check(pid, g):
    for k, rows in g.items():
        assert len(rows) == 8 and all(len(r) == 8 for r in rows), (pid, k, [len(r) for r in rows])

def paint(im, pid):
    g = H[pid]; check(pid, g); p = im.load()
    for x in range(32):                       # clear the old helmet region (top + 4 sides)
        for y in range(16):
            if (8 <= x < 24 and y < 8) or y >= 8: p[x, y] = (0, 0, 0, 0)
    def put(face, rows, mirror=False):
        ox, oy = FACES[face]
        for y, r in enumerate(rows):
            for x, ch in enumerate(r):
                if ch != '.':
                    xx = 7 - x if mirror else x
                    p[ox + xx, oy + y] = KEY[int(ch)] + (255,)
    put('top', g['top']); put('front', g['front']); put('back', g['back'])
    put('right', g['side']); put('left', g['side'], mirror=True)
    return im

if __name__ == '__main__':
    src, dst = sys.argv[1:3]; os.makedirs(dst, exist_ok=True)
    for pid in H:
        im = Image.open(f'{src}/{pid}.png').convert('RGBA')
        paint(im, pid).save(f'{dst}/{pid}.png')
    print('helmets redrawn:', len(H))
