import requests
import json
import os
import yaml
from dotenv import load_dotenv

load_dotenv()

# lark_api_key = 'bearer ' + config.lark_api_key
# lark_api_key = 'bearer ' + os.environ['lark_api_key']
lark_api_key = 'bearer ' + os.environ.get('lark_api_key')


def getItemLV(characterName):
    url = 'https://developer-lostark.game.onstove.com/armories/characters/'

    # profiles: characterClass, itemLV
    response = requests.get(url + characterName + '/profiles', headers={"authorization": lark_api_key})
    if response.status_code == 200:
        characterProfile = json.loads(response.text)
        characterClass = characterProfile['CharacterClassName']
        itemLV = float(characterProfile['ItemMaxLevel'].replace(',', ''))
        del characterProfile
    else:
        return

    # equipment: equipType, equipLV, equipName
    response = requests.get(url + characterName + '/equipment', headers={"authorization": lark_api_key})
    if response.status_code == 200:
        characterEquipment = json.loads(response.text)
        equipment = []
        with open('./data/equipment_set.yml', encoding='utf-8') as file:
            equipSetLevel = yaml.load(file, Loader=yaml.FullLoader)
        for equip in characterEquipment[:6]:
            equipType = equip['Type']
            equipStep = equip['Name'][1:equip['Name'].find(' ')]
            equipName = equip['Name'][equip['Name'].find(' ')+1:]
            equipLV = ''
            for k, v in equipSetLevel.items():
                for setName in v:
                    if setName in equipName:
                        equipLV = k.replace('lv', '')
                        break
                else:
                    continue
                break
            equipment.append(f'{equipType}/{equipStep}/{equipLV}')
        del characterEquipment
    else:
        return

    character_data = {
        'class': characterClass,
        'itemLV': itemLV,
        'equipment': equipment,
    }
    print(character_data)

    return character_data


if __name__ == '__main__':
    lv = getItemLV('너와떠나는여행')


