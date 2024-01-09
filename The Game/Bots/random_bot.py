import requests
import random
import time

# Constants
SERVER_URL = "http://127.0.0.1:5000"
PLAYER_ID = "1"  # Assuming player 1 is the one we're controlling
DIRECTIONS = ["up", "down", "left", "right"]
MOVE_OFFSETS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

def get_player_position():
    """Retrieve the current position of the player."""
    response = requests.get(f"{SERVER_URL}/get_player_position", params={"player_id": PLAYER_ID})
    if response.status_code == 200:
        return response.json()["position"]
    return None

def get_cell_state(x, y):
    """Retrieve the state of the cell at the given coordinates."""
    response = requests.get(f"{SERVER_URL}/get_cell", params={"x": x, "y": y})
    if response.status_code == 200:
        return response.json()["cell_state"]
    return None

def is_move_possible(x, y, direction):
    """Check if a move in the given direction is possible."""
    dx, dy = MOVE_OFFSETS[direction]
    new_x, new_y = x + dx, y + dy
    cell_state = get_cell_state(new_x, new_y)
    return cell_state == "Terrain"

def move_player(direction):
    """Send a move request to the server."""
    response = requests.post(f"{SERVER_URL}/move_player", json={"player_id": PLAYER_ID, "direction": direction})
    return response.json()

def random_walk():
    """Randomly walk on the game field, avoiding impossible moves."""
    while True:
        current_position = get_player_position()
        if current_position is None:
            print("Failed to get player position. Retrying...")
            time.sleep(1)
            continue

        possible_directions = [dir for dir in DIRECTIONS if is_move_possible(*current_position, dir)]
        if not possible_directions:
            print("No valid moves available. Waiting...")
            time.sleep(1)
            continue

        direction = random.choice(possible_directions)
        result = move_player(direction)

        if result['success']:
            print(f"Moved {direction} successfully.")
        else:
            print(f"Failed to move {direction}. Reason: {result['message']}")

        time.sleep(1)  # Wait for 1 second before next move

if __name__ == "__main__":
    random_walk()
