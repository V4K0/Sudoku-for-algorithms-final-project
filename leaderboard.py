import json 
from datetime import date

#time complexity for load_leaderboard is O(n) as it reads the file and loads the data
LEADERBOARD_FILE = f'leaderboard.json'
def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, 'r') as file:
            return json.load(file)  
    except FileNotFoundError:
        raise FileNotFoundError(f"Leaderboard file '{LEADERBOARD_FILE}' not found. Please create it manually.")
    except json.JSONDecodeError:
        raise ValueError(f"Leaderboard file '{LEADERBOARD_FILE}' contains invalid JSON. Please fix the file content.")

#time complexity for save_leaderboard is O(n) as it writes the data to the file        
def save_leaderboard():
    try:
        with open(LEADERBOARD_FILE, 'w') as file:
            json.dump(leaderboard, file, indent=4)  # save with nice indentation
    except Exception as e:
        print(f"Error saving leaderboard: {e}")

leaderboard = {}  # clear any in-memory data at startup // This is needed for server needs
leaderboard = load_leaderboard()

#time complexity for update_leaderboard is O(1) as it updates the leaderboard dictionary
def update_leaderboard(name, elapsed_time: list, level: int):
    # now we have a key for level and name combinations
    leaderboard_key = f"{name}-level-{level}"  
    leaderboard[leaderboard_key] = {
        "name": name,
        "time": elapsed_time,
        "level": level,
        "date": str(date.today())
    }
    print(f"New entry for {name} at level {level} - Time: {elapsed_time[0]} hours, {elapsed_time[1]} minutes, {elapsed_time[2]} seconds.")
    save_leaderboard()  

#time complexity for convert_to_seconds is O(1) 
def convert_to_seconds(time):  #needed for the leaderboard
    return time[0] * 3600 + time[1] * 60 + time[2]

#time complexity for quicksort is O(nlogn). Best case scenario is O(nlogn), worst case scenario is O(n^2) when the pivot is the smallest or largest element in the list, average case scenario is O(nlogn).
def quicksort(timescores):
    if not timescores or len(timescores) == 1:
        return timescores
    pivot = timescores[0]
    pivot_seconds = convert_to_seconds(pivot[1]['time'])
    left_partition = [timescore for timescore in timescores[1:] if convert_to_seconds(timescore[1]['time']) <= pivot_seconds]
    right_partition = [timescore for timescore in timescores[1:] if convert_to_seconds(timescore[1]['time']) > pivot_seconds]
    return quicksort(left_partition) + [pivot] + quicksort(right_partition)