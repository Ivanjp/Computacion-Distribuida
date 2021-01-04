import time
import threading
import socket
import sys
class Par:

	def __init__(self,puerto_s,puerto_cs,puerto_s_cliente,op = 1,rango = 1):
		self.chateando_cliente = False
		self.chateando_servidor = False
		self.conexion_cliente = None
		self.conexion_servidor = None
		self.conexion_arq_cs = None
		self.socket_servidor = None
		self.puerto_s = puerto_s
		self.puerto_cs = puerto_cs
		self.puerto_s_cliente = puerto_s_cliente
		self.info = None
		if op == 1:
			self.op = True
		else:
			self.op = False
		self.rango = rango
		self.diccionario = {}

	def agrega_palabra(self,palabra,significado):
		if not palabra in self.diccionario.keys():
			if self.rango == 1 and ord(palabra[0]) >= 97 and ord(palabra[0]) <= 109 :
				self.diccionario.setdefault(palabra,significado)
				print(":: Palabra agregada!")
				return "Exito"
			if self.rango == 0 and ord(palabra[0]) >= 110 and ord(palabra[0]) <= 122 :
				self.diccionario.setdefault(palabra,significado)
				print(":: Palabra agregada!")
				return "Exito"
		print(":: La palabra ya existe, usa la funcion de edicion")
		return "Error"
	def edita_palabra(self,palabra_anterior,palabra_nueva):
		try:
			if palabra_anterior in self.diccionario.keys():
				significado = self.diccionario[palabra_anterior]
				del self.diccionario[palabra_anterior] #eliminar clave y valor
				if not palabra_nueva in self.diccionario.keys():
					self.diccionario.setdefault(palabra_nueva,significado)
					print(":: Palabra correctamente actualizada!")
				else :
					self.diccionario.setdefault(palabra_anterior,significado)
					print(":: La palabra no se pudo actualizar!")
		except Exception as err:
			print(":: Hubo algun error inesperado!")
			print(err)
	def edita_significado(self,palabra,nuevo_significado):
		if palabra in self.diccionario.keys() :
			self.diccionario[palabra] = nuevo_significado
			print(":: Se ha editado el significado con exito!")
			return
		print(":: La palabra con el significado a cambiar no existe")

	def obten_significado(self,palabra):
		if palabra in self.diccionario.keys():
			significado = self.diccionario[palabra]
			print(":: Significado obtenido")
			return significado
		print(":: Palabra no existente")
	def ejecuta_comando(self,comando):
		arr = comando.split(" ")
		#@p2p P instruccion parametros
		#@p2p R instruccion parametros
		if "@p2p P ag" in comando : #agregar palabra
			mensaje = self.agrega_palabra(arr[3],arr[4])
			if mensaje == "Error" :
				#si es negativo le paso al consulta a otro nodo
				co = "@p2p R ag " + arr[3] + " " + arr[4]
				self.conexion_cliente.sendall(co.encode())#cambio
			else :
				self.conexion_arq_cs.sendall(mensaje.encode())
		elif "@p2p R ag" in comando :
			mensaje = self.agrega_palabra(arr[3],arr[4])
			self.conexion_cliente.sendall(mensaje.encode())
		else :
			self.conexion_arq_cs.sendall(comando.encode())
		self.info = None
		'''
		elif "@p2p edp" in comando: #edita palabra
		elif "@p2p eds" in comando: #edita significado
		elif "@p2p ob" in comando: #obtiene significado palabra
		elif "@p2p dic" in comando: #obtiene diccionario completo 
		'''

	#Funcion que se usa para entablar la comunicacion con un servidor
	def conecta_como_cliente(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = ('localhost', self.puerto_s_cliente)
		sock.connect(server_address)
		self.conexion_cliente = sock
	#Funcion que se usa para esperar la comunicacion con un cliente
	def espera_como_servidor(self):
		if self.op :
			self.conecta_como_cliente()
		#inicializando el socket servidor
		self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = ('localhost', self.puerto_s)
		self.socket_servidor.bind(server_address)
		self.socket_servidor.listen(1)
		print(":: Escuchando en el puerto " + str(self.puerto_s))
		#a la espera de conexion
		self.conexion_servidor, client_address = self.socket_servidor.accept()
		if not self.op :
			print(":: Conectandose como cliente al puerto " + str(self.puerto_s_cliente))
			self.conecta_como_cliente()
		self.escucha()
		#cambio
	def escucha(self):
		print(":: Comenzando a esperar datos")
		while True:
			#info = None
			'''
			if self.info != None :
				self.ejecuta_comando(self.info);
			'''
			try:
				info = self.conexion_servidor.recv(1024).decode("utf-8")
				#si no es comando devolver respuesta a la red cliente servidor
			except:
				print(":: No hay conexion para leer mensajes.")
				break
			if len(info) == 0:
				break
			self.ejecuta_comando(info);

	def espera_solo_servidor(self):
		socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = ('localhost', self.puerto_cs)
		socket_servidor.bind(server_address)
		socket_servidor.listen(1)
		print(":: Escuchando a CS en el puerto " + str(self.puerto_cs))
		#a la espera de conexion
		self.conexion_arq_cs, client_address = socket_servidor.accept()
		while True:
			self.info = self.conexion_arq_cs.recv(1024).decode("utf-8")
			self.ejecuta_comando(self.info);
			#se asigna a una variable global la variable info
	def corre(self):
		print(":: Inicializando servidores")
		threading.Thread(target=self.espera_solo_servidor).start()
		self.espera_como_servidor()
		#self.entrada()
try:
	Par(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5])).corre()
except Exception as err:
	print(err)