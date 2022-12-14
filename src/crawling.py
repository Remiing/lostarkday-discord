import requests
import json
import config

lark_api_key = 'bearer ' + config.lark_api_key
lark_api_key = os.environ['lark_api_key']


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
        for equip in characterEquipment[:6]:
            equipType = equip['Type']
            equipLV = equip['Name'][1:equip['Name'].find(' ')]
            equipName = equip['Name'][equip['Name'].find(' ')+1:]
            equipment.append(f'{equipType}/{equipLV}/{equipName}')
        del characterEquipment
    else:
        return

    character_data = {
        'class': characterClass,
        'itemLV': itemLV,
        'equipment': equipment,
    }

    return character_data

