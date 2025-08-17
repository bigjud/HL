from __future__ import annotations

from dataclasses import dataclass
from .utils import Quote, bps_to_decimal
from .risk import Position


@dataclass
class StrategyParams:
	spread_bps: float
	skew_bps_per_unit: float
	order_size: float


class InventorySkewedQuoter:
	def __init__(self, params: StrategyParams) -> None:
		self.params = params

	def compute_quote(self, mid_px: float, position: Position) -> Quote:
		base_spread = bps_to_decimal(self.params.spread_bps)
		skew = bps_to_decimal(self.params.skew_bps_per_unit) * position.base
		bid_edge = base_spread + max(0.0, skew)
		ask_edge = base_spread + max(0.0, -skew)
		bid_px = mid_px * (1.0 - bid_edge)
		ask_px = mid_px * (1.0 + ask_edge)
		return Quote(bid_px=bid_px, ask_px=ask_px, bid_sz=self.params.order_size, ask_sz=self.params.order_size)

