from __future__ import annotations

import asyncio
import math
import os
import random
import signal
from dataclasses import dataclass
from typing import AsyncIterator, Optional, Tuple


def env_float(name: str, default: float) -> float:
	val = os.getenv(name)
	return float(val) if val is not None else default


def env_str(name: str, default: str) -> str:
	val = os.getenv(name)
	return val if val is not None else default


def bps_to_decimal(bps: float) -> float:
	return bps / 10000.0


class GracefulExit:
	def __init__(self) -> None:
		self._shutdown = asyncio.Event()

	def install(self) -> None:
		loop = asyncio.get_event_loop()
		for sig in (signal.SIGINT, signal.SIGTERM):
			loop.add_signal_handler(sig, self._shutdown.set)

	async def wait(self) -> None:
		await self._shutdown.wait()


@dataclass
class Quote:
	bid_px: float
	ask_px: float
	bid_sz: float
	ask_sz: float


class RandomWalkMid:
	def __init__(self, start_mid: float, vol_bps_per_sec: float = 5.0) -> None:
		self.mid = start_mid
		self.vol = vol_bps_per_sec

	async def stream(self, interval_s: float = 1.0) -> AsyncIterator[float]:
		while True:
			move = random.gauss(0.0, self.vol) / 10000.0
			self.mid = max(0.0001, self.mid * (1.0 + move))
			yield self.mid
			await asyncio.sleep(interval_s)


def round_to_tick(price: float, tick: float) -> float:
	if tick <= 0:
		return price
	return math.floor(price / tick) * tick

