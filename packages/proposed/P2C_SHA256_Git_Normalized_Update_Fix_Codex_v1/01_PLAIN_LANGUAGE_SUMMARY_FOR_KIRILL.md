# Plain-language summary for Kirill

Claude found why `SHA256SUMS.txt` kept drifting.

Simple version:

- Git internally stores text files in normalized form, usually LF line endings.
- A Windows working folder may show the same file with CRLF line endings.
- The old checksum updater hashed the visible working-folder bytes.
- That meant two clones could hash "the same committed file" differently.

The fix:

- for tracked files, checksum the bytes Git has in its index;
- for untracked files, still checksum the raw working file;
- make the checker use the same rule.

Why it matters:

This makes `SHA256SUMS.txt` stable across Windows/Linux/linked worktrees and stops repeated false checksum corrections.

This is repo hygiene only. It does not touch crafting mechanics.
