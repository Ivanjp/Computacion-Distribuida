# Práctica 3 Aplicación distribuida híbrida.
Diccionario

## Requerimientos
`Python 3` `PostgresSQL`

## Modo de Uso
### Crear Base de Datos

1. Tener el servicio de `PostgresSQL` iniciado
2. Crear la base de datos con el script que se encuentra en la carpeta sql.  
3. Cambiar el nombre de usuario(**user**), nombre de la base de datos(**dbname**) y la contraseña(**password**) de la variable global **DATOS** en el archivo par.py 
4. Tener intalado _psycopg2_ , para instalarlo poner el siguiente comando: `pip install psycopg2`

### Iniciar la aplicación

Para iniciar el programa hay que seguir los siguientes pasos:

1. Abrir una terminal, ubicarse en la carpeta del proyecto _Practica3/cliente_servidor/src_ y ejecutar el siguiente comando _python par.py puertoNodoA puertoClienteA puertoNodoB a b_ donde a significa que nodo establecera primero la conexión y b que rango de letras tendrá asignado y los valores que toman son **0 o 1**.

2. Abrir otra terminal y hacer lo mismo del paso anterior solo que como este será el _NodoB_ el comando sería:  _python par.py puertoNodoB puertoClienteB puertoNodoA a b_ donde **puertoNodoA y puertoNodoB** deben coincidir con los que se pusieron en la terminal anterior.

# Ejemplo

_Terminal 1_: `python par.py 1082 1083 1080 0 0`
_Terminal 2_: `python par.py 1080 1081 1082 1 1`

3. Abrir otra terminal, ubicarse en la misma carpeta y correr el siguiente comando: _python servidor.py puerto_ donde el **puerto** debe de ser _puertoClienteA o puertoClienteB_ que se puso en las terminales anteriores es decir cualquiera de los segundos puertos que se colocaron en las terminales anteriores.

# Ejemplo

_Terminal 3_: `python servidor.py 1081`

4. Una vez hecho esto en la terminal donde ejecutamos el archivo **servidor.py** nos aparecera un menu con 5 opciones (agregar palabra, editar palabra, editar significado, buscar una palabra y salir), seleccionar alguna de las opciones y seguir las instrucciones que se soliciten.



