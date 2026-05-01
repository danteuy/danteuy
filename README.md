## Hi there 👋

This is an experimental programming language which aims to teach kids between 8 and 11 years old. 
The whole syntax is written in spanish, and so will be the docs from this point.

<img width="1000" height="630" alt="image" src="https://github.com/user-attachments/assets/23238181-92c1-4f74-9028-9f115cb8065c" />
D.A.N.T.E. v0.1
-
Desarrollo de Aplicaciones para Niños en Trayecto Escolar.
Introducción:
D.A.N.T.E. es un software de aprendizaje para niños en edad escolar, cuya meta es enseñar las bases de la programación utilizando código. Nace de una necesidad particular, en el mundo actual de la programación existen varios tipos de lenguajes que permiten a los niños aprender a programar con bloques, sin embargo el salto de nivel desde la programación con bloques hacia el código puede volverse muy duro, ya que se deben aprender una gran cantidad de conceptos nuevos y complejos que no son aptos para edades demasiado tempranas. D.A.N.T.E. pretende ser un paso intermedio entre el lenguaje de bloques y el código estándar, utilizando código escrito pero en un nivel más básico, con palabras y frases en español y sin tanto requerimiento de simbología (comillas, punto y coma, parentesis, etc). Es un paso previo a salto a un lenguaje más complejo para la niñez temprana como lo sería un Python.

Concepto:
D.A.N.T.E. está hecho en base a tecnología Python, consta de un IDE especial que permite al niño codificar mientras visualiza una barra lateral de estados que le dice en todo momento los nombres de las variables (cajas) y sus contenidos previos a tiempo de ejecución. Posee además varios elementos gráficos que ayudan al aprendizaje, tal como el highlight automático que tienen todos los IDEs, pero sumando además otros conceptos, como por ejemplo, la mayusculización automática de las palabras reservadas, y el coloreado especifico que brinde un gran contraste con lo que no es una palabra reservada, por ejemplo, combinaciones rojo/azul. La idea del lenguaje es manejar líneas independientes de código que hagan hagan una tarea pero la hagan bien, para no complejizar demasiado la legibilidad de las líneas independientes, por ejemplo, en vez de: mostrar “hola ” + nombre + “, gracias por registrarte” en una sola línea, se hará en tres líneas, una para el print del “hola”, otra para el print de la variable “nombre” y otra para el “gracias por registrarte”, esto es menos práctico pero más fácil de entender para los niños de temprana edad, porque no tendrán que aprender cómo incrustar valores de variables dentro de textos hardcodeados en los print. Además, los bloques anidados se harán con INICIO y FIN y se autoindentará.

Tipos de datos:
Los únicos tipos de datos serán: texto y entero.

IDE:
Cajas en el costado que muestren los contenidos de las variables en la linea del cursor.
Mayusculización de palabras reservadas.
Minusculización de palabras no reservadas.
Resaltador de colores, palabras reservadas en azul, no reservadas en rojo.
Autoindentado de un espacio, no necesario pero sí recomendado.

Palabras Reservadas:
CREAR - crea una variable, inicializada sin valor.
EDITAR - modifica el valor de una variable ya creada.
PEDIR - solicita un valor por teclado para guardar en una variable.
MOSTRAR - muestra texto, número, o el valor de una variable en pantalla.
PREGUNTA - estructura condicional
SINO - estructura condicional
REPETIR - estructura de repetición
OPCIONES - estructura de selección
OPCION - cada una de las selecciones de una estructura
INICIO - abre un bloque de código
FIN - cierra un bloque de código
Y - operador AND
O - operador OR

<b>Para abrir la aplicación: Descarga todos los archivos, ponlos en la misma carpeta y ejecuta dante_ide.py.</b>
