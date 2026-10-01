"""Generate a simple empty 16^3 GameTest scene, without third-party NBT tools."""
import gzip
import struct
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
def string(s):
    b=s.encode();return struct.pack('>H',len(b))+b
def named(kind,name,payload):return bytes([kind])+string(name)+payload
def integer(value):return struct.pack('>i',value)
def list_tag(kind,items):return bytes([kind])+integer(len(items))+b''.join(items)

def main():
    # One air palette entry is sufficient: an empty structure must still have
    # palette, blocks, entities and size for StructureTemplate's data loader.
    root=(named(3,'DataVersion',integer(3955))+
          named(9,'size',list_tag(3,[integer(16)]*3))+
          named(9,'palette',list_tag(10,[named(8,'Name',string('minecraft:air'))+b'\0']))+
          named(9,'blocks',list_tag(10,[]))+
          named(9,'entities',list_tag(10,[]))+b'\0')
    path=ROOT/'src/gametest/resources/data/zerog_tweaks/structure/tidewraith_empty.nbt'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(gzip.compress(b'\x0a\x00\x00'+root,mtime=0))

if __name__=='__main__':main()
