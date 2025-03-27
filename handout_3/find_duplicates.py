from pathlib import Path


def find_duplicates(search_path):

	content_seen = []
	duplicates = []

	for file_path in search_path.iterdir():

		with file_path.open('r') as f:

			content = f.read()

			if content not in content_seen:
				content_seen.append(content)

			else:
				duplicates.append(file_path)


	return duplicates


if __name__ == "__main__":

	files_are_here = Path(".") / "a_few_files"

	duplicates = find_duplicates(files_are_here)

	print(f'No of duplicate files: {len(duplicates)}')


