#!/usr/bin/env python3
from pathlib import Path
import sys

def main() -> int:
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path('.')
    zips=[p for p in root.rglob('*.zip') if '.git' not in p.parts]
    if zips:
        for p in zips: print(f'ZIP_FOUND {p}')
        return 1
    print('PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
