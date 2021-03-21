import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from movidesk import *
import dateutil.parser as parser
from words import *

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('!'):
        number_ticket = parser_entry(msg)
        if (number_ticket):
            info_ticket = get_ticket(number_ticket)
            cliente = get_client(info_ticket)
            responsable = get_responsable(info_ticket)
            embedVar = discord.Embed(
                title=f"{info_ticket['subject']}", url=f'{BASE_LINK}{number_ticket}',
                color=colores[info_ticket['status']])
            embedVar.set_author(name=info_ticket['status'].upper())

            embedVar.add_field(name="Número", value=f"{info_ticket['id']}", inline=True)

            if (cliente):
                embedVar.add_field(name="Cliente", value=f"{info_ticket['clients'][0]['businessName']}, {cliente}",
                                   inline=True)
            else:
                embedVar.add_field(name="Cliente", value=f"{info_ticket['clients'][0]['businessName']}", inline=True)

            if (responsable):
                embedVar.add_field(name="Responsável", value=f"{info_ticket['owner']['businessName']}", inline=True)
            else:
                embedVar.add_field(name="Responsável", value="Não Atribuido", inline=True)

            msg = 'Hi {0.author.mention}'.format(message)
            lastUpdate = ajust_timezone(info_ticket['lastUpdate'])
            lastUpdate_text = parser.parse(lastUpdate).strftime('%d/%b/%Y - %H:%M')

            embedVar.set_footer(
                text=f"Atualizado o dia {lastUpdate_text}")
            await message.channel.send(embed=embedVar)

    if msg.startswith('$'):
        data_filter = parser_entry(msg)
        atleast_one_ticket = False
        # Ex.: data_filter = {'status': 'status3', 'category': 'categoria2', 'owner': 'agente1', 'msg': True}
        # Ex.: data_filter = {'msg': True, 'owntickets': True}
        if 'owntickets' in list(data_filter.keys()):
            person = [agente for agente in AGENTES if message.author.name.title().strip() in agente]
            if (person):
                tickets_checked_temp = main_request_mvdsk(summaried=True, agent=person[0])
                if len(tickets_checked_temp) > 0:
                    atleast_one_ticket = True
                    embedVar = discord.Embed(
                        title=f"{message.author.name.title()}, você tem {len(tickets_checked_temp)} tickets")
                    for ticket in tickets_checked_temp:
                        color_emoji = TICKETS_WORDS['actives'][f"{ticket['status']}"]['emoji_color']
                        embedVar.add_field(name=f"{ticket['id']} {color_emoji}",
                                           value=f"[{ticket['subject']}]({BASE_LINK}{ticket['id']})",
                                           inline=True)
                if atleast_one_ticket is False:
                    if 'msg' in list(data_filter.keys()):
                        await message.author.send(embed=empty_response())
                        await message.channel.send(random.choice(respostas_aleatorias_inbox))
                    else:
                        await message.channel.send(embed=empty_response())
                else:
                    if 'msg' in list(data_filter.keys()):
                        await message.author.send(embed=embedVar)
                        await message.channel.send(random.choice(respostas_aleatorias_inbox))
                    else:
                        await message.channel.send(embed=embedVar)
            else:
                if 'msg' in list(data_filter.keys()):
                    await message.author.send(embed=empty_response())
                    await message.channel.send(random.choice(respostas_aleatorias_inbox))
                else:
                    await message.channel.send(embed=empty_response())

        # Ex.: $tickets
        if not 'owner' in list(data_filter.keys()) and not 'status' in list(
                data_filter.keys()) and not 'category' in list(data_filter.keys()) and not 'owntickets' in list(
                data_filter.keys()):
            for owner in AGENTES:
                tickets_checked_temp = main_request_mvdsk(summaried=True, agent=owner)
                if len(tickets_checked_temp) > 0:
                    result = print_summarized_info(tickets_checked_temp, owner)
                    if ('msg' in list(data_filter.keys())):
                        await message.author.send(embed=result)
                    else:
                        await message.channel.send(embed=result)
            if ('msg' in list(data_filter.keys())):
                await message.channel.send(random.choice(respostas_aleatorias_inbox))

        # Ex.: $tickets +agente1
        if not 'status' in list(data_filter.keys()) and not 'category' in list(data_filter.keys()) and 'owner' in list(
                data_filter.keys()):
            tickets_checked_temp = main_request_mvdsk(summaried=True, agent=data_filter['owner'])
            if len(tickets_checked_temp) > 0:
                atleast_one_ticket = True
                result = print_summarized_info(tickets_checked_temp, data_filter['owner'])
            if atleast_one_ticket is False:
                if 'msg' in list(data_filter.keys()):
                    await message.author.send(embed=empty_response())
                    await message.channel.send(random.choice(respostas_aleatorias_inbox))
                else:
                    await message.channel.send(embed=empty_response())
            else:
                if 'msg' in list(data_filter.keys()):
                    await message.author.send(embed=result)
                    await message.channel.send(random.choice(respostas_aleatorias_inbox))
                else:
                    await message.channel.send(embed=result)


        # Ex.: $tickets +status1
        elif not 'owner' in list(data_filter.keys()) and not 'category' in list(
                data_filter.keys()) and 'status' in list(data_filter.keys()):
            for owner in AGENTES:
                tickets_checked_temp = main_request_mvdsk(status=data_filter['status'], agent=owner)
                if len(tickets_checked_temp) > 0:
                    atleast_one_ticket = True
                    result = print_summarized_info(tickets_checked_temp, owner)
                    if ('msg' in list(data_filter.keys())):
                        await message.author.send(embed=result)
                    else:
                        await message.channel.send(embed=result)

            if atleast_one_ticket is False:
                if 'msg' in list(data_filter.keys()):
                    await message.author.send(embed=empty_response())
                    await message.channel.send(random.choice(respostas_aleatorias_inbox))
                else:
                    await message.channel.send(embed=empty_response())
            else:
                if 'msg' in list(data_filter.keys()):
                    await message.channel.send(random.choice(respostas_aleatorias_inbox))




        # Ex.: $tickets +categoria1
        elif not 'owner' in list(data_filter.keys()) and not 'status' in list(
                data_filter.keys()) and 'category' in list(data_filter.keys()):
            for owner in AGENTES:
                tickets_checked_temp = main_request_mvdsk(summaried=True, agent=owner, category=data_filter['category'])
                if len(tickets_checked_temp) > 0:
                    atleast_one_ticket = True
                    result = print_summarized_info(tickets_checked_temp, owner)
                    if ('msg' in list(data_filter.keys())):
                        await message.author.send(embed=result)
                    else:
                        await message.channel.send(embed=result)

            if atleast_one_ticket is False:
                if 'msg' in list(data_filter.keys()):
                    await message.author.send(embed=empty_response())
                    await message.channel.send(random.choice(respostas_aleatorias_inbox))
                else:
                    await message.channel.send(embed=empty_response())
            else:
                if 'msg' in list(data_filter.keys()):
                    await message.channel.send(random.choice(respostas_aleatorias_inbox))


        # Ex.: $tickets +agente1 +status1
        elif 'owner' in list(data_filter.keys()) and 'status' in list(data_filter.keys()) and not 'category' in list(
                data_filter.keys()):
            tickets_checked_temp = main_request_mvdsk(status=data_filter['status'], agent=data_filter['owner'])
            if len(tickets_checked_temp) > 0:
                atleast_one_ticket = True
                result = print_summarized_info(tickets_checked_temp, data_filter['owner'])
                if ('msg' in list(data_filter.keys())):
                    await message.author.send(embed=result)
                else:
                    await message.channel.send(embed=result)

            if atleast_one_ticket is False:
                if 'msg' in list(data_filter.keys()):
                    await message.author.send(embed=empty_response())
                    await message.channel.send(random.choice(respostas_aleatorias_inbox))
                else:
                    await message.channel.send(embed=empty_response())
            else:
                if 'msg' in list(data_filter.keys()):
                    await message.channel.send(random.choice(respostas_aleatorias_inbox))

        # Ex.: $tickets +agente1 +categoria1
        elif 'owner' in list(data_filter.keys()) and not 'status' in list(data_filter.keys()) and 'category' in list(
                data_filter.keys()):
            tickets_checked_temp = main_request_mvdsk(summaried=True, agent=data_filter['owner'],
                                                      category=data_filter['category'])
            if len(tickets_checked_temp) > 0:
                atleast_one_ticket = True
                result = print_summarized_info(tickets_checked_temp, data_filter['owner'])
                if ('msg' in list(data_filter.keys())):
                    await message.author.send(embed=result)
                else:
                    await message.channel.send(embed=result)
            if atleast_one_ticket is False:
                if 'msg' in list(data_filter.keys()):
                    await message.author.send(embed=empty_response())
                    await message.channel.send(random.choice(respostas_aleatorias_inbox))
                else:
                    await message.channel.send(embed=empty_response())
            else:
                await message.channel.send(random.choice(respostas_aleatorias_inbox))

        # Ex.: $tickets +status1 +categoria2
        elif not 'owner' in list(data_filter.keys()) and 'status' in list(data_filter.keys()) and 'category' in list(
                data_filter.keys()):
            for owner in AGENTES:
                tickets_checked_temp = main_request_mvdsk(agent=owner, status=data_filter['status'],
                                                          category=data_filter['category'])
                if len(tickets_checked_temp) > 0:
                    atleast_one_ticket = True
                    result = print_summarized_info(tickets_checked_temp, owner)
                    if ('msg' in list(data_filter.keys())):
                        await message.author.send(embed=result)
                    else:
                        await message.channel.send(embed=result)
            if atleast_one_ticket is False:
                if 'msg' in list(data_filter.keys()):
                    await message.author.send(embed=empty_response())
                    await message.channel.send(random.choice(respostas_aleatorias_inbox))
                else:
                    await message.channel.send(embed=empty_response())
            else:
                await message.channel.send(random.choice(respostas_aleatorias_inbox))

        # Ex.: $tickets +agente1 +status1 +categoria2
        elif 'owner' in list(data_filter.keys()) and 'status' in list(data_filter.keys()) and 'category' in list(
                data_filter.keys()):
            tickets_checked_temp = main_request_mvdsk(status=data_filter['status'], agent=data_filter['owner'],
                                                      category=data_filter['category'])
            if len(tickets_checked_temp) > 0:
                atleast_one_ticket = True
                result = print_summarized_info(tickets_checked_temp, owner=data_filter['owner'])
                if ('msg' in list(data_filter.keys())):
                    await message.author.send(embed=result)
                else:
                    await message.channel.send(embed=result)
            if atleast_one_ticket is False:
                if 'msg' in list(data_filter.keys()):
                    await message.author.send(embed=empty_response())
                    await message.channel.send(random.choice(respostas_aleatorias_inbox))
                else:
                    await message.channel.send(embed=empty_response())
            else:
                await message.channel.send(random.choice(respostas_aleatorias_inbox))

    if msg.startswith("--help"):
        embedVar = discord.Embed(title=f"Movidesk Bot Help", color=colores['Novo'])
        embedVar.add_field(name="Tickets Específicos",
                           value="`!numero_do_ticket`: Serão exibido os detalhes de um ticket.\nEx.: `!10131`",
                           inline=False)
        embedVar.add_field(name="Tickets em Geral",
                           value="`$tickets`: Serão exibidos todos os tickets ativos, sendo os ativos os tickets que estão dict TICKETS_WORDS['actives'] por Agente.\nEx.: `$tickets`",
                           inline=False)
        embedVar.add_field(name="Filtros por Agente, Status e Categoría",
                           value="Agente:`+agente1`, `+agente2`, `+agente3`, `+agente4`, `+agente5`, `+agente6` e `+agente7`.\nEstado: `+status1`, `+status2`, `+status3`, `+status4`, e `+status5`.\nCategoria: `+categoria1`, `+categoria2`, `+categoria3`, `+categoria4` e `+categoria5.\nExemplos:\n`$tickets +alfonso` | `$ticks +agente5 +categoria1` \n`$tickets +categoria3`\t\t| `$tckts +agente3 +status1 +catgoria4 -msg`\n`$ticks +status4`| `$tckts +status3 +categoria1 +agente2`",
                           inline=False)
        embedVar.add_field(name="Atalhos",
                           value="`$mistickets` ou `$meustickets`: Os tickets atribuidos a você serão exibidos, se você for um agente.")
        embedVar.add_field(name="Mensagem Privado",
                           value="Você pode enviar uma mensagem direta para o Bot, mas também pode enviar uma mensagem pública e digitar `-msg` para receber o resultado numa mensagem só para você.\nExemplo: `$meustickets -msg`",
                           inline=False)

        await message.channel.send(embed=embedVar)

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))


def print_summarized_info(tickets_checked_temp, owner):
    """
    Imprime informação dos tickets por agente com cor dos status do seus tickets.
    """
    embedVar = discord.Embed(title=f"Tickets do _{owner}_: {len(tickets_checked_temp)}")
    for ticket in tickets_checked_temp:
        color_emoji = TICKETS_WORDS['actives'][f"{ticket['status']}"]['emoji_color']
        embedVar.add_field(name=f"{color_emoji}  {ticket['id']}",
                           value=f"[{ticket['subject']}]({BASE_LINK}{ticket['id']})",
                           inline=True)
    return embedVar


def empty_response():
    """
    Notifica ao usuário que não há tickets.
    """
    embedVar = discord.Embed(title="Não há tickets com esse filtro.", color=0xb7b7b7)
    embedVar.set_footer(
        text=f"Para mais informações você pode digitar o comando --help")
    return embedVar


keep_alive()
client.run(os.getenv('TOKEN'))
