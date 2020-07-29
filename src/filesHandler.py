import json

METADATA_FILE = 'cloud_info.json'

def load_metadata():
    with open(METADATA_FILE, encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data

def get_folder_id():
    metadata = load_metadata()
    cloud_config = metadata["cloud_config"]
    return cloud_config["folder_id"]

def get_cloud_metadata():
    metadata = load_metadata()
    return metadata["cloud_config"]

def save_metadata(metadata):
    with open(METADATA_FILE, 'w', encoding='utf-8') as outfile:
        json.dump(metadata, outfile)