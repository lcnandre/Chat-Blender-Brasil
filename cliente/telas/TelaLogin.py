#globais
LOGIN_USUARIO_INCORRETO = '1'
LOGIN_SENHA_INCORRETA = '2'

#importações
import os
import gtk, gtk.glade
from util import mostraErro
from TelaPrincipal import TelaPrincipal
from cliente import Cliente

path = os.path.dirname(os.path.abspath(__file__))

class TelaLogin:
	#mapeamento de signals
	dic = {}
	tela = None
	edLogin = None
	edSenha = None
	cliente = Cliente()
	
	def __init__(self):
		#carrega a interface
		xml = gtk.glade.XML(os.path.join(path, 'res/cliente-login-gui.glade'))
		self.dic = {
			'gtk_main_quit': lambda win: gtk.main_quit(),
			'on_btnEntrar_activate': self.impBtnEntrar,
			'on_btnEntrar_clicked': self.impBtnEntrar,
			'on_edLogin_activate': self.impBtnEntrar,
			'on_edSenha_activate': self.impBtnEntrar,
		}
		xml.signal_autoconnect(self.dic)
		self.edLogin = xml.get_widget('edLogin')
		self.edSenha = xml.get_widget('edSenha')
		self.tela = xml.get_widget('telaLogin')
		self.cliente.conecta()
	#__init__
		
	def impBtnEntrar(self, *args):
		login = self.edLogin.get_text()
		senha = self.edSenha.get_text()
		#
		if self.valida(login, senha):
			retorno = self.cliente.fazLogin(login, senha)
			if retorno == LOGIN_USUARIO_INCORRETO:
				mostraErro(self.tela, 'Usuário inexistente')
			elif retorno == LOGIN_SENHA_INCORRETA:
				mostraErro(self.tela, 'Senha incorreta')
			else:
				self.tela.hide()
				self.cliente.usuario = login
				TelaPrincipal(self.cliente).tela.show()				
	#impBtnEntrar
	
	def valida(self, login, senha):
		if len(login.strip()) == 0:
			mostraErro(self.tela, 'Informe seu login')
			return False
		elif len(senha.strip()) == 0:
			mostraErro(self.tela, 'Informe sua senha')
			return False
		#
		return True
	#valida
#class TelaLogin