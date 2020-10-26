# Práctica 1 Aplicación distribuida: cliente/servidor
Aplicación de registros de corredores de atletismo.

## Requerimientos
`Java 8/11` y `Docker CE`

## Modo de Uso
### Iniciar el contenedor

1. Tener el servicio de `Docker CE` iniciado
2. Abrir una terminal y ubicarse en la carpeta donde se clono este repositorio  
3. Una vez estando posicionado en la carepta ejecuta el siguiente comando **`docker-compose up --build`**.  
Al ejecutarlo se iniciara la imagen que contiene `openjdk 8` en el cual esta el servidor asi como el servicio de la Base de Datos de `Postgres`.

### Iniciar la aplicación

1. Abrir otra terminal y ubicarse en la carpeta _Interfaz_ todo esto se encuentra en la carpeta donde se clono el repositorio.
2. Compilar los 3 archivos de `Java` con **`javac *.java`**
3. Ejecutar el archivo _Login_ con **`java Login`**
4. Una vez dentro de la aplicación se mostrará la pantalla de Inicio de Sesión, ahí podrás ingresar con alguno de los siguientes usuarios:  

   - **`Username`** : Ivan  **`Password`**: password
   - **`Username`** : Monica  **`Password`**: moniquinha26
   - **`Username`** : Elizabeth  **`Password`**: qwerty12
   - **`Username`** : Paul  **`Password`**: 543210
   - **`Username`** : Gabriel  **`Password`**: aphelios23
   - **`Username`** : Maite  **`Password`**: sirenita  
   
5. Si no quieres utilizar los usuarios de prueba, crea el tuyo, presiona el botón **`Registrarse`** que se encuentra en la parte inferior izquierda y llena los datos que se te piden
**NOTA** si no modificas los valores de reisdencia y de edad se pondrá por default los valores que se muestran.

## Notas
* Para detener el contenedor ejecuta el siguiente comando **`docker-compose down`**.
* Para cerrar la aplicación basta con darle al botón de cerrar ❌
* Para poder observar como funciona la expiración del `JWT` se tiene configurado por default que expire en 1 minuto, despues de ese minuto ya no podras realizar
ninguna actividad dentro de la aplicación y se te redireccionará a la pantalla de Inicio de Sesión. Si quieres cambiarlo modifica el archivo `Handler.java`que se ubica en
la carpeta `_Practica1/cliente_servidor/src/Handler.java_`. Para ver los cambios tendras que volver a compilar los archivos `Java` antes mencionados y volver a iniciar
el contenedor.
