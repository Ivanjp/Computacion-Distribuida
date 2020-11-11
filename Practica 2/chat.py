import time
import socket
import threading
import sys
import os

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
        self.listaC = ["PepperPots 2920" , "AMLO 4536"]
        self.puerto_v = ""
        self.flagList = False

    def conecta_cliente(self,puerto,op):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_Adress = ('localhost',puerto)
        try:
            sock.connect(server_Adress)
            self.conexion_cliente = sock
            if op:
                cadena = str(self.puerto_s) + " " + self.nickname_chat
                self.conexion_cliente.sendall(cadena.encode())
            else: 
                self.conexion_cliente.sendall(("@" + self.nickname_chat).encode())
            
            self.ch_client = True
        except:
            print("Canal no activo, intenta mas tarde")    

    def espera_servidor(self,op):
        if op:
            self.socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            server_Address = ('localhost',self.puerto_s)
            self.socket_server.bind(server_Address)
            self.socket_server.listen(1)
            print("> Escuchando en el puerto " + str(self.puerto_s))
            print("> Tu nombre de usuario por defecto es "+ self.nickname_chat + " para cambiarlo escribe @chname seguido del nombre que quieres usar" )

        self.conexion_servidor, server_Address = self.socket_server.accept()

        if not self.ch_client:
            try:
                respuesta = self.conexion_servidor.recv(100).decode("utf-8")
                puerto = int(respuesta.split(" ")[0])
                self.puerto_v = str(puerto)
                self.nickname_vecino = respuesta.split(" ")[1]
                print("> Sincronizando en puerto " + str(puerto))
                self.conecta_cliente(puerto,False)
            except:
                return

        self.escucha()

    def entrada(self):
        print("> Bienvenido de nuevo")
        while True:
            comando = input()
            if comando.startswith("@chname"):
                if not self.ch_client and not self.ch_server:
                    self.nickname_chat = comando.split(" ")[1]
                    print("> Nombre de usuario cambiado a " + self.nickname_chat)
                else:
                    print("NO puedes cambiar de nombre mientras chateas")
            elif comando.startswith("@conecta"):
                if not self.ch_client and not self.ch_server:

                    p = ""
                    for n in self.listaC:
                        if comando.split(" ")[1] == n.split(" ")[0]:
                            self.flagList = True
                            p = n
                    
                    if self.flagList == True:
                        puerto = int(p.split(" ")[1])
                        self.puerto_v = str(puerto)
                        self.conecta_cliente(puerto, True)
                    elif self.flagList == False and any(chr.isdigit() for chr in comando.split(" ")[1]) == False:
                        print("> Este usuario no esta en tu lista de contactos, ingresa un usuario que tengas agregado o el puerto de otro usuario")
                    elif self.flagList == False and any(chr.isdigit() for chr in comando.split(" ")[1]) == True:
                        puerto = int(comando.split(" ")[1])
                        self.puerto_v = str(puerto)
                        self.conecta_cliente(puerto, True)  

                else:
                    print("Ya hay un chat activo, escribe @desconecta para terminar")
            elif comando.startswith("@contactos"):
                if not self.ch_client and not self.ch_server:
                    print("Lista de contactos:\n")
                    for x in self.listaC:
                        print(str(self.listaC.index(x)+1)+". "+x)
                else:
                    print("NO puedes consultar tu lista de contactos mientras chateas")
            elif comando.startswith("@desconecta"):
                if not self.ch_client and not self.ch_server:
                    print("> No hay nunguna conexion")
                    continue
                print("> Saliste de la conexion") 
                
                if self.flagList == False:
                    self.listaC.append(self.nickname_vecino+" "+ str(self.puerto_v))

                self.ch_server = False
                self.ch_client = False
                self.flagList = False
                self.conexion_cliente.sendall(comando.encode())
                self.conexion_servidor.close()
                self.conexion_cliente.close()
                threading.Thread(target=self.espera_servidor,args=(False,)).start()
            elif comando.startswith("@salir"):
                if not self.ch_client and not self.ch_server:
                    print("> Hasta luego") 
                    self.socket_server.close()
                    os._exit(1)
                else:
                    print("NO puedes cerrar la aplicacion hasta desconectarte del chat, escribe @desconecta.")
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

                for n in self.listaC:
                    if self.nickname_vecino in n:
                        self.flagList = True
                
                if self.flagList == False:
                 self.listaC.append(self.nickname_vecino+" "+ str(self.puerto_v))

                threading.Thread(target=self.espera_servidor,args=(False,)).start()
                self.flagList = False
                break
            elif info.startswith("@"):
                self.nickname_vecino = info[1:]
                continue
            print("[" + self.nickname_vecino + "]" + info)

    def run(self):
        threading.Thread(target=self.espera_servidor,args=(True,)).start()
        self.entrada()
                        

Chat(int(sys.argv[1])).run()                
                                    
