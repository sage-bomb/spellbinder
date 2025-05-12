# tools/rebuild_file_registry.py

import os
import argparse
from util.file_registry import register_file

def rebuild_registry(target_dir):
    print(f"📦 Rebuilding file registry from directory: {target_dir}")
    
    registered = 0
    skipped = 0
    
    for root, _, files in os.walk(target_dir):
        for filename in files:
            if filename.startswith(".") or filename.endswith(".db") or filename.endswith(".json"):
                continue  # Skip metadata and hidden files
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path):
                file_eid = register_file(file_path)
                if file_eid:
                    print(f"✅ Registered: {filename} (eid: {file_eid})")
                    registered += 1
                else:
                    print(f"⚠️ Skipped (already exists): {filename}")
                    skipped += 1

    print(f"\nSummary: {registered} files registered, {skipped} files skipped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rebuild file registry database from existing files.")
    parser.add_argument(
        "--path", type=str, default="./test_docs/test_search",
        help="Path to scan for files (default: ./test_docs/test_search)"
    )
    args = parser.parse_args()

    rebuild_registry(args.path)
