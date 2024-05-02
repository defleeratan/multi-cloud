import os
import re
import json

def extract_functions_with_comments(file_path):
    functions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        comment = None
        for line in lines:
            if line.strip().startswith('//'):
                if comment is None:
                    comment = line.strip().lstrip('//').strip()
                else:
                    comment += ' ' + line.strip().lstrip('//').strip()
            elif line.strip().startswith('func ') and '(' in line and ')' in line:
                func_name = re.findall(r'func\s+([^\(\s]+)', line)[0]
                functions.append({"name": func_name, "comment": comment})
                comment = None
    return functions

def process_repo(repo_path):
    functions_data = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.go'):
                file_path = os.path.join(root, file)
                functions_data.extend(extract_functions_with_comments(file_path))
    return functions_data

def main():
    repo_path = input("Enter path to the repository: ")
    functions_data = process_repo(repo_path)
    output_file = "data.json"
    with open(output_file, 'w') as f:
        json.dump(functions_data, f, indent=4)

    print(f"Function names and comments extracted and saved to {output_file}.")

if __name__ == "__main__":
    main()
