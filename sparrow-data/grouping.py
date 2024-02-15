import os
import json
import argparse
from shapely.geometry import box
from shapely.ops import unary_union

def merge_boxes(boxes):
    polygons = [box(box_info['rect']['x1'], box_info['rect']['y1'],
                    box_info['rect']['x2'], box_info['rect']['y2']) for box_info in boxes]
    merged_polygon = unary_union(polygons)
    merged_box = {
        'x1': merged_polygon.bounds[0],
        'y1': merged_polygon.bounds[1],
        'x2': merged_polygon.bounds[2],
        'y2': merged_polygon.bounds[3]
    }
    return merged_box

def merge_close_words(word_list, horizontal_threshold=3, vertical_threshold=10):
    merged_words = []
    current_group = [word_list[0]]

    for i in range(1, len(word_list)):
        current_box = box(current_group[-1]['rect']['x1'], current_group[-1]['rect']['y1'],
                          current_group[-1]['rect']['x2'], current_group[-1]['rect']['y2'])
        next_box = box(word_list[i]['rect']['x1'], word_list[i]['rect']['y1'],
                       word_list[i]['rect']['x2'], word_list[i]['rect']['y2'])

        horizontal_distance = next_box.bounds[0] - current_box.bounds[2]
        vertical_distance = abs(current_box.bounds[1] - next_box.bounds[1])
        vertical_overlap = min(current_box.bounds[3], next_box.bounds[3]) - max(current_box.bounds[1], next_box.bounds[1])

        # Check if the baseline is the same and there is no significant vertical overlap
        if (horizontal_distance <= horizontal_threshold and 
            vertical_distance <= vertical_threshold):
            current_group.append(word_list[i])
        else:
            merged_box = merge_boxes(current_group)
            merged_words.append({
                'rect': merged_box,
                'value': ' '.join([word['value'] for word in current_group]),
                'label': ''
            })
            current_group = [word_list[i]]

    if current_group:
        merged_box = merge_boxes(current_group)
        merged_words.append({
            'rect': merged_box,
            'value': ' '.join([word['value'] for word in current_group]),
            'label': ''
        })

    return merged_words

def process_and_save(input_file_path, horizontal_threshold=3, vertical_threshold=10):
    with open(input_file_path, 'r') as input_file:
        data = json.load(input_file)

    words = data['words']
    merged_words = merge_close_words(words, horizontal_threshold, vertical_threshold)

    # Update the input JSON file directly
    data['words'] = merged_words

    with open(input_file_path, 'w') as output_file:
        json.dump(data, output_file, indent=2)

    print(f"Updated data saved to {input_file_path}")

def process_and_save_folder(folder_path, pdf_filenames, horizontal_threshold=10, vertical_threshold=10):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Check if the path is a file, ends with ".json", and contains any of the PDF filenames
        if os.path.isfile(file_path) and file_path.lower().endswith('.json'):
            for pdf_filename in pdf_filenames:
                if pdf_filename.lower() in filename.lower():
                    process_and_save(file_path, horizontal_threshold, vertical_threshold)
                    break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and save JSON files based on provided PDF filenames")
    parser.add_argument("pdf_filenames", nargs="+", help="List of PDF filenames to process")
    parser.add_argument("--input_path", default="docs/json", help="Path to the folder containing JSON files (default: docs/json)")
    parser.add_argument("--horizontal_threshold", type=int, default=3, help="Horizontal threshold for merging words (default: 3)")
    parser.add_argument("--vertical_threshold", type=int, default=10, help="Vertical threshold for merging words (default: 10)")
    args = parser.parse_args()

    input_path = args.input_path
    pdf_filenames = args.pdf_filenames
    horizontal_threshold = args.horizontal_threshold
    vertical_threshold = args.vertical_threshold

    if os.path.isdir(input_path):
        process_and_save_folder(input_path, pdf_filenames, horizontal_threshold, vertical_threshold)
    else:
        print("Invalid input path. Please provide a valid folder path.")
