import asyncio
import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from coscientist.framework import CoscientistConfig, CoscientistFramework
from coscientist.global_state import CoscientistState, CoscientistStateManager

# Import GPT Researcher config to force overrides
from gpt_researcher.config import Config

# ---------------------------------------------------------------------------
# RESEARCH GOALS
# Uncomment the goal you want to investigate, or define your own.
# ---------------------------------------------------------------------------

# Goal 1: Herbicide resistance management through integrated approaches
# GOAL = (
#     "What are the most effective integrated weed management strategies "
#     "for delaying and mitigating the evolution of herbicide-resistant weed "
#     "populations in intensive cereal cropping systems, combining chemical "
#     "(herbicide rotation, mixtures, and novel modes of action), cultural "
#     "(crop rotation, competitive cultivars, cover crops), mechanical "
#     "(harvest weed seed control, strategic tillage), and precision agriculture "
#     "(site-specific weed management, sensor-based spot spraying) approaches, "
#     "with the aim of generating testable hypotheses for multi-year field trials?"
# )

# Goal 2: Precision weed management using sensing and robotics
# GOAL = (
#     "How can emerging precision agriculture technologies—including UAV-based "
#     "multispectral and hyperspectral imaging, deep learning weed detection "
#     "algorithms, autonomous robotic platforms, and variable-rate application "
#     "systems—be integrated into practical site-specific weed management (SSWM) "
#     "frameworks that reduce herbicide use by 50-80% while maintaining weed "
#     "control efficacy comparable to broadcast applications, and what are the "
#     "key biological, technological, and economic barriers to adoption?"
# )

# Goal 3: Cover crops and soil seed bank depletion
# GOAL = (
#     "What are the mechanisms by which cover crop species and mixtures "
#     "suppress weed seed bank replenishment and promote seed bank depletion "
#     "in no-till and reduced-tillage cropping systems, considering allelopathic "
#     "effects, light interception, soil microbiome changes, and weed seed "
#     "predation, and how can these mechanisms be optimized through species "
#     "selection, planting timing, and termination methods to achieve durable "
#     "weed suppression across diverse climatic zones?"
# )

# Goal 4 (default): Parasitic weed control in Mediterranean tomato
GOAL = (
    "In industrial tomato grown under Mediterranean-type climatic conditions, "
    "with emphasis on Chile's Central Valley, what is the current status and distribution "
    "of Phelipanche ramosa resistance to ALS-inhibiting herbicides, and which alternative "
    "herbicide modes of action—including experimental or not-yet-registered molecules "
    "(such as maleic hydrazide and prohexadione-calcium) and mixtures—show potential "
    "for crop-safe control of P. ramosa from the seedbank and germination phases through "
    "to parasite attachment (with secondary consideration of later stages), with the aim "
    "of generating testable hypotheses and designing field and greenhouse trials?"
)


# ---------------------------------------------------------------------------
# IWM & Precision Farming Specialist Fields
# ---------------------------------------------------------------------------
IWM_SPECIALIST_FIELDS = [
    # Weed biology and management
    "weed science",
    "weed ecology",
    "herbicide resistance",
    "integrated weed management",
    "crop-weed competition",
    "soil seed bank ecology",
    "cover crop science",
    "herbicide application technology",
    "agroecology",
    "crop rotation and diversification",
    "harvest weed seed control",
    "weed biological control",
    "plant physiology",
    "soil science",
    "agricultural economics",
    # Precision agriculture and technology
    "precision agriculture",
    "site-specific weed management",
    "agricultural robotics and automation",
    "remote sensing for agriculture",
    "geographic information systems (GIS)",
    # Quantitative and analytical methods
    "agricultural statistics and experimental design",
    "Bayesian data analysis",
    "spatial analysis and geostatistics",
    "mechanistic and simulation modelling",
    "agronomy",
]


async def main():
    print(f"Starting research run for:\n{GOAL}\n")

    # 0. FORCE GPT-RESEARCHER CONFIG
    os.environ["FAST_LLM"] = "openai:gpt-5.1"
    os.environ["SMART_LLM"] = "openai:gpt-5.1"
    os.environ["STRATEGIC_LLM"] = "openai:gpt-5.1"

    # Use Tavily with academic domains (works well for PubMed, ScienceDirect, etc.)
    os.environ["RETRIEVER"] = "tavily"
    print("GPT-Researcher: Using GPT-5.1 + Tavily (academic-focused)")

    # 1. Initialize State
    try:
        initial_state = CoscientistState(goal=GOAL)
        state_manager = CoscientistStateManager(initial_state)
    except FileExistsError:
        print("Goal directory exists. Loading previous state...")
        state_manager = CoscientistStateManager(CoscientistState.load_latest(goal=GOAL))

    # 2. Initialize Config - Using PREMIUM models
    gpt51 = ChatOpenAI(model="gpt-5.1", max_completion_tokens=4000)
    opus45 = ChatAnthropic(model="claude-opus-4-5", max_tokens=4000)

    print("CoScientist IWM Agents:")
    print("   - Literature Review: GPT-5.1")
    print("   - Hypothesis Generation: Claude Opus 4.5 + GPT-5.1")
    print("   - Reflection/Evolution: Claude Opus 4.5 + GPT-5.1")
    print("   - Meta Review: Claude Opus 4.5")
    print("   - Final Report: Claude Opus 4.5")

    config = CoscientistConfig(
        literature_review_agent_llm=gpt51,
        generation_agent_llms={"opus": opus45, "gpt": gpt51},
        reflection_agent_llms={"opus": opus45, "gpt": gpt51},
        evolution_agent_llms={"gpt": gpt51},
        meta_review_agent_llm=opus45,
        supervisor_agent_llm=gpt51,
        final_report_agent_llm=opus45,
        specialist_fields=IWM_SPECIALIST_FIELDS,
    )
    print(f"IWM Specialist fields: {', '.join(IWM_SPECIALIST_FIELDS[:5])}...")

    # 3. Setup Framework
    cosci = CoscientistFramework(config, state_manager)

    # 4. Run the Full Process
    print("Launching Open CoScientist (IWM & Precision Farming Edition)...")
    print("This may take 5-15 minutes. Please wait.")

    final_report, final_meta_review = await cosci.run()

    print("\nResearch Complete!")
    print("=" * 50)
    print("FINAL REPORT PREVIEW:")
    print("=" * 50)
    print(final_report[:2000] + "...\n(Full report saved to disk)")


if __name__ == "__main__":
    asyncio.run(main())
