from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from p2c_engine.monte_carlo.ordinary_add import build_public_smoke_summary
from p2c_engine.static_data import build_static_game_data, materialize_fractured_crit_state


def main() -> int:
    static = build_static_game_data(ROOT)
    initial_state = materialize_fractured_crit_state(static, 1)
    summary = build_public_smoke_summary(
        static=static,
        initial_state=initial_state,
        seed=20260707,
        sample_count=8,
        mode_id="m32_smoke_mml_off",
        run_id="m32_smoke",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
