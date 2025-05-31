from llm_conginitive import generate_goal_and_reason
from goap_planner import GOAPPlanner
from simulation import WorldState, Simulation
import json
import sys

def load_scenario(name):
    with open('scenarios.json') as f:
        scenarios = json.load(f)
    return scenarios[name]

def main():
    if len(sys.argv) < 2:
        print("Usage: python guardian.py <scenario_name>")
        return

    scenario_name = sys.argv[1]
    world_data = load_scenario(scenario_name)
    world = WorldState(world_data)

    # Step 1: Generate goal + reason using LLM
    goal, reason = generate_goal_and_reason(world)
    print(f"\n🎯 Goal: {goal}\n🧠 Reasoning: {reason}\n")

    # Step 2: Plan
    planner = GOAPPlanner()
    plan = planner.plan(world, goal)

    if not plan:
        print("⚠️ No valid plan found.")
        return

    print("\n📜 Plan:")
    for step in plan:
        print(f" - {step.name}")

    # Step 3: Execute
    sim = Simulation(world)
    sim.execute_plan(plan)

if __name__ == "__main__":
    main()