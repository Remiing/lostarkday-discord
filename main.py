import pickle
import time
import os
from src.utils import import_members
from src.crawling import getItemLV
from src.discord import sendMessage


if __name__ == '__main__':
    members = import_members('./data/guild_members.yml')
    after_members_dict = {}
    for characterName in members:
        characterData = getItemLV(characterName)
        after_members_dict[characterName] = characterData
        print(f'{characterName} class: {characterData["class"]} itemLV: {characterData["itemLV"]} equipment: {characterData["equipment"]}')
        time.sleep(1.5)

    if os.path.isfile('./data/members_dict.pkl'):
        with open('./data/members_dict.pkl', 'rb') as f:
            before_members_dict = pickle.load(f)
        for characterName in members:
            if characterName not in before_members_dict.keys() or characterName not in after_members_dict.keys():
                continue
            before_data = before_members_dict[characterName]
            after_data = after_members_dict[characterName]
            if before_data['itemLV'] == after_data['itemLV']:
                continue
            for before_equip, after_equip in zip(before_data['equipment'], after_data['equipment']):
                before_equipType, before_equipLV, before_equipName = before_equip.split('/')
                after_equipType, after_equipLV, after_equipName = after_equip.split('/')
                if before_equipLV == after_equipLV:
                    continue
                sendMessage(characterName, after_data["class"], after_equipType, before_equipLV, after_equipLV)
                print(f'{characterName}/{before_data["class"]}')
                print(f'{before_equipType} {before_equipLV} > {after_equipLV}')

    with open('./data/members_dict.pkl', 'wb') as f:
        pickle.dump(after_members_dict, f)

