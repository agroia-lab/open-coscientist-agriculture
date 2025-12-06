import os
from coscientist.global_state import CoscientistState

# The goal string used in run_agriculture_research.py
GOAL = (
    "In industrial tomato grown under Mediterranean-type climatic conditions, "
    "with emphasis on Chile’s Central Valley, what is the current status and distribution "
    "of Phelipanche ramosa resistance to ALS‑inhibiting herbicides, and which alternative "
    "herbicide modes of action—including experimental or not‑yet‑registered molecules "
    "(such as maleic hydrazide and prohexadione‑calcium) and mixtures—show potential "
    "for crop‑safe control of P. ramosa from the seedbank and germination phases through "
    "to parasite attachment (with secondary consideration of later stages), with the aim "
    "of generating testable hypotheses and designing field and greenhouse trials?"
)

def export_report():
    print(f"📂 Searching for research data for goal:\n{GOAL[:50]}...")
    
    # Load the state
    try:
        state = CoscientistState.load_latest(goal=GOAL)
    except Exception as e:
        print(f"❌ Could not find state: {e}")
        return

    if not state:
        print("❌ No state found. Did the research finish?")
        return

    # Extract Report
    if state.final_report and "result" in state.final_report:
        report_content = state.final_report["result"]
        filename = "Final_Report_Tomato_Broomrape.md"
        
        with open(filename, "w") as f:
            f.write(report_content)
            
        print(f"\n✅ Report exported successfully to: {os.path.abspath(filename)}")
        print(f"📝 Length: {len(report_content)} characters")
    else:
        print("⚠️  Research state found, but Final Report is not ready yet.")
        print("   Status: Still running or failed before report generation.")

if __name__ == "__main__":
    export_report()

