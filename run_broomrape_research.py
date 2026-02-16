"""Run the Open CoScientist multi-agent pipeline for broomrape research.

This script uses the broomrape × industrial-tomato research profile to
configure the full agent pipeline (literature review → hypothesis
generation → reflection → tournament → evolution → meta-review → report).

Quick start
-----------
1.  Set the following environment variables (or a ``.env`` file):
        OPENAI_API_KEY, ANTHROPIC_API_KEY, TAVILY_API_KEY
2.  Select a research goal below (or pass one via the CLI).
3.  Run:
        python run_broomrape_research.py
"""

import asyncio
import os
import sys

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from coscientist.framework import CoscientistConfig, CoscientistFramework
from coscientist.global_state import CoscientistState, CoscientistStateManager
from coscientist.profiles.broomrape_tomato import PROFILE

# Import to force config overrides
from gpt_researcher.config import Config  # noqa: F401


def _print_goals():
    """Print all available research goals from the broomrape profile."""
    print("\nAvailable research goals:")
    print("=" * 60)
    for i, (key, text) in enumerate(PROFILE.list_goals(), 1):
        marker = " (default)" if key == PROFILE.default_goal_key else ""
        print(f"\n  [{i}] {key}{marker}")
        # Print first 120 chars
        print(f"      {text[:120]}...")
    print()


async def main(goal_key: str | None = None):
    """Run the broomrape research pipeline.

    Parameters
    ----------
    goal_key : str | None
        Key from ``PROFILE.research_goals``.  If ``None``, uses the
        profile's default goal (``als_resistance``).
    """

    # -- Resolve goal -------------------------------------------------------
    if goal_key is None:
        goal_key = PROFILE.default_goal_key
    if goal_key not in PROFILE.research_goals:
        print(f"Unknown goal key: {goal_key!r}")
        _print_goals()
        sys.exit(1)

    goal = PROFILE.research_goals[goal_key]

    print(f"Profile  : {PROFILE.name}")
    print(f"Goal key : {goal_key}")
    print(f"Goal     : {goal[:100]}...")
    print()

    # -- GPT-Researcher env -------------------------------------------------
    os.environ["FAST_LLM"] = "openai:gpt-5.1"
    os.environ["SMART_LLM"] = "openai:gpt-5.1"
    os.environ["STRATEGIC_LLM"] = "openai:gpt-5.1"
    os.environ["RETRIEVER"] = "tavily"
    print("GPT-Researcher: GPT-5.1 + Tavily (academic-focused)")

    # -- State --------------------------------------------------------------
    try:
        state = CoscientistState(goal=goal)
        state_manager = CoscientistStateManager(state)
    except FileExistsError:
        print("Goal directory exists — loading previous state...")
        state_manager = CoscientistStateManager(
            CoscientistState.load_latest(goal=goal)
        )

    # -- LLMs ---------------------------------------------------------------
    gpt51 = ChatOpenAI(model="gpt-5.1", max_completion_tokens=4000)
    opus45 = ChatAnthropic(model="claude-opus-4-5", max_tokens=4000)

    print("\nBroomrape CoScientist Agent Configuration:")
    print("  Literature Review    : GPT-5.1")
    print("  Hypothesis Generation: Claude Opus 4.5 + GPT-5.1")
    print("  Reflection/Evolution : Claude Opus 4.5 + GPT-5.1")
    print("  Meta Review          : Claude Opus 4.5")
    print("  Final Report         : Claude Opus 4.5")
    print(f"  Specialist fields    : {len(PROFILE.specialist_fields)} "
          f"({', '.join(PROFILE.specialist_fields[:4])}, ...)")
    if PROFILE.preferred_reasoning_types:
        print(f"  Reasoning types      : {len(PROFILE.preferred_reasoning_types)} "
              f"(of 18 available)")
    print()

    # -- Config -------------------------------------------------------------
    config = CoscientistConfig(
        literature_review_agent_llm=gpt51,
        generation_agent_llms={"opus": opus45, "gpt": gpt51},
        reflection_agent_llms={"opus": opus45, "gpt": gpt51},
        evolution_agent_llms={"gpt": gpt51},
        meta_review_agent_llm=opus45,
        supervisor_agent_llm=gpt51,
        final_report_agent_llm=opus45,
        specialist_fields=PROFILE.specialist_fields,
        preferred_reasoning_types=PROFILE.preferred_reasoning_types,
    )

    # -- Framework ----------------------------------------------------------
    cosci = CoscientistFramework(config, state_manager)

    print("Launching Broomrape × Industrial Tomato research pipeline...")
    print("This may take 5-15 minutes.\n")

    final_report, final_meta_review = await cosci.run()

    print("\nResearch Complete!")
    print("=" * 60)
    print("FINAL REPORT PREVIEW:")
    print("=" * 60)
    print(final_report[:2000] + "...\n(Full report saved to disk)")


if __name__ == "__main__":
    # Accept optional goal key from CLI: python run_broomrape_research.py germination_ecology
    key = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(main(goal_key=key))
