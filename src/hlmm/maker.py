from __future__ import annotations

import asyncio
import logging
from typing import Optional

from .config import MakerConfig
from .risk import RiskLimits, Position
from .strategy import StrategyParams, InventorySkewedQuoter
from .utils import RandomWalkMid, Quote

logger = logging.getLogger(__name__)


class Maker:
	def __init__(self, cfg: MakerConfig, exchange) -> None:  # exchange is duck-typed
		self.cfg = cfg
		self.exchange = exchange
		self.risk = RiskLimits(cfg.max_position_abs)
		self.position = Position()
		self.current_quotes: Optional[Quote] = None
		self.strategy = InventorySkewedQuoter(
			StrategyParams(
				spread_bps=cfg.spread_bps,
				skew_bps_per_unit=cfg.skew_bps_per_unit,
				order_size=cfg.order_size,
			)
		)

	async def run(self) -> None:
		mid_src = RandomWalkMid(start_mid=50000.0) if self.cfg.paper else None
		while True:
			mid_px = await self._get_mid(mid_src)
			await self._sync_position()
			quote = self.strategy.compute_quote(mid_px, self.position)
			await self._requote(quote)
			if self.cfg.paper and hasattr(self.exchange, "simulate_fill"):
				await self.exchange.simulate_fill(mid_px)
			await asyncio.sleep(self.cfg.update_interval_s)

	async def _get_mid(self, mid_src: Optional[RandomWalkMid]) -> float:
		if mid_src is not None:
			aiter = mid_src.stream(self.cfg.update_interval_s)
			return await aiter.__anext__()
		# TODO: implement mid from live L2 or ticker via SDK
		logger.warning("Live mid-price source not implemented; using placeholder")
		return 50000.0

	async def _sync_position(self) -> None:
		pos = await self.exchange.get_position(self.cfg.asset)
		self.position = pos

	async def _requote(self, quote: Quote) -> None:
		await self.exchange.cancel_all(self.cfg.asset)
		# Risk checks per side
		if self.risk.can_place(self.position, is_buy=True, size=quote.bid_sz):
			await self.exchange.place_limit(self.cfg.asset, True, quote.bid_px, quote.bid_sz)
		else:
			logger.debug("Bid blocked by risk limits")
		if self.risk.can_place(self.position, is_buy=False, size=quote.ask_sz):
			await self.exchange.place_limit(self.cfg.asset, False, quote.ask_px, quote.ask_sz)
		else:
			logger.debug("Ask blocked by risk limits")

