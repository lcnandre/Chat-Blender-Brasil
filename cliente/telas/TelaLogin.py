#importações
import os
import gtk, gtk.glade
from util import mostraErro
from TelaPrincipal import TelaPrincipal

path = os.path.dirname(os.path.abspath(__file__))

class TelaLogin:
	#mapeamento de signals
	dic = {}
	tela = None
	edLogin = None
	edSenha = None
	
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
	#__init__
		
	def impBtnEntrar(self, *args):
		import sqlite3
		import hashlib
		#
		conexao = sqlite3.connect(os.path.join(path, '..\..\chat.s3db'))
		cursor = conexao.cursor()
		login = self.edLogin.get_text()
		senha = self.edSenha.get_text()
		#
		if self.valida(login, senha):
			senha = hashlib.md5(senha).hexdigest()
			cursor.execute('select senha from usuario where login = ?', (login,))
			res = cursor.fetchall()
			if len(res) == 0:
				mostraErro(self.tela, 'Usuário inexistente')
			elif res[0][0] != senha:
				mostraErro(self.tela, 'Senha incorreta')
			else:
				self.tela.hide()
				TelaPrincipal(login).tela.show()				
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