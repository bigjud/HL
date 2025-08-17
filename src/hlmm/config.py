from __future__ import annotations

import os
from dataclasses import dataclass
try:
	from dotenv import load_dotenv
except Exception:  # optional dependency
	def load_dotenv(*args, **kwargs):  # type: ignore
		return None


@dataclass
class MakerConfig:
	network: str
	account_address: str | None
	private_key: str | None
	asset: str
	order_size: float
	spread_bps: float
	skew_bps_per_unit: float
	update_interval_s: float
	max_position_abs: float
	paper: bool
	verbosity: int


def load_config(
	asset: str,
	order_size: float | None = None,
	spread_bps: float | None = None,
	skew_bps_per_unit: float | None = None,
	update_interval_s: float | None = None,
	max_position_abs: float | None = None,
	paper: bool = False,
	verbosity: int = 1,
) -> MakerConfig:
	load_dotenv(override=False)

	network = os.getenv("HYPERLIQUID_NETWORK", "testnet").lower()
	account_address = os.getenv("HL_ACCOUNT_ADDRESS")
	private_key = os.getenv("HL_PRIVATE_KEY")

	order_size = float(os.getenv("QUOTE_SIZE", order_size or 0.001))
	spread_bps = float(os.getenv("QUOTE_SPREAD_BPS", spread_bps or 10))
	skew_bps_per_unit = float(os.getenv("QUOTE_SKEW_BPS_PER_UNIT", skew_bps_per_unit or 3))
	update_interval_s = float(os.getenv("QUOTE_UPDATE_INTERVAL", update_interval_s or 1.0))
	max_position_abs = float(os.getenv("RISK_MAX_POSITION", max_position_abs or (order_size * 10)))

	return MakerConfig(
		network=network,
		account_address=account_address,
		private_key=private_key,
		asset=asset,
		order_size=order_size,
		spread_bps=spread_bps,
		skew_bps_per_unit=skew_bps_per_unit,
		update_interval_s=update_interval_s,
		max_position_abs=max_position_abs,
		paper=paper,
		verbosity=verbosity,
	)

