# Bot de Discord que puxa dados de Movidesk

Trata-se de um bot que através do discord consegue obter informações da sua plataforma de atendimento Movidesk.

- Que é movidesk >  Plataforma de Atendimento (Help Desk) [O que é Movidesk?](https://www.movidesk.com)

## Exemplos dos Resultados

![Perguntando por um Ticket](https://github.com/Alfareiza/discordbot-movidesk/blob/main/files/resposta_ticket.png?raw=True)
![Perguntando com dois filtros](https://github.com/Alfareiza/discordbot-movidesk/blob/main/files/respostas_dois_filtros.png?raw=True)
![Meus Tickets](https://github.com/Alfareiza/discordbot-movidesk/blob/main/files/own_tickets.png?raw=True)
![Notificação do Windows](https://github.com/Alfareiza/discordbot-movidesk/blob/main/files/msg_com_notifica%C3%A7%C3%A3o.png?raw=True)
![Não há respostas](https://github.com/Alfareiza/discordbot-movidesk/blob/main/files/nao_ha_respostas.png?raw=True)


## Antes de Começar

Esse bot foi criado com dados pessoais, então você precisa configurar ele com os dados da sua conta de movidesk. Se você não tiver idea de como criar, configurar e obter o bot no discord, recomendo que acompanhe esse tutorial [How to Create a Discord Bot for Free with Python – Full Tutorial
](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/) e junto com os arquivos disponibilizados nesse repositório consiga obter o resultado esperado.

Como trata-se de um bot, ele precisa estar online para assim ficar disponível para os agentes do seu servidor no discord. É por isso que os arquivos devem ser carregados para a plataforma [replit.com](https://replit.com/) e assim que for disponibilizada a URL do serviço web, ela deve ser montada no [uptimerobot.com](http://uptimerobot.com) para que o robot fique disponível sempre. 

## Vamos lá

Criar um arquivo `.env` com informações do **TOKEN** obtido pelo discord e o **TOKEN_MOVIDESK**. Para obter o TOKEN do movidesk você deve acessar ao Movidesk, logo em Configurações > Conta > Parâmetros e na guia ambiente clique no botão "Gerar nova chave.

Logo, os arquivos `.env`, `main.py`, `keep_alive.py`, `movidesk.py` e `words.py` devem ser os únicos arquivos no replit. Para mas informações detalhadas você pode revisar o artigo [How to Create a Discord Bot for Free with Python – Full Tutorial
](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/).

## Arquivos do Projeto

- .env: Arquivo que deve ficar na raiz com as informações de TOKEN e MOVIDESK_TOKEN. Ele possui informações confidenciais e por isso cada usuário deve ter o seu.  
- [main.py](https://github.com/Alfareiza/discordbot-movidesk/blob/main/main.py): Módulo principal que tem a inteligência do bot..
- [keep_alive.py](https://github.com/Alfareiza/discordbot-movidesk/blob/main/keep_alive.py): Arquivo necessário para que o bot fique sendo executado e online sempre. 
- [movidesk.py](https://github.com/Alfareiza/discordbot-movidesk/blob/main/movidesk.py): Módulo com tratamentos e chamados próprios do movidesk.
- [words.py](https://github.com/Alfareiza/discordbot-movidesk/blob/main/words.py): Módulo com palavras-chave e informações obtidas manualmente no movidesk.

## Escopo do Bot

#### Tickets Específicos
`!numero_do_ticket`: Serão exibido os detalhes de um ticket.
Ex.: `!10131`

#### Tickets em Geral
`$tickets`: Serão exibidos todos os tickets ativos, sendo os ativos os tickets que estão dict TICKETS_WORDS['actives'] por Agente.
Ex.: `$tickets`

#### Filtros por Agente, Status e Categoría
Agente:`+agente1`, `+agente2`, `+agente3`, `+agente4`, `+agente5`, `+agente6` e `+agente7`.
Estado: `+status1`, `+status2`, `+status3`, `+status4`, e `+status5`.
Categoria: `+categoria1`, `+categoria2`, `+categoria3`, `+categoria4` e `+categoria5`.
Os dados anteriores são carregados do arquivo [words.py](https://github.com/Alfareiza/discordbot-movidesk/blob/main/words.py)
Exemplos:
`$tickets +agente1` | `$ticks +agente5 +categoria1` 
`$tickets +categoria3`  | `$tckts +agente3 +status1 +categoria4 -msg`
`$ticks +status4`  | `$tckts +status3 +categoria1 +agente2`

#### Atalhos
`$mistickets` ou `$meustickets`: Os tickets atribuidos a você serão exibidos, se você for um agente.

#### Mensagem Privado
Você pode enviar uma mensagem direta para o Bot, mas também pode enviar uma mensagem pública e digitar `-msg` para receber o resultado numa mensagem só para você.
Exemplo: `$meustickets -msg`

#### O Bot não traz informações ao discord se você não solicita. Ou seja que ele não fica monitorando e disparando alertas ao discord, segundo determinados critérios. 
