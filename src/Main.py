import Modules.Models as Models
import Modules.Reddit.Video as Video
import Modules.Reddit.Images as Image
import Modules.Messages as Messages
import Modules.Chat as Chat
import Modules.Pride as Pride
import Modules.Headpat as Headpat
import Initialize, discord, json, sys
from discord import option

# Searches for and opens the data files, the program will stop if they do not exist
try:
  with open("./Data/Token.json", "r") as f:
    token = json.load(f)
  with open("./Data/Flags.json", "r") as f:
    flags = json.load(f)
except Exception as e:
  print(e)
  sys.exit()

#Initialize
client = Initialize.init(token)
Pride.flagCache()

###Run our command handler
#/ping
@client.command(description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {client.latency}")

#/chat <query>
@client.slash_command(description="OpenAI chatbot Integration.")
@option("query", description="What would you like to talk about?")
async def chat(ctx: discord.ApplicationContext, query: str):
  await Chat.chat(ctx, query)

#/gpt <query>
@client.slash_command(description="OpenAI Davinci Integration.")
@option("query", description="Your message to the bot")
async def gpt(ctx: discord.ApplicationContext, query: str):
  await Models.davinci(query, ctx)

#/draw <query>
@client.slash_command(description="Dall-E image generation.")
@option("query", description="What would you like me to draw?")
async def draw(ctx: discord.ApplicationContext, query: str):
  await Models.dalle(ctx, query)

#/images <subreddit> <quantity>
@client.slash_command(description="Pull images from a subreddit.")
@option("subreddit", description="What subreddit to scrape from? (case sensitive)")
@option("quantity", description="How many images to download? (Maximum 6)")
async def images(ctx: discord.ApplicationContext, subreddit: str, quantity: int):
  await Image.images(ctx, subreddit, quantity)

#/videos <subreddit> <quantity>
@client.slash_command(description="Pulls a video from a subreddit.")
@option("subreddit", description="What subreddit to scrape from? (case sensitive)")
@option("quantity", description="How many videos to download? (Maximum 6)")
async def videos(ctx: discord.ApplicationContext, subreddit: str, quantity: int):
  await Video.reddit_video_main(ctx, subreddit, quantity)

#/purge
@client.slash_command(description="Clears all messages.")
async def purge(ctx, channel: discord.TextChannel):
  await Messages.purge(ctx, channel)

#/headpat
@client.slash_command(description="Everyone deserves headpats :heart:")
async def headpat(ctx):
  await Headpat.headpat(ctx)

#/flag <flag1> <flag2> <animated>
@client.slash_command(description="You're all boykissers!")
@option("flag", description="What flag?", choices=flags)
async def flag(ctx, flag=str):
  await Pride.pride(ctx, flag)

# Start the bot
client.run(token["discord"])