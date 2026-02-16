"""Research profiles for domain-specialised CoScientist configurations.

A research profile bundles together:
- One or more curated research goals
- Domain-specific specialist fields for the generation agents
- An optional subset of reasoning types particularly relevant to the domain
- LLM configuration presets

Profiles make it easy to spin up a fully configured CoScientist pipeline
for a specific research domain without manually wiring specialist fields,
goals, and model assignments each time.

Available profiles
------------------
broomrape_tomato
    Phelipanche spp. (broomrape) management in industrial tomato
    under Mediterranean conditions.
"""

from dataclasses import dataclass, field
from typing import Optional

from coscientist.reasoning_types import ReasoningType as ReasoningType


@dataclass
class ResearchProfile:
    """Base container for a domain-specialised research configuration.

    Parameters
    ----------
    name : str
        Human-readable profile name.
    description : str
        One-paragraph summary of the research domain.
    research_goals : dict[str, str]
        Named research goals (key = short label, value = full goal text).
    specialist_fields : list[str]
        Specialist domains assigned to generation agents.
    preferred_reasoning_types : list[ReasoningType] | None
        If provided, generation agents draw reasoning types only from this
        subset.  If ``None``, all 18 reasoning types are available.
    default_goal_key : str
        Key into *research_goals* used when no explicit goal is specified.
    """

    name: str
    description: str
    research_goals: dict = field(default_factory=dict)
    specialist_fields: list = field(default_factory=list)
    preferred_reasoning_types: Optional[list] = None
    default_goal_key: str = ""

    @property
    def default_goal(self) -> str:
        """Return the default research goal text."""
        return self.research_goals[self.default_goal_key]

    def list_goals(self) -> list:
        """Return ``[(key, goal_text), ...]`` for all available goals."""
        return list(self.research_goals.items())
