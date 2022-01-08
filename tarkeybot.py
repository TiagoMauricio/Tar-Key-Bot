from nextcord.ext import commands
import time, discord, configparser as cp

# parse configs on .env file
cfg = cp.ConfigParser()
cfg.read('.env')
TOKEN = cfg['secrets']['TOKEN']

# creating bot
bot = commands.Bot(command_prefix='!')

# setting bot variables
bot.BOT_CHANNEL_CATEGORY = 'Tar-Key-Bot'
bot.LIST_CHANNEL = 'key-list'
bot.REQ_CHANNEL = 'key-request'
bot.IN_MEMORY_DATA = {}
bot.LIST_CHANNEL_OBJ = None
bot.REQ_CHANNEL_OBJ = None

# temp
test_keys = {'Customs':['Tarcone Directors Office', 'Dorms 206']}

# helper functions
async def remote_log(ctx, message):
    await ctx.channel.send(message)

async def create_key_list(ctx):

    await bot.LIST_CHANNEL_OBJ.set_permissions(ctx.guild.default_role, read_messages=False)

    # this could be done better but lets try like this
    key_counter = 1
    for tmap in test_keys:
        await bot.LIST_CHANNEL_OBJ.send(f'---------------------------{tmap}---------------------------')
        for key in test_keys[tmap]:
            await bot.LIST_CHANNEL_OBJ.send(f'#{key_counter}: {key}')
            key_counter += 1

# automatic commands
@bot.event
async def on_ready():
    print('Tar-Key online!')
    # load channels if they exist
    channel_list = bot.get_all_channels()
    key_list_channel = discord.utils.get(channel_list, name=bot.LIST_CHANNEL)
    if key_list_channel:
        bot.LIST_CHANNEL_OBJ = key_list_channel

    key_request_channel = discord.utils.get(channel_list, name=bot.REQ_CHANNEL)
    if key_request_channel:
        bot.REQ_CHANNEL_OBJ = key_request_channel

@bot.event
async def on_raw_reaction_add(payload):
    print(payload)
    if bot.LIST_CHANNEL_OBJ.id == payload.channel_id:
        message = await bot.LIST_CHANNEL_OBJ.fetch_message(payload.message_id)
        if message.content[0] != '#':
            print('Unkown message')
            return
        # strip down the message and grab the key ID
        # this ugly AF but who cares LUL KEKW
        splited_key_msg = message.content.split(': ')
        key_id = splited_key_msg[0].split('#')[1]
        key_name = splited_key_msg[1]
        # create dict entry if it doesnt exist
        try:
            bot.IN_MEMORY_DATA[key_id]['members'].append(payload.member.name)
        except KeyError:
            bot.IN_MEMORY_DATA[key_id] = {'name': key_name, 'members': [payload.member.name]}
        # add record of someone having that key
        print(bot.IN_MEMORY_DATA)

#@bot.event
#async def on_raw_reaction_remove(payload):

# bot commands
@bot.command()
async def ping(ctx):
    await ctx.reply('Pong!')

@bot.command()
async def init(ctx, reset_bot=''):

    reset_bot = (True if reset_bot == 'reset' else False)

    await remote_log(ctx, 'Running init operations!')
    start_time = time.time()

    cat = discord.utils.get(ctx.guild.categories, name=bot.BOT_CHANNEL_CATEGORY)
    if not cat:
        await ctx.message.guild.create_category(bot.BOT_CHANNEL_CATEGORY)
        cat = discord.utils.get(ctx.guild.categories, name=bot.BOT_CHANNEL_CATEGORY)
    else:
        await remote_log(ctx, f'{bot.BOT_CHANNEL_CATEGORY} Category already exists')

    # Check if list channel exists and create if not
    key_list_channel = discord.utils.get(ctx.guild.channels, name=bot.LIST_CHANNEL)
    if key_list_channel:
        await remote_log(ctx, f'Channel already exists: {key_list_channel}')
        first_run = False
    else:
        await remote_log(ctx, f'Creating channel: {key_list_channel}')
        await ctx.message.guild.create_text_channel(bot.LIST_CHANNEL, category=cat)
        key_list_channel = discord.utils.get(ctx.guild.channels, name=bot.LIST_CHANNEL)
        first_run = True

    # Check if request channel exists and create if not
    key_request_channel = discord.utils.get(ctx.guild.channels, name=bot.REQ_CHANNEL)
    if key_request_channel:
        await remote_log(ctx, f'Channel already exists: {key_request_channel}')
    else:
        await remote_log(ctx, f'Creating channel: {key_request_channel}')
        await ctx.message.guild.create_text_channel(bot.REQ_CHANNEL,category=cat)
        key_request_channel = discord.utils.get(ctx.guild.channels, name=bot.REQ_CHANNEL)

    # set bot channels
    bot.LIST_CHANNEL_OBJ = key_list_channel
    bot.REQ_CHANNEL_OBJ = key_request_channel

    # create mesages with keylist
    if first_run or reset_bot:
        await create_key_list(ctx)

    end_time = time.time()
    await remote_log(ctx, "Initial setup has finished in %s seconds" % (round(end_time - start_time, 2)))

bot.run(TOKEN)
