#importações
import gtk
from servidor.telas import TelaPrincipal

#definição do tema padrão
settings = gtk.settings_get_default()
settings.set_string_property('gtk-theme-name', 'MS-Windows', '')

#chama tela de login
TelaPrincipal()
#executa o programa
gtk.main()