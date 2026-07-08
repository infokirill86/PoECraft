# Risks and Limits

## Remaining risks

1. No mechanical validator yet.
   - The schema is documented but not enforced by a tool.
   - This is acceptable for this hygiene step because code/test changes were forbidden.

2. YAML frontmatter requires discipline.
   - Agents must parse the frontmatter and stop if it is invalid.

3. `repo_head_at_last_update` is not a read receipt.
   - Packages and reviews carry `observed_repo_head` and `observed_active_task_sha`; those are the stronger evidence.

4. Schema acceptance is not automatic.
   - Claude audit and ChatGPT/User gate acceptance are still required.

## Scope limits

This patch does not:

- open M34-B;
- design sequence validation;
- implement sequence validation;
- change runtime mechanics;
- add automation;
- add GitHub Actions;
- close SOURCE/PROVENANCE, MML, or PD-013.
