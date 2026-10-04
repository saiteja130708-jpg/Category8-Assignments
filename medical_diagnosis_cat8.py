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
                if all(self.backward_chaining(condition, visited) for condition in rule.conditions):
                    return True

        return False


def main():
    kb = KnowledgeBase()

    symptoms = input("Enter symptoms separated by spaces: ").lower().split()

    for symptom in symptoms:
        kb.add_fact(symptom)

    kb.add_rule(["fever", "cough", "body_pain"], "flu")
    kb.add_rule(["fever", "cough", "breathing_problem"], "pneumonia")
    kb.add_rule(["sneezing", "runny_nose", "headache"], "common_cold")
    kb.add_rule(["fever", "rash", "joint_pain"], "dengue")
    kb.add_rule(["sore_throat", "cough", "fever"], "throat_infection")

    print("\nForward Chaining:")
    derived_facts = kb.forward_chaining()

    diagnoses = ["flu", "pneumonia", "common_cold", "dengue", "throat_infection"]

    found = False

    for diagnosis in diagnoses:
        if diagnosis in derived_facts:
            print("Possible diagnosis:", diagnosis)
            found = True

    if not found:
        print("No diagnosis could be determined.")

    print("\nBackward Chaining:")
    for diagnosis in diagnoses:
        if kb.backward_chaining(diagnosis):
            print("Possible diagnosis:", diagnosis)


if __name__ == "__main__":
    main()