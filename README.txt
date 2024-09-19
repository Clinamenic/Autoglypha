# Autoglypha: Glyph-based Cellular Automata Animation Generator

Autoglypha is a Python script that generates animated GIFs of cellular automata using glyphs (characters) instead of traditional cells. This creates unique, text-based visual patterns that evolve over time.

This README provides a comprehensive guide on how to set up and use the Autoglypha script. It covers installation, usage, customization options, and basic troubleshooting. You may want to adjust some sections based on your specific project structure or add more details about the cellular automata concepts for users who might be unfamiliar with them.

## Prerequisites

- Python 3.6 or higher
- Pillow library (for image processing)

## Installation

1. Clone this repository or download the `autoglypha.py` script.

2. Install the required dependencies:

```
pip install Pillow
```

3. (Optional) Create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate # On Windows, use venv\Scripts\activate
```

## Usage

1. Place your initial grid configuration in a text file (e.g., `opencivics_logo.txt`) in the `static/grid_init/` directory. Use numbers 1-5 to represent different states.

2. Customize the script parameters in `autoglypha.py`:
- Adjust grid dimensions (`GRID_WIDTH`, `GRID_HEIGHT`)
- Modify cell size (`CELL_WIDTH`, `CELL_HEIGHT`)
- Change font size (`FONT_SIZE`)
- Set the number of iterations (`ITERATIONS`)
- Adjust frame duration (`FRAME_DURATION`)
- Choose a font (`FONT_FAMILY`)
- Set background color (`BACKGROUND_COLOR`)
- Select animation mode (`ANIMATION_MODE`)
- Set initial and final linger frames (`INITIAL_LINGER_FRAMES`, `FINAL_LINGER_FRAMES`)
- Customize states and their corresponding glyphs and colors (`STATES`)
- Choose a ruleset (`CHOSEN_RULESET`)

3. Run the script:

```
python autoglypha.py
```

4. The generated GIF will be saved in the `output/` directory.

## Customization

### States and Glyphs

Modify the `STATES` dictionary to change the glyphs and colors for each state:

```python
STATES = {
 1: {'glyph': '1', 'color': '#FFFFFF'},
 2: {'glyph': '2', 'color': '#FAF9F6'},
 # Add more states as needed
}

### Rulesets

Choose from existing rulesets or create your own in the RULESETS dictionary:

```
RULESETS = {
    'default': lambda cell, neighbors: ...,
    'inverse': lambda cell, neighbors: ...,
    # Add your custom rulesets here
}
```

Set the CHOSEN_RULESET variable to select which ruleset to use.

### Animation Modes

1: Normal animation
2: Reversed animation
3: Boomerang effect (forward then backward)

###Output

The script generates a GIF file with the naming convention:

autoglypha_{CHOSEN_RULESET}_mode{ANIMATION_MODE}_linger{INITIAL_LINGER_FRAMES}_{FINAL_LINGER_FRAMES}.gif

### Troubleshooting

If you encounter font-related issues, ensure the specified font file exists or fall back to a system font.
For any import errors, make sure all required libraries are installed.

### License

[Specify your license here]