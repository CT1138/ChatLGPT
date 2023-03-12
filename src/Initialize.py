import discord, openai

def init(data):
    """This function logs into our two main API's"""
    # Sets the API key for OpenAI
    openai.api_key = data["davinci"]
    
    # Logging into the Discord API
    intents = discord.Intents.all()
    intents.members = True
    client = discord.Bot(intents=intents)

    # Provide some feedback so we know the bot has connected
    @client.event
    async def on_ready():
        print(f"{client.user} is connected.")
    return client