import pickle
import time
import os
import pandas as pd
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
        # time.sleep(1.5)

    if os.path.isfile('./data/members_dict.pkl'):
        with open('./data/members_dict.pkl', 'rb') as f:
            before_members_dict = pickle.load(f)
        step_price = pd.read_csv('./data/step_price.csv')
        step_price = step_price.to_dict('records')
        for characterName in members:
            if characterName not in before_members_dict.keys() or characterName not in after_members_dict.keys():
                continue
            before_data = before_members_dict[characterName]
            after_data = after_members_dict[characterName]
            if before_data['itemLV'] == after_data['itemLV']:
                continue
            for before_equip, after_equip in zip(before_data['equipment'], after_data['equipment']):
                before_equipType, before_equipStep, before_equipLV = before_equip.split('/')
                after_equipType, after_equipStep, after_equipLV = after_equip.split('/')
                if before_equipStep == after_equipStep:
                    continue
                part_gold = 0
                for step in step_price:
                    step_level = step['level'].replace('level_', '')
                    step_num = int(step['step'].replace('step_', ''))
                    if step_level != before_equipLV and step_level != after_equipLV: continue
                    elif step_level == '1302' and step_num > 15: continue
                    elif step_level == '1340' and step_num <= 6 or step_num > 20: continue
                    elif step_level == '1390' and step_num <= 12 or step_num > 19: continue
                    elif step_level == '1525' and step_num <= 12: continue
                    elif step_level == before_equipLV and step_num <= int(before_equipStep): continue
                    elif step_level == after_equipLV and step_num > int(after_equipStep): continue
                    print(step)
                    if after_equipType == '무기':
                        part_gold += step['weaponAvg']
                    else:
                        part_gold += step['armorAvg']
                if part_gold == 0: continue
                sendMessage(characterName, after_data["class"], after_equipType, before_equipStep, after_equipStep, part_gold)
                print(f'{characterName}/{before_data["class"]}')
                print(f'{before_equipType} {before_equipStep} > {after_equipStep}')
                print(f'기대값 {part_gold}')

    with open('./data/members_dict.pkl', 'wb') as f:
        pickle.dump(after_members_dict, f)

