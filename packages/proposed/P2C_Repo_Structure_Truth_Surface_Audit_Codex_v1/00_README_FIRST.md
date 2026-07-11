# P2C Repository Structure and Truth-Surface Audit

Status: **PROPOSED AUDIT — NO CLEANUP APPLIED**

This package investigates repeated agent failures to read the live task correctly. It audits the tracked GitHub structure, routing documents, accepted-truth surfaces, package/review lifecycle, references, and hygiene tools.

The audit changes no runtime, mechanics, data semantics, accepted truth, package location, or historical evidence. It deletes and moves nothing. A later cleanup delta requires Claude audit and an explicit ChatGPT/User gate.

Headline finding: the repository is physically compact and has no exact duplicate tracked files, but its navigation contract is internally inconsistent. Agents are told to read stale orientation/status documents before the sole live dispatcher, while three historical task files still live under `work/active/`.
