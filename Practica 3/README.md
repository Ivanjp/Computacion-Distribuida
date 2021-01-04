# Práctica 3 Aplicación distribuida híbrida.
Diccionario

## Requerimientos
`Python 3` `PostgresSQL`

## Modo de Uso
### Crear Base de Datos

1. Tener el servicio de `PostgresSQL` iniciado
2. Crear la base de datos con el script que se encuentra en la carpeta sql.  
3. Cambiar el nombre de usuario, nombre de la base de datos y la contraseña en el archivo servidor.py 
4. Tener intalado _psycopg2_ , para instalarlo poner el siguiente comando: `pip install psycopg2`

### Iniciar la aplicación

Para iniciar el programa hay que seguir los siguientes pasos:

1. Abrir una terminal, ubicarse en la carpeta del proyecto y ejecutar el siguiente comando _python par.py puerto1 puerto2 puerto3 op1 op2_
donde los 3 puertos tienen que ser diferentes y op1 es  y op2 es, Ejemplo.

2. Abrir otra terminal y hacer lo mismo del paso anterior solo que

3. Abrir otra terminal, ubicarse en la carpeta del proyecto y correr el siguiente comando: _python servidor.py puerto1_

4. Una vez hecho esto en la terminal donde ejecutamos el archivo **servidor.py** nos aparecera un menu con 5 opciones (agregar palabra, editar significado, buscar una palabra, ver todo el diccionario y salir), seleccionar alguna de las opciones y seguir las instrucciones que se soliciten.



