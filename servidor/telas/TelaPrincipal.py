#importações
import os
import gtk, gtk.glade, gobject
from util import mostraErro, getIpWan
from servidor import Servidor

gobject.threads_init()
path = os.path.dirname(os.path.abspath(__file__))
servidor = Servidor()

class TelaPrincipal:
	#mapeamento de signals
	dic = {}
	tela = None
	btnIniciar = None
	btnParar = None
	edLog = None
	
	def __init__(self):
		#carrega a interface
		xml = gtk.glade.XML(os.path.join(path, 'res/servidor-principal-gui.glade'))
		self.dic = {
			'on_telaPrincipal_destroy': self.sair,
			'on_btnIniciar_activate': self.impBtnIniciar,
			'on_btnIniciar_clicked': self.impBtnIniciar,
			'on_btnParar_activate': self.impBtnParar,
			'on_btnParar_clicked': self.impBtnParar,
		}
		xml.signal_autoconnect(self.dic)
		self.tela = xml.get_widget('telaPrincipal')
		self.btnIniciar = xml.get_widget('btnIniciar')
		self.btnParar = xml.get_widget('btnParar')
		self.edLog = xml.get_widget('edLog')
		xml.get_widget('lblIp').set_text(getIpWan())
	#__init__
	
	def impBtnIniciar(self, *args):
		servidor.inicia(self.edLog)
		self.btnIniciar.set_sensitive(False)
		self.btnParar.set_sensitive(True)
		self.edLog.get_buffer().insert(self.edLog.get_buffer().get_start_iter(), 'Servidor iniciado\n')
	#impBtnIniciar
	
	def impBtnParar(self, *args):
		servidor.para()
		self.btnParar.set_sensitive(False)
		self.btnIniciar.set_sensitive(True)
		self.edLog.get_buffer().insert(self.edLog.get_buffer().get_start_iter(), 'Servidor parado\n')
	#impBtnParar
	
	def sair(self, *args):
		if self.btnIniciar.state == gtk.STATE_INSENSITIVE:
			servidor.para()
		gtk.main_quit()
	#impBtnParar
#class TelaPrincipal