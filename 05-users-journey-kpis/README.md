## Métricas para cuantificación de experiencia de usuario

En este módulo nos dedicamos al estudio de las métricas de seguimiento
y de monitorización de objetivos, conocidas por sus siglas en inglés KPIs 
(*Key Performance Indicators*). Por último, veremos la construcción formal
de la *Ecuación Maestra* que describe la evolución de la distribución de
usuarios en un conjunto de estados (de un espacio de estados discreto) en los 
que estamos interesados hacer seguimiento (user's journey).

El contenido de este capítulo se encuentra en las transparencias facilitadas
durante el curso en la plataforma oficial de la Universidad.

La aplicación de la *ecuación maestra* al estudio de la trayectoria de un usario
en un conjunto de estados de interés nos lleva al estudio de **cadenas de Markov**.
En particular, hemos aplicado el estudio de cadenas de Markov a un caso práctico,
donde hemos estudiado:

1. La extracción de la matriz de probabilidades de transición *T*
2. El análisis de los efectos de eliminación, para el consiguiente estudio de 
   atribución de responsabilidad a los diferentes estados de la cadena.

El ejemplo práctico se puede encontrar en [este notebook](markov-chain-study.ipynb).