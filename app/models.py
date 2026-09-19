"""Request/response Pydantic models for versioned JSON API."""
from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class ChargeInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    charge: int = Field(..., description="允许的电荷态（正整数）")


class PeakInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mz: str = Field(..., description="质荷比，十进制字符串（精确）")
    intensity: int = Field(..., description="强度（正整数）")


class DeconvRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    peaks: List[PeakInput] = Field(..., description="按质荷比严格递增排列的 2-36 个峰")
    charges: List[int] = Field(..., description="允许的电荷态集合（正整数，可重复会被去重）")
    tolerance_da: str = Field(..., description="十进制容差（>=0 的十进制数）")


class ClusterOut(BaseModel):
    charge: int
    peak_indices: List[int]
    mz: List[str]
    intensity: int


class WitnessOut(BaseModel):
    clusters: List[ClusterOut]
    unexplained: List[int]


class Verdict(str, Enum):
    UNIQUE = "UNIQUE"
    AMBIGUOUS = "AMBIGUOUS"
    UNRESOLVED = "UNRESOLVED"


class DeconvResponse(BaseModel):
    verdict: Verdict
    clusters: List[ClusterOut]
    unexplained: List[int]
    witness: WitnessOut | None = Field(
        default=None,
        description="AMBIGUOUS 时返回另一个同样最优但不同的组合见证",
    )
