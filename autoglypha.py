import random
from PIL import Image, ImageDraw, ImageFont
import os

# Get the directory of the script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Customizable parameters
GRID_WIDTH = 160
GRID_HEIGHT = 88
CELL_WIDTH = 15
CELL_HEIGHT = 25
FONT_SIZE = 14
ITERATIONS = 50
FRAME_DURATION = 120
FONT_FAMILY = os.path.join(SCRIPT_DIR, 'static', 'font', 'GeistMono-Regular.otf'), 'Arial'
BACKGROUND_COLOR = '#4EFA9F'

# Animation mode
# 1: Normal, 2: Reversed, 3: Boomerang
ANIMATION_MODE = 3

# Linger frames (how many frames to hold on initial and final states)
INITIAL_LINGER_FRAMES = 10
FINAL_LINGER_FRAMES = 5

# States and corresponding glyphs and colors,
STATES = {
    1: {'glyph': '1', 'color': '#FFFFFF'}, # "White"
    2: {'glyph': '2', 'color': '#FAF9F6'}, # "Off White"
    3: {'glyph': '3', 'color': '#4E36E4'}, # "Light OpenCivics Blue"
    4: {'glyph': '4', 'color': '#3D21E8'}, # "OpenCivics Blue"
    5: {'glyph': '5', 'color': '#3D21E8'}, # "OpenCivics Blue"
}

NUM_STATES = len(STATES)

# Define multiple rulesets
RULESETS = {
    'default': lambda cell, neighbors: (cell % NUM_STATES) + 1 if neighbors[(cell % NUM_STATES) + 1] >= 2 else cell,
    'inverse': lambda cell, neighbors: (cell - 2) % NUM_STATES + 1 if neighbors[(cell - 2) % NUM_STATES + 1] >= 2 else cell,
    'random': lambda cell, neighbors: random.randint(1, NUM_STATES) if sum(neighbors.values()) >= 4 else cell,
    'majority': lambda cell, neighbors: max(neighbors, key=neighbors.get) if max(neighbors.values()) > 2 else cell,
    'crystal': lambda cell, neighbors: max(neighbors, key=neighbors.get) if neighbors[max(neighbors, key=neighbors.get)] >= 3 else cell,
    'dynamic': lambda cell, neighbors: (cell % NUM_STATES) + 1 if neighbors[(cell % NUM_STATES) + 1] >= 2 else cell,
    'clusters': lambda cell, neighbors: (cell % NUM_STATES) + 1 if sum(neighbors.values()) % 2 == 0 else (cell - 2) % NUM_STATES + 1,
    'fractal': lambda cell, neighbors: (cell % NUM_STATES) + 1 if len(set(neighbors.values())) > 2 else cell,
    'wave': lambda cell, neighbors: (cell % NUM_STATES) + 1 if abs(cell - sum(neighbors.values()) / len(neighbors)) > 1 else cell,
    'spiral': lambda cell, neighbors: ((cell + sum(neighbors.values()) - 1) % NUM_STATES) + 1 if ((cell + sum(neighbors.values()) - 1) % NUM_STATES) + 1 != cell else (cell % NUM_STATES) + 1,
}

# Choose a ruleset (you can change this to select different rulesets)
CHOSEN_RULESET = 'inverse'

