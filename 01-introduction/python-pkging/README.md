## Convirtiendo nuestro código en una librería de Python

Uno de los inconvenientes de guardar todo nuestro trabajo en un 
*Jupyter Notebook* es la imposibilidad de reutilizar código, salvo por la
posibilidad de "copiar y pegar" bloques enteros de código. Ésto, por supuesto,
no es una buena práctica (de hecho se denomina *duplicidad de código*) y
puede conllevar una gran multitud de problemas adicionales, e.g. ¿Qué versión
del código modificamos si nos damos cuenta que tiene un error, o comportamiento
no deseado? Esto nos puede llevar a la pregunta, ¿Entonces, escribir código en 
Notebooks es una mala práctica? La respuesta es que **NO**. Ni mucho menos, 
y en esta pequeña sección vamos a ver cómo convertir el código generado en 
un `.ipynb` en una librería de Python, que podremos usar como si de `Pandas` o
`Numpy` se tratara, i.e. usando:

```python
from mi_libreria import mi_funcion
saludo = mi_funcion(nombre="Miguel")
```

Donde, `mi_libreria` será el nombre que nosotros deseemos que tenga nuestro
módulo (módulo y librería se usarán como sinónimos), y `mi_funcion` sería una función dentro de dicha libreria. 
Y, ¿Por qué es esto útil, y cómo? En primer lugar será muy útil porque, mientras
podemos explorar y seguir desarrollando en Jupyter, aquellas funcionalidades
que ya hayamos comprobado que funcionan acorde a nuestras expectativas correctamente
podremos moverlas al **repositorio**, que podremos instalar en nuestro entorno
virtual, con `pip install -e .`, y seguir trabajando en nuestro Notebook simplemente
haciendo *imports* desde nuestro módulo.

