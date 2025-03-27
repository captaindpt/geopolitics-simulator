# Geopolitics Simulator

A Python-based simulation of geopolitical interactions between countries, using language-based rules and LLM-powered decision making.

## Project Structure

```
geopolitics-simulator/
├── src/
│   ├── models/      # Core data models
│   ├── agents/      # Agent implementations
│   ├── actions/     # Action definitions
│   ├── simulation/  # Simulation engine
│   └── visualization/ # Visualization tools
├── tests/           # Test files
├── examples/        # Example simulations
└── requirements.txt # Project dependencies
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your HuggingFace API key
```

## Running Tests

```bash
pytest tests/
pytest --cov=src tests/  # Run with coverage
```

## Running Examples

```bash
python examples/basic_simulation.py
```

## Development Status

Currently in Phase 1: Core Environment
- [x] Country class implementation
- [x] World class implementation
- [x] Basic tests
- [ ] Agent system (next phase) 