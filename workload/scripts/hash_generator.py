import os
import sys
import hashlib

def generate_hash(dir_path):
    """
    Generate a hash based on the contents of all .tf files in the given directory and its subdirectories.

    This function walks through the directory tree, reads all .tf files,
    and generates a SHA256 hash based on their contents. The files are processed
    in a sorted order to ensure consistency across different runs.

    Args:
        dir_path (str): The path to the directory containing .tf files.

    Returns:
        str: The first 8 characters of the generated SHA256 hash.
    """
    sha256 = hashlib.sha256()
    for root, _, files in os.walk(dir_path):
        for file in sorted(files):  # Sort files for consistency
            if file.endswith('.tf'):
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    while chunk := f.read(8192):
                        sha256.update(chunk)
    return sha256.hexdigest()[:8]

def main():
    """
    Main function to handle command-line arguments and generate the configuration hash.

    This function checks for the correct number of command-line arguments,
    validates the input directory, generates the hash, and prints the result.

    Usage:
        python hash_generator.py <directory>

    Exits:
        0: Success
        1: Incorrect number of arguments or invalid directory
    """
    if len(sys.argv) != 2:
        sys.exit(1)
    
    input_directory = sys.argv[1]
    if not os.path.isdir(input_directory):
        sys.exit(1)
    
    config_hash = generate_hash(input_directory)
    print(config_hash, end='')

if __name__ == "__main__":
    main()