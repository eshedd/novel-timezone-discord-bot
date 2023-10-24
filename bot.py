import discord
import random
from discord.ext import commands

from utils import get_random_wikipedia_page, save_messages
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import networkx as nx
from textblob import TextBlob
from jasper_calendar import get_pure_date, get_pure_now
import pydot


matplotlib.use('Agg')

api_key = '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'

# List of GIF URLs
gif_urls = [
    'https://media.tenor.com/HP-H7t_K2O4AAAAC/swarm-buzz.gif',
    'https://media.tenor.com/Gb-b1gz8yDwAAAAC/bugs-plague.gif',
    'https://media.tenor.com/PNCYorqu7HEAAAAC/run-away-jurassic-world-dominion.gif',
    'https://media.tenor.com/FlHGMvloQQ8AAAAC/batty-bat.gif'
]

# organization structure
org_structure = {
    "Purifier": ["Guardian of Purity", "Populace", "Mechanical Wrangler"],
    "Guardian of Purity": ["The Clock"],
    "Mechanical Wrangler": ["Impure"],
    "Populace": [],
    "Impure": []
}

# Define the intents your bot needs
intents = discord.Intents.default()
intents.message_content = True  # Enable this intent to receive message content

# Create a bot instance with a command prefix and intents
bot = commands.Bot(command_prefix='&', intents=intents)

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(ctx):
    # Check if the message author is the bot itself to avoid an infinite loop
    if ctx.author == bot.user:
        return
    # Check if the bot was mentioned in the message
    if bot.user.mentioned_in(ctx):
        await ctx.channel.send(f'Hello, {ctx.author.mention}!')
    # Continue processing other commands or messages
    await bot.process_commands(ctx)

@bot.command()
async def say(ctx, *, message):
    '''
    Parrot what user says.
    '''
    await ctx.send(message)
    await save_messages(ctx)

@bot.command()
async def crazy(ctx, *, message):
    '''
    Crazy parrot what user says.
    '''
    message += ' '
    await ctx.send(f'{message*5} WHOOOO BOY... YES! {message.upper()}!')
    await save_messages(ctx)

@bot.command()
async def davidme(ctx):
    '''
    Image of David
    '''
    # Create an embed message
    embed = discord.Embed(
        title="Look, David!",
        description="Enjoy this _cool_ image...",
        color=discord.Color.blue()
    )

    file = discord.File("/Users/edawg/Documents/junk-drawer/memories/other/d1.jpeg", filename="davie.png")
    embed.set_image(url="attachment://davie.png")

    # Send the embed message with the image attachment
    await ctx.send(embed=embed, file=file)
    await save_messages(ctx)

@bot.command()
async def inform(ctx):
    '''
    Return random line of a random Wikipedia page
    '''
    await ctx.send(get_random_wikipedia_page())
    await save_messages(ctx)

@bot.command()
async def swarm(ctx):
    '''
    Send swarm gif from list above
    '''
    random_gif_url = random.choice(gif_urls)
    await ctx.send(random_gif_url)
    await save_messages(ctx)

@bot.command()
async def code(ctx, *, message):
    '''
    Encode a string to secret code
    '''
    s = 'code: ' + str(sum([ord(c) for c in message]))
    await ctx.send(s)
    await save_messages(ctx)

@bot.command()
async def interpret(ctx, *, message):
    '''
    Interpret a code
    '''
    replies = ['careful', 'no good', 'dangerous', 'safe', 'neutral']
    try:
        code = int(message)
        await ctx.send(replies[code % len(replies)])
    except:
        await ctx.send('nope, that code is no good')
    await save_messages(ctx)

@bot.command()
async def graph(ctx, *, message_count=None):
    '''
    Return graph of user message sentiment
    '''
    if message_count:
        try:
            message_count = int(message_count)
        except:
            await ctx.send('gimme a number')
    else:
        message_count = 10
    # Get the user who sent the command
    author = ctx.author
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=100):
        if message.author == author:
            messages.append(message.content)
        if len(messages) >= message_count:
            break
    scores = []
    for m in messages:
        blob = TextBlob(m)
        scores.append(blob.sentiment.polarity)

    plt.plot(range(len(messages)), scores, marker='o')
    plt.xlabel('message')
    plt.ylabel('sentiment polarity')
    plt.title(f'Sentiment of the Last {message_count} Messages in {channel.name} from {author}')
    plt.savefig('./graph.png')
    
    file = discord.File("./graph.png", filename="graph.png")
    embed = discord.Embed(
        title=f"Information for {author}",
        description="please read carefully",
        color=discord.Color.red()  # You can choose a different color
    )
    embed.set_image(url="attachment://graph.png")

    if os.path.isfile('./graph.png'):
        os.remove('./graph.png')
    plt.clf()
    # Send the embed message with the image attachment
    await ctx.send(embed=embed, file=file)
    await save_messages(ctx)

@bot.command()
async def date(ctx, *, message):
    '''
    Get date in pure time
    '''
    try:
        await ctx.send(get_pure_date(message))
    except:
        await ctx.send('GIMME YEAR/MONTH/DAY')
    await save_messages(ctx)

@bot.command()
async def now(ctx):
    '''
    Get current time in pure time
    '''
    await ctx.send(get_pure_now())
    await save_messages(ctx)

@bot.command()
async def org(ctx):
    '''
    Return organization of roles with users
    '''
    # roles = ctx.guild.roles
    # Generate the org chart
    org_chart = "Organization Roles:\n"
    for position, subordinates in org_structure.items():
        org_chart += f"- {position}\n"
        for subordinate in subordinates:
            org_chart += f"  └── {subordinate}\n"

    await ctx.send(org_chart)
    await save_messages(ctx)


@bot.command()
async def call(ctx):
    return

# Run the bot with your bot token
bot.run('MTE1NDI5ODg2ODk3MjkyOTA3NQ.G-U-oa.Oll4TdQZPBOXSUdz-mxxjMdqil-08nM7kYEhiA')


# bot = interactions.Client(token="MTE1NDI5ODg2ODk3MjkyOTA3NQ.G-U-oa.Oll4TdQZPBOXSUdz-mxxjMdqil-08nM7kYEhiA")
# # bot = interactions.Client(token=api_key)

# @bot.command(
#     name="egg",
#     description="This is the first command I made!",
# )
# async def egg(ctx: interactions.CommandContext):
#     await ctx.send("Hi there!")

# bot.start()