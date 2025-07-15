import yaml
import sys
import os

def get_full_unique_songs_from_yaml_files(yaml_files):
    """
    Extracts unique full song data based on title and artist from multiple YAML files and returns them in YAML format.
    
    :param yaml_files: List of YAML file paths.
    :return: YAML string of unique full songs.
    """
    try:
        all_songs = []
        for yaml_file in yaml_files:
            with open(yaml_file, 'r') as file:
                data = yaml.safe_load(file)
                if 'songs' not in data:
                    print(f"Warning: YAML file {yaml_file} does not contain 'songs' key. Skipping.")
                    continue
                all_songs.extend(data['songs'])
        
        seen = set()
        unique_songs = []
        for song in all_songs:
            if 'title' in song and 'artist' in song:
                key = (song['title'], song['artist'])
                if key not in seen:
                    seen.add(key)
                    unique_songs.append(song)
        
        output_data = {'songs': unique_songs}
        return yaml.dump(output_data, default_flow_style=False)
    
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_data_directory>")
        sys.exit(1)
    
    data_dir = sys.argv[1]
    if not os.path.isdir(data_dir):
        print(f"Error: {data_dir} is not a directory.")
        sys.exit(1)
    
    yaml_files = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                yaml_files.append(os.path.join(root, file))
    
    if not yaml_files:
        print("No YAML files found in the directory or its subdirectories.")
        sys.exit(1)
    
    output_yaml = get_full_unique_songs_from_yaml_files(yaml_files)
    print(output_yaml)