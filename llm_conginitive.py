# llm_cognitive.py

import json
import time
from call_llm import call_llm  # Ensure call_llm.py is in a separate file or define here

GOALS = ["Survive", "EliminateThreat", "ProtectTreasure", "PrepareForBattle"]

def world_state_to_prompt(state_dict):
    return "\n".join([f"{k}: {v}" for k, v in state_dict.items()])

def generate_goal_and_reason(world):
    """
    Uses the LLM to decide on the best goal and justify it in natural language.
    """
    state_prompt = world_state_to_prompt(world.state)

    with open("goal_prompt.txt", "r") as file:
        prompt_template = file.read()

    prompt = prompt_template.format(
        state_prompt=state_prompt,
        GOALS=GOALS
    )

    max_retries = 5
    for _ in range(max_retries):
        try:
            response = call_llm(prompt)
            parsed = json.loads(response)
            goal = parsed.get("goal")
            reason = parsed.get("reason")

            if goal is not None and reason is not None:
                return goal, reason
        except Exception:
            pass
        time.sleep(1)

    return "Survive", "Defaulted to survival due to repeated errors."