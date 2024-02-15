import json
import sys

BUFFER = 5  # Adjust this buffer value as needed

def append_header_to_labels(data, labels_to_append_header):
    # Iterate through the data and append "header:" to the respective labels
    for item in data["words"]:
        if item["label"] in labels_to_append_header:
            item["label"] = "header:" + item["label"]

def create_label_list(data):
    items_in_same_row = []  # Initialize an empty list to store items in the same row

    # Iterate through the data to find items with labels matching the pattern
    for item in data["words"]:
        if "items_row" in item["label"]:
            items_in_same_row.append(item)

    # Extract the labels to update
    labels_to_update = [item["label"] for item in items_in_same_row]

    # Return the list of labels to update
    return labels_to_update

def update_labels_in_same_row(data, labels_to_update):
    # Iterate through the data to find values with labels in labels_to_update
    for item in data["words"]:
        if item["label"] in labels_to_update:
            # Store the y-coordinate of the current item
            item_y = (item["rect"]["y1"] + item["rect"]["y2"]) / 2
            string = item["label"]
            variable = string.split(":")[0]
            
            # Create a rectangle starting from the current item's bbox
            left_x = item["rect"]["x1"]
            right_x = item["rect"]["x2"]
            top_y = item["rect"]["y1"]
            bottom_y = item["rect"]["y2"]

            # Extend the rectangle to the left
            for other_item in data["words"]:
                other_item_y = (other_item["rect"]["y1"] + other_item["rect"]["y2"]) / 2
                if (other_item["label"] and abs(other_item_y - item_y) < BUFFER
                        and other_item["rect"]["x2"] < left_x):
                    left_x = other_item["rect"]["x1"]

            # Extend the rectangle to the right
            for other_item in data["words"]:
                other_item_y = (other_item["rect"]["y1"] + other_item["rect"]["y2"]) / 2
                if (other_item["label"] and abs(other_item_y - item_y) < BUFFER
                        and other_item["rect"]["x1"] > right_x):
                    right_x = other_item["rect"]["x2"]

            # Update labels of items intersecting with the rectangle
            for other_item in data["words"]:
                sequence = "items_row"
                if other_item["label"] == item["label"] or sequence in other_item["label"]:
                    pass
                else:
                    other_item_y = (other_item["rect"]["y1"] + other_item["rect"]["y2"]) / 2
                    if (other_item["label"] and abs(other_item_y - item_y) < BUFFER
                            and left_x <= other_item["rect"]["x1"] <= right_x):
                        other_item["label"] = f"{variable}:{other_item['label']}"

def update_labels_same_as_variable2(data, variable2):
    count = 2
    for item in data["words"]:
        #print(item)
        print(item["label"])
        print(variable2)
        if item["label"] == variable2:
            print("here")
            item["label"] = f"items_row{count}:{variable2}"
            count += 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <json_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Define the labels to append "header:" to
    labels_to_append_header = ["invoiceNumber", "invoiceDate", "poNumber", "SalesOrderNumber"]

    # Load JSON data
    with open(json_path, 'r') as file:
        data = json.load(file)
    labels_to_update = create_label_list(data)
    # Update labels with "header:" prefix
    append_header_to_labels(data, labels_to_append_header)
    
   
    for item in labels_to_update:
        variable2 = item.split(":")[1]
        print(variable2)
        update_labels_same_as_variable2(data, variable2)

    print(labels_to_update)
    labels_to_update = create_label_list(data)
    # Update labels in the same row
    update_labels_in_same_row(data, labels_to_update)

    # Update labels same as variable2


    # Write the modified data back to the JSON file
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=2)

    print("Labels updated and written to the JSON file:", json_path)
