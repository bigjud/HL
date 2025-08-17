from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Position:
	base: float = 0.0


class RiskLimits:
	def __init__(self, max_position_abs: float) -> None:
		self.max_position_abs = max_position_abs

	def can_place(self, current_position: Position, is_buy: bool, size: float) -> bool:
		tentative = current_position.base + (size if is_buy else -size)
		return abs(tentative) <= self.max_position_abs + 1e-12

