import requests
from bs4 import BeautifulSoup
import random
import json
# import datetime


WIKIPEDIA_RANDOM_URL = "https://en.wikipedia.org/wiki/Special:Random"

def get_random_wikipedia_page():
    try:
        response = requests.get(WIKIPEDIA_RANDOM_URL)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find all paragraphs in the page content
            paragraphs = soup.find_all('p')
            text_lines = [p.get_text() for p in paragraphs if p.get_text().strip()]
            random_line = random.choice(text_lines)
            return random_line.strip()  # Remove leading/trailing whitespace
        else:
            return f"Failed to get page! (HTTP {response.status_code})."
    except Exception as e:
        return f"Oopsies: {str(e)}"

async def save_messages(ctx):
    channel = ctx.message.channel
    channel_dict = {}
    async for message in channel.history(limit=100):
        message_info = (message.content, message.created_at.strftime('"%Y.%m.%d.%H.%M.%S"'))
        channel_dict[message.author.id] = channel_dict.get(message.author.id, []) + [message_info]
    
    # {channel : {author : (message, time)}}
    with open('./messages.json', 'r') as f:
        message_dict = json.load(f)
    
    message_dict[channel.id] = message_dict.get(channel.id, {})
    for author, message_infos in channel_dict.items():
        seen_message_infos = set(list(map(tuple, message_dict[str(channel.id)].get(str(author), []))))
        for message_info in message_infos:
            if message_info in seen_message_infos:
                break  # message already in message.json --> so are the rest
            seen_message_infos.add(message_info)
        message_dict[channel.id][author] = list(seen_message_infos)
    
    with open('./messages.json', 'w') as f:
        message_dict = json.dump(message_dict, f, indent=4)