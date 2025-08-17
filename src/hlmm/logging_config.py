from __future__ import annotations

import logging
try:
	from rich.logging import RichHandler
except Exception:  # rich not installed
	RichHandler = None  # type: ignore


def configure_logging(verbosity: int = 1) -> None:
	level = logging.INFO if verbosity <= 1 else logging.DEBUG
	if RichHandler is not None:
		logging.basicConfig(
			level=level,
			format="%(message)s",
			handlers=[RichHandler(rich_tracebacks=True, show_time=True, show_path=False)],
		)
	else:
		logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

