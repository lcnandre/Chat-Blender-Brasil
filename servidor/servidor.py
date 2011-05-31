#globais
LOGIN_OK = '0'
LOGIN_USUARIO_INCORRETO = '1'
LOGIN_SENHA_INCORRETA = '2'

#porta e IP do servidor
PORTA = 2021
HOST = '127.0.0.1'

#variavel de controle do estado do servidor
global iniciado, clientes, s
iniciado = False
clientes = []
s = None

#importações
import os
import socket
import threading
import gobject

path = os.path.dirname(os.path.abspath(__file__))

class Servidor():
	def __init__(self):
		pass
	#__init__
	
	def inicia(self, log):
		global iniciado, s
		#criacao do socket
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#colocacao do socket no IP e portas informadas
		s.bind((HOST, PORTA))
		#abertura do socket a novas conexoes
		s.listen(2)
		iniciado = True
		if log == None:
			print 'Servidor rodando na porta', PORTA
		ThreadNovasConexoes(log).start()
		#inicio da thread que trata novas conexoes
	#inicia

	def para(self):
		global clientes, iniciado, s
		for cliente in clientes:
			cliente.close()
		s.close()
		s = None
		iniciado = False
	#para
#Servidor

#criacao da thread responsavel por tratar novas conexoes ao servidor
class ThreadNovasConexoes(threading.Thread):	
	log = None

	def __init__(self, log):
		self.log = log
		threading.Thread.__init__ (self)
		
	def atualizaLog(self, end):
		end = 'Conectado a '+end[0]+' na porta '+str(end[1])+'\n'
		self.log.get_buffer().insert(self.log.get_buffer().get_start_iter(), end)
	
	def run (self):
		global clientes, iniciado, s
		while iniciado:
			con, end = s.accept() #aceitacao de nova conexao
			#se existe um objeto log, atualiza a tela, senao mostra mensagem no console
			if self.log != None:
				gobject.idle_add(self.atualizaLog, end)
			else:
				print 'Conectado a '+end[0]+' na porta '+str(end[1])+'\n'
			clientes.append(con) #colocacao do socket recem conectado na lista de clientes
			ThreadMensagensRecebidas(con, self.log).start() #inicio da thread que trata mensagens recebidas pelo cliente em questao
#ThreadNovasConexoes

#criacao da thread que trata mensagens recebidas por cada cliente
class ThreadMensagensRecebidas(threading.Thread):
	con = None #socket do cliente
	log = None

	#inicializacao da thread e atribuicao do socket do cliente
	def __init__(self, con, log):
		self.con = con
		self.log = log
		threading.Thread.__init__ (self)

	def atualizaLog(self, ip):
		end = 'Desconectado de '+ip+'\n'
		self.log.get_buffer().insert(self.log.get_buffer().get_start_iter(), end)

	def run(self):
		global iniciado
		while iniciado: #loop infinito
			try: #tentativa de recepcao de dados do cliente
				dados = self.con.recv(1024)
				#comando "sair"
				if dados.find('qwerasdfzxcvtyuighjkbnm,789+456,/*-0 ASDFdaDFDsfS fdfD54df2DF45Dsf') != -1:
					if self.log != None:
						gobject.idle_add(self.atualizaLog,self.con.getpeername()[0])
					else:
						print 'Desconectado de '+self.con.getpeername()[0]
					self.con.send(dados) #envio da mensagem ao cliente que a enviou
					clientes.remove(self.con)
					self.con.close()
					break
				#comando "login"
				elif dados.find('ASIdas7f873rfasf7a83 as7da 8327ra s 32893') != -1:
					validaLogin(self.con)
				#outra mensagem (chat)
				elif len(dados) != 0: #se a mensagem nao esta em branco
					broadCast(dados) #envio da mensagem a todos os clientes
			except: #caso a tentativa falhe
				self.con.close() #fechamento do socket do cliente
				break #fim do loop infinito
#ThreadMensagensRecebidas

def broadCast(dados):
	global clientes
	for cliente in clientes: #para cada socket de cliente na lista
		cliente.send(dados) #envio da mensagem recebida
#broadCast

def validaLogin(con):
	import sqlite3
	# recepcao dos dados
	login = con.recv(1024)
	con.send('OK')
	senha = con.recv(1024)
	# validacao dos dados
	conexao = sqlite3.connect(os.path.join(path, '..\chat.s3db'))
	cursor = conexao.cursor()
	cursor.execute('select senha from usuario where login = ?', (login,))
	res = cursor.fetchall()
	#retorno ao cliente
	if len(res) == 0:
		con.send(LOGIN_USUARIO_INCORRETO)
	elif res[0][0] != senha:
		con.send(LOGIN_SENHA_INCORRETA)
	else:
		con.send(LOGIN_OK)
	con.recv(1024) #aguarda ok do cliente
#validaLogin

if __name__ == "__main__":
	servidor = Servidor()
	servidor.inicia(None)