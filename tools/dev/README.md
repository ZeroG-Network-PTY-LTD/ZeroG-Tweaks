# Dev machine tools

Everything needed to work on ZeroG-Tweaks from any Windows PC, plus the helper scripts used for world generation and
the Concord Vault.

## New PC setup (one command)

Open PowerShell on the new PC and run:

```powershell
iwr https://raw.githubusercontent.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/1.21.x/tools/dev/setup-main-pc.ps1 -OutFile $env:TEMP\zg-setup.ps1; powershell -ExecutionPolicy Bypass -File $env:TEMP\zg-setup.ps1 -Design
```

The script first lists anything missing (Git, GitHub CLI, Python, Java 21) with the `winget` command to install it;
install those, open a new PowerShell window and run the line again. It then:

- sets the commit name for ZeroG repos to **MrWhiteFlamesYT** `<popmaster124@gmail.com>`; other repos are unchanged
- signs the GitHub CLI in as **ZeroG-Network** (a browser window opens the first time), makes it the active account and
  lets git push with it
- clones `1.21.x` to `%USERPROFILE%\Desktop\claude\ZeroG-Tweaks` (change with `-Path`), and with `-Design` the Design
  branch next to it as `ZeroG-Tweaks-Design`
- installs the Python package `nbtlib`
- prepares `run-server\` with RCON on and a random password (git ignores this folder), and asks you about the
  Minecraft EULA

Run it again any time: it skips what is already done and pulls the latest `1.21.x`.

## Working rules

- `1.21.x` holds all code, `Design` the design files, `Docs` the docs and jars; `Released` is the major release and is
  not touched.
- Before committing: `git fetch --all`, bring in what others pushed (`git pull --rebase`), then commit and push.
- Check `gh auth status` shows **ZeroG-Network** as the active account before pushing; it can switch back to another
  account by itself (`gh auth switch --user ZeroG-Network`).

## Everyday commands

| What | Command |
|---|---|
| Play / test in the client | `.\gradlew.bat runClient` |
| Dev server | `.\gradlew.bat runServer` |
| Game tests | `.\gradlew.bat runZeroGTests -PzeroGTests -PtidewraithTests` |
| Server command from outside | `python tools\dev\rcon.py "list"` |

## Scripts

| Script | What it does |
|---|---|
| `setup-main-pc.ps1` | The new-PC setup above. |
| `rcon.py` | Sends commands to the running dev server (`--file` runs a list of commands). |
| `worldscan.py` | Counts every block in an area of a saved dev-server world, read straight from the region files, and marks vanilla blocks. |
| `vault_world_check.py` | Finds the Concord Vault in the running dev-server world and reports rooms, Key Altars placed and how far apart the keys are. |
| `check_rooms.py` | Checks the 10 vault room templates against the vault brief: size, doors, free centre for the altar, allowed blocks, chest loot tables. Needs one Gradle build first. |
| `concord_vault/build_concord_vault.py` | Rebuilds the vault templates (chamber, the three key stages, corridors, entrance, placeholder rooms) into `build\concord_vault_out\`. Copy only what you changed into `src\main\resources\data\zerog_tweaks\structure\concord_vault\`: the rooms in the mod are the designed ones from the Design branch. |
| `concord_vault/build_prism_arena_v3.py` | The arena layout the vault chamber is built from (used by the vault builder). |

Scanning a planet for what generated (dev server running):

```powershell
python tools\dev\rcon.py "execute in zerog_tweaks:cerulon run forceload add -64 -64 63 63"
python tools\dev\rcon.py "save-all flush"
python tools\dev\worldscan.py world zerog_tweaks:cerulon 0 0 4
```
