#importações
import gtk, gtk.glade, gobject
import os

gobject.threads_init()
path = os.path.dirname(os.path.abspath(__file__))

class TelaConversa:
	dic = {}
	tela = None
	edMensagem = None
	edConversa = None

	def __init__(self, contato):
		xml = gtk.glade.XML(os.path.join(path, 'res/cliente-conversa-gui.glade'))
		self.dic = {
			'on_telaConversa_destroy': self.sair,
			'on_edMensagem_activate': self.impEdMensagem,
		}
		xml.signal_autoconnect(self.dic)
		self.tela = xml.get_widget('telaConversa')
		self.tela.set_title('Conversa com %s'%contato['nome'])
		self.edConversa = xml.get_widget('edConversa')
		self.edMensagem = xml.get_widget('edMensagem')
	#__init__
	
	def impEdMensagem(self, *args):
		pass
	#impEdMensagem
	
	def sair(self, *args):
		self.tela.destroy()
	#sair
#class TelaConversa