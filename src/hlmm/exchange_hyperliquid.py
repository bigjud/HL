from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Optional

from .risk import Position

logger = logging.getLogger(__name__)


class HyperliquidExchange:
	def __init__(self, network: str, account_address: str, private_key: str) -> None:
		self.network = network
		self.account_address = account_address
		self.private_key = private_key
		self._initialized = False
		self._info = None
		self._exchange = None

	async def _lazy_init(self) -> None:
		if self._initialized:
			return
		try:
			# Lazy import to allow paper mode without SDK installed
			from hyperliquid.info import Info
			from hyperliquid.utils import constants
			self._info = Info(
				constants.TESTNET_API_URL if self.network == "testnet" else constants.MAINNET_API_URL,
				skip_ws=True,
			)
			# Some SDKs separate data and trading; placeholder for real trading client
			self._exchange = self._info  # Replace with actual exchange client if different
			self._initialized = True
		except Exception as e:
			logger.error("Failed to initialize Hyperliquid SDK. Is it installed? %s", e)
			raise

	async def get_position(self, asset: str) -> Position:
		await self._lazy_init()
		try:
			user_state = self._info.user_state(self.account_address)
			# Map user_state to position in base units; adapt to SDK response structure
			base_pos = 0.0
			if isinstance(user_state, dict):
				positions = user_state.get("assetPositions") or user_state.get("positions") or []
				for p in positions:
					if (p.get("asset") or p.get("symbol") or p.get("ticker")) == asset:
						base_pos = float(p.get("position", 0.0) or p.get("base", 0.0) or 0.0)
						break
			return Position(base=base_pos)
		except Exception as e:
			logger.exception("Error fetching position: %s", e)
			return Position(base=0.0)

	async def cancel_all(self, asset: str) -> None:
		await self._lazy_init()
		try:
			# Replace with actual cancel-all call if available
			logger.info("[hl] cancel_all for %s (implement with SDK method)", asset)
		except Exception as e:
			logger.exception("Error cancel_all: %s", e)

	async def place_limit(self, asset: str, is_buy: bool, price: float, size: float) -> str:
		await self._lazy_init()
		try:
			# Replace below with the actual order placement call per SDK
			logger.info(
				f"[hl] place {asset} {'BUY' if is_buy else 'SELL'} {size} @ {price:.2f} (implement with SDK)"
			)
			return "hl-order-temp-id"
		except Exception as e:
			logger.exception("Error placing order: %s", e)
			raise

