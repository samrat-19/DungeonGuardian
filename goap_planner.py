from collections import deque


class Action:
    def __init__(self, name, preconditions, effects, cost=1):
        self.name = name
        self.preconditions = preconditions  # Dict
        self.effects = effects              # Dict
        self.cost = cost

    def is_applicable(self, state):
        return all(
            k in state and (v(state[k]) if callable(v) else state[k] == v)
            for k, v in self.preconditions.items()
        )

    def apply(self, state):
        new_state = state.copy()
        for k, v in self.effects.items():
            new_state[k] = v(new_state[k]) if callable(v) else v
        return new_state


# All available actions
ACTIONS = [
    Action("HealSelf", {"hasPotion": True, "health": lambda h: h < 100},
           {"health": 100, "hasPotion": False}),
    Action("AttackEnemy", {"enemyNearby": True},
           {"enemyNearby": False, "stamina": lambda s: max(0, s - 5)}),
    Action("Retreat", {"inSafeZone": False},
           {"inSafeZone": True}),
    Action("DefendTreasure", {},
           {"treasureThreatLevel": "low"}),
    Action("CallBackup", {},
           {"backupCalled": True}),
    Action("SearchForPotion", {},
           {"hasPotion": True}),
]


def evaluate_conditions(conditions, state):
    for k, v in conditions.items():
        current = state.get(k, 0)
        if callable(v):
            if not v(current):
                return False
        elif current != v:
            return False
    return True


class GOAPPlanner:
    def __init__(self, actions=ACTIONS):
        self.actions = actions
        self.goal_state_map = {
            "Survive": {"health": lambda h: h > 50},
            "EliminateThreat": {"enemyNearby": False},
            "ProtectTreasure": {"treasureThreatLevel": "low"},
            "PrepareForBattle": {"hasPotion": True, "stamina": lambda s: s > 10},
        }

    # Use BFS for finding the shortest path
    def plan(self, world_state, goal):
        desired_state = self.goal_state_map.get(goal, {})
        if not desired_state:
            return []

        queue = deque()
        queue.append((world_state, []))

        visited = set()

        while queue:
            current_state, plan_so_far = queue.popleft()
            state_key = frozenset(current_state.items())
            if state_key in visited:
                continue
            visited.add(state_key)

            if evaluate_conditions(desired_state, current_state):
                return plan_so_far

            for action in self.actions:
                if evaluate_conditions(action.preconditions, current_state):
                    next_state = apply_effects(current_state, action.effects)
                    queue.append((next_state, plan_so_far + [action]))

        return []

def apply_effects(current_state, effects):
    new_state = current_state.copy()
    for k, v in effects.items():
        current_value = new_state.get(k, 0)
        new_state[k] = v(current_value) if callable(v) else v
    return new_state