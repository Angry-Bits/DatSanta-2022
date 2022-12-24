from pathlib import Path


BASE_DIR = Path.cwd()
MAP_FIXTURE_NAME = 'map.json'
MAP_FIXTURE_PATH = BASE_DIR.joinpath(MAP_FIXTURE_NAME)


def write_to_file(data, file_path=BASE_DIR):
    with file_path.open('w', encoding='utf-8') as file:
        file.write(data)
