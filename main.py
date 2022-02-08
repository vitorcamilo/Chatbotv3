import requests
import time
import json
import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def hello_world():
  return '<h1>OK</h1>'

def run():
  app.run(host="0.0.0.0", port=8000)

def keep_alive():
  server = Thread(target=run)
  server.start()

class TelegramBot:
  dadosmsg = ''
  def __init__(self):
    token = '5114227953:AAHWQZc1s2zHd1nZKsRwf3HBFP3cDyiinqw'
    self.url_base = f'https://api.telegram.org/bot{token}/'

  def Iniciar(self):
    update_id = None
    level = [0, 0]
    while True:
      atualizacao = self.obter_novas_mensagens(update_id)
      dados = atualizacao["result"]
      if dados:
        for dado in dados:
          update_id = dado['update_id']
          mensagem = str(dado["message"]["text"])
          chat_id = dado["message"]["from"]["id"]
          eh_primeira_mensagem = int(dado["message"]["message_id"]) ==1
          resposta = self.criar_resposta(mensagem, eh_primeira_mensagem, level)
          self.responder(resposta, chat_id)

  def obter_novas_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)

  def criar_resposta(self, mensagem, eh_primeira_mensagem, level):
    global status, programa, anuncio, nome, telefone
    if eh_primeira_mensagem == True or mensagem in ('menu', 'Menu','voltar', 'Voltar'):
        level[1] = 0
        return f'''Gostaria de fazer um anúncio de milhas?{os.linesep}1-Sim{os.linesep}2-Não'''

    if mensagem == '1' and level[1] == 0:
        level[1] = 1
        return f'''Gostaria de comprar ou vender milhas?{os.linesep}1-Comprar{os.linesep}2-Vender'''

    elif mensagem == '2' and level[1] == 0:
        return f'''Obrigado!{os.linesep}Digite "voltar" para iniciar novamente.'''

    if mensagem == '1' and level[1] == 1:
        level[1] = 2
        status = 'comprar'
        return f'''Gostaria de comprar de qual programa?{os.linesep}1-Smiles{os.linesep}2-Azul{os.linesep}3-LATAM{os.linesep}4-Tap{os.linesep}Caso queira voltar ao começo digite "voltar".'''
    elif mensagem == '2' and level[1] == 1:
        level[1] = 2
        status = 'vender'
        return f'''Gostaria de vender por qual programa?{os.linesep}1-Smiles{os.linesep}2-Azul{os.linesep}3-LATAM{os.linesep}4-Tap{os.linesep}Caso queira voltar ao começo digite "voltar".'''

    if mensagem == '1' and level[1] == 2:
        level[1] = 3
        programa = 'Smiles'
        return f'''Qual o seu nome?'''
    elif mensagem == '2' and level[1] == 2:
        level[1] = 3
        programa = 'Azul'
        return f'''Qual o seu nome?'''
    elif mensagem == '3' and level[1] == 2:
        level[1] = 3
        programa = 'LATAM'
        return f'''Qual o seu nome?'''
    elif mensagem == '4' and level[1] == 2:
        level[1] = 3
        programa = 'Tap'
        return f'''Qual o seu nome?'''
    elif level[1] == 3:
        nome = mensagem
        level[1] = 4
        return f'''Qual o seu telefone?'''
    elif level[1] == 4:
        telefone = mensagem
        level[1] = 5
        return f'''Qual a quantidade de milhas?'''
    if level[1] == 5 and mensagem not in ('menu', 'Menu', 'voltar','Voltar'):
        qtd = mensagem
        level[1] = 6
        self.dadosmsg = f'''{nome}{os.linesep}Deseja {status} {qtd} milhas da {programa}{os.linesep}Tel:{telefone}'''
        return f'''{self.dadosmsg}{os.linesep}{os.linesep}Confirma o texto acima?(S/N)'''
    if mensagem in ('S', 's') and level[1] == 6:
        level[1] = 7
        link_requisicao = f'{self.url_base}sendMessage?chat_id=-1001770018245&text={self.dadosmsg}'
        requests.get(link_requisicao)
        return f'''Muito Obrigado!{os.linesep}Caso queira fazer outro anúncio digite "voltar".'''
    elif mensagem in ('N', 'n') and level[1] == 6:
        return f'''Digite "voltar" para começar novamente.'''
    else:
        return 'Olá, sou o balcão de milhas. Gostaria de acessar o menu? Digite "menu".'

  def responder(self, resposta, chat_id):
      link_requisicao = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
      requests.get(link_requisicao)

bot = TelegramBot()
bot.Iniciar()
