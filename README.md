# **Asistente de tutor**

**SOLO PUEDE SER EJECUTABLE EN WINDOWS**

Asitente de tutor es una aplicación de escritorio diseñada con la interfaz gráfica Tkinter, la cual utiliza controladores automáticos de navegación como Selenium y una base de datos local para agrupar, analizar y revisar el estado académico de los estudiantes pertenecientes a un grupo en Kodland.

## Funcionamiento
El programa automátiza la entrada del tutor en el Backoffice, escanea los grupos y puede escanear adémas a todos los estudiantes.

## Limitaciónes
Solo funciona con grupos en la región de Latam, y que estén en los grupos de Python (old) y Scracth (old and new).

## Muestra
### 1. Ejecución del programa
##### Se ejecuta con el script "__main__", al ejecutarlo se abriran dos ventanas.
##### 1.1 La interfaz grafica
<a href="https://ibb.co/BqmxRZR"><img src="https://i.ibb.co/QrZRGNG/image-1.png" alt="image-1" border="0"></a>
##### 1.2 Controlador
<a href="https://ibb.co/GTJT2k0"><img src="https://i.ibb.co/Srxrn0P/image-2.png" alt="image-2" border="0"></a>

### 2. Ingreso al BO

Debe colocar sus credenciales, en caso de que estén equivocadas el programa no podra ingresar al BO. La aplicación ingresará desde el motor y extraerá todos lo grupos.

<a href="https://ibb.co/TkCTwzz"><img src="https://i.ibb.co/mGxBRQQ/image-3.png" alt="image-3" border="0"></a>

<a href="https://ibb.co/z4VTxR5"><img src="https://i.ibb.co/6W07wPZ/image-4.png" alt="image-4" border="0"></a>

### 3. home

En el  home encontrará dos botones, uno para ver los grupos y otro para extraer metricas generales de todos los grupos -aún en desarrollo-.

<a href="https://ibb.co/qJyv0h4"><img src="https://i.ibb.co/GHxqsG1/image-5.png" alt="image-5" border="0"></a>

### 4. Grupos

Se generá un tabla con todos los grupos con varias características por grupo:
- El nombre es un hipervinculo para el al BO del grupo.
- Botón para extraer una tabla de clasificación del grupo.
- Boton para ver a detalle las métricas de cada estudiante.
- Botón para ir a la grabación de la ultima clase.
<a href="https://imgbb.com/"><img src="https://i.ibb.co/rmy6vxr/image-6.png" alt="image-6" border="0"></a>
<a href="https://ibb.co/JCsZCjw"><img src="https://i.ibb.co/YbLgbBF/image-7.png" alt="image-7" border="0"></a>

### 5. Ranking
El botón de ranking, genera un formato html con la tabla de clasificación de los estudiantes. 

<a href="https://ibb.co/bj4bmTQ"><img src="https://i.ibb.co/CpjP8gm/image-8.png" alt="image-8" border="0"></a>

### 5. Extraer contactos (Detalles del grupo)
Revisa uno por uno cada estudiante, y genera otra ventana con los detalles del grupos -aún sigue en desarollo-, pero se puede usar para saber como es el rendimiento de los estudiantes. 
<a href="https://ibb.co/tB59H7f"><img src="https://i.ibb.co/jhFS8cK/image.png" alt="image" border="0"></a>
