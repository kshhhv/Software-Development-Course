from pathlib import Path

files_are_here = Path(".") / "a_few_files"

if __name__ == "__main__":
	for file_path in files_are_here.iterdir():
		print(file_path)
