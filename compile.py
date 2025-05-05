import os
import re
import argparse

def pad_zeros(text, width):
    """Pad numeric parts of a string with leading zeros."""
    return re.sub(r'\d+', lambda m: m.group(0).zfill(width), text)

def compile_chapters(input_dir, output_file, tag="CHAPTER", width=3):
    # Collect and sort .txt files by zero-padded numeric order
    txt_files = [
        (pad_zeros(fname, width), fname)
        for fname in os.listdir(input_dir)
        if fname.endswith(".txt")
    ]
    txt_files.sort(key=lambda x: x[0])

    tag = tag.upper()

    with open(output_file, 'w', encoding='utf-8') as fout:
        for _, fname in txt_files:
            path = os.path.join(input_dir, fname)
            fout.write(f"<!-- {tag} START --!>\n")
            with open(path, 'r', encoding='utf-8') as fin:
                fout.write(fin.read().strip() + '\n')
            fout.write(f"<!-- {tag} END --!>\n\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile sorted .txt files into a single output file.")
    parser.add_argument("input_dir", nargs="?", default=".", help="Directory containing .txt files")
    parser.add_argument("output_file", nargs="?", default="../compiled_text.txt", help="Path to output file")
    parser.add_argument("--tag", "-t", default="CHAPTER", help="Tag label used in comment markers")
    args = parser.parse_args()

    compile_chapters(args.input_dir, args.output_file, tag=args.tag)
