import json


def update_json_file_from_dict(json_file: str, json_dict: dict) -> None:
    with open(json_file, "r+", encoding="utf8") as f:
        f.seek(0)
        json.dump(json_dict, f, indent=4)


def get_dict_from_json_file(json_file: str) -> dict:
    with open(json_file, "r+", encoding="utf8") as f:
        data = json.load(f)
        return data
