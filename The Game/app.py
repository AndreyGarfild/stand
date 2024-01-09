from flask import Flask, request, jsonify
import random
import config

app = Flask(__name__)

class GameField:
    def __init__(self):
        self.grid_size = config.GRID_SIZE
        self.field = [[random.choices(
                population=list(config.CELL_TYPES), 
                weights=[config.SPAWN_RATIOS[cell] for cell in config.CELL_TYPES],
                k=1)[0] for _ in range(config.GRID_SIZE)] for _ in range(config.GRID_SIZE)]

    def update_cell(self, x, y, value):
        self.field[x][y] = value

    def get_cell_state(self, x, y):
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.field[x][y]
        else:
            return "Invalid coordinates"

class Player:
    def __init__(self, player_id, position, dig_skill=0):
        self.id = player_id
        self.position = position
        self.dig_skill = dig_skill
        self.inventory = []  # Initialize an empty inventory

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def increase_dig_skill(self, amount):
        self.dig_skill += amount

class Game:
    def __init__(self):
        self.field = GameField()
        self.players = {player_id: Player(player_id, position) for player_id, position in config.players.items()}
        self.initialize_players()

    def initialize_players(self):
        for player in self.players.values():
            x, y = player.position
            self.field.update_cell(x, y, f"Player {player.id}")

    def move_player(self, player_id, direction):
        player = self.players.get(player_id)
        if not player:
            return False, "Player not found"

        x, y = player.position
        move_offsets = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        if direction not in move_offsets:
            return False, "Invalid direction"

        dx, dy = move_offsets[direction]
        new_position = (x + dx, y + dy)

        if self.is_valid_move(player.position, new_position):
            self.field.update_cell(x, y, "Terrain")
            self.field.update_cell(*new_position, f"Player {player_id}")
            player.position = new_position
            return True, "Move successful"
        else:
            return False, "Invalid move"

    def is_valid_move(self, current_position, new_position):
        new_x, new_y = new_position
        if 0 <= new_x < self.field.grid_size and 0 <= new_y < self.field.grid_size:
            cell_type = self.field.get_cell_state(new_x, new_y)
            passable = config.CELL_DEFINITIONS[cell_type]['passable']
            
            # Check if the cell is passable and not occupied by another player
            return passable and not any(
                p.position == (new_x, new_y) for p in self.players.values()
            )
        return False

    def get_player_position(self, player_id):
        player = self.players.get(player_id)
        if player:
            return player.position
        else:
            return "Player not found"
        
    def dig_cell(self, player_id, x, y):
        player = self.players.get(player_id)
        if not player:
            return False, "Player not found"

        # Check if the cell is adjacent to the player
        px, py = player.position
        if abs(px - x) <= 1 and abs(py - y) <= 1:
            cell_type = self.field.get_cell_state(x, y)
            # Check if the cell is of the type 'GoldenOre'
            if cell_type == "GoldenOre":
                self.field.update_cell(x, y, "Terrain")  # Replace 'GoldenOre' with 'Terrain'
                return True, "Dig successful"
            else:
                return False, "Not a GoldenOre cell"
        else:
            return False, "Cell not adjacent to player"
        


game = Game()

@app.route('/get_field', methods=['GET'])
def get_field():
    field_with_players = [[cell for cell in row] for row in game.field.field]

    for player in game.players.values():
        x, y = player.position
        field_with_players[x][y] = f"Player {player.id}"

    return jsonify({"game_field": field_with_players})

@app.route('/move_player', methods=['POST'])
def handle_move_player():
    data = request.json
    player_id = data.get('player_id')
    direction = data.get('direction')

    success, message = game.move_player(player_id, direction)
    return jsonify({"success": success, "message": message})

@app.route('/get_cell', methods=['GET'])
def handle_get_cell():
    x = request.args.get('x', type=int)
    y = request.args.get('y', type=int)

    if x is None or y is None:
        return jsonify({"error": "Coordinates not provided"}), 400

    cell_state = game.field.get_cell_state(x, y)
    return jsonify({"cell_state": cell_state})

@app.route('/get_player_position', methods=['GET'])
def handle_get_player_position():
    player_id = request.args.get('player_id')
    position = game.get_player_position(player_id)

    if isinstance(position, tuple):
        return jsonify({"position": position})
    else:
        return jsonify({"error": position}), 404

@app.route('/dig', methods=['POST'])
def handle_dig():
    data = request.json
    player_id = data.get('player_id')
    x = data.get('x')
    y = data.get('y')   

    success, message = game.dig_cell(player_id, x, y)
    return jsonify({"success": success, "message": message})

if __name__ == '__main__':
    app.run(debug=True)
