## Agregación, evaluación y monitorización de imagen de empresa


Una vez hemos visto las técnicas fundamentales para la recopilación de datos sociales,
el siguiente paso natural es el de utilizar estos datos para el análisis de la actividad
de una marca, que podría ser la nuestra propia, y hacer frente así a cuestiones naturales
sobre la popularidad, aceptación y/o sentimientos que se pueden desprender de las
comunicaciones entre la marca y sus seguidores. A día de hoy, cualquier marca comercial
utiliza las redes sociales (múltiples) para comunicarse con sus potenciales consumidores,
bien sea informando sobre nuevos productos, servicios, noticias de la compañía de relevancia, 
colaboraciones con otras marcas/personas de interés, etc. Este flujo de comunicación, 
como ya hemos podido anticipar en el apartado [anterior](../02-social-data-collection/README.md),
es abrumador, pudiendo perdernos en la infinidad de contenidos de lo que realmente se 
está hablando (y cómo) en ellos. El objetivo principal de este apartado es precisamente el
de mostrar el procedimiento genérico de colección-procesamiento-análisis (también conocido 
como *pipeline*), a partir del cual podremos extraer conclusiones para resolver nuestras
preguntas sobre la actividad y percepción de la marca y sus productos. Para ello, usaremos
una marca conocida que tenga actividad considerable en varias plataformas, e.g. Twitter y
Facebook. Así, en este capítulo cubriremos los siguientes puntos:

- Extracción de datos sociales de la página oficial de Facebook de la marca
- Extracción de datos sociales de la cuenta oficial de Twitter de la marca
- Limpieza/preprocesado de los datos sociales
- Procesado para la extracción de palabras claves (*keywords*), bigramas, y hashtags
- Procesado de comentarios para el análisis de sentimiento
- Análisis de los resultados anteriores

Estos tópicos encajan en el siguiente diagrama que ilustra los 7 pasos fundamentales
de una aplicación analítica:

<img src="_img/pipeline.png" alt="Pipeline" width="400"/>






    - Planificación del proyecto
    - Análisis: Palabras clave y sintagmas nominales
    - Detección de tendencias