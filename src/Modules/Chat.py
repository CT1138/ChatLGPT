import openai, json
def chatgpt(queries):
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=queries)
    return chat['choices'][0]['message']['content']

def conversation(query, role):
    dictionary = {"role": role, "content": query}

    # Read the JSON file
    with open('./Data/convo.json', 'r') as file:
        data = json.load(file)

    # Append the input dictionary
    data.append(dictionary)

    # Write to the JSON file
    with open('./Data/convo.json', 'w') as file:
        json.dump(data, file)
    
    # Read the JSON file
    with open('./Data/convo.json', 'r') as file:
        context = json.load(file)
    return context
        
async def chat(ctx, input):
    await ctx.defer()

    context = conversation(input, "user")
    response = chatgpt(context)
    conversation(response, "assistant")

    await ctx.respond(response)