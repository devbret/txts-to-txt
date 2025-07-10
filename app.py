import os

def combine_txt_files(directory: str, output_filename: str = "combined_output.txt") -> None:
    combined_lines = []

    for filename in os.listdir(directory):
        if filename.endswith(".txt") and filename != output_filename:
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    combined_lines.append(f"\n--- Begin {filename} ---\n")
                    combined_lines.append(file.read())
                    combined_lines.append(f"\n--- End {filename} ---\n")
            except Exception as e:
                print(f"Failed to read {filename}: {e}")

    output_path = os.path.join(directory, output_filename)
    try:
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write("\n".join(combined_lines))
        print(f"\n✅ Combined file saved to: {output_path}")
    except Exception as e:
        print(f"❌ Failed to write output file: {e}")

if __name__ == "__main__":
    input_directory = os.path.join(os.getcwd(), "input")
    combine_txt_files(input_directory)

