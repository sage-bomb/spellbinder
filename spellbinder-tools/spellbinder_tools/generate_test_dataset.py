import os
import json
from spellbinder_llm.prompt_manager import PromptManager

def extract_test_queries_from_file(file_path, prompt_manager, template_name="EmbeddingSearchTestGeneration"):
    """Reads a file and generates test queries from its content."""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    response = prompt_manager.run_template(
        name=template_name,
        variables={"input": text},
        metadata={"source_file": os.path.basename(file_path)}
    )

    queries = []
    for line in response.split("\n"):
        line = line.strip()
        if line and line[0].isdigit():
            query = line.split(".", 1)[-1].strip()
            queries.append(query)

    return queries

def build_test_dataset(input_dir, output_file="test_dataset.json"):
    """Generates a JSON test dataset from a folder of text files."""
    dataset = []
    pm = PromptManager()

    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        if not filename.lower().endswith(".txt") or not os.path.isfile(file_path):
            continue

        print(f"📥 Processing {filename}")
        queries = extract_test_queries_from_file(file_path, pm)

        for query in queries:
            dataset.append({
                "search_string": query,
                "expected_result_file": filename
            })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)

    print(f"✅ Test dataset saved to {output_file}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate embedding test dataset from text files.")
    parser.add_argument("input_dir", type=str, help="Folder containing source text files")
    parser.add_argument("--output", type=str, default="test_dataset.json", help="Output JSON file")
    args = parser.parse_args()

    build_test_dataset(args.input_dir, args.output)
