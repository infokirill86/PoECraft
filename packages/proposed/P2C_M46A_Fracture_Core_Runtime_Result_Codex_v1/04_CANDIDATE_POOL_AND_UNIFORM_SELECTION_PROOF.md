# Candidate Pool and Uniform Selection Proof

| Property | Implementation evidence | Test evidence | Status |
|---|---|---|---|
| Rare quarterstaff only | precondition builder | eligible/invalid-state tests | PASS |
| Minimum installed count | precondition builder | below-floor rejection | PASS |
| No existing fracture | precondition builder | existing-fracture rejection | PASS |
| No Desecrated/placeholder state | precondition builder | both disputed-state rejections | PASS |
| One combined prefix/suffix pool | iteration over installed instance identities, without side lottery | mixed-side pool test | PASS |
| Ordinary and crafted eligible | no crafted exclusion | crafted-candidate test | PASS |
| Uniform instance selection | every candidate has the same unit weight | exact-path and negative-control tests | PASS |
| No generation weights | installed-instance candidates do not consult modifier generation weight | pool test | PASS |
| Exact total mass conserved | exact rational branch enumeration | mass-sum boolean | PASS |

No probability values are published in this package.
