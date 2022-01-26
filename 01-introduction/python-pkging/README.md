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


### Metodología 