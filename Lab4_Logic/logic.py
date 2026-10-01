from collections import deque


class Action:
    def __init__(self, name, positive_preconditions, negative_preconditions,
                 positive_effects, negative_effects):
        self.name = name
        self.positive_preconditions = set(positive_preconditions)
        self.negative_preconditions = set(negative_preconditions)
        self.positive_effects = set(positive_effects)
        self.negative_effects = set(negative_effects)

    def is_applicable(self, state):
        return (
            self.positive_preconditions.issubset(state)
            and self.negative_preconditions.isdisjoint(state)
        )

    def apply(self, state):
        new_state = set(state)
        new_state -= self.negative_effects
        new_state |= self.positive_effects
        return frozenset(new_state)

    def __str__(self):
        return self.name


def bfs_plan(initial_state, goal, actions):
    initial_state = frozenset(initial_state)
    goal = set(goal)

    queue = deque()
    queue.append((initial_state, [], [initial_state]))

    visited = {initial_state}

    while queue:
        state, plan, states = queue.popleft()

        if goal.issubset(state):
            return plan, states

        for action in actions:
            if action.is_applicable(state):
                new_state = action.apply(state)

                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((
                        new_state,
                        plan + [action],
                        states + [new_state]
                    ))

    return None, None


initial_state = {
    "At(Robot,A)",
    "At(Package,A)"
}

goal = {
    "At(Package,C)"
}


actions = [
    Action(
        "Move(A,B)",
        {"At(Robot,A)"},
        set(),
        {"At(Robot,B)"},
        {"At(Robot,A)"}
    ),

    Action(
        "Move(B,A)",
        {"At(Robot,B)"},
        set(),
        {"At(Robot,A)"},
        {"At(Robot,B)"}
    ),

    Action(
        "Move(B,C)",
        {"At(Robot,B)"},
        set(),
        {"At(Robot,C)"},
        {"At(Robot,B)"}
    ),

    Action(
        "Move(C,B)",
        {"At(Robot,C)"},
        set(),
        {"At(Robot,B)"},
        {"At(Robot,C)"}
    ),

    Action(
        "PickUp(Package,A)",
        {"At(Robot,A)", "At(Package,A)"},
        {"Holding(Package)"},
        {"Holding(Package)"},
        {"At(Package,A)"}
    ),

    Action(
        "PickUp(Package,B)",
        {"At(Robot,B)", "At(Package,B)"},
        {"Holding(Package)"},
        {"Holding(Package)"},
        {"At(Package,B)"}
    ),

    Action(
        "PickUp(Package,C)",
        {"At(Robot,C)", "At(Package,C)"},
        {"Holding(Package)"},
        {"Holding(Package)"},
        {"At(Package,C)"}
    ),

    Action(
        "Drop(Package,A)",
        {"At(Robot,A)", "Holding(Package)"},
        set(),
        {"At(Package,A)"},
        {"Holding(Package)"}
    ),

    Action(
        "Drop(Package,B)",
        {"At(Robot,B)", "Holding(Package)"},
        set(),
        {"At(Package,B)"},
        {"Holding(Package)"}
    ),

    Action(
        "Drop(Package,C)",
        {"At(Robot,C)", "Holding(Package)"},
        set(),
        {"At(Package,C)"},
        {"Holding(Package)"}
    )
]


plan, states = bfs_plan(initial_state, goal, actions)

if plan is None:
    print("No plan found")
else:
    print("Plan found:\n")

    print("S0:", sorted(states[0]))

    for i, action in enumerate(plan, start=1):
        print(f"{i}. {action}")
        print(f"S{i}:", sorted(states[i]))