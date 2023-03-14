import Modules.Models as Models
import Modules.Reddit.Video as Video
import Modules.Reddit.Images as Image
import Modules.Messages as Messages
import Modules.Chat as Chat
import Modules.Flag as Flag
import Initialize, discord, json, sys
from discord import option

# Searches for and opens the data files, the program will stop if they do not exist
try:
  with open("./Data/Token.json", "r") as f:
      data = json.load(f)
  with open('./Data/Models.json', 'r') as f:
      model_data = json.load(f)
except Exception as e:
   print(e)
   sys.exit()

AImodel = [model['id'] for model in model_data]


#Initialize
client = Initialize.init(data)


# Thread listener
@client.event
async def on_message(message):
     return


###Run our command handler
#/ping
@client.command(description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {client.latency}")

#/chat <query>
@client.slash_command(description="OpenAI chatbot Integration.")
@option("query", description="What would you like to talk about?", required=True)
async def chat(ctx: discord.ApplicationContext, query: str):
  await Chat.chat(ctx, query)

#/gpt <query> <model>
@client.slash_command(description="OpenAI chatbot Integration.")
@option("query", description="Your message to the bot", required=True)
async def gpt(ctx: discord.ApplicationContext, query: str):
  await ctx.defer(); await ctx.send(Models.generate_response(query))

#/info <model>
@client.slash_command(description="Info on the AI models compatible with /gpt.")
@option("model", description="Choose your AI model", choices=AImodel, required=True)
async def info(ctx: discord.ApplicationContext, model: str):
  await Models.info(ctx, model, model_data)

#/draw <query>
@client.slash_command(description="Dall-E image generation.")
@option("query", description="What would you like me to draw?", required=True)
async def draw(ctx: discord.ApplicationContext, query: str):
  await Models.dalle(ctx, query)

#/reddit images <subreddit> <quantity>
@client.slash_command(description="Pull images from a subreddit.")
@option("subreddit", description="What subreddit to scrape from? (case sensitive)", required=True)
@option("quantity", description="How many images to download? (Maximum 6)", required=True)
async def images(ctx: discord.ApplicationContext, subreddit: str, quantity: int):
  await Image.images(ctx, subreddit, quantity)

#/reddit video <subreddit> <quantity>
@client.slash_command(description="Pulls a video from a subreddit.")
@option("subreddit", description="What subreddit to scrape from? (case sensitive)", required=True)
@option("quantity", description="How many videos to download? (Maximum 6)", required=True)
async def videos(ctx: discord.ApplicationContext, subreddit: str, quantity: int):
  await Video.reddit_video_main(ctx, subreddit, quantity)

#/purge
@client.slash_command(description="Clears all messages.")
async def purge(ctx, channel: discord.TextChannel):
  await Messages.purge(ctx, channel)

#/draw <query>
@client.slash_command(description="Turns a pfp into a pride flag.")
@option("flag", description="What kind of boykisser are you?", required=True)
@option("user", description="Who's flag do I make?")
async def flag(ctx: discord.ApplicationContext, flag: str, user: discord.User):
  await Flag.pride(ctx, flag, user)

# Start the bot
client.run(data["discord"])
