import os
import io
import random
import discord
from PIL import Image

async def headpat(ctx):
    """This command randomly selects an image from the Headpats directory and sends it"""
    images_dir = "./Data/Images/Headpats/"
    images = os.listdir(images_dir)
    random_image = random.choice(images)
    with open(images_dir + random_image, 'rb') as f:
        image_data = f.read()

    # Open the image from the bytes
    img = Image.open(io.BytesIO(image_data))

    # Resize the image to 256x256
    img = img.resize((256, 256))

    # Convert the image to bytes again
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()

    # Send the resulting image as a message
    await ctx.respond(file=discord.File(io.BytesIO(img_bytes), filename=random_image))
