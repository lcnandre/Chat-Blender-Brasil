#globais
LOGIN_OK = '0'
LOGIN_USUARIO_INCORRETO = '1'
LOGIN_SENHA_INCORRETA = '2'
STATUS_ONLINE = 1
STATUS_OFFLINE = 0

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
from conexao import getConexao

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
		if iniciado:
			#avisa e desconecta todos os clientes
			for cliente in clientes:
				cliente.send('23498 f/2423rdfs99xcv0a ad8 09 /45//88908/ sdf99089/*-)(*53/ 324 -3243-')
				cliente.close()
			iniciado = False
			#conecta o servidor a ele mesmo para matar a thread de novas conexoes
			s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s1.connect((HOST, PORTA))
			#finaliza ambos os sockets
			s1.close()
			s.close()
			#define todos os clientes como offline
			broadCastPresenca(STATUS_OFFLINE)
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
	usuario = None
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
					#define cliente como offline no BD
					if self.usuario != None:
						atualizaPresenca(self.usuario, STATUS_OFFLINE)
					break
				#comando "login"
				elif dados.find('ASIdas7f873rfasf7a83 as7da 8327ra s 32893') != -1:
					self.usuario = fazLogin(self.con)
				#comando "getListaContatos"
				elif dados.find('(9s8d9s asudhasiud 8s9d8as /*-393 2 s8duas98d U8s8a SD98j /00s*') != -1:
					if self.usuario != None:
						contatos = getListaContatos(self.usuario)#obtem a lista de contatos do cliente
						#envia os contatos ao cliente
						for contato in contatos:
							self.con.send(str(contato))
							self.con.recv(1024)#aguarda ok do cliente
						self.con.send('(9s8d9s asudhasiud 8s9d8as /*-393 2 s8duas98d U8s8a SD98j /00s*')#envia para dizer que a lista acabou
				
				# Solano passou por aqui
				# comandos IRC-Like (/add, /me por enquanto)
				elif dados[0] == '/':
					if dados.find('/add '):
						amigo = dados[5:]
						addContato(self.usuario, amigo)
					elif dados.find('/me '):
						msg = dados[4:]
						broadCast(msg, modo='me', usuario=self.usuario)
						
				#outras mensagens (chat)
				elif len(dados) != 0: #se a mensagem nao esta em branco
					broadCast(dados) #envio da mensagem a todos os clientes
			except: #caso a tentativa falhe
				clientes.remove(self.con)
				self.con.close() #fechamento do socket do cliente
				break #fim do loop infinito
#ThreadMensagensRecebidas

def broadCast(dados, **kwargs):
	global clientes
	try: 
		modo = kwargs['modo']
		usuario = kwargs['usuario']
		if modo=='me':
			for cliente in clientes:
				cliente.send('*** %s %s ***'%(usuario,dados,))
	except:
		for cliente in clientes: #para cada socket de cliente na lista
			cliente.send(dados) #envio da mensagem recebida
#broadCast

def getListaContatos(login):
	contatos = []
	#busca a lista de contatos (apenas os que estao online) no BD
	sql = """select u.login, u.ip, u.status
			 from contato c inner join usuario u on u.id = c.amigo_id
			 where c.usuario_id = (select id from usuario where login = %s)
			 and u.status = 1"""
	conexao = getConexao()
	cursor = conexao.cursor()
	cursor.execute(sql,(login,))
	for contato in cursor:
		c = {}
		c['nome'] = contato[0]
		c['ip'] = contato[1]
		contatos.append(c)
	conexao.close()
	return contatos
#getListaContatos

def atualizaPresenca(login, status):
	sql = """update usuario 
			 set status = %s
			 where login = %s"""
	conexao = getConexao()
	cursor = conexao.cursor()
	cursor.execute(sql, (status,login,))
	conexao.commit()
	conexao.close()
#atualizaPresenca

def broadCastPresenca(status):
	sql = """update usuario 
			 set status = %s
			 where 1=1"""
	conexao = MySQLdb.connect(host=HOST, user='root', passwd='', db='chat')
	cursor = conexao.cursor()
	cursor.execute(sql, (status,))
	conexao.commit()
	conexao.close()
#broadCastPresenca
def addContato(login, contato):
	sql = """select * from usuario
			where login = %s"""
	conexao = getConexao()
	loginId = conexao.cursor()
	loginId.execute(sql, (login,))
	contatoId = conexao.cursor()
	contadoId.execute(sql, (contato,))
	
	sql = """insert into contato (usuario_id, amigo_id)
		values (%s, %s)"""
	# TODO: daqui meu SQL eh muito enferrujado pra continuar
	conexao.commit()
	conexao.close()
	
def atualizaIp(ip, login):
	conexao = getConexao()
	cursor = conexao.cursor()
	cursor.execute('update usuario set ip = %s where login = %s', (ip,login,))
	conexao.commit()
	conexao.close()
#atualizaIp

def fazLogin(con):
	# recepcao dos dados
	login = con.recv(1024)
	con.send('OK')
	senha = con.recv(1024)
	# validacao dos dados
	conexao = getConexao()
	cursor = conexao.cursor()
	cursor.execute('select senha from usuario where login = %s', (login,))
	res = cursor.fetchall()
	conexao.close()
	#retorno ao cliente
	if len(res) == 0:
		con.send(LOGIN_USUARIO_INCORRETO)
		con.recv(1024) #aguarda ok do cliente
	elif res[0][0] != senha:
		con.send(LOGIN_SENHA_INCORRETA)
		con.recv(1024) #aguarda ok do cliente
	else:
		con.send(LOGIN_OK)
		con.recv(1024) #aguarda ok do cliente
		atualizaIp(con.getpeername()[0], login)#atualiza IP do cliente no banco de dados
		atualizaPresenca(login, STATUS_ONLINE)#atualiza o status do cliente
		return login #devolve o login para a thread
	return None #se nao fizer login, devolve nada para athread
#validaLogin

if __name__ == "__main__":
	servidor = Servidor()
	servidor.inicia(None)