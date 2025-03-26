# Geopolitics Simulator

A sophisticated agent-based simulation of international relations using LLM-powered decision making. This project aims to create emergent geopolitical behavior through language-based rules rather than purely mathematical ones.

## Current Status

The project is in active development, with Phase 4 completed. Current features include:

### Implemented Features (✅)
- **Core Country System**
  - Basic attributes (name, strength, ideology)
  - Relationship management (allies, enemies)
  - State machine (peace, war)

- **World Simulation**
  - Turn-based system
  - Event logging
  - War resolution mechanics

- **Agent System**
  - Personality-based behavior (Aggressive, Cautious, Neutral)
  - LLM-powered decision making
  - Action generation and execution

- **Action System**
  - Declare war
  - Propose alliances
  - Help other countries
  - Basic war resolution

### Planned Features (🚧)
- Enhanced state representation with sentiment tracking
- Historical context and memory
- Strategic goals and sophisticated decision making
- Economic system with resources and trade
- Network visualization of relationships
- Historical scenarios and templates
- Profile system for countries

## Project Structure
```
geopolitics-simulator/
├── models/           # Core data models
│   ├── country.py   # Country representation
│   └── world.py     # World state management
├── agents/          # Agent system
│   ├── base_agent.py    # Base agent class
│   └── llm_agent.py     # LLM-powered agent
├── actions/         # Action system
│   ├── base_action.py   # Base action class
│   └── specific_actions.py  # Concrete actions
├── simulation/      # Simulation engine
│   └── engine.py    # Main simulation logic
├── examples/        # Usage examples
│   └── run_simulation.py    # Basic simulation
└── tests/          # Test suite
```

## Setup

1. Install dependencies:
```bash
pip install -e .
```

2. Configure LLM endpoint:
```python
llm_config = {
    "base_url": "your_endpoint_url",
    "api_key": "your_api_key"
}
```

3. Run example simulation:
```bash
python examples/run_simulation.py
```

## Current Simulation Example

The simulation currently models a Cold War-like scenario with:
- USA (Democratic, Cautious)
- USSR (Communist, Aggressive)
- UK (Democratic, Neutral)
- France (Democratic, Cautious)
- Germany (Fascist, Aggressive)

Each country makes decisions based on:
- Their personality type
- Current world state
- Ideological alignment
- Other countries' actions

## Development Status

- ✅ Phase 1: Core Environment
- ✅ Phase 2: Simple Agent System
- ✅ Phase 3: Action System
- ✅ Phase 4: Simulation Engine
- 🚧 Phase 5: Enhanced State Representation
- 🚧 Phase 6: Improved LLM Integration
- 🚧 Phase 7: Visualization
- 🚧 Phase 8: Profile System

## Contributing

The project is in active development. Key areas for contribution:
1. Enhanced state representation
2. Historical context integration
3. Economic system implementation
4. Visualization tools
5. Historical scenarios

## License

MIT License 