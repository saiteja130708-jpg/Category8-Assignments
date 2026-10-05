class Rule:
    def __init__(self, conditions, conclusion):
        self.conditions = conditions
        self.conclusion = conclusion

class KnowledgeBase:
    def __init__(self):
        self.facts = set()
        self.rules = []

    def add_fact(self, fact):
        self.facts.add(fact)

    def add_rule(self, conditions, conclusion):
        self.rules.append(Rule(conditions, conclusion))

    def forward_chaining(self):
        changed = True

        while changed:
            changed = False

            for rule in self.rules:
                if all(condition in self.facts for condition in rule.conditions):
                    if rule.conclusion not in self.facts:
                        self.facts.add(rule.conclusion)
                        changed = True

        return self.facts

    def backward_chaining(self, goal, visited=None):
        if visited is None:
            visited = set()

        if goal in self.facts:
            return True

        if goal in visited:
            return False

        visited.add(goal)

        for rule in self.rules:
            if rule.conclusion == goal:
                if all(self.backward_chaining(condition, visited)
                       for condition in rule.conditions):
                    return True

        return False


def main():
    kb = KnowledgeBase()

    sensors = input("Enter vehicle conditions separated by spaces: ").lower().split()

    for sensor in sensors:
        kb.add_fact(sensor)

    kb.add_rule(["red_light"], "stop")
    kb.add_rule(["green_light", "road_clear"], "move")
    kb.add_rule(["obstacle", "moving"], "brake")
    kb.add_rule(["obstacle", "moving"], "avoid_obstacle")
    kb.add_rule(["pedestrian", "road_clear"], "slow_down")
    kb.add_rule(["rain", "road_wet"], "reduce_speed")
    kb.add_rule(["green_light", "road_clear", "no_obstacle"], "safe_to_move")

    print("\nForward Chaining:")
    derived_facts = kb.forward_chaining()

    actions = [
        "stop",
        "move",
        "brake",
        "avoid_obstacle",
        "slow_down",
        "reduce_speed",
        "safe_to_move"
    ]

    found = False

    for action in actions:
        if action in derived_facts:
            print("Vehicle action:", action)
            found = True

    if not found:
        print("No action could be determined.")

    print("\nBackward Chaining:")

    for action in actions:
        if kb.backward_chaining(action):
            print("Vehicle action:", action)

if __name__ == "__main__":
    main()