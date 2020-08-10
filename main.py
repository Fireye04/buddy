import discord
from discord.ext import commands
import random
import pickle
import asyncio

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

rollInitiative = False
total = 0

Initiatives = []
Healths = []


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='.help'))
    print("Ready")


@client.command(aliases=["h", "H"])
async def help(ctx):
    await ctx.send("How to use this help menu\n ")

    embed = discord.Embed(
        title='main command help',
        colour=discord.Colour.blue()
    )
    embed.add_field(name="<> - anything between these brackets should be replaced with an input", value="<input here>", inline=False)
    embed.add_field(name="() - anything between these parenthesis is optional", value="(Optional stuff here)", inline=False)
    embed.add_field(name="[] - choose one of the items between these brackets", value="[Choice1,Choice2]", inline=False)

    await ctx.send(embed=embed)

    async with ctx.typing():
        await asyncio.sleep(1)
        embed = discord.Embed(
            title='command description help',
            colour=discord.Colour.blue()
        )
        embed.add_field(name="The Description contains 3 sections", value="Each section is seperated with a '-'", inline=False)
        embed.add_field(name="Number 1", value="Command description", inline=False)
        embed.add_field(name="Number 2", value="An example of the use of a command", inline=False)
        embed.add_field(name="Number 3", value="Command aliases", inline=False)
    await ctx.send(embed=embed)
    
    
    ################################ENTER NEW COMMAND HELP HERE########################################################
    async with ctx.typing():
        await asyncio.sleep(1)
        embed = discord.Embed(
            title='Help',
            colour=discord.Colour.blue()
        )
        embed.add_field(name=".roll (<Number of dice>d<Number of sides>)([+,-]<Modifier>)", value="rolls dice, auto"
                                                                                                  " rolls 1d20 - .r"
                                                                                                  " 5d20+1 - .r",
                        inline=False)
        embed.add_field(name=".initiative <number of characters; both npcs and pcs>", value="makes an initiative chart; files"
                                                                                            " can be overridden -"
                                                                                            " .i 4 - "
                                                                                            ".i", inline=False)
        embed.add_field(name=".recallInitiative <save name; caps sensitive>", value="recalls a previous initiative order - "
                                                                          ".ri InitiativeOrder - .ri", inline=False)
        embed.add_field(name=".health <number of characters; both npcs and pcs>", value="stores health; files"
                                                                                            " can be overridden -"
                                                                                            " .hp 4 - "
                                                                                            ".hp", inline=False)
        embed.add_field(name=".recallHealth <save name; caps sensitive>", value="recalls a previous health chart - "
                                                                                     ".rh HealthStorage - .rh", inline=False)
    await ctx.send(embed=embed)

    ################################ENTER NEW COMMAND HELP HERE########################################################
    

# automatically sets args to 1d20
@client.command(aliases=["r","R"])
async def roll(ctx, *, args="1d20"):
    global total
    total = 0
    rollList = []
    plus = False
    minus = False
    # Checks for +
    if len(args.split('+')) == 2:
        # Sets + to true and splits args
        plus = True
        plusSplit = args.split('+')
    # Checks for -
    elif len(args.split('-')) == 2:
        # Sets - to true and splits args
        minus = True
        minusSplit = args.split('-')

    try:
        # splits d depending on whether +, -, or none of the above
        if plus is True:
            # +
            num = plusSplit[0].split('d')[0]
            die = plusSplit[0].split('d')[1]
        elif minus is True:
            # -
            num = minusSplit[0].split('d')[0]
            die = minusSplit[0].split('d')[1]
        else:
            # none
            num = args.split('d')[0]
            die = args.split('d')[1]
    # if no d (.r 12)
    except IndexError:
        num = 1
        die = args
    # if no num before d (.r d20)
    if num == '':
        num = 1
    try:
        # try to convert to int
        num = int(num)
        die = int(die)
    except TypeError:
        # sets roll to 1d20 if str
        num = 1
        die = 20

    for i in range(num):
        x = random.randint(1,die)
        total += x
        rollList.append(str(x))

    if plus is True:
        try:
            total = total + int(plusSplit[1])
        except ValueError:
            ctx.send("Sorry! Please provide a number for a modifier.")
        z = f"+{plusSplit[1]}"
    elif minus is True:
        try:
            total = total - int(minusSplit[1])
        except ValueError:
            ctx.send("Sorry! Please provide a number for a modifier.")
        z = f"-{minusSplit[1]}"
    if len(rollList) == 1:
        embed = discord.Embed(
            title='Roll Results',
            colour=discord.Colour.red()
        )
        embed.add_field(name=str(total), value="Total value", inline=True)
        if plus is True or minus is True:
            embed.add_field(name=z, value="Modifier", inline=False)

    else:
        embed = discord.Embed(
            title='Roll Results',
            colour=discord.Colour.red()
        )
        embed.add_field(name=str(total),value="Total Value", inline=True)
        if plus is True or minus is True:
            embed.add_field(name=z, value="Modifier", inline=False)
        embed.add_field(name=", ".join(rollList),value="All Rolls", inline=False)

    await ctx.send(embed=embed)


