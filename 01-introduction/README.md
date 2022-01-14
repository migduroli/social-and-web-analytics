## Introducción

En este módulo vamos a dedicarnos a preparar nuestro entorno de desarrollo,
que va a requerir de los siguientes componentes:

- [Python](): Será nuestro lenguaje de programación. Las ventajas de este lenguaje de
  programación son innumerables, e.g. permite escribir código conciso y fácilmente
  inteligible, hay una comunidad ingente de desarrolladores de código abierto soportando
  numerosas librerías públicas que nos hacen la programación mucho más sencilla, existe una
  cantidad ingente de librerías analíticas que han hecho de este el lenguaje de facto
  para la programación en áreas de gran interés como Machine Learning, etc. En este curso,
  a no ser que digamos lo contrario en algún ejemplo en particular, usaremos
  [Python 3.8](https://www.python.org/downloads/release/python-380/).


- [Conda](): Conda es un sistema de administración de paquetes y entornos de desarrollo
  disponible para los principales sistemas operativos (OS, de sus siglas en inglés):

    - [Windows](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html)

    - [macOS](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html)

    - [Linux](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html)

  Conda instala, ejecuta y actualiza rápidamente paquetes y sus dependencias de manera
  sencilla y efectiva. Con la línea de comandos seremos capaces de crear, guardar, cargar
  y cambiar fácilmente entre entornos, lo que nos será muy útil para aislar entornos de
  trabajo y conseguir robustez en nuestros desarrollos. Inicialmente se creó para la
  gestión de programas Python, pero a día de hoy puede empaquetar y distribuir software
  para cualquier lenguaje.


- [Jupyter](https://jupyter.org/): Un entorno web interactivo de desarrollo, ideal para
  la exploración y el desarrollo de informes técnicos. Su interfaz flexible permite la configuración
  y organización de flujos de trabajo para analítica avanzada, computación científica,
  periodismo computacional y *Machine Learning*. Las instrucciones para su instalación
  se pueden encontrar [aquí](https://jupyter.org/install).

## Python y Conda

En el apartado anterior hemos comentado que el lenguaje de programación usado en este curso
será Python, y hemos también hecho mención al gestor de entornos Conda (también se suele
referir como Anaconda, aunque Conda es el administrador de paquetes mientras que Anaconda
es un conjunto de alrededor de cien paquetes que incluye entre otros: conda, numpy, scipy,
ipython notebook, etc.) Procedamos a entender un poco mejor su interrelación y
utilización mediante una serie de preguntas y respuestas:


### ¿Tengo que instalar python y conda?

La respuesta rápida es que *NO*. Utilizaremos
Conda como gestor de entornos, y será Conda quien gestione la instalación y activación
de la versión de python que necesitemos cuando procedamos a la creación de un entorno.

### ¿Qué tengo que hacer para instalar conda?
Esto depende un poco del OS con el que estés
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

### ¿Cómo sé si se ha instalado bien?
Si has ejecutado estos comandos y has ido guiando la instalación de conda en tu terminal, 
al finalizar tendrás que reiniciar tu terminal para asegurarte que la dirección de conda 
está cargada en el PATH. Cuando lo hayas hecho, deberías poder ejecutar el siguiente
comando:
```shell
> conda --version
conda 4.8.2
```

### Gestión de entornos con conda

Una vez hemos comprobado que podemos usar la línea de comandos recien instalada, vamos a 
proceder a la creación de nuestro primer entorno Python. En particular, vamos a crear un
entorno con el nombre `swa-dev` (inspirados por las iniciales del curso, y añadiendod `dev`
para remarcar que estamos en la etapa de desarrollo), con `Python 3.8`:

```shell
conda create --name swa-dev python=3.8 --yes
```

El parámetro adicional `--yes` lo hemos añadido para pasarlo directamente a la pregunta:

```shell
The following NEW packages will be INSTALLED:

  ca-certificates    pkgs/main/osx-64::ca-certificates-2021.10.26-hecd8cb5_2
  certifi            pkgs/main/osx-64::certifi-2021.10.8-py38hecd8cb5_2
  libcxx             pkgs/main/osx-64::libcxx-12.0.0-h2f01273_0
  libffi             pkgs/main/osx-64::libffi-3.3-hb1e8313_2
  ncurses            pkgs/main/osx-64::ncurses-6.3-hca72f7f_2
  openssl            pkgs/main/osx-64::openssl-1.1.1m-hca72f7f_0
  pip                pkgs/main/osx-64::pip-21.2.4-py38hecd8cb5_0
  python             pkgs/main/osx-64::python-3.8.12-h88f2d9e_0
  readline           pkgs/main/osx-64::readline-8.1.2-hca72f7f_1
  setuptools         pkgs/main/osx-64::setuptools-58.0.4-py38hecd8cb5_0
  sqlite             pkgs/main/osx-64::sqlite-3.37.0-h707629a_0
  tk                 pkgs/main/osx-64::tk-8.6.11-h7bc2e8c_0
  wheel              pkgs/main/noarch::wheel-0.37.1-pyhd3eb1b0_0
  xz                 pkgs/main/osx-64::xz-5.2.5-h1de35cc_0
  zlib               pkgs/main/osx-64::zlib-1.2.11-h4dc903c_4
```

en la que se nos informa (pausando la creación del entorno hasta que se de autorización)
de los diferentes paquetes que serán instalados en la creación de nuestro nuevo entorno
llamado `swa-dev`.

Una vez terminada la creación, deberemos haber obtenido un mensaje como el que sigue:
```shell
# To activate this environment, use
#
#     $ conda activate swa-dev
#
# To deactivate an active environment, use
#
#     $ conda deactivate
```
que nos informa de los dos comandos que tendremos que usar para la activación y desactivación
del entorno. Si queremos saber que entornos tenemos creados ahora mismo en nuestro sistema,
podemos usar el siguiente comando:
```shell
conda env list

# conda environments:
#
base                  *  /YOUR_USER_PATH/anaconda3
swa-dev                  /YOUR_USER_PATH/anaconda3/envs/swa-dev
```
El símbolo `*` denota que tenemos activado el entorno por defecto (`base`). Para comenzar
con nuestro curso, vamos a proceder a la activación del entorno:
```shell 
conda activate swa-dev && conda env list
 
# conda environments:
#
base                     /YOUR_USER_PATH/anaconda3
swa-dev               *  /YOUR_USER_PATH/anaconda3/envs/swa-dev
```




