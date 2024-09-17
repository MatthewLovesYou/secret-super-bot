import discord
from discord.ext import commands
from discord import app_commands
import random
import re

class client(commands.Bot):
    async def on_ready(self):
        print(f'Ja, {self.user}')

        try: 
            guild = discord.Object(id=949679010592481290)
            synced = await self.tree.sync(guild=guild)
            print(f'Synchronizacja {len(synced)} powiodła się {guild.id}')
        except Exception as e:
            print(f'Błąd: {e}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startswith('hej'):
            await message.channel.send(f'serwus {message.author}')
        
        if message.content.startswith('roll'):
            randList = re.findall("\d+",message.content)
            match len(randList):
                case 1:
                    await message.channel.send(f'{losujLiczbe(randList[0])}')
                case 2:
                    await message.channel.send(f'{wiadomoscLosow(seriaLosow(randList, True))}')
                case 3:
                    await message.channel.send(f'{wiadomoscLosow(seriaLosow(randList, True))}')
                case _:
                    await message.channel.send(f'Błąd w argumentach!')

        if message.content.startswith('adv'):
            randList = re.findall("\d+",message.content)
            match len(randList):
                case 1:
                    await message.channel.send(f'{wzmocnionaDecyzja(2, randList[0], 0)}')
                case 2:
                    await message.channel.send(f'{kilkaWzmocnien(randList[0], randList[1], 0)}')
                case 3:
                    await message.channel.send(f'{kilkaWzmocnien(randList[0], randList[1], randList[2])}')
                case _:
                    await message.channel.send(f'Błąd w argumentach!')


        if message.content.startswith('disadv'):
            randList = re.findall("\d+",message.content)
            match len(randList):
                case 1:
                    await message.channel.send(f'{oslabionaDecyzja(2, randList[0], 0)}')
                case 2:
                    await message.channel.send(f'{kilkaOslabien(randList[0], randList[1], 0)}')
                case 3:
                    await message.channel.send(f'{kilkaOslabien(randList[0], randList[1], randList[2])}')
                case _:
                    await message.channel.send(f'Błąd w argumentach!')


def losujLiczbe(kosc):
    if int(kosc): #upewnianie sie przed bledami
        return(random.randrange(int(kosc))+1)

def seriaLosow(listaIlosciKosciBonusow, dacKosciBonusy):
    listaKostkaBonusyIlosci = []
    if len(listaIlosciKosciBonusow)>3:
        return("Nie moge przetworzyc tylu argumentów!")
    else:
        iloscRzutow = int(listaIlosciKosciBonusow[0])
        kosc = int(listaIlosciKosciBonusow[1])
        try:
            bonus = int(listaIlosciKosciBonusow[2])
        except IndexError:
            bonus = 0

        for number in range(iloscRzutow+2):
                liczba = random.randrange(int(kosc))+1
                match number:
                    case 0:
                        listaKostkaBonusyIlosci.append(kosc)
                    case 1:
                        listaKostkaBonusyIlosci.append(bonus)
                    case _:
                        listaKostkaBonusyIlosci.append(liczba) 
        if dacKosciBonusy:
            return(listaKostkaBonusyIlosci)#pierwsza to kosc a druga to bonus!
        else:
            del listaKostkaBonusyIlosci[:2]
            listaIlosci = listaKostkaBonusyIlosci
            return(listaIlosci)

def wiadomoscLosow(listaKostkaBonusyIlosci):
    sumaCyfr = 0
    dzialanieWiadomosc = ''
    kosc = listaKostkaBonusyIlosci[0]
    bonus = listaKostkaBonusyIlosci[1]
    del listaKostkaBonusyIlosci[:2]
    for idnumber, number in enumerate(listaKostkaBonusyIlosci):
        sumaCyfr += number
        number = str(number)
        if number == str(kosc):
            number = f'***{number}***'
        elif number == '1':
                number = f'**{number}**'

        match idnumber:
            case 0:
                dzialanieWiadomosc += number
            case _:
                dzialanieWiadomosc += " + "+number

        
    sumaCyfr += bonus

    if bonus == 0:
            return(f'{dzialanieWiadomosc}  =  __{sumaCyfr}__')
    else:
        return(f'{dzialanieWiadomosc} + *{bonus}* =  __{sumaCyfr}__')
    
def wzmocnionaDecyzja(ilosc, kosc, bonus):
    kolejnoWiadomosc = ''
    wynik = seriaLosow([ilosc, kosc], False)
    for idelement, element in enumerate(wynik):
        element = str(element)
        if element == max(wynik):
            element = f'*{element}*'
        
        match idelement:
            case 0:
                kolejnoWiadomosc += element
            case _:
                kolejnoWiadomosc += " / "+element
    if bonus==0:
        return(f'{kolejnoWiadomosc} / **{max(wynik)}**')
    else:
        return(f'{kolejnoWiadomosc} + {bonus} / **{max(wynik)+int(bonus)}**')

def kilkaWzmocnien(powtorzenia, kosc, bonus):
    tekst = ''
    for element in range(int(powtorzenia)):
        tekst += wzmocnionaDecyzja(2, kosc, bonus)+ "\n"
    return(f'{tekst}')

def oslabionaDecyzja(ilosc, kosc, bonus):
    kolejnoWiadomosc = ''
    wynik = seriaLosow([ilosc, kosc], False)
    for idelement, element in enumerate(wynik):
        element = str(element)
        if element == min(wynik):
            element = f'*{element}*'
        
        match idelement:
            case 0:
                kolejnoWiadomosc += element
            case _:
                kolejnoWiadomosc += " / "+element
    if bonus==0:
        return(f'{kolejnoWiadomosc} / **{min(wynik)}**')
    else:
        return(f'{kolejnoWiadomosc} + {bonus} / **{min(wynik)+int(bonus)}**')

def kilkaOslabien(powtorzenia, kosc, bonus):
    tekst = ''
    for element in range(int(powtorzenia)):
        tekst += oslabionaDecyzja(2, kosc, bonus)+ "\n"
    return(f'{tekst}')

intents = discord.Intents.default()
intents.message_content = True
client = client(command_prefix="!",intents=intents)

GUILD_ID = discord.Object(id=949679010592481290)

@client.tree.command(name="help", description="Dostępne komendy.", guild = GUILD_ID)
async def messageHelp(interaction: discord.Interaction):
    await interaction.response.send_message(f'Moje główne komendy to:\n\n roll *kosc* \n roll *ilosc* *kosc* *bonusy* \n\n adv *kosc* \n adv *ilosc* *kosc* *bonusy* \n\n disadv *kosc* \n disadv *ilosc* *kosc* *bonusy* ')

@client.tree.command(name="say", description="Wymuś wiadomość.", guild = GUILD_ID)
async def sayWiadomosc(interaction: discord.Interaction, wiadmosc: str):
    await interaction.response.send_message(f'{wiadmosc}')


@client.tree.command(name="roll", description="Rzuć kością!", guild = GUILD_ID)
async def sayWiadomosc(interaction: discord.Interaction, ilosc: int, kosc: int, bonus: int):
    await interaction.response.send_message(f'{wiadomoscLosow(seriaLosow([ilosc, kosc, bonus], True))}')

@client.tree.command(name="adv", description="Rzuć kością, z przewagą!", guild = GUILD_ID)
async def sayWiadomosc(interaction: discord.Interaction, ilosc: int, kosc: int, bonus: int):
    await interaction.response.send_message(f'{kilkaWzmocnien(ilosc, kosc, bonus)}')

@client.tree.command(name="disadv", description="Rzuć kością, z osłabieniem!", guild = GUILD_ID)
async def sayWiadomosc(interaction: discord.Interaction, ilosc: int, kosc: int, bonus: int):
    await interaction.response.send_message(f'{kilkaOslabien(ilosc, kosc, bonus)}')
