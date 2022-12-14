import requests
import config

day_webhook_url = config.day_webhook_url


def sendMessage(characterName, characterClass, equipType, before_equipLV, after_equipLV):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "embeds": [
            {
                "title": characterName,
                "description": characterClass,
                "fields": [
                    {
                        "name": equipType,
                        "value": f"{before_equipLV} > {after_equipLV}"
                    },
                    {
                        "name": "기대값",
                        "value": "-1골드"
                    }
                ]
            }
        ]
    }
    response = requests.post(day_webhook_url, headers=headers, json=data)

