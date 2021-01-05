import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', int(sys.argv[1]))
sock.connect(server_address)

def main():
    print("Selecciona una opción")
    print("\t1 - Agregar palabra.")
    print("\t2 - Editar palabra")
    print("\t3 - Editar significado")
    print("\t4 - Obtener significado")
    print("\t5 - Ver diccionario")
    print("\t0 - Salir")


while True:
    # Mostramos el menu
    main()

    # solicituamos una opción al usuario
    opcionMenu = input("\nIngresa la opcion >> ")

    if opcionMenu == "1":
        palabra = input("Ingresa tu palabra >> \n")
        significado = input("Ingresa el significado >> \n")
        sock.sendall((f"@p2p P ag {palabra} {significado}").encode())
        print(sock.recv(1024).decode("utf-8"))
        print("\n")
    elif opcionMenu == "2":
        palabra_a = input("Ingresa la palabra que quieres modificar >> \n")
        palabra_n = input("Ingresa la nueva palabra >> \n")
        sock.sendall((f"@p2p edp {palabra_a} {palabra_n}").encode())
        print(sock.recv(1024).decode("utf-8"))
        print("\n")
    elif opcionMenu == "3":
        palabra = input("Ingresa la palabra cuyo significado quieres modificar >> \n")
        significado_n = input("Ingresa el nuevo significado >> \n")
        sock.sendall((f"@p2p eds {palabra} {significado_n}").encode())
        print(sock.recv(1024).decode("utf-8"))
        print("\n")
    elif opcionMenu == "4":
        palabra = input("Ingresa la palabra >> \n")
        sock.sendall((f"@p2p ob {palabra}").encode())
        print(sock.recv(1024).decode("utf-8"))
        print("\n")
    elif opcionMenu == "5":
        sock.sendall(("@p2p dic").encode())
        print(sock.recv(1024).decode("utf-8"))
        print("\n")
    elif opcionMenu == "0":
        break
    else:
        print("")
        input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")
