import discord
import openai
import Modules.Models as Models

def init(data):
    # Sets the API key for OpenAI
    openai.api_key = data["davinci"]

    # Logging into the Discord API
    intents = discord.Intents.all()
    intents.members = True
    client = discord.Bot(intents=intents)

    status = Models.completions("Give me a random news headline.")
    activity = discord.Activity(name=status, type=discord.ActivityType.watching)
    client = discord.Bot(intents=intents, activity=activity)

    # Provide some feedback so we know the bot has connected
    @client.event
    async def on_ready():
        print(f"{client.user} is connected.")
        
    return client