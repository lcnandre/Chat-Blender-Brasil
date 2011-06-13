========================
Chat Blender Brasil v0.1
========================

IMPORTANTE
==========

Por enquanto, não é possível conversar pela rede sem alterar o código, apenas numa mesma máquina

REQUERIMENTOS
=============

- Python 2
- PyGTK (http://www.pygtk.org/downloads.html)
- Python-MYSQL (http://sourceforge.net/projects/mysql-python)


PARA USAR
==========

#. Execute o arquivo "servidor.bat" ou "servidor.sh", dependendo de seu ambiente (ou ainda "servidor.py" diretamente)
#. Na tela do servidor, clique em Iniciar
#. Execute o arquivo "cliente.bat" ou "cliente.sh" (ou ainda "cliente.py" diretamente)
#. Use o usuário "teste" e senha "123" para entrar
#. Converse, de preferência abra outro cliente

TODO
====

- Definir a arquitetura do servidor que irá rodar no cliente (para IM)
- Implementar tela de conversa privada
- Permitir que um usuário adicione outro como contato (criar um botão na tela principal para isso)
- Quando um usuário fica offline, a lista de contatos de cada um de seus amigos deve ser atualizada com tal informação
- Hospedar o banco de dados na web
- Hospedar o servidor na web, com IP fixo ou dinâmico
- Criar uma página para a criação de contas
- Implementar o botão "Crie sua conta" no cliente

FIXME
=====

- Servidor:
	- para fechar o servidor, é preciso apertar o botão Parar duas vezes
	- o BD não funciona em sistemas Linux

MEMBROS
=======

- André Luan (Brutto AVT)
- Solano Felício (Solano)
- Leandro Benedet Garcia (Cerberus_1746)