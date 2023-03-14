from PIL import Image, ImageDraw
import discord, requests, os, json, random
from io import BytesIO

def flagCache():
    """This function checks for any images in Flags.json and creates an array to list each once for later use"""
    dir_path = "./Data/Images/Pride/"
    
    # Get a list of all files in the directory
    files = os.listdir(dir_path)
    
    # Filter the list to only include .png files
    png_files = [f for f in files if f.endswith(".png")]
    
    # Create an empty list to store the file names
    file_names = []
    
    # Loop through the list of .png files and extract the file name (minus the .png extension)
    for png_file in png_files:
        file_name = os.path.splitext(png_file)[0]
        file_names.append(file_name)
    
    # Convert the list to a JSON array and store it in a file
    with open("./Data/Flags.json", "w") as file:
        json.dump(file_names, file)


async def pride(ctx, flag1, user):
    """Takes the user's avatar and pastes the selected pride flag behind it"""
    if not user:
        user = ctx.author
    flags = flag1
    if flag1 == "Random":
        with open("./Data/Flags.json", "r") as file:
            flagArray = json.load(file)
            flags = random.choice(flagArray)

    # Get the user's avatar URL
    user_avatar_url = str(user.avatar.url)
    # Download the user's avatar
    response = requests.get(user_avatar_url)
    avatar_image = Image.open(BytesIO(response.content)).resize((100, 100)).convert('RGBA')

    # Create a circular mask
    mask = Image.new("L", avatar_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + avatar_image.size, fill=255)

    # Apply the mask to the avatar image
    avatar_image.putalpha(mask)

    # Open the image file to be overlaid
    print(flags)
    base_image = Image.open(f"./Data/Images/Pride/{flags}.png").resize((200, 200)).convert('RGBA')
    # Overlay the avatar onto the base image
    base_image.paste(avatar_image, (50, 50), avatar_image)
    # Save the resulting image
    imagename = f"{user.name}-{flags}"
    base_image.save(f"./Data/Images/Pride/{imagename}.png")

    # Send the resulting image as a message
    await ctx.respond(file=discord.File(f"./Data/Images/Pride/{imagename}.png"))
    os.remove(f"./Data/Images/Pride/{imagename}.png")