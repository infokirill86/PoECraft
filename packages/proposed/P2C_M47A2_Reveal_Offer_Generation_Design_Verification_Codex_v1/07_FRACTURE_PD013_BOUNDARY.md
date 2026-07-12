# Fracture and PD-013 Boundary

This design preserves accepted behavior without widening it:

- A hidden placeholder counts toward Fracture's minimum installed count.
- A hidden placeholder is never a Fracture target.
- Base Reveal replaces that placeholder with an installed modifier marked `desecrated: true` only after explicit caller selection.

The ratified future project rule says a revealed Desecrated modifier may be a Fracture target and may retain both `fractured` and `desecrated`. This package records that future compatibility requirement but does not implement it, admit it, or close PD-013.

Required later gate sequence:

1. accept and implement base Reveal;
2. audit canonical revealed state behavior;
3. separately authorize the revealed-Desecrated Fracture extension;
4. keep PD-013 status explicit until its own closure gate.
