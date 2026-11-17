"""Independent toy portfolio demo: exhaustive constrained multi-period search."""
import argparse
import itertools
import json
from pathlib import Path

def step(scenario, state, demand, decision):
    cash, electric, emissions, served_total = state
    fare, conversion = decision
    electric += conversion
    if electric > scenario["total_vehicles"]:
        return None
    capacity = (scenario["total_vehicles"] - electric) * 7 + electric * 9
    served = min(max(0, demand - (fare - 4) * 3), capacity)
    cost = 16 + (scenario["total_vehicles"] - electric) * 6 + electric * 3 + conversion * 45
    cash += served * fare - cost
    if cash < scenario["minimum_cash"]:
        return None
    emissions += (scenario["total_vehicles"] - electric) * 8 + electric * 2
    return cash, electric, emissions, served_total + served

def solve(scenario):
    actions = list(itertools.product(scenario["fares"], scenario["conversions"]))
    initial = (scenario["initial_cash"], scenario["initial_electric"], 0, 0)
    best = None
    feasible = 0
    evaluated = 0
    for plan in itertools.product(actions, repeat=scenario["periods"]):
        evaluated += 1
        state = initial
        trace = []
        for demand, choice in zip(scenario["demand"], plan, strict=True):
            state = step(scenario, state, demand, choice)
            if state is None:
                break
            trace.append(dict(zip(("cash", "electric", "emissions", "served"), state)))
        if state is None:
            continue
        feasible += 1
        cash, electric, emissions, served = state
        objective = cash + 2 * served - 3 * emissions
        if best is None or objective > best["objective"]:
            best = {"objective": objective, "decisions": [{"fare": a, "conversion": b} for a,b in plan], "trace": trace}
    if best is None:
        raise ValueError("No feasible plan")
    return {"evidence": "synthetic_only", "evaluated": evaluated, "feasible": feasible, "best": best}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario", type=Path)
    args = parser.parse_args()
    print(json.dumps(solve(json.loads(args.scenario.read_text())), indent=2))
