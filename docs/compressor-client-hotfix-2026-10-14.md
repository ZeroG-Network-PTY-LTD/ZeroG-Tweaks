# Industrial Compressor client repair

The owner's client screenshot showed striped white chassis corners and rejected
press dies/recipe inputs. A native model regression reproduced overlapping
same-facing planes between silver corner trim and the dark backing, and between
the terminal and its backing. The Design geometry generator now separates those
planes by 0.02 model units. The source regression fails on the prior model and
passes on the corrected generated model. This is geometry evidence, not a GPU
appearance test.

The compressor input/die menu slots now permit client insertion clicks to reach
the server even when the client's recipe view cannot validate a custom recipe.
Server inventory validation is unchanged and rejects invalid ingredients/dies;
output/upgrade slots are not made permissive. The exact cause of the owner's
input failure remains subject to an installed-client retest. A real-menu
shift-click regression covers reusable Plate Press routing, two copper ingots
and rejection of cobblestone as a die, alongside the existing pressing tests.

Use upper-left input for ingots and lower-left die for Plate Press/Cog Press.
Plate Press: two ingots → one compressed plate. Cog Press: four ingots → one
cog. Presses are reusable. The compressor needs FE; the front is not an
automation port. Other five faces retain item/FE controls.

All 21 required isolated owner-followup GameTests passed, including the new real
menu shift-click case, pressing outputs, die preservation and five-face routing.
The disposable server shut down normally. The chassis plane regression also
passed. Saves and already placed machines do not need regeneration. Manual
client insertion and visual appearance remain explicitly awaiting owner retest.

Same-version normal build passed, optional test classes excluded, and installed
in ZeroG/mods while the client was closed. Previous JAR archived under
`zerog-mod-backups/20261014-004700-UTC`; other mods and saves untouched.
Archived JAR: `jars/zerog-tweaks-1.21.1-1.0.12-dev-compressor-hotfix-20261014.jar`.
SHA256: `90f8262c837767c6f67b38cd434f7aab2e05bc982855778021d240821ba75ab2`.