@client.command(aliases=["i", "I"])
async def initiative(ctx, *, args=None):
    global Initiatives
    peopleint = False
    b = "f"
    sLst = []
    lst = []
    nums = []
    names = []
    final = []
    if args is None:
        await ctx.send("Please enter the number of creatures rolling initiative (players or otherwise) (like: .i 4)")
    else:
        try:
            people = int(args)
            peopleint = True
        except ValueError:
            await ctx.send("Please enter the number of creatures rolling initiative, players or otherwise (like: .i 4)")
        if peopleint is True:

            async def check(ctx):
                global b
                b = str(ctx.author)
                if ctx.content.find('.r') != -1 and ctx.author.bot is False:
                    return True
                else:
                    return False

            async def check2(ctx):
                strctx = str(ctx.content)

                if strctx.is_integer() is True:
                    if ctx.author.bot is False:
                        return True
                    else:
                        return False
                else:
                    await ctx.send("Please enter a number")
                    return False

            async def checc(ctx):
                if ctx.author.bot is False:
                    return True
                else:
                    return False

            await ctx.send("Please enter the number of NPCs rolling initiative")
            npcs = await client.wait_for('message', timeout=30, check=lambda message: message.author != ctx.bot.user and float(message.content).is_integer() is True)

            npcs = str(npcs.content)
            npcs = int(npcs)

            await asyncio.sleep(0.5)

            await ctx.send(f"Enter a save name. (You will need this to retrieve this initiative order)")
            save = await client.wait_for('message', timeout=30, check=lambda message: message.author != ctx.bot.user)

            save = str(save.content)

            await asyncio.sleep(0.5)

            Initiatives.append(save)
            pickle.dump(Initiatives, open("XxX32MillinnXxX", "wb"))
            for i in range(people-npcs):
                i += 1

                await ctx.send(f"Player Character {i}, roll initiative!")
                await client.wait_for('message', timeout=30, check=lambda message: message.author != ctx.bot.user and message.content.find('.r') != -1)

                await asyncio.sleep(0.5)

                await ctx.send(f"Enter Player Character {i}'s name")
                name = await client.wait_for('message', timeout=30, check=lambda message: message.author != ctx.bot.user)

                await asyncio.sleep(0.5)

                name = str(name.content)

                storage = name + ":" + str(total)
                sLst.append(storage)

            async with ctx.typing():
                await asyncio.sleep(0.5)

            for i in range(npcs):
                i += 1

                await ctx.send(f"Roll initiative for NPC {i}")
                await client.wait_for('message', timeout=30, check=lambda message: message.author != ctx.bot.user and message.content.find('.r') != -1)

                await asyncio.sleep(0.5)

                await ctx.send(f"Enter NPC {i}'s name")
                name = await client.wait_for('message', timeout=30, check=lambda message: message.author != ctx.bot.user)

                await asyncio.sleep(0.5)

                name = str(name.content)

                storage = name + ":" + str(total)
                sLst.append(storage)

            pickle.dump(sLst, open(save, "wb"))
            pickkle = pickle.load(open(save, "rb"))
            for i in range(len(pickkle)):
                sp = pickkle[i].split(":")

                lst.append(sp[0])
                lst.append(sp[1])
                names.append(sp[0])
                nums.append(sp[1])

            lst1 = sorted(nums, reverse=True)
            print(lst1)
            print(lst)
            for i in range(len(lst1)):
                index = lst.index(lst1[i])
                final.append(lst[index-1])
                final.append(lst[index])

            embed = discord.Embed(
                title='Initiative Order',
                colour=discord.Colour.green()
            )
            for i in range(len(lst)):
                if i%2 == 0:

                    embed.add_field(name=str(final[i]), value=final[i+1], inline=False)
            await ctx.send(embed=embed)

@client.command(aliases=["ri","Ri","RI","rI"])
async def recallInitiative(ctx, *, args=None):
    lst = []
    names = []
    nums = []
    final = []
    Initiatives = pickle.load(open("XxX32MillinnXxX", "rb"))
    if args is None:
        await ctx.send("Please enter your save name. (.re <save name here>)")
    elif args not in Initiatives:
        await ctx.send("Sorry! Looks like you entered a health save file. Please try again.")
    else:
        try:
            lOAd = pickle.load(open(str(args), "rb"))
            for i in range(len(lOAd)):
                sp = lOAd[i].split(":")

                lst.append(sp[0])
                lst.append(sp[1])
                names.append(sp[0])
                nums.append(sp[1])

            lst1 = sorted(nums)
            print(lst1)
            print(lst)
            for i in range(len(lst1)):
                index = lst.index(lst1[i])
                final.append(lst[index-1])
                final.append(lst[index])

            embed = discord.Embed(
                title='Initiative Order',
                colour=discord.Colour.green()
            )
            for i in range(len(lst)):
                if i%2 == 0:

                    embed.add_field(name=str(final[i]), value=final[i+1], inline=False)
            await ctx.send(embed=embed)
        except FileNotFoundError:
            await ctx.send("404 File not found.\n That Initiative does not exist. Remember that it is caps sensitive!")


