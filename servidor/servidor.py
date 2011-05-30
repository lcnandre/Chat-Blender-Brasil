#porta e IP do servidor
PORTA = 2021
HOST = '127.0.0.1'

#variavel de controle do estado do servidor
global iniciado, clientes, s
iniciado = False
clientes = []
s = None

#importações
import socket
import threading
import gobject

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
		#inicio da thread que trata novas conexoes
		ThreadNovasConexoes(log).start()
		iniciado = True
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
		
	def atualizaLog(self, mensagem):
		mensagem = 'Conectado a '+mensagem[0]+' na porta '+str(mensagem[1])+'\n'
		self.log.get_buffer().insert(self.log.get_buffer().get_start_iter(), mensagem)
		
	def run (self):
		global clientes, iniciado, s
		while iniciado:
			con, end = s.accept() #aceitacao de nova conexao
			gobject.idle_add(self.atualizaLog, end)
			clientes.append(con) #colocacao do socket recem conectado na lista de clientes
			ThreadMensagensRecebidas(con).start() #inicio da thread que trata mensagens recebidas pelo cliente em questao
#ThreadNovasConexoes

#criacao da thread que trata mensagens recebidas por cada cliente
class ThreadMensagensRecebidas(threading.Thread):
    con = None #socket do cliente

    #inicializacao da thread e atribuicao do socket do cliente
    def __init__(self, con):
        self.con = con
        threading.Thread.__init__ (self)
		
    def run(self):
		global iniciado
		while iniciado: #loop infinito
			try: #tentativa de recepcao de dados do cliente
				dados = self.con.recv(1024)
				if dados.find('qwerasdfzxcvtyuighjkbnm,789+456,/*-0 ASDFdaDFDsfS fdfD54df2DF45Dsf') != -1:
					break
				if len(dados) != 0: #se a mensagem nao esta em branco
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
