# Práctica 2 Aplicación distribuida: peer to peer
Chat

## Requerimientos
`Python 3`

## Modo de Uso
* Abrir una terminal y ubicarse en la carpeta donde se clono este repositorio.
* Correr el programa con el comando `python3 chat.py XXXX` donde **XXXX** representa el puerto donde se estará conectado.

## Notas
Los comandos disponibles dentro de la aplicacion son:
* `@conecta XXXX o @conecta name` donde **XXXX** es algún puerto al que se quiera conectar o **name** el nombre de algún contacto. Si no
se encuentra **name** en la lista de contactos se mandara un aviso, si **XXXX** no esta activo también se mandara un aviso.
* `@chname name`Comando para cambiar tu nombre de usuario predeterminado por otro diferente.
* `@desconecta`Comando para desconectarse del chat que tenemos activo.
* `@contactos`Comando para poder ver la lista de contactos.
* `@salir`Comando para salir de la aplicación.

## Reglas de Comandos ##
Si hay un chat activo el único comando disponible es `@desconecta`los demás estarán disponibles una vez finalice el chat. 
