## What's working
- Auth flow in `src/auth.py`: token check, tested.
- DB connection in `src/db.py`: DSN-based, returns an open handle.

## What's stubbed or absent
- Password reset (not started).

## Decisions to make
- Session store: in-memory vs persistent.
