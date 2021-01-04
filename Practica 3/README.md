# Práctica 3 Aplicación distribuida híbrida.
Diccionario

## Requerimientos
`Python 3` `Docker CE`

## Modo de Uso
### Iniciar el contenedor

1. Tener el servicio de `Docker CE` iniciado
2. Abrir una terminal y ubicarse en la carpeta donde se clono este repositorio  
3. Una vez estando posicionado en la carepta ejecuta el siguiente comando **`docker-compose up --build`**.  
Al ejecutarlo se iniciara la imagen que contiene `Python` en el cual esta el servidor asi como el servicio de la Base de Datos de `Postgres`.

### Iniciar la aplicación

## Notas
Los comandos disponibles dentro de la aplicacion son:
* `@conecta XXXX o @conecta name` donde **XXXX** es algún puerto al que se quiera conectar o **name** el nombre de algún contacto. Si no
se encuentra **name** en la lista de contactos se mandara un aviso, si **XXXX** no esta activo también se mandara un aviso.
* `@chname name`Comando para cambiar tu nombre de usuario predeterminado por otro diferente.
* `@desconecta`Comando para desconectarse del chat que tenemos activo.
* `@contactos`Comando para poder ver la lista de contactos.
* `@salir`Comando para salir de la aplicación.


