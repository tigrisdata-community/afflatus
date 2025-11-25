from __future__ import annotations
from typing import List, Optional, Literal, Annotated
from pydantic import BaseModel, Field, conint, confloat


class StoneFloorInfo(BaseModel):
    """Information about the current stone/floor for this run."""

    raw_text: str = Field(
        ...,
        description=(
            'Raw text such as "STONE 50" or "FLOOR 90" in all caps on a blue background.'
        ),
    )
    kind: Optional[Literal["STONE", "FLOOR"]] = Field(
        None,
        description="Whether the label is a STONE or FLOOR indicator, if it can be inferred.",
    )
    number: Optional[
        Annotated[
            int,
            Field(
                strict=True,
                ge=1,
                description="Parsed numeric stone/floor value (e.g. 50 from STONE 50).",
            ),
        ]
    ]


class EnemyInfo(BaseModel):
    """Information about the enemy displayed in red at the top of the frame."""

    name: Optional[str] = Field(
        None,
        description="Enemy name in red text at the top of the frame.",
    )
    health_percent: Optional[
        Annotated[
            float,
            Field(
                strict=True,
                ge=0,
                le=100,
                description="Enemy HP percentage shown next to the name (0–100).",
            ),
        ]
    ]


class HealEvent(BaseModel):
    """A single heal/spell entry."""

    name: Optional[str] = Field(
        None,
        description='Optional spell name such as "Afflatus Rapture".',
    )
    amount: Optional[
        Annotated[
            int,
            Field(
                strict=True,
                ge=0,
                description="Amount of HP restored by the heal.",
            ),
        ]
    ]


class DamageSpell(BaseModel):
    """A single damaging spell entry (orange text under the boss)."""

    name: Optional[str] = Field(
        None,
        description='Spell name such as "Glare III".',
    )
    amount: Optional[
        Annotated[
            int,
            Field(
                strict=True,
                ge=0,
                description="Amount of damage dealt by the spell.",
            ),
        ]
    ]


class FrameDescription(BaseModel):
    """
    Structured description of a single gameplay frame extracted from an image.
    """

    # messages: List[str] = Field(
    #     default_factory=list,
    #     description="Any text that is gold on a black background (e.g. status messages).",
    # )
    stone_floor: Optional[StoneFloorInfo] = Field(
        None,
        description="Information about the current STONE/FLOOR for this run.",
    )
    enemy: Optional[EnemyInfo] = Field(
        None,
        description="Enemy information in red at the top of the frame.",
    )
    heals: List[HealEvent] = Field(
        default_factory=list,
        description="List of heals/spells with their optional names and HP amounts.",
    )
    damage_spells: List[DamageSpell] = Field(
        default_factory=list,
        description="Damaging spells shown as orange combat text under/near the boss.",
    )
    hp: Optional[
        Annotated[
            int,
            Field(
                strict=True,
                ge=0,
                description="Player HP number under the green capsule above the button bars.",
            ),
        ]
    ]
    mp: Optional[
        Annotated[
            int,
            Field(
                strict=True,
                ge=0,
                description="Player MP number under the red capsule above the button bars.",
            ),
        ]
    ]
    aetherpool_arm_level: Optional[
        Annotated[
            int,
            Field(
                strict=True,
                ge=0,
                description="Aetherpool arm level (e.g. +95).",
            ),
        ]
    ]
    aetherpool_armor_level: Optional[
        Annotated[
            int,
            Field(
                strict=True,
                ge=0,
                description="Aetherpool armor level (e.g. +99).",
            ),
        ]
    ]
