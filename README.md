
# Blackjack Card Counting Simulator

## Overview

This project is a Monte Carlo simulation-based Blackjack card counting simulator written in Python. It allows users to simulate blackjack games using various card counting strategies to estimate the effectiveness of these strategies through metrics such as Expected Value (EV) and Risk of Ruin (RoR).

## Features

- Simulate thousands of hands of blackjack to estimate card counting efficiency
- Implementations of popular card counting systems (Hi-Lo, KO, etc.)
- Calculation of EV and RoR for different strategies and conditions
- Flexible game rules to simulate different casino settings
- Command-line interface for easy use and configuration

## Installation

To run the simulation, you will need Python 3.x installed on your computer. After you have Python set up, clone this repository using Git:

```bash
git clone https://github.com/jtth3brick/blackjack-simulator.git
cd blackjack-simulator
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To start a simulation, run the `main.py` file with Python. You can configure the simulation parameters by editing the `config.json` file or by passing arguments on the command line.

```bash
python main.py
```

## Configuration

You can adjust the simulation settings such as the number of decks, the betting spread, and the counting system by modifying the `config.json` file.

Example `config.json`:

```json
{
    "decks": 6,
    "spread": [1, 8],
    "count_system": "Hi-Lo",
    "rounds": 10000,
    "players": 1
}
```

## Simulation Output

The simulation will output the results including the total hands played, total amount bet, total amount won, and overall win/loss ratio. A detailed statistical analysis will be printed out containing the EV and RoR.

## Development

This simulator is structured into several modules:

- `card_utils.py`: Utilities for handling cards and decks.
- `utils.py`: General utility functions.
- `player.py`: Definitions for player actions and strategies.
- `game.py`: Game flow logic.
- `simulator.py`: Simulation execution.
- `strategy.py`: Strategy definitions and implementations.
- `statistics.py`: Statistical analysis functions.
- `visualization.py`: (Optional) Visualization of results.

You can contribute to the project by submitting pull requests via GitHub.

## Testing

Unit tests are available in the `tests/` directory. To run the tests, use the following command:

```bash
python -m unittest discover -s tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to anyone whose code was used as inspiration.
- Special thanks to the contributors of this project.

## Disclaimer

This simulator is intended for educational and research purposes only. The use of simulation and card counting systems in actual casinos may be subject to legal restrictions and is not endorsed by the creators of this simulator.
