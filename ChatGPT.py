import openai
import discord
from discord.ext import commands

import setting

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='', intents=intents)

MSlist=[]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    global MSlist
    if message.author == bot.user:
        return
    user_input = message.content
    if user_input in ["クリア","clear","くりあ","x","消して","けして","リセット","りせっと"]:
        MSlist=[]
        await message.channel.send("了解です。"+user_input+"しました")
        return
    response =  chat_with_gpt(user_input)
    await message.channel.send(response)
    print(user_input)

def chat_with_gpt(user_input):
    global MSlist
    openai.api_key = setting.OpenaiAPI

    if len(MSlist)==0:
        MSlist=[{"role": "user", "content": user_input }]

    else:
        MSlist.append({"role": "user", "content": user_input })

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=MSlist)

    prev_user_content =user_input 
    prev_assistant_content = response.choices[0]["message"]["content"].strip()

    MSlist.append({"role": "assistant", "content":prev_assistant_content})

    return prev_assistant_content



def main():
    print("Welcome to ChatGPT! Type 'exit' to end the conversation.")
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        response = chat_with_gpt(user_input)
        print("ChatGPT:", response)



if __name__ == '__main__':
    bot.run(setting.DiscordTOKEN)