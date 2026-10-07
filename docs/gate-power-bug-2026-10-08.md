# Gate power transfer — reported regression, pending reproduction

Owner reports that combustion generator → energy conduits → controller and
combustion generator → conduits → formed Gate Energy Port both fail in game.
Do not dismiss this as an incorrect player connection. Prior assistant advice
that only ports should accept power was not supported by current code.

## Confirmed source boundary

`SurvivalGates.capabilities` registers EnergyStorage on the controller block
entity only. `portEnergy` resolves a formed gate's energy port but has no
production capability registration/caller found in this focused review.
Conduit adjacency/transfer uses `level.getCapability(EnergyStorage.BLOCK,...)`.
The earlier gate regression calls `portEnergy` directly; it does not test a
conduit's actual capability access to that block. Missing port registration is
therefore confirmed source evidence, not a complete diagnosis of both failures.
Controller input exists and rejects incomplete structures. Hub admin gates and
their display/ledger also need separate checks; no cause is invented for them.

## Next reproduction and acceptance

1. Add an isolated public-capability regression: real combustion generator,
   burning supported fuel, enabled output face, real energy conduits and formed
   tier1 gate. Assert actual generated FE reaches the controller storage.
2. Repeat using the actual Gate Energy Port capability, not direct `portEnergy`.
   Record generator/cable/gate stores and conserved successful transfer.
3. Cover all gate facings and representative higher tiers; unformed/unbound ports
   reject FE. Break/reform/move parts: stale connections must not keep routing.
4. Check the admin hub separately: full/free gates need not accept additional FE;
   test connection and displayed backend state without removing admin semantics.
5. Capture failing evidence before runtime repair; test generator output settings,
   network direction/cache and gate formation independently. Rerun original loop.
6. Clean same-version build, asset checks and backed-up installation only after
   passing tests; publish code and Docs separately. Preserve hub/player saves.

## Current delivery and limits

No runtime fix, new JAR or isolated launch in this inspection-only turn.
Installed Prism Spire build remains SHA256
`3fe1deb13ca89bd3bb2e1ed1107cfe612a2a44a537f10959ce375f393be4450f`.
Code/Design/Docs were fetched first. At94% primary usage, the owner's10%-remaining
light-work rule applies: save this handoff and prioritize the repair next window.
No claim of reproduced/verified fixed gameplay is made.
