#importações
import gtk
from cliente.telas import TelaLogin

#definição do tema padrão
settings = gtk.settings_get_default()
settings.set_string_property('gtk-theme-name', 'MS-Windows', '')

#chama tela de login
TelaLogin()
#executa o programa
gtk.main()