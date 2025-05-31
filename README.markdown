# DungeonGuardian

DungeonGuardian is a Python-based project that implements a **Goal-Oriented Action Planning (GOAP)** system integrated with a Large Language Model (LLM) to simulate intelligent decision-making for a guardian character in a dungeon-like environment. The system evaluates world states, selects goals based on priorities, plans actions to achieve those goals, and executes them in a simulated environment.

## How It Works

### Overview
The project simulates a guardian's decision-making process in a dungeon scenario. The guardian assesses the world state (e.g., health, stamina, enemy presence, treasure threat level) and uses an LLM to select a goal based on predefined priorities. A GOAP planner then generates a sequence of actions to achieve the chosen goal, and a simulation executes the plan, updating the world state.

### Key Components
1. **World State Management (`simulations.py`)**
   - The `WorldState` class manages the current state of the world (e.g., `health`, `stamina`, `enemyNearby`).
   - It supports querying, updating, and copying the state for planning purposes.

2. **LLM Integration (`call_llm.py`, `llm_cognitive.py`)**
   - The `call_llm.py` script interfaces with an LLM API (running locally at `http://localhost:11434/api/generate`) to generate responses.
   - The `llm_cognitive.py` script formats the world state into a prompt, uses `goal_prompt.txt` to define rules and priorities, and queries the LLM to select a goal and provide reasoning in JSON format.

3. **GOAP Planner (`goap_planning.py`)**
   - The `GOAPPlanner` class uses Breadth-First Search (BFS) to find the shortest sequence of actions to achieve a goal.
   - Actions (e.g., `HealSelf`, `AttackEnemy`) have preconditions and effects, ensuring they are only applied when valid.
   - Goals are mapped to desired world states (e.g., `Survive` requires `health > 50`).

4. **Simulation (`simulations.py`)**
   - The `Simulation` class executes the planned actions, applying their effects to the world state if preconditions are met.
   - It logs the execution process and final world state.

5. **Main Script (`guardian.py`)**
   - Loads a scenario from `scenarios.json`.
   - Calls the LLM to select a goal and reason.
   - Uses the GOAP planner to generate a plan.
   - Executes the plan in the simulation.

6. **Scenarios (`scenarios.json`)**
   - Defines initial world states for different scenarios (e.g., `scenario1` with `health: 60`, `treasureThreatLevel: "medium"`).
   - Scenarios drive the simulation by providing the starting conditions.

### Goal Selection and Reasoning
The LLM selects one of four goals (`Survive`, `EliminateThreat`, `ProtectTreasure`, `PrepareForBattle`) based on the rules in `goal_prompt.txt`:
- **Survive**: Prioritized if health < 50.
- **PrepareForBattle**: Selected if the guardian has a potion and stamina > 10.
- **EliminateThreat**: Chosen if an enemy is nearby.
- **ProtectTreasure**: Selected if the treasure threat level is medium or high.

The LLM returns a JSON response with the chosen goal and a natural-language explanation, simulating human-like reasoning.

### Action Planning
The GOAP planner evaluates available actions (e.g., `HealSelf`, `AttackEnemy`, `Retreat`) and builds a plan to achieve the selected goal. Each action has:
- **Preconditions**: Conditions that must be true to execute the action (e.g., `hasPotion: True` for `HealSelf`).
- **Effects**: Changes to the world state (e.g., `health: 100`, `hasPotion: False` for `HealSelf`).
- **Cost**: A default cost of 1 (could be extended for weighted planning).

The planner uses BFS to ensure the shortest valid plan is found.

## Simulating Reasoning with LLM
The LLM (assumed to be LLaMA 3.1 running locally via Ollama) is queried with a prompt constructed from:
- The current world state (e.g., `health: 60`, `enemyNearby: false`).
- The rules and priorities defined in `goal_prompt.txt`.

The LLM processes the prompt and returns a JSON object with:
- `goal`: The selected goal.
- `reason`: A natural-language explanation of why the goal was chosen.

If the LLM fails to respond or returns invalid JSON, the system retries up to 5 times before defaulting to the `Survive` goal with a fallback reason.

## How to Run
### Prerequisites
1. **Python 3.8+**: Ensure Python is installed.
2. **Ollama LLM Server**:
   - Install [Ollama](https://ollama.ai/) and run it locally.
   - Pull and run the `llama3.1` model: `ollama pull llama3.1` and `ollama run llama3.1`.
   - Ensure the server is running at `http://localhost:11434`.
3. **Dependencies**:
   - Install required Python packages: `pip install requests`.
4. **Project Files**:
   - Ensure all provided files (`call_llm.py`, `goal_prompt.txt`, `goap_planning.py`, `guardian.py`, `llm_cognitive.py`, `scenarios.json`, `simulations.py`) are in the same directory.

### Running the Project
1. Start the Ollama server:
   ```bash
   ollama run llama3.1
   ```
2. Run the main script with a scenario name:
   ```bash
   python guardian.py scenario1
   ```
   - Replace `scenario1` with the desired scenario name defined in `scenarios.json`.
3. The script will:
   - Load the scenario from `scenarios.json`.
   - Query the LLM to select a goal and provide reasoning.
   - Generate a plan using the GOAP planner.
   - Execute the plan in the simulation and print the results.

### Example Command
```bash
python guardian.py scenario1
```


## Notes
- Ensure the Ollama server is running before executing the script.
- Add more scenarios to `scenarios.json` to test different world states.
- Extend the `ACTIONS` list in `goap_planning.py` to support more complex behaviors.
- The LLM's reasoning quality depends on the model's performance and the clarity of `goal_prompt.txt`.