# External libs import
# execute command `pip install -r requirements.txt` to install all the dependencies
import asyncio

# utils import
from utils import create_new_member_welcome_card, check, update_json_file_from_dict

# constants import
from globals import *

if ENVIRONMENT.casefold() == "DEV".casefold():
    DISCORD_GUILD_ID = 700439581706682428
    DISCORD_WELCOME_CHANNEL = 813158607155757157
elif ENVIRONMENT.casefold() == "PROD".casefold():
    DISCORD_GUILD_ID = 1264408428697096284
    DISCORD_WELCOME_CHANNEL = 1264408430677065799

bot_strings = strings["discord_bot"]


def reload_strings():
    global bot_strings
    bot_strings = strings["discord_bot"]

@bot.event
async def on_ready():
    if STATUS.casefold() == "MAINT".casefold():
        await bot.change_presence(
            status=discord.Status.do_not_disturb,
            activity=discord.Game(
                name=bot_strings["on_ready"]["statuses"]["maintenance"]
            )
        )
    else:
        await bot.change_presence(
            activity=discord.Game(
                name=bot_strings["on_ready"]["statuses"]["online"]
            )
        )
    print(f"{bot_strings['on_ready']['ready_message']} | {bot_strings['version']}")


# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.MissingRole):
#         await ctx.send(strings["on_command_error"]["no_permission"])
#     else:
#         await ctx.send(f"{strings['on_command_error']['unknown_error']} : {error}")


@bot.event
async def on_message(message: discord.Message):
    # MiaouBot id
    if '<@1300938645108297779>' in message.content:
        await bot.get_channel(message.channel.id).send(bot_strings["on_message"]["automatic_bot_message"])


@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(DISCORD_WELCOME_CHANNEL)

    card = create_new_member_welcome_card(member)

    # map welcome message
    welcome_message = bot_strings["on_member_join"]["welcome_message"].replace("{member.mention}", member.mention).replace("{server.name}", bot.get_guild(DISCORD_GUILD_ID).name)

    # Sending welcome message
    await asyncio.sleep(delay=0)
    await channel.send(
        content=f"{welcome_message}",
        file=card
    )


@bot.hybrid_command(name="setup_welcome_background_image", description="Met à jour l'image de fond du message de bienvenue")
@commands.has_any_role("membre IUT", 1264408428931977223, 1264408428931977221)
async def setup_welcome_background_image(ctx: commands.Context, file: discord.Attachment):
    if os.path.isfile('./background.png'):
        os.remove('./background.png')

    await file.save('./background.png')
    await ctx.send(bot_strings["setup_welcome_background_image"]["action_success"])


@bot.hybrid_command(name="edit_welcome_message", description="Modifie le message de bienvenue")
@commands.has_any_role("membre IUT", 1264408428931977223, 1264408428931977221)
async def edit_welcome_message(ctx: commands.Context):
    await ctx.defer()
    card = create_new_member_welcome_card(ctx.author)
    bot_message = await ctx.send(
        bot_strings["edit_welcome_message"]["what_to_edit"],
        file=card,
        ephemeral=True
    )

    # free memory and disk space
    card.close()
    os.remove(f"{ctx.author.id}_card.html")
    os.remove("page.png")

    user_edit_choice = await bot.wait_for('message', check=check)

    while user_edit_choice.content.casefold() not in ['message'.casefold(), 'background'.casefold()]:
        await user_edit_choice.delete()
        await bot_message.edit(content=bot_strings["edit_welcome_message"]["wrong_user_input"], attachments=[])
        user_edit_choice = await bot.wait_for('message', check=check)

    await user_edit_choice.delete()

    if user_edit_choice.content.casefold() == "message".casefold():
        await bot_message.edit(content=bot_strings["edit_welcome_message"]["user_choice_message"], attachments=[])
        new_message = await bot.wait_for('message', check=check)
        new_message_content = new_message.content

        await new_message.delete()

        strings["discord_bot"]["on_member_join"]["welcome_message"] = new_message_content
        update_json_file_from_dict("./strings.json", strings)
        reload_strings()

    if user_edit_choice.content.casefold() == "background".casefold():
        await bot_message.edit(content=bot_strings["edit_welcome_message"]["user_choice_background"], attachments=[])
        new_background = await bot.wait_for('message', check=check)
        new_background_file = new_background.attachments[0]

        if os.path.isfile('./background.png'):
            os.remove('./background.png')

        await new_background_file.save('./background.png')
        await new_background.delete()

    await bot_message.edit(content=bot_strings["edit_welcome_message"]["action_success"])


@bot.hybrid_command(name="simulate_member_join", description="Simule l'évent on_member_join")
@commands.has_any_role("membre IUT", 1264408428931977223, 1264408428931977221, 1264408428931977220)
async def simulate_member_join(ctx: commands.Context, member: discord.Member):
    await ctx.defer()
    await asyncio.sleep(1)
    await on_member_join(member)
    await ctx.interaction.response.send_message(bot_strings["simulate_member_join"]["action_success"], ephemeral=True)


@bot.hybrid_command(name="sync", description="Synchronise les commandes avec l'arbre courant.")
@commands.has_any_role("membre IUT", 1264408428931977223, 1264408428931977221, 1264408428931977220)
async def sync(ctx: commands.Context):
    bot.tree.copy_global_to(guild=discord.Object(id=DISCORD_GUILD_ID))
    await bot.tree.sync(guild=discord.Object(id=DISCORD_GUILD_ID))
    await ctx.send(bot_strings["sync"]["action_success"])


@bot.hybrid_command()
async def ping(ctx: commands.Context):
    await ctx.typing()
    await asyncio.sleep(1)
    await ctx.send(bot_strings["ping"]["message"])


bot.run(DISCORD_BOT_TOKEN)
