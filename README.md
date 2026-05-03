## Hi there 👋

This is an experimental programming language which aims to teach kids between 8 and 11 years old. 
The whole syntax is written in spanish, and so will be the docs from this point.
<br>
<img width="1000" height="630" alt="image" src="https://github.com/user-attachments/assets/23238181-92c1-4f74-9028-9f115cb8065c" />
<b>D.A.N.T.E. v0.1</b><br>
<b>Desarrollo de Aplicaciones para Niños en Trayecto Escolar.</b><br>
<br>Introducción:<br>
D.A.N.T.E. es un software de aprendizaje para niños en edad escolar, cuya meta es enseñar las bases de la programación utilizando código. Nace de una necesidad particular, en el mundo actual de la programación existen varios tipos de lenguajes que permiten a los niños aprender a programar con bloques, sin embargo el salto de nivel desde la programación con bloques hacia el código puede volverse muy duro, ya que se deben aprender una gran cantidad de conceptos nuevos y complejos que no son aptos para edades demasiado tempranas. D.A.N.T.E. pretende ser un paso intermedio entre el lenguaje de bloques y el código estándar, utilizando código escrito pero en un nivel más básico, con palabras y frases en español y sin tanto requerimiento de simbología (comillas, punto y coma, parentesis, etc). Es un paso previo a salto a un lenguaje más complejo para la niñez temprana como lo sería un Python.<br>
<br>
<b>Concepto:</b><br>
D.A.N.T.E. está hecho en base a tecnología Python, consta de un IDE especial que permite al niño codificar mientras visualiza una barra lateral de estados que le dice en todo momento los nombres de las variables (cajas) y sus contenidos previos a tiempo de ejecución. Posee además varios elementos gráficos que ayudan al aprendizaje, tal como el highlight automático que tienen todos los IDEs, pero sumando además otros conceptos, como por ejemplo, la mayusculización automática de las palabras reservadas, y el coloreado especifico que brinde un gran contraste con lo que no es una palabra reservada, por ejemplo, combinaciones rojo/azul. La idea del lenguaje es manejar líneas independientes de código que hagan hagan una tarea pero la hagan bien, para no complejizar demasiado la legibilidad de las líneas independientes, por ejemplo, en vez de: mostrar “hola ” + nombre + “, gracias por registrarte” en una sola línea, se hará en tres líneas, una para el print del “hola”, otra para el print de la variable “nombre” y otra para el “gracias por registrarte”, esto es menos práctico pero más fácil de entender para los niños de temprana edad, porque no tendrán que aprender cómo incrustar valores de variables dentro de textos hardcodeados en los print. Además, los bloques anidados se harán con INICIO y FIN y se autoindentará.<br>
<br>
<b>Tipos de datos:</b><br>
Los únicos tipos de datos serán: texto y entero.<br>
<br>
<b>IDE:</b><br>
Cajas en el costado que muestren los contenidos de las variables en la linea del cursor.<br>
Mayusculización de palabras reservadas.<br>
Minusculización de palabras no reservadas.<br>
Resaltador de colores, palabras reservadas en azul, no reservadas en rojo.<br>
Autoindentado de un espacio, no necesario pero sí recomendado.<br>
<br>
<b>Palabras Reservadas:</b><br>
CREAR - crea una variable, inicializada sin valor.<br>
EDITAR - modifica el valor de una variable ya creada.<br>
PEDIR - solicita un valor por teclado para guardar en una variable.<br>
MOSTRAR - muestra texto, número, o el valor de una variable en pantalla.<br>
PREGUNTA - estructura condicional<br>
SINO - estructura condicional<br>
REPETIR - estructura de repetición<br>
OPCIONES - estructura de selección<br>
OPCION - cada una de las selecciones de una estructura<br>
INICIO - abre un bloque de código<br>
FIN - cierra un bloque de código<br>
Y - operador AND<br>
O - operador OR<br>
<br>
<b>Para abrir la aplicación: Descarga todos los archivos, ponlos en la misma carpeta y ejecuta dante_ide.py.</b>
