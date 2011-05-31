#IP e host do servidor
PORTA = 2021
HOST = '127.0.0.1'

#importações
import socket

class Cliente:	
	usuario = ''
	conectado = False
	s = None

	def __init__(self):
		pass
	#__init__
	
	def conecta(self):
		#criacao do socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#conexão do cliente com o host e porta especificadas
		self.s.connect((HOST, PORTA))
		self.conectado = True
	#conecta

	def envia(self, mensagem):
		#envio da string 'Teste' ao servidor
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
		#término da conexão
		self.s.send('qwerasdfzxcvtyuighjkbnm,789+456,/*-0 ASDFdaDFDsfS fdfD54df2DF45Dsf') #ninguém vai acertar enviar isso aqui
		self.s.recv(1024)#aguarda ok do servidor
		self.s.close()
		self.s = None
		self.conectado = False
	#desconecta
#Cliente
