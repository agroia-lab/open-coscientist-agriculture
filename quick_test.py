"""
Quick, cheap test of the CoScientist pipeline.
Uses gpt-4o-mini to minimize costs (~$0.05-0.10)
"""
import asyncio
import os
from langchain_openai import ChatOpenAI
from coscientist.framework import CoscientistConfig, CoscientistFramework
from coscientist.global_state import CoscientistState, CoscientistStateManager

# Simple, focused question (cheaper to research)
GOAL = "What are the main herbicide resistance mechanisms in Palmer amaranth?"

async def main():
    print("=" * 60)
    print("🧪 QUICK TEST - CoScientist Pipeline")
    print("=" * 60)
    print(f"\n📝 Question: {GOAL}")
    print("💰 Estimated cost: $0.05-0.10")
    print("⏱️  Estimated time: 2-5 minutes\n")

    # Force cheap models for GPT-Researcher
    os.environ["FAST_LLM"] = "openai:gpt-4o-mini"
    os.environ["SMART_LLM"] = "openai:gpt-4o-mini"
    os.environ["STRATEGIC_LLM"] = "openai:gpt-4o-mini"
    os.environ["RETRIEVER"] = "tavily"
    
    # Clear any previous state
    try:
        CoscientistState.clear_goal_directory(GOAL)
    except:
        pass
    
    # Initialize with cheap model
    cheap_llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=2000)
    
    config = CoscientistConfig(
        literature_review_agent_llm=cheap_llm,
        generation_agent_llms={"mini": cheap_llm},
        reflection_agent_llms={"mini": cheap_llm},
        evolution_agent_llms={"mini": cheap_llm},
        meta_review_agent_llm=cheap_llm,
        supervisor_agent_llm=cheap_llm,
        final_report_agent_llm=cheap_llm,
    )
    
    initial_state = CoscientistState(goal=GOAL)
    state_manager = CoscientistStateManager(initial_state)
    cosci = CoscientistFramework(config, state_manager)
    
    print("🚀 Starting pipeline...")
    print("   Phases: Literature Review → Hypothesis → Reflection → Report\n")
    
    final_report, final_meta_review = await cosci.run()
    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETE!")
    print("=" * 60)
    print("\n📄 FINAL REPORT PREVIEW:\n")
    print(final_report[:1500] if final_report else "No report generated")
    print("\n..." + "(truncated)" if final_report and len(final_report) > 1500 else "")
    
    # Save to file
    with open("quick_test_report.md", "w") as f:
        f.write(f"# Quick Test Report\n\n**Question:** {GOAL}\n\n")
        f.write(final_report or "No report")
    print("\n📁 Full report saved to: quick_test_report.md")

if __name__ == "__main__":
    asyncio.run(main())

