from cogs.utils import *
from uuid import getnode as get_mac
import hashlib
import requests
'''
 Removed some code that loads the config from an old API that dont exist anymore
'''

#intesnt
intents = discord.Intents.default()
intents.reactions = True
intents.members = True

# main client variable
client = commands.AutoShardedBot(command_prefix=converted_prefixes, intents=intents)

# removing default help command
client.remove_command("help")

# console channel
client.system_channel = null

client.starttime = datetime.datetime.now()
client.color=0x268740

client.path="./info.json"
client.yt = ""
client.server = ""
client.invite=""

client.info = {}

file = open(client.path, "r", encoding="utf8")
result = json.load(file)
client.info = result
file.close()

client.message_count = client.info["message count"]
client.command_count = client.info["command count"]



'''
---bot extensions---

example:
{"test_folder": ["test_cog"]}

in this example a cog named "test_cog" in the folder named "test_folder" will be loaded
'''

extensions = client.info["cogs"]

# when program is activated, this function will run
if __name__ == "__main__":

    # loading jishakue cog
    client.load_extension('jishaku')
    os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
    client.reload_extension("jishaku")
    client.load_extension('cogs.startup')

    # looping trogh extension dictionary
    for key, value in extensions.items():

        # printing a message for every folder
        print(f"\nLoading: {key}\n")

        #going trugh cogs in folder
        for extension in value:

            #trying to load cog
            try:

                #loading cog
                client.load_extension(f"cogs.{key}.{extension}")

                #printing succes message
                print(f"succesfully loaded {key}.{extension}")

            except Exception as Exc:
                #if loading failed

                #print fail message
                print(f"failed to load extension {key}.{extension}\n{Exc}")





# what status the bot is curently on
client.current_status = 0

@tasks.loop(seconds=10)
async def status_loop():
    '''
    Function that loops every 10th seconds

    This function is constantly editing the bot status
    '''

    '''
    ---statuses---
    [["playing", "Nothing"]]

    this will result in the playing status and Nothing as game
    '''
    statuses = [["playing", "Nothing"], ["watching", "out for ,"], ["listening to", "sick music"], ["watching", "you"], ["playing", f"with my {len(client.users)} users"], ["watching", f"over my {len(client.guilds)} servers"]]

    #the status that will be used this iteration
    this_status = statuses[client.current_status]


    # adding to current status variable
    if client.current_status + 1 < len(statuses):
        # if adding one does not get larger than the amount of statuses add 1
        client.current_status += 1

    else:
        #else set current_status to 0
        client.current_status = 0


    if this_status[0] == "playing":
        #if first argument is "playing"
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=this_status[1]))


    if this_status[0] == "watching":
        #if first argument is "watching"
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=this_status[1]))


    if this_status[0] == "listening to":
        #if first argument is "listening to"
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=this_status[1]))




@client.event
async def on_ready():
    # when bot has succesfully started

    #trying to run status loop
    try:
        status_loop.start()

    except:
        #if runing status loop failed
        print("Failed to start status loop.")

    # printing online message
    permissions = discord.Permissions(1007675638)
    client.invite = discord.utils.oauth_url(permissions=permissions, client_id=client.user.id)

    # creating console webhook


    # printing the bot is online
    print(f"NoobBot is ready\nStartup time: {datetime.datetime.now().timestamp() - client.starttime.timestamp()}")




# ignore this command
@client.command()
async def test(ctx):
    message_sent = round(ctx.message.created_at.timestamp(), 2)
    message_detected = round(datetime.datetime.utcnow().timestamp(), 2)
    diference = round(message_detected-message_sent, 2)

    sending_respons = round(datetime.datetime.utcnow().timestamp(), 2)
    msg = await ctx.send(f"==========\n{message_sent} - Message sent\n{message_detected} - Message detected\n{diference} - Difference\n==========\n... - Sending respons\n... - Respons sent\n... - Difference\n==========\n... - Total difference")
    respons_sent = round(datetime.datetime.utcnow().timestamp(), 2)
    diference2 = round(respons_sent - sending_respons, 2)
    diference3 = round(respons_sent-message_sent, 2)
    await msg.edit(content=f"==========\n{message_sent} - Message sent\n{message_detected} - Message detected\n{diference} - Difference\n==========\n{sending_respons} - Sending respons\n{respons_sent} - Respons sent\n{diference2} - Difference:\n==========\n{diference3} - Total difference")



# running bot with token
client.run(str(client.info["token"]))
