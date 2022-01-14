## Introducción

En este módulo vamos a dedicarnos a preparar nuestro entorno de desarrollo,
que va a requerir de los siguientes componentes:

- [Python](): Será nuestro lenguaje de programación. Las ventajas de este lenguaje de
  programación son innumerables, e.g. permite escribir código conciso y fácilmente 
  inteligible, hay una comunidad ingente de desarrolladores de código abierto soportando
  numerosas librerías públicas que nos hacen la programación mucho más sencilla, existe una 
  cantidad ingente de librerías analíticas que han hecho de éste el lenguaje de facto
  para la programación en áreas de gran interés como Machine Learning, etc. 
  En este curso, a no ser que digamos lo contrario en algún ejemplo en particular, usaremos
  [Python 3.8](https://www.python.org/downloads/release/python-380/). 


- [Conda](): Conda es un sistema de administración de paquetes y entornos de desarrollo 
  disponible para los principales sistemas operativos (OS, de sus siglas en inglés): 
  
    - [Windows](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html)
      
    - [macOS](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html)
      
    - [Linux](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html) 
      
  Conda instala, ejecuta y actualiza rápidamente paquetes y sus dependencias de manera 
  sencilla y efectiva. Con la línea de comandos seremos capaces de crear, guardar, cargar
  y cambiar fácilmente entre entornos, lo que nos será muy útil para aislar entornos de 
  trabajo y conseguir robustez en nuestros desarrollos. 
  Inicialmente se creó para la gestión de programas Python, pero a día de hoy 
  puede empaquetar y distribuir software para cualquier lenguaje.
  

- [Jupyter](https://jupyter.org/): Un entorno web interactivo de desarrollo, ideal para 
  la exploración y el desarrollo de informes técnicos. Su interfaz flexible permite la configuración 
  y organización de flujos de trabajo para analítica avanzada, computación científica, 
  periodismo computacional y *Machine Learning*. 
  Las instrucciones para su instalación se pueden encontrar [aquí](https://jupyter.org/install).
  
## Python y Conda

En el apartado anterior hemos comentado que el lenguaje de programación usado en este curso
será Python, y hemos también hecho mención al gestor de entornos Conda (también se suele 
referir como Anaconda, aunque Conda es el administrador de paquetes mientras que Anaconda 
es un conjunto de alrededor de cien paquetes que incluye entre otros: conda, numpy, scipy,
ipython notebook, etc.) Procedamos a entender un poco mejor su interrelación y 
utilización mediante una serie de preguntas y respuestas:


- **¿Tengo que instalar python y conda?**: La respuesta rápida es que *NO*. Utilizaremos 
  Conda como gestor de entornos, y será Conda quien gestione la instalación y activación
  de la versión de python que necesitemos cuando procedamos a la creación de un entorno.
  
- **¿Qué tengo que hacer para instalar conda?**: Esto depende un poco del OS con el que estés
  trabajando como hemos comentado en el apartado anterior. En cualquier caso, a continuación 
  apuntamos los comandos a ejecutar por terminal en caso que prefiramos hacer una instalación
  programática:
  
  *Windows*:
  ```shell
  winget install -e --id Anaconda.Anaconda3
  ```
  
  *Linux*:
  ```shell
  wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh && \
  chmod a+x Anaconda3-2021.11-Linux-x86_64.sh && \
  ./Anaconda3-2021.11-Linux-x86_64.sh
  ```
  
  *macOS*:
  ```shell
  wget https://repo.anaconda.com/archive/Anaconda3-2021.11-MacOSX-x86_64.sh && \
  chmod a+x Anaconda3-2021.11-MacOSX-x86_64.sh && \
  ./Anaconda3-2021.11-MacOSX-x86_64.sh 
  ```