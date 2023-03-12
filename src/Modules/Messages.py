import json
async def purge(ctx, channel):
    """This command deletes and recreates a channel to clear its content"""
    with open("./Data/Blacklist.json", "r") as f:
      blacklist = json.load(f)
    if not channel.permissions_for(ctx.author).manage_channel:
        await ctx.respond("You do not have permissions to clear this channel.")
        return
    if str(channel.id) in blacklist["purgeID"]:
        await ctx.respond("This channel cannot be purged.")
        return

    # Store the channel information
    channel_name = channel.name
    channel_topic = channel.topic
    channel_position = channel.position
    channel_category = channel.category
    channel_overwrites = channel.overwrites

    # Delete the channel
    await channel.delete()

    # Recreate the channel with the stored information
    new_channel = await channel_category.create_text_channel(
        name=channel_name,
        topic=channel_topic,
        position=channel_position,
        overwrites=channel_overwrites
    )

    # Send a message confirming the recreation
    await new_channel.send(f"The channel **{channel_name}** has been successfully deleted and recreated with the same settings and permissions.")

async def appendContext(context, response, speaker, id):
    context[id] += f"{speaker}: {response.choices[0].text} "
    with open('./Data/Context.json', 'w') as f:
      json.dump(context, f)