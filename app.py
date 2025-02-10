from flask import Flask, jsonify, request, render_template
import time
import copy
import leaderboard  
import uuid
import main
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  #server needs this to allow cross-origin requests (requests from different servers)


level_lives = main.initialize_lives()
sessions = {} #this will store all the game sessions. Sessions are needed because we need to keep track of the game state for each player. It is needed more for the frontend to work properly with the leaderboard.

def initialize_session(level):
    grid = main.get_sudoku(level)
    if grid is None:
        return None
    
    solution_grid = main.solve_sudoku_puzzle(grid)
    return {
        "original_grid": copy.deepcopy(grid), #this is the same as doing [row[:] for row in grid]
        "current_grid": copy.deepcopy(grid),
        "solution_grid": solution_grid,
        "lives": level_lives,
        "start_time": time.time()
    }

@app.route("/")
def index():
    return render_template("index.html") # Render the HTML template

@app.route('/start_game', methods=['POST'])
def start_game():
    try:
        data = request.get_json()
        level = data.get("level")
        name = data.get("name", "Anonymous").strip()  # default to "Anonymous" if no name provided

        if level is None or not (1 <= level <= 11): #should be 1 to 10, but level 11 is used for testing
            return jsonify({"error": "Invalid level. Please choose a level between 1 and 10."}), 400

        if not name:
            return jsonify({"error": "Please provide a valid name."}), 400

        #initialize a new session
        session_id = str(uuid.uuid4())  #generates a unique session ID
        session_data = initialize_session(level)
        
        if session_data is None:
            return jsonify({"error": "Invalid level. Please choose a level between 1 and 10."}), 400

        # Add the player's name to the session
        session_data["name"] = name
        session_data["level"] = level  # add level to session for leaderboard

        # Store the session in the `sessions` dictionary
        sessions[session_id] = session_data

        return jsonify({
            "session_id": session_id, 
            "grid": session_data["current_grid"],
            "lives": session_data["lives"]
        }), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An unexpected error occurred. Please try again."}), 500


@app.route("/make_move", methods=["POST"])
def make_move():
    try:
        # Parse the request data
        data = request.json
        session_id = data.get("session_id")
        row = data.get("row")
        col = data.get("col")
        num = data.get("num")

        #validate input
        if None in (session_id, row, col, num):
            return jsonify({"error": "Invalid input. Row, column, number, and session ID are required."}), 400

        #fetch the session
        session = sessions.get(session_id)
        if not session:
            return jsonify({"error": "Session not found."}), 404

        #get session details
        grid = session["current_grid"]
        solution_grid = session["solution_grid"]

        #check if the cell is already filled
        if grid[row][col] != 0:
            return jsonify({"error": "Cell is already filled."}), 400

        #check if the move is correct
        if main.is_valid_move(grid, solution_grid, row, col, num):
            grid[row][col] = num  # Update grid with the correct move

            # check if the puzzle is complete
            if main.is_puzzle_complete(grid):  
                
                player_name = session.get("name", "Anonymous")
                
                elapsed_time = main.calculate_elapsed_time(session["start_time"], time.time())
                hours, minutes, seconds = elapsed_time 

                # Update the leaderboard
                leaderboard.update_leaderboard(
                    name=player_name,
                    elapsed_time=elapsed_time,
                    level=session["level"]
                )

                # Save the leaderboard after updating it
                leaderboard.save_leaderboard()

                # Clean up session
                del sessions[session_id]

                return jsonify({
                    "success": "Puzzle complete!",
                    "time": f"{int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds",
                    "reset_grid": True  # trigger to clear the grid
                })

            return jsonify({"success": "Correct move.", "grid": grid, "lives": session["lives"]}), 200
        else:
            # Incorrect move
            session["lives"] -= 1
            if session["lives"] <= 0:  # Game over
                del sessions[session_id]
                return jsonify({
                    "error": "Game over. No lives remaining.",
                    "reset_grid": True  
                }), 200

            return jsonify({"error": "Incorrect move.", "grid": grid, "lives": session["lives"]}), 200

    except Exception as e:
        print(f"Unexpected error: {e}")  #debugging purposes, these errors will be logged in the server console
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    try:
        level = int(request.args.get('level', 0))
        if not (1 <= level <= 11):
            return jsonify({"error": "Invalid level. Please choose a level between 1 and 10."}), 400

        leaderboard_data = leaderboard.load_leaderboard()

        # leaderboard is filtered by level
        filtered_leaderboard = {
            name: details for name, details in leaderboard_data.items() if details["level"] == level
        }

        if not filtered_leaderboard:
            return jsonify({"message": f"No leaderboard entries found for level {level}."}), 200

        # sorts the leaderboard by time
        sorted_leaderboard = leaderboard.quicksort(list(filtered_leaderboard.items()))

        # formats leaderboard for output
        formatted_leaderboard = [
            {
                "rank": idx + 1,
                "name": details["name"],
                "time": f"{details['time'][0]} hours, {details['time'][1]} minutes, {details['time'][2]} seconds"
            }
            for idx, (_, details) in enumerate(sorted_leaderboard)
        ]

        return jsonify({"level": level, "leaderboard": formatted_leaderboard}), 200
    except Exception as e:
        print("Error retrieving leaderboard:", e) #debugging purposes, these errors will be logged in the server console
        return jsonify({"error": "An unexpected error occurred while retrieving the leaderboard."}), 500


if __name__ == "__main__":
    app.run(debug=True)
