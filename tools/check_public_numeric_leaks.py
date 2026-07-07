#!/usr/bin/env python3
from pathlib import Path
import re, sys

PATTERNS=[
    ('percent', re.compile(r'\b\d+(?:\.\d+)?%')),
    ('decimal', re.compile(r'(?<![A-Za-z0-9_])\d+\.\d+(?![A-Za-z0-9_])')),
    ('fraction_display', re.compile(r'(?<![A-Za-z0-9_])\d+\s*/\s*\d+(?![A-Za-z0-9_])')),
    ('fraction_constructor', re.compile(r'Fraction\s*\(')),
]
EXCLUDE_DIRS={'.git','QUARANTINED_M8G_NUMERIC_ARTIFACTS','QUARANTINED_M12_NUMERIC_ARTIFACTS','QUARANTINED_M13_NUMERIC_ARTIFACTS','QUARANTINED_M23_M25_ECONOMICS_ARTIFACTS'}
TEXT_SUFFIX={'.md','.json','.txt','.py','.toml','.yaml','.yml'}

def main() -> int:
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path('.')
    findings=[]
    for p in root.rglob('*'):
        if not p.is_file() or p.suffix not in TEXT_SUFFIX: continue
        if any(part in EXCLUDE_DIRS for part in p.parts): continue
        text=p.read_text(encoding='utf-8', errors='ignore')
        for name, rx in PATTERNS:
            for m in rx.finditer(text):
                findings.append((str(p), name, m.group(0)))
                break
    if findings:
        for f in findings[:100]: print('LEAK_CANDIDATE', *f)
        return 1
    print('PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
