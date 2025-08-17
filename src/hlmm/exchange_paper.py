from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Dict, Optional

from .risk import Position


logger = logging.getLogger(__name__)


@dataclass
class LiveOrder:
	order_id: str
	asset: str
	is_buy: bool
	price: float
	size: float


class PaperExchange:
	def __init__(self) -> None:
		self.position = Position()
		self.orders: Dict[str, LiveOrder] = {}
		self._next_id = 1

	async def get_position(self, asset: str) -> Position:
		return self.position

	async def cancel_all(self, asset: str) -> None:
		if self.orders:
			logger.info(f"[paper] cancel {len(self.orders)} orders")
		self.orders.clear()

	async def place_limit(self, asset: str, is_buy: bool, price: float, size: float) -> str:
		order_id = str(self._next_id)
		self._next_id += 1
		order = LiveOrder(order_id=order_id, asset=asset, is_buy=is_buy, price=price, size=size)
		self.orders[order_id] = order
		logger.info(f"[paper] place {asset} {'BUY' if is_buy else 'SELL'} {size} @ {price:.2f} (id={order_id})")
		return order_id

	async def simulate_fill(self, mid_px: float) -> None:
		to_delete = []
		for order_id, order in self.orders.items():
			if order.is_buy and order.price >= mid_px:
				self.position.base += order.size
				logger.debug(f"[paper] filled BUY {order.size} @ {order.price:.2f}")
				to_delete.append(order_id)
			elif (not order.is_buy) and order.price <= mid_px:
				self.position.base -= order.size
				logger.debug(f"[paper] filled SELL {order.size} @ {order.price:.2f}")
				to_delete.append(order_id)
		for oid in to_delete:
			self.orders.pop(oid, None)

