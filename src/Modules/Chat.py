import openai, json, os, shutil

def chatgpt(queries):
    # This function handles the OpenAI API
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=queries)
    
    # ChatGPT sends its responses as a json object, to get our response content we have to access multiple levels and then return it:
    return chat['choices'][0]['message']['content']

def conversation(query, role, ctx):

    # Creates a context file for the user if it doesn't exist
    output_path = f"./Data/Conversations/{ctx.author.id}.json"
    if not os.path.exists(output_path):
        shutil.copyfile("./Data/ConvoTemplate.json", output_path)
    
    dictionary = {"role": role, "content": query}

    # Read the JSON file
    with open(output_path, 'r') as file:
        data = json.load(file)

    # Append the input dictionary
    data.append(dictionary)

    # Write to the JSON file
    with open(output_path, 'w') as file:
        json.dump(data, file)
    
    # Read the JSON file
    with open(output_path, 'r') as file:
        context = json.load(file)
    return context
        
async def chat(ctx, input):
    await ctx.defer()
    try:

        context = conversation(input, "user", ctx)
        response = chatgpt(context)

        # Check if response is over 2000 characters
        if len(response) > 2000:
            response_chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
            for chunk in response_chunks:
                # If the response exceeds discord's character limit, the bot will split its response into chunks which will be sent individually
                conversation(chunk, "assistant", ctx)
                await ctx.respond(chunk)
                print(f"[ChatGPT] Query: {input[:20]}...\nResponse: {chunk[:20]}...")
        else:
            # Otherwise, if the response is a sufficient length to be sent raw, it will be sent to discord directly.
            conversation(response, "assistant", ctx)
            await ctx.respond(response)
            print(f"[ChatGPT] Query: {input[:20]}...\nResponse: {response[:20]}...")
    except Exception as e:
        #If there's an error, this will keep the bot from crashing and instead output the error in the terminal and cease the function
        await ctx.respond("There was an error, please contact an administrator for help!")
        print(e)
        return