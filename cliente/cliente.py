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
		self.s.send(self.usuario+': '+mensagem)
	#envia

	def recebe(self):
		#recebimento da resposta do servidor (ver código do servidor)
		return self.s.recv(1024)
	#recebe

	def desconecta(self):
		#término da conexão
		self.s.close()
		self.s = None
		self.conectado = False
	#desconecta
#Cliente