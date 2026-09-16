import argparse
from pathlib import Path
from colorama import Fore, init
from linter import check_dockerfile, check_requirements

init(autoreset=True)

def parse_arguments():
    parser = argparse.ArgumentParser(description='CLI-scanner for Dockerfile and Python requirements.')
    parser.add_argument('file', type=str, help='Path to the file to scan (e.g., Dockerfile or requirements.txt)')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    clean_path_str = args.file.strip("'\"").strip("/")
    file_path = Path(clean_path_str).resolve()

    if not file_path.is_file():
        print(f'{Fore.RED}[ERROR] File path not found: {file_path}')
        return

    print(f'{Fore.GREEN}[OK] File loaded successfully: {file_path.name}')
    
    filename = file_path.name.lower()
    
    if 'dockerfile' in filename or file_path.suffix == '.containerfile':
        check_dockerfile(file_path)
    elif file_path.suffix == '.txt' or 'requirements' in filename:
        check_requirements(file_path)
    else:
        print(f'{Fore.RED}[ERROR] Unsupported file type! Name must contain "Dockerfile" or end with ".txt"')

if __name__ == '__main__':
    print(f'{Fore.BLUE}[INFO] CLI-scanner started.')
    main()