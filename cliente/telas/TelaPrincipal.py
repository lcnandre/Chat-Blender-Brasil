#globais
STATUS_ONLINE = 1
STATUS_OFFLINE = 0

#importações
import os
import threading
import gtk, gtk.glade, gobject
from util import mostraErro

gobject.threads_init()
path = os.path.dirname(os.path.abspath(__file__))
global cliente
cliente = None

class TelaPrincipal:
	#mapeamento de signals
	dic = {}
	tela = None
	edChat = None
	edMensagem = None
	
	def __init__(self, cli):
		global cliente
		#carrega a interface
		xml = gtk.glade.XML(os.path.join(path, 'res/cliente-principal-gui.glade'))
		self.dic = {
			'on_telaPrincipal_destroy': self.sair,
			'on_edMensagem_activate': self.impEdMensagem,
		}
		xml.signal_autoconnect(self.dic)
		self.tela = xml.get_widget('telaPrincipal')
		self.edChat = xml.get_widget('edChat')
		self.edMensagem = xml.get_widget('edMensagem')
		cliente = cli
		cliente.getListaContatos()#atualiza lista de contatos
		ThreadMensagensRecebidas(self.edChat).start()
	#__init__
	
	def impEdMensagem(self, *args):
		global cliente
		mensagem = self.edMensagem.get_text()
		self.edMensagem.set_text('')
		cliente.envia(mensagem)
	#impEdMensagem
	
	def sair(self, *args):
		global cliente
		cliente.desconecta()
		gtk.main_quit()
	#sair
#class TelaPrincipal

#criacao da thread que trata mensagens recebidas do servidor
class ThreadMensagensRecebidas(threading.Thread):
	chat = None
	
	def __init__(self, chat):
		self.chat = chat
		threading.Thread.__init__ (self)

	def atualizaChat(self, mensagem):
		self.chat.get_buffer().insert(self.chat.get_buffer().get_end_iter(), mensagem+'\n')
		
	def run(self):
		global cliente
		while cliente.conectado: #loop infinito
			try: #tentativa de recepcao de dados do servidor
				dados = cliente.recebe()
				#comando "sair"
				if dados.find('qwerasdfzxcvtyuighjkbnm,789+456,/*-0 ASDFdaDFDsfS fdfD54df2DF45Dsf') != -1:
					break
				#comando "encerrar servidor"
				elif dados.find('23498 f/2423rdfs99xcv0a ad8 09 /45//88908/ sdf99089/*-)(*53/ 324 -3243-') != -1:
					self.atualizaChat('O servidor está sendo encerrado')
					cliente.desconecta()
				#outras mensagens (chat)
				elif len(dados) != 0: #se a mensagem nao esta em branco
					gobject.idle_add(self.atualizaChat, dados)
			except: #caso a tentativa falhe
				pass
#ThreadMensagensRecebidas