#!/usr/bin/env python3
from __future__ import annotations
import hashlib, sys
from pathlib import Path

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    file = Path(sys.argv[1]) if len(sys.argv)>1 else Path('SHA256SUMS.txt')
    root=file.parent
    if not file.exists():
        print(f'MISSING {file}')
        return 2
    ok=True
    for line in file.read_text(encoding='utf-8').splitlines():
        if not line.strip() or line.startswith('#'): continue
        parts=line.split()
        if len(parts)<2: continue
        expected, rel=parts[0], parts[-1].lstrip('*')
        p=root/rel
        if not p.exists(): print(f'MISSING {rel}'); ok=False; continue
        got=sha256(p)
        if got!=expected:
            print(f'FAIL {rel} expected={expected} got={got}')
            ok=False
    print('PASS' if ok else 'FAIL')
    return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
