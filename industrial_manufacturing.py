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

    conditions = input("Enter manufacturing conditions separated by spaces: ").lower().split()

    for condition in conditions:
        kb.add_fact(condition)

    kb.add_rule(["machine_on", "raw_material_available"], "production_start")
    kb.add_rule(["machine_overheated"], "machine_stop")
    kb.add_rule(["low_oil", "machine_running"], "maintenance_required")
    kb.add_rule(["high_vibration", "machine_running"], "machine_inspection")
    kb.add_rule(["quality_issue", "machine_running"], "production_stop")
    kb.add_rule(["machine_on", "raw_material_available", "quality_ok"], "production_continue")
    kb.add_rule(["machine_running", "temperature_normal"], "machine_safe")

    print("\nForward Chaining:")
    derived_facts = kb.forward_chaining()

    actions = [
        "production_start",
        "machine_stop",
        "maintenance_required",
        "machine_inspection",
        "production_stop",
        "production_continue",
        "machine_safe"
    ]

    found = False

    for action in actions:
        if action in derived_facts:
            print("Manufacturing action:", action)
            found = True

    if not found:
        print("No manufacturing action could be determined.")

    print("\nBackward Chaining:")

    for action in actions:
        if kb.backward_chaining(action):
            print("Manufacturing action:", action)


if __name__ == "__main__":
    main()