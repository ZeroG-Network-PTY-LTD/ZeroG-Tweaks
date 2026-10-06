"""Mechanically reconcile the shared tracker snapshot with the verified repair batch."""
import argparse,json,re
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--commit',required=True);a=p.parse_args()
root=Path(__file__).resolve().parent.parent
html=root/'shared-systems-tracker.html';md=root/'shared-systems-tracker.md'
content=html.read_text(encoding='utf-8')
match=re.search(r'let tasks = (\[.*?\]), area =',content,re.S);assert match
tasks=json.loads(match.group(1))
details={
 'b01-ore-drops':'39 BlockInit ore registrations and Cerulite Cluster require correct tools. Survival wrong/right-pick eligibility and all tier-tagged blocks passed.',
 'b03-ore-refinery':'Powered shared processing terminal,79 recipes, bounded casing upgrades, upgraded output reservation and safe legacy inventory migration. Raw blocks yield18/27 ingots with proportionate FE. Paid jobs survive reload.',
 'h01-transport-cap':'Loaded networks traverse beyond256 nodes with one leader/budget.257-node transfer conservation passed; no remote chunk loading.',
 'h02-transport-routing':'Route changes propagate from any connected loaded terminal. Nearest uses port priority then breadth-first distance from buffered source. Disabled-face alternate paths remain reachable.',
 'h04-transport-fluids':'Every connected pipe must meet hazardous-fluid tier. Simulation/fill and buffered delivery reject unsafe mixed networks without deleting contents.',
 'h05-jelly-tank':'Royal/Cosmic source,flowing,blocks and collectable buckets registered. Actual bucket-to-splicer interaction passes. Four addon items per1000mB preserves250mB job dose; dedicated art/standalone synthesis pending.'
}
for task in tasks:
 if task['id'] in details:
  task['done']=True;task['detail']=details[task['id']];task['evidence']='1.21.x '+a.commit+'; 73 addon-present tests and11 overlapping addon-absent tests; Docs/blocker-repairs-2026-10-06.md'
 elif 'research gating' in task['title'].lower():
  task['detail']='Approved mechanism: Concord Codex advancements. Per-trait unlock mapping/caps and implementation remain pending; AGENTS no longer claims research gating exists.'
content=content[:match.start(1)]+json.dumps(tasks,ensure_ascii=False)+content[match.end(1):]
html.write_text(content,encoding='utf-8')
text=md.read_text(encoding='utf-8')
oldtasks={t['id']:t for t in tasks}
for key in details:
 text=text.replace('- [ ] **'+oldtasks[key]['title']+'**','- [x] **'+oldtasks[key]['title']+'**')
text=text.replace('**33 open, 13 done.**','**27 open, 19 done.**')
text=text.replace('Three things block survival play: ores drop for any tool so the mining ladder isn\'t enforced, the bee machines and consumables have no recipes in ZeroG Tweaks, and the Ore Refinery still runs a 5-item hardcoded table.',
 'The six repaired items below are now server-verified. Bee-machine/consumable survival recipes remain a blocker.')
text=text.replace('`1.21.x` at `15200c39`','`1.21.x` at `'+a.commit+'`')
heading='## Verified repair update — 6 October 2026\n\n'
if heading not in text:
 section=heading+'73 addon-present tests passed;11 overlapping blocker tests also passed without addons. Detailed historical audit descriptions below explain the original defects; the checked status and this update supersede them.\n\n'
 section+='\n'.join('- '+v for v in details.values())+'\n\nConcord Codex advancements are the approved research mechanism, but research gates are not implemented. Dedicated jelly artwork, standalone synthesis, client approval and the remaining queue stay pending.\n\n'
 text=text.replace('## Open: Blockers',section+'## Open: Blockers',1)
md.write_text(text,encoding='utf-8')
print('Reconciled6verified repairs; retained all other tracker entries and historical evidence.')
