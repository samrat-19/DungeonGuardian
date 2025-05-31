# class WorldState:
#     def __init__(self, state_dict):
#         self.state = state_dict
#
#     def copy(self):
#         return self.state.copy()

class WorldState:
    def __init__(self, state_dict):
        self.state = state_dict

    def copy(self):
        return WorldState(self.state.copy())

    def get(self, key, default=None):
        return self.state.get(key, default)

    def items(self):
        return self.state.items()

    def __getitem__(self, key):
        return self.state[key]

    def __setitem__(self, key, value):
        self.state[key] = value

    def __contains__(self, key):
        return key in self.state

    def to_dict(self):
        return self.state


class Simulation:
    def __init__(self, world_state):
        self.world_state = world_state

    def execute_plan(self, plan):
        print("\n🚀 Executing Plan:")
        for action in plan:
            if action.is_applicable(self.world_state.state):
                print(f" 👉 Executing: {action.name}")
                self.world_state = action.apply(self.world_state)
            else:
                print(f" ❌ Cannot execute: {action.name} (preconditions not met)")

        print("\n✅ Final World State:")
        for k, v in self.world_state.items():
            print(f"  {k}: {v}")