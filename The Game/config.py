# Configuration for the game field

GRID_SIZE = 20  # Size of the grid

# Define properties for each cell type
CELL_DEFINITIONS = {
    "Terrain": {
        "passable": True,
        "can_pick": False,
        "can_dig": False,
        "interactable": False,
        "spawn_ratio": 0.9,
    },
    "Forest": {
        "passable": False,
        "can_pick": False,
        "can_dig": True,
        "interactable": False,
        "spawn_ratio": 0.001,
    },
    "Water": {
        "passable": False,
        "can_pick": False,
        "can_dig": False,
        "interactable": False,
        "spawn_ratio": 0.001,
    },
    "Treasure": {
        "passable": True,
        "can_pick": True,
        "can_dig": False,
        "interactable": False,
        "spawn_ratio": 0.4,
    },
    "GoldenOre": {
        "passable": True,
        "can_pick": False,
        "can_dig": True,
        "interactable": False,
        "spawn_ratio": 0.3,
    }
}

# List of cell types for convenience
CELL_TYPES = list(CELL_DEFINITIONS.keys())

# Calculating spawn ratios for each cell type
SPAWN_RATIOS = {cell: CELL_DEFINITIONS[cell]["spawn_ratio"] for cell in CELL_TYPES}

players = {"1": (0, 0), "2": (GRID_SIZE - 1, GRID_SIZE - 1)} 

# Colors and abbreviation length (optional)
CELL_COLORS = {
    "Player": "lightblue",
    "Terrain": "lightgreen",
    "Forest": "saddlebrown",
    "Water": "blue",
    "Treasure": "gold",
}
ABBREVIATION_LENGTH = 3

#FIELD_OF_VIEW
FIELD_OF_VIEW = 2 