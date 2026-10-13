"""Export the owner-approved native64 Codex; no concept-image resampling.
Usage: python generate.py <runtime assets/zerog_tweaks directory>
"""
from pathlib import Path
import runpy,shutil,sys
HERE=Path(__file__).resolve().parent
runpy.run_path(str(HERE/'generate_hd.py'),run_name='__main__')
assets=Path(sys.argv[1])
for folder in (HERE/'source',assets):
    for rel in ('textures/item/concord_codex.png','models/item/concord_codex.json'):
        target=folder/rel;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(HERE/'hd64'/rel,target)
shutil.copyfile(HERE/'hd64/manifest.json',HERE/'manifest.json')
print('Approved native64 PNG/model exported; same item ID and book functionality.')
