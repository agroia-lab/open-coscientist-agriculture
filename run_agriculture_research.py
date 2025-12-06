import asyncio
import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from coscientist.framework import CoscientistConfig, CoscientistFramework
from coscientist.global_state import CoscientistState, CoscientistStateManager

# Import GPT Researcher config to force overrides
from gpt_researcher.config import Config

# Define the EXACT research goal provided by the user
GOAL = (
    "In industrial tomato grown under Mediterranean-type climatic conditions, "
    "with emphasis on Chile's Central Valley, what is the current status and distribution "
    "of Phelipanche ramosa resistance to ALS‑inhibiting herbicides, and which alternative "
    "herbicide modes of action—including experimental or not‑yet‑registered molecules "
    "(such as maleic hydrazide and prohexadione‑calcium) and mixtures—show potential "
    "for crop‑safe control of P. ramosa from the seedbank and germination phases through "
    "to parasite attachment (with secondary consideration of later stages), with the aim "
    "of generating testable hypotheses and designing field and greenhouse trials?"
)

async def main():
    print(f"🔬 Starting research run for:\n{GOAL}\n")

    # 0. FORCE GPT-RESEARCHER CONFIG - Use GPT-5.1 for web research
    os.environ["FAST_LLM"] = "openai:gpt-5.1"
    os.environ["SMART_LLM"] = "openai:gpt-5.1"
    os.environ["STRATEGIC_LLM"] = "openai:gpt-5.1"
    
    # Use Tavily with academic domains (works well for PubMed, ScienceDirect, etc.)
    os.environ["RETRIEVER"] = "tavily"
    print("🤖 GPT-Researcher: Using GPT-5.1 + Tavily (academic-focused)")

    # 1. Initialize State
    try:
        initial_state = CoscientistState(goal=GOAL)
        state_manager = CoscientistStateManager(initial_state)
    except FileExistsError:
        print("⚠️  Goal directory exists. Loading previous state...")
        state_manager = CoscientistStateManager(CoscientistState.load_latest(goal=GOAL))

    # 2. Initialize Config - Using PREMIUM models
    # GPT-5.1 for reasoning tasks, Claude Opus 4.5 for creative/writing tasks
    gpt51 = ChatOpenAI(model="gpt-5.1", max_completion_tokens=4000)
    opus45 = ChatAnthropic(model="claude-opus-4-5", max_tokens=4000)
    
    print("🤖 CoScientist Agents:")
    print("   - Literature Review: GPT-5.1")
    print("   - Hypothesis Generation: Claude Opus 4.5")
    print("   - Reflection/Evolution: GPT-5.1")
    print("   - Meta Review: Claude Opus 4.5")
    print("   - Final Report: Claude Opus 4.5")
    
    # Agricultural specialist fields for hypothesis generation
    AGRICULTURE_SPECIALIST_FIELDS = [
        "weed science",
        "plant pathology",
        "agronomy",
        "soil science",
        "herbicide physiology",
        "parasitic plant biology",
        "integrated pest management",
        "crop physiology",
        "plant biochemistry",
        "agricultural ecology",
    ]
    
    config = CoscientistConfig(
        literature_review_agent_llm=gpt51,
        generation_agent_llms={"opus": opus45, "gpt": gpt51},
        reflection_agent_llms={"opus": opus45, "gpt": gpt51},
        evolution_agent_llms={"gpt": gpt51},
        meta_review_agent_llm=opus45,
        supervisor_agent_llm=gpt51,
        final_report_agent_llm=opus45,
        specialist_fields=AGRICULTURE_SPECIALIST_FIELDS,
    )
    print(f"🌱 Specialist fields: {', '.join(AGRICULTURE_SPECIALIST_FIELDS[:5])}...")
    
    # 3. Setup Framework
    cosci = CoscientistFramework(config, state_manager)

    # 4. Run the Full Process
    print("🚀 Launching Open CoScientist Agents (Agricultural Edition)...")
    print("This may take 5-15 minutes. Please wait.")
    
    # We run the full loop
    final_report, final_meta_review = await cosci.run()
    
    print("\n✅ Research Complete!")
    print("="*50)
    print("FINAL REPORT PREVIEW:")
    print("="*50)
    print(final_report[:2000] + "...\n(Full report saved to disk)")

if __name__ == "__main__":
    asyncio.run(main())
