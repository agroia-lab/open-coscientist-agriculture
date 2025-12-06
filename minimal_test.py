"""
Minimal test to verify the CoScientist system components work.
Tests: OpenAI API, Tavily search, and basic agent setup.
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_openai():
    """Test OpenAI API connection"""
    print("🔍 Testing OpenAI API...")
    from langchain_openai import ChatOpenAI
    
    llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=50)
    response = await llm.ainvoke("Say 'OpenAI works!' in exactly 3 words.")
    print(f"   ✅ OpenAI: {response.content}")
    return True

async def test_tavily():
    """Test Tavily search API"""
    print("🔍 Testing Tavily Search API...")
    from tavily import TavilyClient
    
    client = TavilyClient()
    result = client.search("Palmer amaranth herbicide resistance", max_results=2)
    print(f"   ✅ Tavily: Found {len(result.get('results', []))} results")
    return True

async def test_literature_agent():
    """Test basic literature review agent initialization"""
    print("🔍 Testing Literature Review Agent...")
    from coscientist.literature_review_agent import build_literature_review_agent
    from langchain_openai import ChatOpenAI
    
    llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=500)
    agent = build_literature_review_agent(llm)
    print(f"   ✅ Literature Agent: Initialized successfully")
    return True

async def test_simple_research():
    """Run a minimal research query"""
    print("🔍 Testing Simple Research Query (this may take 30-60 seconds)...")
    from gpt_researcher import GPTResearcher
    
    # Force OpenAI models
    os.environ["FAST_LLM"] = "openai:gpt-4o-mini"
    os.environ["SMART_LLM"] = "openai:gpt-4o-mini"
    os.environ["STRATEGIC_LLM"] = "openai:gpt-4o-mini"
    
    researcher = GPTResearcher(
        query="What is Palmer amaranth?",
        report_type="brief_report"
    )
    
    # Just run the research (minimal)
    context = await researcher.conduct_research()
    print(f"   ✅ GPT Researcher: Gathered {len(context)} characters of context")
    
    # Generate a brief report
    report = await researcher.write_report()
    print(f"   ✅ Report generated: {len(report)} characters")
    print(f"\n   📝 Report Preview:\n   {report[:300]}...")
    return True

async def main():
    print("=" * 60)
    print("🧪 MINIMAL TEST - Open CoScientist Agents")
    print("=" * 60)
    print(f"\n📌 Models being used:")
    print(f"   - Main LLM: gpt-4o-mini (OpenAI)")
    print(f"   - Search: Tavily")
    print()
    
    tests = [
        ("OpenAI API", test_openai),
        ("Tavily Search", test_tavily),
        ("Literature Agent", test_literature_agent),
        ("Simple Research", test_simple_research),
    ]
    
    results = {}
    for name, test_fn in tests:
        try:
            results[name] = await test_fn()
        except Exception as e:
            print(f"   ❌ {name} FAILED: {e}")
            results[name] = False
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status}: {name}")
    
    all_passed = all(results.values())
    print("\n" + ("🎉 All tests passed! System is ready." if all_passed else "⚠️ Some tests failed. Check errors above."))
    return all_passed

if __name__ == "__main__":
    asyncio.run(main())

