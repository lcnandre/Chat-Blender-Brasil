import MySQLdb

HOST = 'localhost'
DB = 'chat'
USER = 'root'
PASSWD = ''

def getConexao():
	return MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DB)