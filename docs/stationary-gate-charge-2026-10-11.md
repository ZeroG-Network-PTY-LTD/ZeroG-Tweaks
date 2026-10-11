# Stationary gate charging

The owner's 11 October update removes physical levitation from the gate countdown. Passengers stay on the ordinary landing pad while the gate charges.

## Changed

- No gate-applied Levitation effect and no charge-time camera FOV stretch.
- Counter-rotating end-rod and violet light rings around the pad during the final charging stage.
- Animated cyan/violet on-screen reticle, followed by the existing white-out and dimensional transition.
- Cancellation and teleportation no longer remove Levitation supplied by unrelated effects.
- Ordinary pad bounds apply throughout charging. Actual departure or a changed passenger group still cancels travel.

The countdown, destination permissions, readiness checks, successful-jump FE charges, powered pillar lights and destination landing clearance are unchanged. No hub, save, dimension, weather or recipe changes are included. The legacy `gate_lift` packet name remains for compatibility, but now represents visual charging only.

## Review in game

1. Charge a complete gate and select a permitted destination.
2. Stand on its central pad, Engage and confirm Ready for any additional passengers.
3. Remain still: your feet should stay on the pad while the final light rings rotate.
4. Confirm the existing transition appears and the destination loads.
5. Check the controller paid exactly one normal jump tariff (admin gates remain free).
6. Separately step off during charging: the attempt should cancel without spending its jump tariff.

All four required isolated gate tests passed in `20261011_101635_runWorkflowTests.log`: stationary charge with unchanged passenger height and no Levitation, successful single-charge travel, cooperative return, relocated return preservation and owner controls (the last checks share the four test methods). The disposable server shut down normally.

The installed-artifact receipt is recorded with this delivery. On-screen presentation still requires client approval; isolated tests do not establish visual quality. Deliberate pad departure remains a manual review step in this batch, not a newly exercised regression case.

Normal clean build passed (`20261011_101807_clean.log`); asset binding audit found zero errors and the production JAR contains no workflow test fixtures. Installed into the existing ZeroG mods folder after the closed-client check. Previous JAR is recoverable under `zerog-mod-backups/20261011-101915-UTC`; saves and other mods were not changed. Version remains `1.0.12-dev`.

SHA256: `d6dc88f4528aeb1a04a8c454cf42f723c6c3fa1ef1dcfa1f99b811a9cc570e75`.
