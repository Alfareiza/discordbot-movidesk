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
