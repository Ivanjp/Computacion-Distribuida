import time
import socket
import threading
import sys

class Chat:

    def __init__(self,puerto):
        self.ch_client = False
        self.ch_server = False
        self.conexion_cliente = None
        self.conexion_servidor = None
        self.socket_server = None
        self.nickname_chat = "Noobmaster69"
        self.nickname_vecino = "JohnConnor3"
        self.puerto_s = puerto
        self.listaC = ["jejei 2920" , "juds 4536"]

    def conecta_cliente(self,puerto,op):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_Adress = ('localhost',puerto)
        sock.connect(server_Adress)
        self.conexion_cliente = sock
        if op:
            cadena = str(self.puerto_s) + " " + self.nickname_chat
            self.conexion_cliente.sendall(cadena.encode())
        else: 
            self.conexion_cliente.sendall(("@" + self.nickname_chat).encode())
        
        self.ch_client = True

    def espera_servidor(self,op):
        if op:
            self.socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            server_Address = ('localhost',self.puerto_s)
            self.socket_server.bind(server_Address)
            self.socket_server.listen(1)
            print("> Escuchando en el puerto " + str(self.puerto_s))

        self.conexion_servidor, server_Address = self.socket_server.accept()

        if not self.ch_client:
            try:
                respuesta = self.conexion_servidor.recv(100).decode("utf-8")
                puerto = int(respuesta.split(" ")[0])
                self.nickname_vecino = respuesta.split(" ")[1]
                print("> Sincronizando en puerto " + str(puerto))
                self.conecta_cliente(puerto,False)
            except:
                return

        self.escucha()

    def entrada(self):
        print("> Listo para recibir comandos o mensajes")
        while True:
            comando = input()
            if comando.startswith("@sobrenombre"):
                if not self.ch_client and not self.ch_server:
                    self.nickname_chat = comando.split(" ")[1]
                    print("> El sobrenombre a cambiado a " + self.nickname_chat)
                else:
                    print("No fue posible cambiar el sobrenombre durante la ocnversacion")
            elif comando.startswith("@conecta"):
                if not self.ch_client and not self.ch_server:
                    puerto = int(comando.split(" ")[1])
                    self.conecta_cliente(puerto, True)
                    self.listaC.append(self.nickname_vecino + " " + str(puerto))
                else:
                    print("Ya hay un chat activo, escribe @desconecta para terminar")
            elif comando.startswith("@contactos"):
                print("Lista de contactos:\n")
                for x in self.listaC:
                    print(str(self.listaC.index(x)+1)+". "+x)
            elif comando.startswith("@desconecta"):
                if not self.ch_client and not self.ch_server:
                    print("> No hay nunguna conexion")
                    continue
                print("> Saliste de la conexion") 
                self.ch_server = False
                self.ch_client = False
                self.conexion_cliente.sendall(comando.encode())
                self.conexion_servidor.close()
                self.conexion_cliente.close()
                threading.Thread(target=self.espera_servidor,args=(False,)).start()
            elif comando.startswith("@salir"):
                print("> Hasta luego")    
                try:
                    self.conexion_servidor.close()
                    sys.exit()
                except:
                    pass
            elif comando.startswith("@"):
                print("> Comando no soportado")
            else: 
                try:
                    self.conexion_cliente.sendall(comando.encode())
                except:
                    print("> No hay conexion para enviar mensajes")

    def escucha(self):
        while True:
            info = None
            try:
                info = self.conexion_servidor.recv(1024).decode("utf-8")
            except:
                print("> No hay conexion para leer mensajes")
                break
            if len(info) == 0:
                break
            if info.startswith("@desconecta"):
                time.sleep(1)
                self.ch_server = False
                self.ch_client = False
                print("> " + self.nickname_vecino + " cerro la conversacion")
                threading.Thread(target=self.espera_servidor,args=(False,)).start()
                break
            elif info.startswith("@"):
                self.nickname_vecino = info[1:]
                continue
            print("[" + self.nickname_vecino + "ppp]" + info)

    def corre(self):
        threading.Thread(target=self.espera_servidor,args=(True,)).start()
        self.entrada()

Chat(int(sys.argv[1])).corre()                
                                    
