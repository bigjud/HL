from __future__ import annotations

import argparse
import asyncio
import logging
import os

from hlmm.config import load_config
from hlmm.logging_config import configure_logging
from hlmm.exchange_paper import PaperExchange
from hlmm.exchange_hyperliquid import HyperliquidExchange
from hlmm.maker import Maker


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Hyperliquid Market Maker")
	parser.add_argument("--asset", required=True, help="Asset symbol, e.g., BTC")
	parser.add_argument("--size", type=float, help="Order size in base units")
	parser.add_argument("--spread-bps", type=float, help="Half spread in bps")
	parser.add_argument("--skew-bps-per-unit", type=float, help="Inventory skew in bps per base unit")
	parser.add_argument("--update-interval", type=float, default=1.0, help="Quote update interval in seconds")
	parser.add_argument("--max-position", type=float, help="Absolute max position in base units")
	parser.add_argument("--paper", action="store_true", help="Run in paper trading mode")
	parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase logging verbosity")
	return parser.parse_args()


async def main() -> None:
	args = parse_args()
	configure_logging(verbosity=args.verbose)

	cfg = load_config(
		asset=args.asset,
		order_size=args.size,
		spread_bps=args.spread_bps,
		skew_bps_per_unit=args.skew_bps_per_unit,
		update_interval_s=args.update_interval,
		max_position_abs=args.max_position,
		paper=args.paper,
		verbosity=args.verbose,
	)

	if cfg.paper:
		exchange = PaperExchange()
	else:
		if not (cfg.account_address and cfg.private_key):
			raise SystemExit("Missing HL_ACCOUNT_ADDRESS and/or HL_PRIVATE_KEY. Set env vars or use .env.")
		exchange = HyperliquidExchange(cfg.network, cfg.account_address, cfg.private_key)

	maker = Maker(cfg, exchange)
	await maker.run()


if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		logging.getLogger(__name__).info("Shutting down...")