Como no hay nada mejor que un ejemplo para entender el funcionamiento, a continuación
mostramos como empezar a crear nuestra librería con nombre `swa` (los nombres de 
las librerías/módulos suelen ser en minúsculas, separados por `-` en caso que fueran
nombres compuestos, según convenio [PEP423](https://www.python.org/dev/peps/pep-0423/).


### Objetivo y planteamiento

**Objetivo**: Queremos colectar datos meteorológicos de una 
lista de ciudades mediante un programa de `Python`. 

**Planteamiento**: Para ello podemos usar la información ofrecida en la web
[wttr.in](https://wttr.in/:help), usando las librerías nativas del lenguaje, en particular
`requests`. Sabiendo esto, para cada ciudad tendremos que hacer algo como:
```python
import requests

data = {}

response = requests.get(url="https://wttr.in/madrid")
if response.status_code == requests.status_codes.codes.ALL_GOOD:
    data["madrid"] = response.text
else:
    print(f"Error colectando datos, status_code = {response.status_code}")

```
Ahora, si quisiéramos hacer lo mismo para varias ciudades, tendríamos que proceder
con un `for-loop` adecuadamente. ¿Qué ocurre si en cualquier momento posterior
queremos hacer más consultas a esta web? tendremos que volver a escribir el bloque 
anterior y ejecutarlo. Vamos a encapsular la funcionalidad en una función por
tanto, lo que nos hará más sencilla su utilización a posteriori en el mismo 
documento:

```python
import requests

WEATHER_URL = "https://wttr.in/"


def get_weather_conditions(city_name: str) -> dict:
    """Gets the weather conditions via https://wttr.in
    
    :param city_name: Name of the city
    
    :return: dict {city_name: response.text}
    """
    url = WEATHER_URL if not city_name else f"{WEATHER_URL}/{city_name}"
    response = requests.get(url)
    data = {}
    
    if response.status_code == requests.status_codes.codes.ALL_GOOD:
        # Cambiamos la firma de @igor_chibi: 
        signature = "Follow \x1b[46m\x1b[30m@igor_chubin\x1b[0m for wttr.in updates"
        color_open = "\x1b[46m\x1b[30m"
        color_close = "\x1b[0m"
        text = response.text.replace(
            signature,
            f"This is {color_open}Social and Web Analytics{color_close} in live!"
        )
        data[city_name] = text
    else:
        print(f"Error colectando datos, status_code = {response.status_code}")
        data[city_name] = None
    return data
```

Así, el bloque de nuestro Jupyter notebook podría ser algo como:
```python
data = {}
city_names = ["madrid", "paris", "rome", "nocitywiththisname"]
for city in city_names:
    result = get_weather_conditions(city_name=city)
    data = {**data, **result}
```
lo cual produce el resultado deseado (y esperado):
```json
{
  "madrid": "Weather report: madrid\\n\\n...",
  "paris": "Weather report: paris\\n\\n...", 
  "rome": "Weather report: rome\\n\\n...",
  "nocitywiththisname": null
}
```
El problema que queremos resolver ahora es, ¿Cómo podemos hacer para que esta 
función (así como otras que podamos generar a posteriori para análisis de datos 
meteorológicos) pueda ser utilizada en otro Jupyter, o incluso por otros desarrolladores?


### Creando nuestra librería

En primer lugar, vamos a generar una carpeta que será la que contenga el código
de nuestra librería. Dicha carpeta puede localizarse donde queramos en nuestro
sistema (de hecho, si queremos podríamos tenerla sincronizada en nuestro [GitHub](https://github.com/)).
En este ejemplo vamos a asumir que nos encontramos en `Desktop`, y creamos la 
carpeta con nombre `swa`:
```shell
> mkdir swa
```

A continuación, copiamos el contenido de la carpeta [swa_pkg](swa_pkg) que tenemos
en este repositorio dentro de nuestra carpeta local.

Comentemos brevemente los directorios y ficheros que hemos copiado:

* [src](swa_pkg/src): Aquí es donde guardaremos todo el código que vayamos a querer
  empaquetar en la librería `swa`. Dentro de `src`, veremos que tenemos una única
  carpeta, que se llama como la librería que estamos creando, y no habrá ningún 
  otro contenido. En teoría se podría evitar este doble encapsulamiento de `swa` 
  (simplemente evitando la carpeta `src` teniendo directamente `swa` en la raíz del
  directorio creado), pero esto resulta en muchas ocasiones en el enmascarado de 
  errores de resolución de dirección de la librería, por lo que no recomendamos 
  evitarlo. Dentro de [src/swa](swa_pkg/src/swa) podemos tener tantas carpetas y 
  ficheros como queramos, éste es nuestro repositorio de código.

* [examples](swa_pkg/examples): Se suele crear una carpeta con ejemplos de utilización,
  aunque no es obligatorio. En nuestro caso podemos encontrar un ejemplo que importa y 
  usa las funciones implementadas en [src/swa/core.py](swa_pkg/src/swa/core.py) y 
  [src/swa/utils/weather.py](swa_pkg/src/swa/utils/weather.py).
  
* [setup.py](swa_pkg/setup.py) y [setup.cfg](swa_pkg/setup.cfg): Estos son los ficheros
  encargados de llevar a cabo la instalación del paquete [swa](swa_pkg/src/swa) (es decir,
  de todo el contenido de la carpeta [src/swa](swa_pkg/src/swa)), así como de las dependencias
  que especifiquemos como necesarias en [setup.cfg](swa_pkg/setup.cfg).
  

Una inspección un poco más detallada de [setup.cfg](swa_pkg/setup.cfg):
```ini
[metadata]
name = swa
description = Social and Web Analytics
version = 1.0.0
author = Miguel Duran

[options]
package_dir=
    =src
packages = find:
zip_safe = False
python_requires = >3.7
install_requires =
    requests
    pandas
    numpy

include_package_data = True

[options.packages.find]
where = src

[options.entry_points]
console_scripts =
    hello-world = swa.core:salute
    my-weather = swa.core:my_weather
```

Primero, hemos de saber que esto es lo que se conoce como un fichero de configuración.
Los ficheros de configuración se dividen en secciones (o bloques) que se denotan
como `[bloque]`. Cuando dichos ficheros se leen desde `Python` (ver este [link](https://docs.python.org/3/library/configparser.html)
para saber más sobre ello), las propiedades que se encuentran anidadas en cada bloque se
acceden como si un diccionario se tratase, e.g. si abrimos una terminal en la carpeta
y ejecutamos el siguiente código:
```python
from configparser import ConfigParser

config = ConfigParser()
config.read("setup.cfg")

name = config["metadata"]["name"]
print(name)
```
obtendremos `swa`. Esto nos puede ayudar a entender un poco mejor lo que está ocurriendo 
cuando `setup.py` se ejecuta a la hora de hacer `pip install -e .`. 
En cualquier caso, la sección de `metadata` nos da información genérica sobre
la librería, que podemos recuperar cuando lo tengamos instalado como librería
de la misma forma que con cualquier otra librería:
```python
from importlib import metadata
m = metadata.metadata("swa")
print(m)
```
que resultaría:
```shell

Metadata-Version: 2.1
Name: swa
Version: 1.0.0
Summary: Social and Web Analytics
Home-page: UNKNOWN
Author: Miguel Duran
License: UNKNOWN
Platform: UNKNOWN
Requires-Python: >3.7
```
Si nos fijamos, en la sección `[option]` tenemos especificada la lista de dependencias que
queremos que estén instaladas cuando instalemos nuestra librería. Esto resulta muy conveniente
para establecer cuál es el entorno necesario para que nuestra librería funcione.
De este modo, cuando hagamos `pip install -e .`, esto no solo copiará nuestro código donde
debe, sino que `pip` se garantizará de instalar `requests`, `pandas`, y `numpy` en este
caso en concreto. 

Por último, la sección `[options.entry_points]` nos será muy útil, pues especifica 
*aliases* que podemos ejecutar directamente desde la terminal para llamar a una función 
específica de nuestra librería. Así, una vez haya terminado la instalación con `pip install -e .`
podremos esrcibir directamente en el terminal:

```shell
> my-weather

Weather report: madrid

     \  /       Partly cloudy
   _ /"".-.     +6(3) °C
     \_(   ).   ↙ 6 km/h
     /(___(__)  10 km
                0.0 mm
```

### Instalación de nuestra librería

Una vez hemos copiado el contenido de [swa_pkg](swa_pkg) en nuestra carpeta local, 
como hemos comentado en la sección anterior, podemos directamente proceder a la instalación
de la librería. Dado que asumimos que vamos a estar modificando la librería en *vivo*, y
queremos que estos cambios estén disponibles directamente en nuestro entorno de python
sin tener que ejecutar de nuevo `pip install .`, añadiremos la opción `-e` o `--editable`
(o modo editable, [docu](https://pip.pypa.io/en/latest/cli/pip_install/)). Al ejecutar
el comando, deberíamos obtener algo similar a lo siguiente:

```shell
> pip install -e .

Obtaining file:///Users/YOUR_USERNAME/Documents/Root/Dev/github/social-and-web-analytics/01-introduction/python-pkging/swa_pkg
Requirement already satisfied: requests in /Users/YOUR_USERNAME/anaconda3/envs/swa-dev/lib/python3.8/site-packages (from swa==1.0.0) (2.27.1)
Requirement already satisfied: pandas in /Users/YOUR_USERNAME/anaconda3/envs/swa-dev/lib/python3.8/site-packages (from swa==1.0.0) (1.3.5)
Requirement already satisfied: numpy in /Users/YOUR_USERNAME/anaconda3/envs/swa-dev/lib/python3.8/site-packages (from swa==1.0.0) (1.22.0)
Requirement already satisfied: pytz>=2017.3 in /Users/YOUR_USERNAME/anaconda3/envs/swa-dev/lib/python3.8/site-packages (from pandas->swa==1.0.0) (2021.3)
Requirement already satisfied: python-dateutil>=2.7.3 in /Users/YOUR_USERNAME/anaconda3/envs/swa-dev/lib/python3.8/site-packages (from pandas->swa==1.0.0) (2.8.2)
Requirement already satisfied: six>=1.5 in /Users/YOUR_USERNAME/anaconda3/envs/swa-dev/lib/python3.8/site-packages (from python-dateutil>=2.7.3->pandas->swa==1.0.0) (1.16.0)
Requirement already satisfied: certifi>=2017.4.17 in /Users/YOUR_USERNAME/anaconda3/envs/swa-dev/lib/python3.8/site-packages (from requests->swa==1.0.0) (2021.10.8)
Requirement already satisfied: urllib3<1.27,>=1.21.1 in /Users/YOUR_USERNAME/anaconda3/envs/swa-dev/lib/python3.8/site-packages (from requests->swa==1.0.0) (1.26.8)
Requirement already satisfied: idna<4,>=2.5 in /Users/YOUR_USERNAME/anaconda3/envs/swa-dev/lib/python3.8/site-packages (from requests->swa==1.0.0) (3.3)
Requirement already satisfied: charset-normalizer~=2.0.0 in /Users/YOUR_USERNAME/anaconda3/envs/swa-dev/lib/python3.8/site-packages (from requests->swa==1.0.0) (2.0.10)
Installing collected packages: swa
  Running setup.py develop for swa
Successfully installed swa-1.0.0
```