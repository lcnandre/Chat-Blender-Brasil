#importações
import gtk
import re 
import urllib

# cria um dialogo de erro
def mostraErro(pai, mensagem):
	telaErro = gtk.MessageDialog(pai, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO,
							   gtk.BUTTONS_NONE, mensagem)
	telaErro.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
	telaErro.run()
	telaErro.destroy()
#mostraErro

def getIpWan():
	reg = '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' 
	pag = urllib.urlopen('http://meuip.net/') 
	pag = str(pag.readlines()) 
	return re.findall(reg, pag)[0]
#getIpWan