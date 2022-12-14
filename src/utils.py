import yaml


def import_members(file_path):
    with open(file_path, encoding='utf-8') as file:
        members = yaml.load(file, Loader=yaml.FullLoader)
        members = members['main_character'] + members['sub_character']
    return members

