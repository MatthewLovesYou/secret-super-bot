import discord
import random
import re

class client(discord.Client):
    async def on_ready(self):
        print(f'Ja, {self.user}')

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
                    await message.channel.send(f'{wzmocnionaDecyzja(2, randList[0])}')
                case 2:
                    await message.channel.send(f'{wzmocnionaDecyzja(2, randList[0])}')
                case _:
                    await message.channel.send(f'Błąd w argumentach!')


        if message.content.startswith('disadv'):
            randList = re.findall("\d+",message.content)
        
        if message.content.startswith('!help'):
            await message.channel.send(f'Moje główne komendy to:\n roll *kosc* \n roll *ilosc* *kosc* *bonusy* \n adv *kosc*')


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
    for number in listaKostkaBonusyIlosci:
        sumaCyfr += number
        number = str(number)
        if number == str(kosc):
            number = f'***{number}***'
        elif number == '1':
                number = f'**{number}**'

        match number:
            case 0:
                dzialanieWiadomosc += number
            case _:
                dzialanieWiadomosc += " + "+number

        
    sumaCyfr += bonus

    if bonus == 0:
            return(f'{dzialanieWiadomosc}  =  __{sumaCyfr}__')
    else:
        return(f'{dzialanieWiadomosc} + *{bonus}* =  __{sumaCyfr}__')
    

def wzmocnionaDecyzja(ilosc, kosc):
    kolejnoWiadomosc = ''
    wynik = seriaLosow([ilosc, kosc], False)
    for element in wynik:
        element = str(element)
        if element == max(wynik):
            element = f'*{element}*'

        match element:
            case 0:
                kolejnoWiadomosc += element
            case _:
                kolejnoWiadomosc += " / "+element
    return(f'{kolejnoWiadomosc} / **{max(wynik)}**')


intents = discord.Intents.default()
intents.message_content = True