@client.command(aliases=["hp", "hP", "Hp", "HP"])
async def Health(ctx, *, args=None):
    global Initiatives
    peopleint = False
    b = "f"
    sLst = []
    lst = []
    nums = []
    names = []
    final = []
    if args is None:
        await ctx.send("Please enter the number of creatures you want to save the health of, players or otherwise (like: .hp 4)")
    else:
        try:
            people = int(args)
            peopleint = True
        except ValueError:
            await ctx.send("Please enter the number of creatures you want to save the health of, players or otherwise (like: .hp 4)")
        if peopleint is True:
            async def check2(ctx):
                strctx = str(ctx.content)

                if strctx.is_integer() is True:
                    if ctx.author.bot is False:
                        return True
                    else:
                        return False
                else:
                    await ctx.send("Please enter a number")
                    return False

            async def checc(ctx):
                if ctx.author != ctx.bot.user:
                    return True
                else:
                    return False

            await ctx.send("Please enter the number of NPCs (including monsters) you want to store the health of")
            npcs = await client.wait_for('message', timeout=30, check=lambda message: message.author != ctx.bot.user and float(message.content).is_integer() is True)

            npcs = str(npcs.content)
            npcs = int(npcs)

            await asyncio.sleep(0.5)

            await ctx.send(f"Enter a save name. (You will need this to retrieve this health save)")
            save = await client.wait_for('message', timeout=30, check=lambda message: message.author != ctx.bot.user)

            await asyncio.sleep(0.5)

            save = str(save.content)
            Healths.append(save)

            pickle.dump(Healths, open("tHisMake5nOsen5e", "wb"))

            for i in range(people-npcs):
                i += 1

                await ctx.send(f"Enter Player Character {i}'s health")
                num = await client.wait_for('message', timeout=30, check=lambda message: message.author != ctx.bot.user and float(message.content).is_integer() is True)

                await asyncio.sleep(0.5)

                await ctx.send(f"Enter Player Character {i}'s name")
                name = await client.wait_for('message', timeout=30, check=lambda message: message.author != ctx.bot.user)

                await asyncio.sleep(0.5)

                name = str(name.content)

                storage = name + ":" + str(num.content)
                sLst.append(storage)

            async with ctx.typing():
                await asyncio.sleep(0.5)

            for i in range(npcs):
                i += 1

                await ctx.send(f"Enter NPC {i}'s health")
                num = await client.wait_for('message', timeout=30, check=lambda message: message.author != ctx.bot.user and float(message.content).is_integer() is True)

                await asyncio.sleep(0.5)

                await ctx.send(f"Enter NPC {i}'s name")
                name = await client.wait_for('message', timeout=30, check=lambda message: message.author != ctx.bot.user)

                await asyncio.sleep(0.5)

                name = str(name.content)

                storage = name + ":" + str(num.content)
                sLst.append(storage)

            pickle.dump(sLst, open(save, "wb"))
            pickkle = pickle.load(open(save, "rb"))
            for i in range(len(pickkle)):
                sp = pickkle[i].split(":")

                lst.append(sp[0])
                lst.append(sp[1])

            embed = discord.Embed(
                title='Health Chart',
                colour=discord.Colour.orange()
            )
            for i in range(len(lst)):
                if i%2 != 0:

                    embed.add_field(name=str(lst[i-1]), value=lst[i], inline=False)
            await ctx.send(embed=embed)


@client.command(aliases=["rh"])
async def recallHeath(ctx, *, args=None):
    lst = []
    Healths = pickle.load(open("tHisMake5nOsen5e", "rb"))
    if args is None:
        await ctx.send("Please enter your save name. (.re <save name here>)")
    elif args not in Healths:
        await ctx.send("Sorry! Looks like you didn't enter a health file!.")
    else:
        try:
            lOAd = pickle.load(open(str(args), "rb"))
            for i in range(len(lOAd)):
                sp = lOAd[i].split(":")

                lst.append(sp[0])
                lst.append(sp[1])

            embed = discord.Embed(
                title='Health chart',
                colour=discord.Colour.orange()
            )
            for i in range(len(lst)):
                if i%2 != 0:

                    embed.add_field(name=str(lst[i-1]), value=lst[i], inline=False)
            await ctx.send(embed=embed)
        except FileNotFoundError:
            await ctx.send("404 File not found.\n That Health file does not exist. Remember that it is caps sensitive!")

"""@client.event
async def on_message(message):
    if rollInitiative is True:
        if message.content.find(".r"):


    await client.process_commands(message)"""

token = pickle.load(open("token", "rb"))

client.run(token)
