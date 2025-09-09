import os
import json

def scan_directory(directory_path):
    """Scans a directory and its subdirectories for FLAC and MP3 files."""
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name).replace('\\', '/')
        if os.path.isfile(file_path) and (file_name.endswith('.flac') or file_name.endswith('.mp3')):
            yield file_path
        elif os.path.isdir(file_path):
            yield from scan_directory(file_path)

def sort_songs(songs):
    """Sorts a list of song dictionaries by name."""
    return sorted(songs, key=lambda song: song['name'])


if __name__ == '__main__':
    completed_songs_file = './MonsterSiren/completed_songs.json'
    with open(completed_songs_file, 'w+', encoding='utf8') as f:
        songs = []
        for file_path in scan_directory('./MonsterSiren/'):
            song_name = os.path.splitext(os.path.basename(file_path))[0].replace("_", " ")
            cover_path = os.path.join(os.path.dirname(file_path), 'cover.png').replace('\\', '/')
            relative_cover_path = os.path.relpath(cover_path, './MonsterSiren/').replace('\\', '/')
            relative_file_path = os.path.relpath(file_path, './MonsterSiren/').replace('\\', '/')
            songs.append({
                'cover': relative_cover_path,
                'path': relative_file_path,
                'name': song_name
            })

        songs = sort_songs(songs)

        json.dump(songs, f, ensure_ascii=False, indent=4)

        