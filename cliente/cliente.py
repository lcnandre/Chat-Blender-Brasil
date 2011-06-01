#globais
LOGIN_USUARIO_INCORRETO = '1'
LOGIN_SENHA_INCORRETA = '2'

#importações
import socket
from util import getIpWan

#IP e host do servidor
PORTA_CHAT = 2021
PORTA_CONVERSA = 2120
HOST_CHAT = '127.0.0.1'
HOST_CONVERSA = '127.0.0.1'

class Cliente:	
	usuario = ''
	conectado = False
	s = None
	sConversas = None
	contatos =  []
	conversas = []

	def __init__(self):
		pass
	#__init__
	
	def conecta(self):
		#criacao dos sockets cliente e servidor
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sConversas = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#conexão do cliente com o host e porta especificadas
		self.s.connect((HOST_CHAT, PORTA_CHAT))
		self.conectado = True
		#abertura do servidor para conversas
		try:
			self.sConversas.bind((HOST_CONVERSA, PORTA_CONVERSA))
			self.sConversas.listen(2)
		except:
			pass
	#conecta

	def envia(self, mensagem):
		if self.conectado:
			#envio da mensagem ao servidor
			if len(self.usuario) > 0:
				self.s.send('%s: %s'%(self.usuario,mensagem))
			else:
				self.s.send(mensagem)
	#envia

	def recebe(self):
		#recebimento da resposta do servidor (ver código do servidor)
		return self.s.recv(1024)
	#recebe

	def desconecta(self):
		if self.conectado:
			#término da conexão
			self.s.send('qwerasdfzxcvtyuighjkbnm,789+456,/*-0 ASDFdaDFDsfS fdfD54df2DF45Dsf') #ninguém vai acertar enviar isso aqui
			self.s.recv(1024)#aguarda ok do servidor
			self.s.close()
			self.s = None
			self.conectado = False
	#desconecta
	
	def getListaContatos(self):
		self.contatos = [] #limpa a lista
		self.s.send('(9s8d9s asudhasiud 8s9d8as /*-393 2 s8duas98d U8s8a SD98j /00s*')
		c = self.s.recv(1024) #recebe primeiro contato
		#enquanto houverem contatos, coloca na lista
		while c != '(9s8d9s asudhasiud 8s9d8as /*-393 2 s8duas98d U8s8a SD98j /00s*':
			self.contatos.append(eval(c))#converte de string novamente para lista
			self.s.send('OK')#envia ok ao servidor
			c = self.s.recv(1024)#recebe o proximo contatos
	#getListaContatos
	
	def fazLogin(self, login, senha):
		import hashlib
		
		senha = hashlib.md5(senha).hexdigest()
		self.envia('ASIdas7f873rfasf7a83 as7da 8327ra s 32893') #comando para login
		self.envia(login) #envia login
		self.recebe() #aguarda ok do servidor
		self.envia(senha) #envia senha
		retorno = self.recebe() #retorno do servidor
		self.envia('OK')
		return retorno
	#fazLogin
#Cliente