# Read TXT file
def read_txt_grid(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        print("File content:")
        print(content)
        lines = content.strip().split('\n')
        grid = []
        max_width = 0
        for line in lines:
            row = [int(cell) for cell in line if cell in '12345']
            grid.append(row)
            max_width = max(max_width, len(row))
        
        # Pad shorter rows with ones
        for row in grid:
            row.extend([1] * (max_width - len(row)))
        
    return grid

# Apply chosen ruleset
def apply_rules(cell, neighbors):
    return RULESETS[CHOSEN_RULESET](cell, neighbors)

# Initialize grid
def initialize_grid(width, height, txt_file=None):
    if txt_file:
        grid = read_txt_grid(txt_file)
        actual_height = len(grid)
        actual_width = len(grid[0]) if grid else 0
        print(f"Loaded grid dimensions: {actual_width}x{actual_height}")
        print(f"Grid content (first 5 rows):")
        for row in grid[:5]:
            print(row)
        print(f"Specified dimensions: {width}x{height}")
        if actual_height != height or actual_width != width:
            print("Warning: Loaded grid dimensions do not match specified dimensions.")
            print("Adjusting dimensions to match the loaded grid.")
        return grid, actual_width, actual_height
    else:
        return [[random.randint(1, NUM_STATES) for _ in range(width)] for _ in range(height)], width, height
        
# Count neighbors of each state
def count_neighbors(grid, x, y):
    height = len(grid)
    width = len(grid[0]) if grid else 0
    neighbors = {state: 0 for state in STATES.keys()}
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nx, ny = (x + i) % width, (y + j) % height
            if 0 <= ny < height and 0 <= nx < width:
                cell_value = grid[ny][nx]
                if cell_value in STATES:
                    neighbors[cell_value] += 1
    return neighbors

# Update grid
def update_grid(grid):
    height = len(grid)
    width = len(grid[0])
    new_grid = [[1 for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            neighbors = count_neighbors(grid, x, y)
            new_grid[y][x] = apply_rules(grid[y][x], neighbors)
    return new_grid

# Create frame
def create_frame(grid, font):
    height = len(grid)
    width = max(len(row) for row in grid)
    image = Image.new('RGB', (width * CELL_WIDTH, height * CELL_HEIGHT), color=BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)
    
    for y, row in enumerate(grid):
        for x, cell_value in enumerate(row):
            glyph = STATES[cell_value]['glyph']
            color = STATES[cell_value]['color']
            position = (x * CELL_WIDTH + (CELL_WIDTH - FONT_SIZE) // 2, 
                        y * CELL_HEIGHT + (CELL_HEIGHT - FONT_SIZE) // 2)
            draw.text(position, glyph, font=font, fill=color)
    
    return image

# Load font
def load_font():
    for font in FONT_FAMILY:
        print(f"Attempting to load font: {font}")
        try:
            if os.path.isfile(font):
                # If it's a file path, load it directly
                loaded_font = ImageFont.truetype(font, FONT_SIZE)
            else:
                # If it's a system font name, let Pillow find it
                loaded_font = ImageFont.truetype(font, FONT_SIZE)
            print(f"Successfully loaded font: {font}")
            return loaded_font
        except IOError:
            print(f"Could not load font: {font}")
    
    print("All specified fonts failed to load. Falling back to default font.")
    return ImageFont.load_default()

# Main function
def generate_cellular_automata_gif(txt_file=None):
    print(f"Starting cellular automata GIF generation with ruleset: {CHOSEN_RULESET}")
    
    font = load_font()
    
    print("Initializing grid...")
    grid, width, height = initialize_grid(GRID_WIDTH, GRID_HEIGHT, txt_file)
    
    print(f"Actual grid dimensions: {width}x{height}")
    
    print(f"Generating {ITERATIONS} frames...")
    frames = []
    
    # Add initial linger frames
    initial_frame = create_frame(grid, font)
    frames.extend([initial_frame] * INITIAL_LINGER_FRAMES)
    
    # Generate main animation frames
    for i in range(ITERATIONS):
        if i % 10 == 0:
            print(f"Processing frame {i + 1}/{ITERATIONS}")
        frame = create_frame(grid, font)
        frames.append(frame)
        grid = update_grid(grid)
    
    # Add final linger frames
    final_frame = frames[-1]
    frames.extend([final_frame] * FINAL_LINGER_FRAMES)
    
    # Apply animation mode
    if ANIMATION_MODE == 2:
        frames = frames[::-1]
    elif ANIMATION_MODE == 3:
        frames = frames + frames[-2:0:-1]
    
    output_dir = os.path.join(SCRIPT_DIR, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    print("Saving GIF...")
    base_filename = f'autoglypha_{CHOSEN_RULESET}_mode{ANIMATION_MODE}_linger{INITIAL_LINGER_FRAMES}_{FINAL_LINGER_FRAMES}.gif'
    output_file = os.path.join(output_dir, base_filename)

    file_number = 1
    while os.path.exists(output_file):
        file_number += 1
        filename, extension = os.path.splitext(base_filename)
        output_file = os.path.join(output_dir, f"{filename}({file_number}){extension}")

    frames[0].save(output_file, 
                save_all=True, 
                append_images=frames[1:], 
                duration=FRAME_DURATION, 
                loop=0)
    
    print(f"GIF created successfully: {output_file}")
    print(f"GIF size: {os.path.getsize(output_file) / 1024:.2f} KB")

# Run the script
if __name__ == "__main__":
    print(f"Script running from: {SCRIPT_DIR}")
    file_path = os.path.join(SCRIPT_DIR, 'static', 'grid_init', 'opencivics_logo.txt')
    print(f"Attempting to load grid from: {file_path}")
    generate_cellular_automata_gif(file_path)