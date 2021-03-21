import os
import requests
import json
from words import *

TOKEN_MOVIDESK = os.getenv('MOVIDESK_TOKEN')
query = {'token': TOKEN_MOVIDESK, }
url = "https://api.movidesk.com/public/v1/tickets"
colores = {"Status1": 0x020202, "Status2": 0x737070, "Status3": 0x737070,
           "Status4": 0xffffff, "Status5": 0x007eff, "Status6": 0xe62020,
           "Status7": 0xe27709, "Status8": 0xe62020, "Status9": 0x00ff43}

# Movidesk fornece aos seus clientes o link para os tickets
BASE_LINK = 'https://suporte.minha_empresa.com.br/Ticket/Edit/'


def get_ticket(id_ticket):
    """
    Principal request para API da movidesk
    :param id_ticket: str: Id do ticket que quero procurar.
    :return: data: dict: Informações do ticket, resposta da API do movidesk
    """
    resp = requests.get(f'https://api.movidesk.com/public/v1/tickets?token={TOKEN_MOVIDESK}&id={id_ticket}')
    if not resp.status_code == 404:
        data = json.loads(resp.text.encode('utf8'))
    else:
        data = False
    return data


def main_request_mvdsk(summaried=None, status=None, agent=None, category=None):
    """
    Retorna tickets segundo o tipo.
    :return: List de dicts com os valores indicados no select
    """
    status_body_filter = "status eq '{}'".format("' or status eq '".join(list(TICKETS_WORDS['actives'].keys())))
    query['$select'] = 'id,subject,category,status,createdDate,ResolvedIn,lifeTimeWorkingTime,lastUpdate'
    if summaried:
        if not status and not category and agent:
            # agent is True, status & category are False
            query['$filter'] = f"({status_body_filter}) and owner/businessName eq '{agent}'"
        elif not status and category and agent:
            # agent is True, status & category are False
            query[
                '$filter'] = f"({status_body_filter}) and owner/businessName eq '{agent}' and category eq '{category}'"
    else:
        if status:
            # status is True
            query['$filter'] = f"status eq '{status}'"
            if agent:
                # status agent are True
                query['$filter'] = f"status eq '{status}' and owner/businessName eq '{agent}'"
                if category:
                    # status agent category are True
                    query[
                        '$filter'] = f"status eq '{status}' and owner/businessName eq '{agent}' and category eq '{category}'"
            elif category:
                # status category are True | agent False
                query['$filter'] = f"status eq '{status}' and category eq '{category}'"
            elif agent:
                # agent is True
                query['$filter'] = f"owner/businessName eq '{agent}'"
                if category:
                    # agent category are True | status False
                    query['$filter'] = f"owner/businessName eq '{agent}' and category eq '{category}'"
            elif category:
                # category is True
                query['$filter'] = f"category eq '{category}'"
                if status:
                    # category status are True | agent False
                    query['$filter'] = f"category eq '{category}' and status eq '{status}'"
            else:
                pass

    query['$expand'] = 'owner,createdBy'
    query['$orderby'] = 'lastUpdate asc'
    resp = requests.get(url, params=query)
    if not resp.status_code == 404:
        data = json.loads(resp.text.encode('utf8'))
    else:
        data = False
    return data


def parser_entry(entry):
    """
    entry = $tickets +status1 +murilo +problema -msg
    entry = !80894
    """
    entries = entry.split()
    parsed_msg = dict()
    try:
        if entries[0][0] == '!' and int(entries[0][1:]):
            print('Ticket Existente')
            return int(entries[0][1:])
        elif entries[0][0] == '$':
            if (want_all_tickets(entries[0][1:])):  # entries[0][1:] = tickets
                for param in entries[1:]:  # entries[1:] = ['+problema', '+murilo', '+status1', '-msg']
                    if want_inbox(param):
                        parsed_msg['msg'] = True
                    param = valid_params(param)
                    if param:
                        parsed_msg[param[0]] = param[1]
                return parsed_msg
            elif (want_your_tickets(entries[0][1:])):  # entries[0][1:] = mistickets
                for param in entries[1:]:
                    if want_inbox(param):  # entries[1] = -msg
                        parsed_msg['msg'] = True
                parsed_msg['owntickets'] = True
                return parsed_msg
            else:
                print('Para obter informação de tickets, a palavra deve ser TICKETS ou MEUSTICKETS')
        else:
            print('Informação não valida')
            return False

    except Exception as e:
        print("Error > ", e)
        return False


def get_client(ticket_resp):
    """
    Nome do cliente quem abriu o ticket (se tiver)
    :param ticket_resp: dict: Json respondido da função get_ticket()
    :return: client: str: Nome do cliente do client, se ele já está cadastrado no movidesk
    """
    client = False
    if not ticket_resp['clients'][0]['organization'] is None:
        client = ticket_resp['clients'][0]['organization']['businessName']
    return client


def get_responsable(ticket_resp):
    """
    Nome do agente responsável (se tiver)
    :param ticket_resp: dict: Json respondido da função get_ticket()
    :return: client: str: Nome do cliente do responsável
    """
    responsable = False
    if not ticket_resp['owner'] is None:
        responsable = ticket_resp['owner']['businessName']
    return responsable


def want_all_tickets(word):
    """
    Valida que a palavra digitada seja 'tickets'
    """
    if word.lower() in TICKETS_WORDS['default']:
        return True


def want_your_tickets(word):
    """
    Valida que a palavra digitada seja 'mistickets' ou 'meustickets'
    """
    if word.lower() in TICKETS_WORDS['shortcuts']:
        return True


def valid_params(param):
    """
    Valida que o corpo dos parámetros enviados pelo usuário tenha a estrutura seguinte:
    +category ou +owner ou +status
    """
    if param[0] == '+':
        for ticket in TICKETS_WORDS['actives']:
            if param[1:].lower() in TICKETS_WORDS['actives'][ticket]['key_words']:
                return ('status', ticket)

        for official_word in AGENTES:
            if param[1:].lower() == official_word.lower().split()[0]:
                return ('owner', official_word)

        for official_word, related_word in CATEGORIES['name'].items():
            if param[1:].lower() in related_word:
                return ('category', official_word)


def want_inbox(param):
    if param[0] == '-':
        if param[1:] == 'msg':
            return True


def ajust_timezone(info):
    """
    Resta -3 ao horário que o movidesk entrega.
    Ex: Valor do Movidesk: 2021-03-17T22:32:02.7619819
        Valor entregado: 2021-03-17T22:32:02.7619819
    """
    hora = int(info.split("T")[1].split(':')[0])
    if hora > 4:
        hora = hora - 3

    info = info.split("T")[0] + 'T' + str(hora) + info[13:]
    return str(info)
