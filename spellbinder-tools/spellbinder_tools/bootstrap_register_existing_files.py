from spellbinder_util.file_registry import register_file
import os

folder = "../test_docs/test_search"  # adjust to your folder if needed

def bootstrap_folder(folder_path):
    count = 0
    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        if os.path.isfile(path) and filename.endswith(".txt"):
            register_file(path)
            count += 1
    print(f"✅ Registered {count} files.")

if __name__ == "__main__":
    bootstrap_folder(folder)