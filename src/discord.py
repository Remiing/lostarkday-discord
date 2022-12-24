import requests
# import config
import os
from dotenv import load_dotenv


load_dotenv()
# day_webhook_url = config.day_webhook_url
# day_webhook_url = os.environ['day_webhook_url']
day_webhook_url = os.environ.get('day_webhook_url')


def sendMessage(characterName, characterClass, equipType, before_equipLV, after_equipLV, part_gold):
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
                        "value": f"{part_gold} 골드"
                    }
                ]
            }
        ]
    }
    response = requests.post(day_webhook_url, headers=headers, json=data)

