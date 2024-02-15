import os

def delete_files_in_path(directory_path):
    try:
        # List all files in the specified directory
        file_list = os.listdir(directory_path)

        # Iterate through the files and delete each one
        for file_name in file_list:
            file_path = os.path.join(directory_path, file_name)
            
            # Check if it's a file (not a subdirectory) before deletion
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")

        print("Deletion completed.")

    except Exception as e:
        print(f"Error deleting files: {e}")

# Example: Specify the path to the directory containing the files you want to delete
directory_path1_to_delete = "../sparrow-data/docs/input/invoices/Dataset with valid information"
directory_path2_to_delete = "../sparrow-data/docs/input/invoices/processed/output"
directory_path3_to_delete = "../sparrow-data/docs/input/invoices/processed/images"
directory_path4_to_delete = "../sparrow-data/docs/input/invoices/processed/ocr"

delete_files_in_path(directory_path1_to_delete)
delete_files_in_path(directory_path2_to_delete)
delete_files_in_path(directory_path3_to_delete)
delete_files_in_path(directory_path4_to_delete)
