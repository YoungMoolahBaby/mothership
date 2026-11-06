# mothership

Sizing model for a lifetime mothership: a spinning habitat where people live a normal life in
space for years or generations. Read first:
- `README.md`: what it is, how to run.
- `docs/PLAN.md`: phases, decisions, status. **Start here.**
- `docs/RESEARCH.md`: the research queue (placeholders to source, ordered by the sensitivity table).

## Rules

- Every number the model uses lives in `params/*.yaml` with value, low, high, unit, conf, source.
  No magic numbers in code (physical constants excepted, named in `src/mothership/constants.py`).
  Placeholders are marked `conf: placeholder`, never passed off as sourced.
- Every number in docs comes from a real run (`uv run mothership report`) or a cited source.
- Check physics against known results (closed forms, textbook values) in tests before building on it.
- `uv run mothership check` and `uv run pytest` must pass before a commit.
- Subsystems that need real computation (active radiation shield, reactor magnets, spin dynamics,
  magnetic nozzle, structures) are built as projects in `C:\dev\cortenforge-cfsem` with cfsem and
  CortenForge; their results come back here as parameters with `source` naming the project and run.
- Log tool friction in `docs/FINDINGS.md`; nice-to-haves for CortenForge and cfsem go in the
  Suggestions lists in cortenforge-cfsem's `docs/CORTENFORGE.md` and `docs/CFSEM.md`.
- Commit and push only when Jon asks; ask before downloads over 1 GB and before deletes.
