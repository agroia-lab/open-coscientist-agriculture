import asyncio
import os
from langchain_openai import ChatOpenAI
from coscientist.framework import CoscientistConfig, CoscientistFramework
from coscientist.global_state import CoscientistState, CoscientistStateManager
from coscientist.literature_review_agent import build_literature_review_agent

async def main():
    # 1. Define a VERY specific, narrow goal to limit scope
    goal = "What are the main herbicide resistance mechanisms in Palmer Amaranth?"
    print(f"🔬 Starting test run for: {goal}")

    # 2. Initialize State
    initial_state = CoscientistState(goal=goal)
    
    # 3. Initialize Config and FORCE the LLM to OpenAI GPT-4o
    llm = ChatOpenAI(model="gpt-4o")
    print(f"🤖 Using LLM: {getattr(llm, 'model_name', 'unknown')}")
    
    config = CoscientistConfig(literature_review_agent_llm=llm)
    
    # 4. Setup Framework
    state_manager = CoscientistStateManager(initial_state)
    cosci = CoscientistFramework(config, state_manager)

    # 5. Run just the first phase manually (Literature Review only)
    print("📚 Starting mini literature review (limit: 1 subtopic)...")
    
    # Manually trigger a small review
    lit_agent = build_literature_review_agent(llm)
    
    # Limit to 1 subtopic only!
    initial_lit_state = state_manager.next_literature_review_state(max_subtopics=1)
    
    final_lit_state = await lit_agent.ainvoke(initial_lit_state)
    state_manager.update_literature_review(final_lit_state)
    
    print("\n✅ Literature Review Complete!")
    print("Subtopics found:", final_lit_state.get('subtopics'))
    print("\n--- Report Preview ---\n")
    print(final_lit_state.get('meta_review')[:1000] + "...")
    print("\n----------------------")

if __name__ == "__main__":
    asyncio.run(main())
