import yaml
import sys

def get_unique_artists_from_yaml(yaml_content):
    """
    Extracts unique artists from YAML content and returns them in YAML format.
    
    :param yaml_content: The YAML content as a string.
    :return: YAML string of unique artists.
    """
    try:
        data = yaml.safe_load(yaml_content)
        if 'songs' not in data:
            raise ValueError("YAML does not contain 'songs' key.")
        
        songs = data['songs']
        artists = set()
        for song in songs:
            if 'artist' in song:
                artists.add(song['artist'])
        
        unique_artists = sorted(list(artists))
        output_data = {'artists': unique_artists}
        return yaml.dump(output_data, default_flow_style=False)
    
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_yaml_file>")
        sys.exit(1)
    
    yaml_file_path = sys.argv[1]
    try:
        with open(yaml_file_path, 'r') as file:
            yaml_content = file.read()
        
        output_yaml = get_unique_artists_from_yaml(yaml_content)
        print(output_yaml)
    
    except Exception as e:
        print(f"An error occurred: {e}")