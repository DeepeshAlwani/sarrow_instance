import json
import sys

# Check if the JSON path is provided as an argument
if len(sys.argv) != 2:
    print("Usage: python script.py <json_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load the JSON data
with open(json_path, "r") as file:
    data = json.load(file)

# Dictionary to store labels by x-coordinate range
label_dict = {}

# Buffer size to consider words as aligned
buffer_size = 1  # Increase buffer size for efficiency
cutoff_distance = 40  # Define a cutoff distance
max_distance = 40    # Define maximum allowed distance between word and labeled text
max_size_difference = 18  # Define maximum allowed size difference between bounding boxes

# Iterate through the words to identify entries with labels
for word in data["words"]:
    if word["label"]:
        x1 = word["rect"]["x1"]
        x2 = word["rect"]["x2"]
        width = abs(x2 - x1)  # Calculate the width of the bounding box
        label_dict[(x1 - buffer_size, x2 + buffer_size)] = (word["label"], word["rect"]["y2"], width)

# Assign labels to words within the buffer zone, cutoff distance, and x-coordinate range
for word in data["words"]:
    if not word["label"]:
        x_coordinate = (word["rect"]["x1"] + word["rect"]["x2"]) / 2  # Calculate the x-coordinate of the word's center
        y_coordinate = word["rect"]["y2"]  # Y-coordinate of the word
        width = abs(word["rect"]["x2"] - word["rect"]["x1"])  # Width of the current word's bounding box
        closest_label = None
        min_distance = float('inf')  # Initialize minimum distance to infinity
        for (start, end), (label, labeled_y, labeled_width) in label_dict.items():
            if labeled_y > y_coordinate:  # Exclude words positioned below the labeled words
                continue
            if start <= x_coordinate <= end:  # Check if x-coordinate falls within the range
                distance = abs((start + end) / 2 - x_coordinate)
                if (
                    distance < min_distance and 
                    distance <= cutoff_distance and 
                    distance <= max_distance and 
                    (
                        width > labeled_width or  # Compare sizes only if the word is larger
                        width <= labeled_width + max_size_difference  # If smaller, allow a tolerance
                    )
                ):
                    min_distance = distance
                    closest_label = label
        if closest_label:
            word["label"] = closest_label

# Write the updated data back to the file
with open(json_path, "w") as file:
    json.dump(data, file, indent=2)
