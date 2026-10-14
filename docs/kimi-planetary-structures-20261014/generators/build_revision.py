"""Original voxel revision candidates. Never writes runtime assets or saves."""
import argparse, collections, json, math
from pathlib import Path
from showcase_augment_lib import write_nbt

AIR = 'minecraft:air'

class Build:
    def __init__(self, n, h, depth, planet, stone, trim, core):
        self.n, self.h, self.d = n, h, depth
        self.planet, self.stone, self.trim, self.core = planet, stone, trim, core
        self.cells, self.tags = {}, {}
        self.rooms, self.loot = [], []
        self.towers = []
    def put(self, x, y, z, b):
        if 0 <= x < self.n and 0 <= y < self.h and 0 <= z < self.n:
            self.cells[x,y,z] = b
    def box(self, x0,y0,z0,x1,y1,z1,b):
        for x in range(x0,x1+1):
            for y in range(y0,y1+1):
                for z in range(z0,z1+1): self.put(x,y,z,b)
    def room(self,x0,y0,z0,x1,y1,z1):
        self.box(x0,y0,z0,x1,y1,z1,self.stone)
        self.box(x0+1,y0+1,z0+1,x1-1,y1-1,z1-1,AIR)
        self.rooms.append([x0+1,y0+1,z0+1,x1-1,y1-1,z1-1])
    def tunnel(self,x0,z0,x1,z1,y):
        steps=max(abs(x1-x0),abs(z1-z0),1)
        for i in range(steps+1):
            x=round(x0+(x1-x0)*i/steps);z=round(z0+(z1-z0)*i/steps)
            self.box(x-2,y-1,z-2,x+2,y+4,z+2,self.stone)
            self.box(x-1,y,z-1,x+1,y+3,z+1,AIR)
    def circle(self,cx,cz,y,r,width,b):
        for x in range(self.n):
            for z in range(self.n):
                if abs(math.hypot(x-cx,z-cz)-r)<=width: self.put(x,y,z,b)
    def tower(self,cx,cz,r,top):
        self.towers.append((cx,cz,r,top))
        # Hollow cylindrical tower, walkable spiral stair and overlook decks.
        for y in range(self.d,top):
            for x in range(cx-r,cx+r+1):
                for z in range(cz-r,cz+r+1):
                    dist=math.hypot(x-cx,z-cz)
                    if dist<=r:self.put(x,y,z,self.trim if dist>r-1.4 else AIR)
            self.circle(cx,cz,y,r,.8,self.trim)
        for y in range(self.d,top-4):
            a=(y-self.d)*math.pi/8
            x=round(cx+(r-2)*math.cos(a));z=round(cz+(r-2)*math.sin(a))
            self.box(x-1,y,z-1,x+1,y,z+1,self.stone)
            self.box(x-1,y+1,z-1,x+1,y+3,z+1,AIR)
        for y in range(self.d+7,top,8):self.circle(cx,cz,y,r+1,1.6,self.trim)
        for y in range(top-4,min(top+5,self.h)):
            rr=max(0,(top+4-y)//2)
            self.circle(cx,cz,y,rr,.7,self.trim)
        # Door toward front; ground-floor chamber joins the central route.
        self.box(cx-1,self.d+1,cz+r-1,cx+1,self.d+4,cz+r+1,AIR)
    def arch(self,cx,cz,r,y,b):
        for angle in range(181):
            a=math.radians(angle);x=round(cx+r*math.cos(a));yy=round(y+r*math.sin(a))
            self.box(x-1,yy-1,cz-1,x+1,yy+1,cz+1,b)
    def landscape(self):
        """Feather only exposed terrain cells; never carve rooms or routes."""
        c=self.n/2;d=self.d
        terrain={'zerog_tweaks:'+self.planet+'_soil','zerog_tweaks:'+self.planet+'_grass_block'}
        for p,block in list(self.cells.items()):
            x,y,z=p
            radius=math.hypot((x-c)*.92,(z-c)*1.05)
            edge=self.n*.47+1.7*math.sin(x*.31)+1.1*math.cos(z*.37)
            if block in terrain and radius>edge:
                # Unauthored outer cells leave existing native terrain intact.
                del self.cells[p]
            elif block in terrain and y==d and radius>edge-3:
                self.cells[p]='zerog_tweaks:'+self.planet+'_star_sand'
        rock={'cerulon':'cerulean_stone','skarn':'skarn_rock','eidolon':'permafrost'}[self.planet]
        # Uneven clusters, with separation from architecture and the entry path.
        for x,z,r in [(5,20,3),(self.n-6,24,3),(18,self.n-6,2),(self.n-12,5,2)]:
            for xx in range(x-r,x+r+1):
                for zz in range(z-r,z+r+1):
                    dist=math.hypot(xx-x,zz-z)
                    height=max(0,round((r-dist)*1.35))
                    if height and self.cells.get((xx,d,zz)) in terrain:
                        for yy in range(d+1,d+height+1):
                            if (xx,yy,zz) not in self.cells:self.put(xx,yy,zz,'zerog_tweaks:'+rock)
        for x in range(3,self.n-3):
            for z in range(3,self.n-3):
                ground=self.cells.get((x,d,z))
                if ground not in terrain or (x,d+1,z) in self.cells:continue
                # Sparse clustered native growth, not a uniform dotted grid.
                field=math.sin(x*.43)+math.cos(z*.39)+math.sin((x+z)*.21)
                if field>1.85 and (x*19+z*23)%7==0:
                    plant='glow_shrub' if (x+z)%3==0 else 'short_grass'
                    self.put(x,d+1,z,'zerog_tweaks:'+self.planet+'_'+plant)
    def gradients(self):
        """Coherent lower/mid/upper shades with grouped weathering patches."""
        palettes={
            'cerulon':(['polished_black_prismstone','cerulean_stone_bricks','prismstone'],
                       ['cracked_prismstone_bricks','chiseled_prismstone']),
            'skarn':(['skarn_rock','skarn_rock_bricks','oxide_crust'],
                     ['skarn_rock','skarn_rock_bricks']),
            'eidolon':(['polished_black_permafrost','frostrock_bricks','glacial_ice'],
                      ['cracked_permafrost_bricks','chiseled_permafrost'])}
        shades,weather=palettes[self.planet]
        architecture={self.stone,self.trim}
        for (x,y,z),block in list(self.cells.items()):
            if block not in architecture:continue
            height=(y-self.d)/max(1,self.h-self.d)
            patch=math.sin(x*.24)+math.cos(z*.27)+math.sin(y*.38)
            band=0 if height<.12 else 1 if height<.58 else 2
            material=shades[band]
            # Weathered patches remain grouped, sparing stair tread surfaces.
            exposed=any(self.cells.get((x+dx,y,z+dz),AIR)==AIR for dx,dz in [(1,0),(-1,0),(0,1),(0,-1)])
            if exposed and patch>2.25 and y>self.d+2:material=weather[0]
            if exposed and y%8==0 and patch<-.7:material=weather[1]
            self.cells[x,y,z]='zerog_tweaks:'+material
    def architecture(self):
        """Exterior-only details: preserve stairwell and basement interiors."""
        accent={'cerulon':'chiseled_prismstone','skarn':'oxide_crust',
                'eidolon':'chiseled_permafrost'}[self.planet]
        lamp={'cerulon':'coral_lantern','skarn':'fusion_lamp',
              'eidolon':'selenite_lamp'}[self.planet]
        accent='zerog_tweaks:'+accent;lamp='zerog_tweaks:'+lamp
        for cx,cz,r,top in self.towers:
            # Splayed footings and vertical ribs break up the circular cylinders.
            for dx,dz in [(-1,0),(1,0),(0,-1),(0,1)]:
                for y in range(self.d+1,top-5):
                    reach=r+2 if y<self.d+4 else r+1
                    x=cx+dx*reach;z=cz+dz*reach
                    self.put(x,y,z,accent)
                    if y<self.d+4:
                        self.put(x+dx,y,z+dz,self.stone)
                # Grouped narrow windows, not random holes in load-bearing walls.
                for y in range(self.d+5,top-7,8):
                    x=cx+dx*r;z=cz+dz*r
                    for yy in range(y,y+3):self.put(x,yy,z,AIR)
                    self.put(x,y-1,z,accent);self.put(x,y+3,z,accent)
                    self.put(x+dx,y-1,z+dz,lamp)
            # Clustered tapering pinnacles, with varied heights and setbacks.
            for j,(dx,dz) in enumerate([(-1,-1),(-1,1),(1,-1),(1,1)]):
                x=cx+dx*(r-1);z=cz+dz*(r-1)
                cap=min(self.h-1,top+2-j%3)
                for y in range(max(self.d+1,top-5),cap+1):
                    radius=1 if y<cap-2 else 0
                    self.box(x-radius,y,z-radius,x+radius,y,z+radius,self.trim)
        # Threshold markers and room lighting outside the walking centre line.
        c=self.n//2
        for dx in (-3,3):
            x=c+dx;z=self.entry[2]
            self.box(x,self.d+1,z,x,self.d+3,z,accent)
            self.put(x,self.d+4,z,lamp)
        for x,z in [(8,8),(self.n-9,8),(8,self.n-9),(self.n-9,self.n-9)]:
            self.put(x-3,5,z-3,lamp);self.put(x+3,5,z+3,lamp)
    def build_base(self):
        n,d=self.n,self.d;c=n//2
        # Thin authored terrain shelf; runtime foundation extends into terrain.
        self.box(0,d-2,0,n-1,d-1,n-1,'zerog_tweaks:'+self.planet+'_soil')
        self.box(0,d,0,n-1,d,n-1,'zerog_tweaks:'+self.planet+'_grass_block')
        self.room(c-7,1,c-7,c+7,8,c+7)
        for x,z in [(8,8),(n-9,8),(8,n-9),(n-9,n-9)]:
            self.room(x-4,1,z-4,x+4,7,z+4)
            self.tunnel(x,z,c,z,2);self.tunnel(c,z,c,c,2)
            p=(x,2,z);self.put(*p,'minecraft:chest')
            table={'cerulon':'water_bio_habitat','skarn':'hot_ring_monolith','eidolon':'ice_spire_outpost'}[self.planet]
            self.tags[p]={'LootTable':'zerog_tweaks:chests/'+table+'_supplies'}
            self.loot.append(p)
        # Straight 3-wide staircase from surface to central underground room.
        for i in range(d-1):
            z=c+2+i;y=2+i
            self.box(c-2,y-1,z-1,c+2,y+4,z+1,self.stone)
            self.box(c-1,y,z,c+1,y+3,z,AIR)
        self.box(c-2,d,c+d-1,c+2,d,c+d+2,self.stone)
        self.box(c-1,d+1,c+d-2,c+1,d+4,min(n-1,c+d+3),AIR)
        p=(c-4,2,c-4);self.put(*p,'minecraft:spawner')
        self.tags[p]={'mob':'minecraft:stray' if self.planet=='eidolon' else 'minecraft:husk' if self.planet=='skarn' else 'minecraft:spider'}
        self.box(c-1,2,c-1,c+1,3,c+1,self.core)
        self.entry=(c,d+1,min(n-2,c+d+1))
    def write(self,path,assets):
        for b in set(self.cells.values()):
            if b.startswith('zerog_tweaks:') and not (assets/(b.split(':')[1]+'.json')).exists():
                raise ValueError('Unregistered asset '+b)
        palette=[{'Name':v} for v in sorted(set(self.cells.values()))]
        idx={v['Name']:i for i,v in enumerate(palette)}
        blocks=[]
        for p,b in self.cells.items():
            v={'pos':list(p),'state':idx[b]}
            if p in self.tags:v['nbt']=self.tags[p]
            blocks.append(v)
        write_nbt(path,{'size':[self.n,self.h,self.n],'palette':palette,'blocks':blocks})
        return {'size':[self.n,self.h,self.n],'surface_y':self.d,'entry':self.entry,
                'non_air':sum(b!=AIR for b in self.cells.values()),'loot_positions':self.loot,
                'rooms':self.rooms,'status':'candidate; native collision, loot and visual review pending'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--blockstates',type=Path,required=True);a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=True);report={}
    specs=[('water_bio_habitat',48,52,16,'cerulon','cerulean_stone_bricks','prismstone','cerulite_block'),
           ('hot_ring_monolith',48,56,20,'skarn','skarn_rock_bricks','oxide_crust','emberite_block'),
           ('ice_spire_outpost',54,50,14,'eidolon','frostrock_bricks','glacial_ice','selenite_block')]
    for name,n,h,d,planet,stone,trim,core in specs:
        b=Build(n,h,d,planet,*['zerog_tweaks:'+v for v in (stone,trim,core)]);b.build_base();c=n//2
        if planet=='skarn':
            b.tower(c,c,7,h-5)
            for y,r in [(d+12,16),(d+23,18)]:
                for yy in (y,y+1):b.circle(c,c,yy,r,1.5,b.trim)
                for x in range(c-r,c+r+1):b.put(x,y,c,b.stone)
            for x,z in [(8,9),(n-9,9),(9,n-10)]:b.tower(x,z,4,d+14)
        elif planet=='cerulon':
            for x,z,r,t in [(15,16,7,h-5),(32,15,5,h-10),(12,32,4,h-14)]:b.tower(x,z,r,t)
            b.arch(32,31,12,d+1,b.trim)
            # Elevated walkway from main tower to habitat.
            for i in range(18):b.box(18+i,d+5+i//3,24,20+i,d+5+i//3,26,b.trim)
            b.room(28,d+1,29,43,d+9,42)
            b.box(32,d+2,41,35,d+5,43,AIR)
        else:
            b.room(15,d+1,15,39,d+11,35)
            b.box(25,d+2,34,28,d+6,36,AIR)
            b.arch(c,30,17,d+1,b.trim);b.arch(c,17,12,d+5,b.trim)
            for x,z,r,t in [(9,12,4,h-5),(19,10,4,h-1),(39,13,4,h-10),(45,38,3,h-15)]:b.tower(x,z,r,t)
        # Surface walking connection; restore underground stair clearance last.
        b.tunnel(c,c,c,min(n-3,c+d),d+1)
        # Restore tread/headroom after overlapping exterior and tunnel shells.
        for i in range(d-1):
            b.box(c-1,1+i,c+2+i,c+1,1+i,c+2+i,b.stone)
            b.box(c-1,2+i,c+2+i,c+1,5+i,c+2+i,AIR)
        b.box(c-1,2,c+1,c+1,5,c+2,AIR)
        b.box(c-1,1,c+1,c+1,1,c+2,b.stone)
        # Crossing tunnel shells must not seal the room doorway they meet.
        for x,z in [(8,8),(n-9,8),(8,n-9),(n-9,n-9)]:
            b.box(min(x,c)-1,1,z-1,max(x,c)+1,1,z+1,b.stone)
            b.box(min(x,c)-1,2,z-1,max(x,c)+1,5,z+1,AIR)
            b.box(c-1,1,min(z,c)-1,c+1,1,max(z,c)+1,b.stone)
            b.box(c-1,2,min(z,c)-1,c+1,5,max(z,c)+1,AIR)
        # Re-place functional loot after route carving through room centres.
        for p in b.loot:b.put(*p,'minecraft:chest')
        # Basement bypass keeps the southern rooms accessible beside the stair.
        for x0,z0,x1,z1 in [(c+4,c,c+4,n-9),(c,c,c+4,c),(c,n-9,c+4,n-9)]:
            b.box(x0-1,1,z0-1,x1+1,1,z1+1,b.stone)
            b.box(x0-1,2,z0-1,x1+1,5,z1+1,AIR)
        for i in range(d-1):
            b.box(c-1,1+i,c+2+i,c+1,1+i,c+2+i,b.stone)
            b.box(c-1,2+i,c+2+i,c+1,5+i,c+2+i,AIR)
        b.box(c-1,2,c+1,c+1,5,c+1,AIR)
        b.landscape();b.gradients();b.architecture()
        report[name]=b.write(a.output/(name+'.nbt'),a.blockstates)
    (a.output/'revision-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
