import os, zipfile
from PIL import Image
from gear2 import PIECES, shade
from gear_sets import S, HAND
from data import M
OUT='out/assets/zerog_tweaks/textures/item'
ICONS={}
for i,(k,cfg) in enumerate(S.items()):
    pal=M[k]['pal']
    for piece,fn in PIECES.items():
        L=fn(cfg[piece]); im=shade(L,pal,HAND[cfg['hand']],cfg['acc'],cfg['motif'],seed=i*31+len(piece))
        ICONS[(k,piece)]=im; im.save(f'{OUT}/{k}_{piece}.png')
import pickle; pickle.dump({f'{a}|{b}':v.tobytes() for (a,b),v in ICONS.items()},open('icons.pkl','wb'))
# preview grid
W=Image.new('RGBA',(9*20*4,20*20*4),(245,245,245,255))
for r,k in enumerate(S):
    for c,p in enumerate(PIECES):
        W.alpha_composite(ICONS[(k,p)].resize((64,64),Image.NEAREST),(c*80+8,r*80+8))
W.save('/tmp/claude-0/gear_preview.png')
