"""Tidewraith geometry from the installed Minecraft 1.21.1 PhantomModel.

Eight vanilla cuboids and their hinge chain; Y-down Java coordinates are
converted to Blockbench Y-up. The vanilla half-pixel X offset is recentered
for bilateral symmetry. Only original painted scales and paired gill decals
are added. No vanilla texture or game jar is redistributed.
"""
import math

def geometry(palette):
    boxes=[]
    def add(name,bone,lo,hi,color,texture='scales'):
        boxes.append(dict(name=name,bone=bone,**{'from':lo,'to':hi},color=color,texture=texture))
    add('body','body',[-2.5,23,-8],[2.5,26,1],'skin')
    add('head','head',[-3.5,22,-12],[3.5,25,-7],'skin_dark')
    add('tail','tail',[-1.5,24,1],[1.5,26,7],'skin_dark')
    add('tail tip','tail_tip',[-.5,24.5,7],[.5,25.5,13],'skin_dark')
    for s,label in ((-1,'l'),(1,'r')):
        lo,hi=sorted((s*2.5,s*8.5))
        add('wing '+label,'wing_'+label,[lo,24,-8],[hi,26,1],'skin')
        lo,hi=sorted((s*8.5,s*21.5))
        add('wing '+label+' outer','wing_'+label+'_outer',[lo,25,-8],[hi,26,1],'skin')
        # Four paired short manta gill slits on the underside, as planes.
        for n in range(4):
            x0,x1=sorted((s*.65,s*2.15))
            add('manta gill fin '+label+str(n),'body',[x0,22.965,-6+n*1.25],[x1,22.965,-5.8+n*1.25],'mouth','noise')
    add('pale belly fin plane','body',[-2.5,22.985,-8],[2.5,22.985,1],'belly','scales')
    add('mouth fin plane','head',[-2,21.965,-11],[2,21.965,-10.75],'mouth','noise')
    pivots={'body':[0,24,0],'head':[0,23,-7],'tail':[0,26,1],'tail_tip':[0,25.5,7],
            'wing_l':[-2.5,26,-8],'wing_r':[2.5,26,-8],
            'wing_l_outer':[-8.5,26,-8],'wing_r_outer':[8.5,26,-8]}
    rotations={'body':[math.degrees(.1),0,0],'head':[math.degrees(-.2),0,0]}
    return boxes,pivots,rotations
