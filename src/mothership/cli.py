"""mothership check | report"""

from __future__ import annotations

import argparse
import sys

import numpy as np

from . import OUT_DIR
from .model import SCENARIOS, run
from .params import check_params, load_params, values
from .report import write


def cmd_check(args) -> int:
    params = load_params()
    problems = check_params(params)
    needed = [f"mission.scenario.{s}.years" for s in SCENARIOS] + ["mission.scenario.park.dv"]
    problems += [f"missing parameter {k}" for k in needed if k not in params]
    if not problems:
        r = run(values(params))
        s = r["ship"]
        if not float(s["tube_over_radius"]) < 1.0:
            problems.append("the tube is wider than the spin radius: no torus fits")
        if not bool(s["spin_stable"]):
            problems.append("the ring stack would not spin stably at the central values")
        if not float(s["ring_spin_factor"]) < 1.0:
            problems.append("the ring cannot hold itself against the spin at this radius")
        if not np.isfinite(float(s["dry_t"])):
            problems.append("ship mass is not finite at the central values")
    for p in problems:
        print("PROBLEM", p)
    n_ph = sum(p.conf == "placeholder" for p in params.values())
    print(f"{len(params)} parameters ({n_ph} placeholders), {len(problems)} problems")
    return 1 if problems else 0


def cmd_report(args) -> int:
    params = load_params()
    problems = check_params(params)
    if problems:
        for p in problems:
            print("PROBLEM", p)
        return 1
    path = OUT_DIR / "report.md"
    text = write(params, path, args.n, args.seed)
    print(text)
    print(f"wrote {path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="mothership")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="validate parameters and the central run").set_defaults(func=cmd_check)
    rp = sub.add_parser("report", help="central run, Monte Carlo, sensitivity -> out/report.md")
    rp.add_argument("--n", type=int, default=5000)
    rp.add_argument("--seed", type=int, default=1)
    rp.set_defaults(func=cmd_report)
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
