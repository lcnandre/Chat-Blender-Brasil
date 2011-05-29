#importações
import os
import threading
import gtk, gtk.glade, gobject
from util import mostraErro
from cliente import Cliente

gobject.threads_init()
path = os.path.dirname(os.path.abspath(__file__))
cliente = Cliente()

class TelaPrincipal:
	#mapeamento de signals
	dic = {}
	tela = None
	edChat = None
	edMensagem = None
	
	def __init__(self, usuario):
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
		cliente.conecta()
		cliente.usuario = usuario
		ThreadMensagensRecebidas(self.edChat).start()
	#__init__
	
	def impEdMensagem(self, *args):
		mensagem = self.edMensagem.get_text()
		self.edMensagem.set_text('')
		cliente.envia(mensagem)
	#impEdMensagem
	
	def sair(self, *args):
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
		while cliente.conectado: #loop infinito
			try: #tentativa de recepcao de dados do servidor
				dados = cliente.recebe()
				if len(dados) != 0: #se a mensagem nao esta em branco
					gobject.idle_add(self.atualizaChat, dados)
			except: #caso a tentativa falhe
				pass
#ThreadMensagensRecebidas