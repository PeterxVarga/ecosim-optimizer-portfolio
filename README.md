# EcoSim-inspired decision optimization — portfolio demo

A small, independently reconstructed demonstration inspired by the decision-support workflow used in a university business simulation project. It illustrates constrained multi-period scenario search, financial modeling and independent result replay with fictional data.

**Scope:** This is a synthetic portfolio demonstration, not the original competition engine, official EcoSim software, an actual competition strategy or a reproduction of official scoring rules. All parameters were invented for this example. The original private research repository and competition data are not included. AI-assisted implementation.

## Run locally

Requires Python 3.10+ and Node.js 18+. No third-party packages, accounts or network access.

```sh
python3 optimizer.py fixtures/scenario.json > result.json
node verify.mjs fixtures/scenario.json result.json
python3 -m unittest discover -s tests
```

The Python engine exhaustively enumerates a toy three-period decision space, filters infeasible plans by electric-fleet capacity and minimum cash, and selects the best objective in that finite set. The JavaScript validator independently replays the chosen path and checks the constraints, intermediate balances and objective. Its replay does not independently prove global optimality. The score is arbitrary and not an EcoSim score.

## Repository boundaries

No authenticated browser access, real game inputs, account information, private strategies, vendor code or competition API identifiers. No external dependencies or write access to competition systems.
