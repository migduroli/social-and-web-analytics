## Recopilación de información de redes sociales

El primer paso ineludible para poder cumplir con las expectativas planteadas en el
nombre de este curso, i.e. *analítica social y de la web*, es el de **colectar** (o recopilar)
la información (o **datos sociales**) de alguna o múltiples fuentes. 
En este curso vamos a ver que existen dos formas fundamentales de obtener datos de un 
*tercero* (como es el caso de grande plataformas sociales como [Twitter](https://twitter.com/), 
[Facebook](https://www.facebook.com), etc.): a través de API (*Application Programming
Interface*), lo cual nos dará acceso directo a los datos almacenados por el tercero
en cuestión; mediante técnicas de *Web Scrapping* como *HTML parsing* o *DOM parsing*, 
que consisten en recopilar información de forma automática de una web.

El uso de APIs para compartir (bien de forma privada o pública) datos relacionados con
la actividad específica del proveedor en cuestión ha supuesto una revolución tecnológica
en los últimos años de impacto incalculable. Esta forma sistemática de colección de datos
de diferentes plataformas ha dado lugar a la creación de miles de aplicaciones basadas
en el análisis de dichos datos que han cambiado y siguen transformando nuestro día a 
día. De hecho, y aunque las APIs no son nada nuevo, se han convertido en el canal estándar
para monetización de un activo de negocio muy preciado en la actualidad, el dato.
Gracias a las APIs muchas empresas tecnológicas han podido monetizar datos (directos
o derivados) generados en su actividad diaria como un subproducto, dando la posibilidad
de explotación a externos, creando esto a su vez la posibilidad de fundación de nuevos
productos.

En cuanto a las técnicas de web scrapping, éstas suelen ser la alternativa al uso de APIs,
bien sea por falta de presupuesto, o porque el proveedor de esos datos en cuestión no tiene
API. Es una de las vías favoritas de las *Startups* a la hora de conseguir datos baratos,
aunque es cierto que las grandes compañías tecnológicas cada vez ponen más difícil la posibilidad
de hacer web scrapping, precisamente porque tienen un modelo de negocio basado en APIs y,
por ende, buscan eliminar esta posibilidad (*free lunch*).

Con esta pequeña introducción en mente, en este capítulo vamos a ver:

- [APIs: Tipos, autenticación, conexión y limitaciones](#apis-tipos-autenticación-conexión-y-limitaciones-apis)
- [Análisis de las respuestas de APIs]()
- [Limpieza y almacenamiento]()
- [Medición, recopilación y análisis de los datos...]()


### APIs: Tipos, ventajas e inconvenientes, autenticación y conexión

Para una discusión formal sobre la definición de API, aconsejamos consultar el siguiente
[enlace](https://www.redhat.com/en/topics/api/what-are-application-programming-interfaces).
En este documento vamos a ser bastante más prácticos, y por ello vamos a adoptar la definición
práctica:

> *Una API es un medio de comunicación de información entre un servidor (el servicio) y el
cliente (usuario, desarrollador, u otro servicio)*.

Como podemos comprobar, la definición es bastante genérica, y es que una API no es un
protocolo sino un *medio* de comunicación, y por tanto cada API tiene su propia forma 
(*modelo*) de representar/exponer la información intercambiada. En el fondo, una API
se puede entender como un contrato entre el cliente y el servidor, donde el acuerdo 
establecido entre las partes suele estar recogido en forma de documentación técnica.
En el caso de redes sociales como Twitter, o Facebook, veremos que dicha documentación
es pública y tiene su propia web:

- Documentación API Twitter: [Twitter API](https://developer.twitter.com/en/docs/twitter-api) 
- Documentación API Facebook: [Graph API](https://developers.facebook.com/docs/graph-api/)

La diferente naturaleza de los datos subyacentes, así como del propio servicio, implica
de forma directa diferentes APIs, ya que cada una tiene su diseño (*diseño de software*)
para representar sus datos de la forma que más le conviene a cada proveedor.
A su vez, la información servida vía API raramente es apta para el análisis directamente, 
lo que normalmente requerirá un post-porcesado de la misma, y por ende su almacenamiento
para su posterior explotación. Todo ello hace que el proceso de recolección de datos
no sea todo lo generalizable como gustaría, además de convertir esta etapa en una
de las más tediosas, aunque también entretenida.

#### Tipos de APIs
En 2022, podemos decir que existen básicamente dos tipos de APIs:

- RESTful API (*estáticas*)
- Steaming API

##### RESTful APIs
REST proviene de la definición inglesa: *Representational State Transfer*, una 
arquitectura de diseño de API que impone una política de mínimos en cuanto a 
acuerdo cliente-servidor, y es por ello por lo que se ha hecho tan popular, por
su flexibilidad. Estos mínimos que debe cumplir una API para considerarse 
RESTful son ([referencia](https://www.redhat.com/es/topics/api/what-are-application-programming-interfaces)):
 
- Arquitectura cliente-servidor, y administración de solicitudes con protocolo `HTTP`.

- Sistema sin estado (*Stateless*): la información sobre el estado de la sesión es 
  responsabilidad del cliente

- Capacidad de almacenamiento en caché

- Sistema en capas: Las interacciones cliente-servidor pueden estar mediadas por capas
  adicionales. Estas capas pueden ofrecer funcionalidades adicionales, 
  e.g. seguridad, balanceador de carga, o cachés compartidas.

- Código disponible según se solicite (opcional)
  
- Interfaz uniforme: Fundamental para el diseño, y requiere de:
    - Identificación de los recursos en las solicitudes, y separación de las representaciones
      devueltas al cliente
    - Gestión de recursos mediante representaciones
    - Respuestas autodescriptivas
    - Debe contener hipertexto o hipervínculos que permita al cliente conocer las acciones 
      disponibles a posteriri de la respuesta

El incremento del uso de APIs ha hecho necesaria la definición de estándares
mínimos. A día de hoy, el estándar *de facto* que se ha propagado exponencialmente
en la comunidad es [**OpenAPI Specification**](https://swagger.io/specification/) 
(OAS) el cual define un estándar para el diseño de APIs tipo RESTful agnóstico al
lenguaje de programación.

##### Steaming APIs

Las APIs de *streaming* constituyen casi el opuesto de REST.
En esencia, una API de streaming invierte el orden de la comunicación con respecto
a REST. En lugar de tratarse de una comunicación iniciada por una petición de cliente,
que es respondida por el servidor, en *streaming* el servidor está continuamente (más 
específicamente, cada vez que hay una actualización subyacente) enviando información
al cliente. Por hacer un análogo práctico, mientras que REST se puede entender como una
conversación entre dos personas, en la que una pregunta y la otra responde, el Streaming
es algo más similar a comprar una entrada de cine y sentarse a ver la película (recibir 
información de manera pasiva). Se trata de una inversión total del paradigma REST.
Además, en streaming la API no es *stateless*, más bien al contrario, es una comunicación
*stateful*. ¿Qué significa esto en la práctica? Esto normalmente se materializa en forma 
de una conexión persistente con el servidor *streaming* en cuestión (cierto es que dichas 
conexiones suelen tener un *tiempo de vida* finito), y es durante esta conexión cuando el 
contenido es enviado desde el servidor al cliente.
Otra gran diferencia con respecto a REST que merece ser mencionada es que una API de streaming
es mucho menos flexible que una API REST.

<img src="_img/rest-vs-streaming.png" alt="REST vs Streaming" width="400"/>


#### Ventajas e inconvenientes de las APIs

La pregunta natural que puede surgir a estas alturas es: ¿Qué ventajas representa el uso 
de APIs en el contexto de la analítica social y de la web?

##### Ventajas de las APIs 

Entre otras muchas, podemos destacar las siguientes ventajas:

- Representan una forma *sencilla* de *extracción* de datos (desde el punto 
  de vista del cliente) en cualquier etapa del análisis, bien sea en *discovery*, en
  *desarrollo*, o en *producción*
- Permiten la *automatización* de las labores de extracción y enriquecimiento de datos,
  ya que están diseñadas para la comunicación entre máquinas
- Existe una gran variedad de APIs de las que podemos obtener distintas representaciones 
  de un mismo *objeto* (por ejemplo un perfil de Twitter), las cuales podemos conjugar 
  programáticamente para obtener una representación más completa (*Aditividad*)  

##### Inconvenientes de las APIs 

Por otra parte, las APIs no solo conllevan ventajas, sino que también tienen sus propios
inconvenientes. A continuación listamos algunos de los más notables, que han de ser 
considerados cuando se diseña una solución:

- *Limites* de consultas: Toda API que encontremos en el mercado va a tener un límite de 
  consultas (o *quota*) y/o velocidad de descarga. La explicación es bastante lógica,
  una compañía que expone sus datos vía APIs tiene que poner controles sobre los datos
  que entran/salen de su plataforma, así como evitar que un "consumidor" muy exigente ponga
  en peligro la plataforma por saturación. Cada API tendrá sus *quotas*, y por ello es 
  muy aconsejable tenerlas en cuenta a la hora de diseñar una estrategia de extracción
  de datos.
  
- *Refactorizaciones* de la API: Este representa uno de los *inconvenientes* a la hora de 
  desarrollar una aplicación de analítica que necesite del uso de APIs. Suele ocurrir, 
  más habitualmente de lo que gustaría al cliente, que la API con la que se comienza el 
  desarrollo de una herramienta no sea la misma unos meses después de iniciar el desarrollo.
  Esto se debe a razones muy variadas, desde cambios estratégicos en la compañía que 
  expone la API, o cambios de diseño para mejorar la experiencia de usuarios, etc. 
  En definitiva, esto suele conllevar que nuestro código también tenga que cambiar para
  adaptarse a los nuevos *endpoints*, o a los nuevos modelos de repuesta. Uno de los cambios
  más notados es el que se está sufriendo a día de hoy (`Enero de 2022`) en la API de 
  Twitter ([v1.1](https://developer.twitter.com/en/docs/twitter-api/v1) vs 
  [v2](https://developer.twitter.com/en/docs/twitter-api/data-dictionary/introduction)),
  la cual ha sido reformulada desde cero, no manteniendo compatibilidad en el modelo de
  datos con la versión anterior.
  
- *Legalidad*: Las normas establecidas para el uso de los datos obtenidos por cada API 
  pueden ser muy dispares. Además, dichas restricciones legales pueden cambiar a lo largo
  del tiempo. Es por ello que necesitamos ser conocedores (expertos) del marco legal
  en el que nos movemos en cada momento antes de proceder al uso de cualquier dato para 
  no incurrir en ninguna violación de los términos acordados.


#### Autenticación y conexión

A la hora de trabajar con APIs es inevitable que nos topemos con alguna forma de 
autenticación, mediante la cual el servidor nos reconocerá (o no) y permitirá la petición
y acceso de datos correspondientes. El conocimiento profundo de cada una de las posibles
técnicas de autenticación existentes va más allá del objetivo de este curso. Para 
aquellos que quieran tener un conocimiento más detallado de esquemas de autenticación
como:

- `Basic Auth`: [link](https://en.wikipedia.org/wiki/Basic_access_authentication)
- `API keys`: [link](https://en.wikipedia.org/wiki/Application_programming_interface_key)
- `Bearer Authentication`: [link](https://swagger.io/docs/specification/authentication/bearer-authentication/)
- `OAuth 1.0` o `OAuth 2.0`: [link](https://en.wikipedia.org/wiki/OAuth)
- `OpenID Connect Discovery (OIDCD)`: [link](https://openid.net/specs/openid-connect-discovery-1_0.html)
- `Cookie Authentication`: [link](https://en.wikipedia.org/wiki/HTTP_cookie)

Recomendamos consultar el siguiente [link](https://swagger.io/docs/specification/authentication/).
A continuación comentamos brevemente algunas de estos esquemas, de los cuales, los más 
usados en este curso serán `API keys`, `Bearer Authentication` y `Oauth`.

##### Basic Auth
`Basic Auth` es un esquema de autenticación simple integrado en el protocolo HTTP. 
El cliente envía solicitudes HTTP con el encabezado de autorización (`Authorization` header)
que contiene la palabra `Basic` seguida de un espacio y una cadena codificada en `base64`, 
`username:password`. Por ejemplo, para autenticarse como usuario `demo` y password
`p@55w0rd` el cliente tendrá que enviar el siguiente encabezado:
```shell
Authorization: Basic ZGVtbzpwQDU1dzByZA==
```
Para hacer una petición a un servidor con el *header* anterior, usando [cURL], procederíamos
como sigue:
```shell
> curl ${SERVER_URL}/sample-endpoint \
 --request GET \
 --header "Authorization: Basic ZGVtbzpwQDU1dzByZA==" \
 ${SERVER_URL}/sample-endpoint
```

##### API Keys

En otros casos, la autenticación ocurre mediante un *TOKEN* que es intercambiado con el 
servidor, bien mediante `query string`, es decir añadiéndose el *TOKEN* a la URL:
```shell
> curl --request GET ${SERVER_URL}/sample-endpoint?api_key=abcdef12345
```
o bien como header:
```shell
> curl ${SERVER_URL}/sample-endpoint \
  --request GET \
  --http1.1 \
  --header "X-API-Key: abcdef12345"
```
o bien como *cookie*:
```shell
> curl ${SERVER_URL}/sample-endpoint \
  --request GET \
  --http1.1 \
  --cookie "Cookie: X-API-KEY=abcdef12345"
```

##### Bearer Token

En el caso de autenticación por *token* al portador (*Bearer Token*)
se usan tokens de seguridad, normalmente generados por el servidor, que dan acceso a aquél
que "porte" dicho token. Así, este tipo de autenticación se puede entender
como "dar acceso al portador de un este token". 
El token al portador es una cadena de caracteres encriptada, 
generalmente generada por el servidor en respuesta a una solicitud de
inicio de sesión. El cliente debe enviar este token en el encabezado de
autenticación al realizar peticiones. Imaginemos que el servidor nos
ha facilitado el token `AbCdEf123456`, procederíamos de la siguiente
forma:

```shell
curl ${SERVER_URL}/sample-endpoint \
   --header "Accept: application/json"
   --header "Authorization: Bearer AbCdEf123456"
```

##### OAuth 1.0 y 2.0

OAuth (*Open Authorization*) es un protocolo estándar de autorización en el que
se le garantiza acceso limitado a los datos en servidor a un cliente API.
Es el mecanismo de autenticación preferido por grandes compañías tecnológicas
como Google, Amazon, Facebook, Microsoft o Twitter para permitir a los usuarios
de sus plataformas el compartir datos de sus cuentas con aplicaciones de terceros
u otras webs.

Para entender el flujo de OAuth, y su necesidad, podemos echar un vistazo a estas
dos imágenes de [wikipedia](https://en.wikipedia.org/wiki/OAuth):

- Situación hipotética en la que se comparte información de *login* del usuario con una 
  aplicación de un tercero para acceder a cierta información del usuario:
  
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Without-oauth.png/600px-Without-oauth.png" 
alt="3rd party authorization, security flaw" width="400"/>
  
  Evidentemente, esto supone un riesgo serio de ciberseguridad, que puede ser evitado
  mediante el uso de un flujo de autenticación OAuth (a continuación).
  
- Flujo de autenticación OAuth: Las credenciales del usuario se usan solo 
  en el servidor de autorización, y no en el cliente (por ejemplo, la aplicación de un 
  tercero):
  
  <img src="https://upload.wikimedia.org/wikipedia/commons/7/72/Abstract-flow.png" alt="Flujo OAuth" width="400"/>

Los diferentes flujos de OAuth v1.0 u v2.0 se puede encontrar en los siguientes enlaces:

- Flujo v1.0: [link](https://oauth.net/core/1.0/); [link2](https://albertomolina.wordpress.com/2013/05/11/utilizacion-paso-a-paso-de-oauth-1-0-en-twitter-con-python-bottle/)
- Flujo v2.0: [link](https://www.soapui.org/docs/oauth2/oauth2-overview/); [link2](https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps?hl=es)

Un ejemplo práctico de cómo este flujo de autenticación ocurre puede verse en este
[link](https://developers.google.com/identity/protocols/oauth2) sobre el uso de OAuth 2.0
para el acceso a las APIs de Google.


Finalmente, cabe mencionar que existen dos tipos básicos de autenticación con OAuth: 
autenticación tipo `user` (usuario), y tipo `app` (aplicación). En el primero de los casos,
es decir, tipo `user`, se garantiza al cliente de la API no solo para el uso de los datos
del usuario, sino para actuar en su nombre. En el segundo de los casos, la aplicación está 
autorizada a un uso limitado de la API, y a actuar en su propio nombre, nunca en el nombre
del usuario. 

En el escenario que nos concierne, lo más normal será usar `App Authentication` 
ya que estamos interesados en extraer datos, no en modificar el estado del usuario.
Como veremos en el caso de [Twitter](https://developer.twitter.com/), el procedimiento
habitual para poner en funcionamiento una autorización `OAuth` de este tipo requerirá
normalmente los siguientes pasos:

1. Crear una **cuenta de desarrollador** en la plataforma.
   
2. Crear una **aplicación** en la plataforma de desarrollador. Esta aplicación será a la 
   que autorizaremos para hacer consultas de nuestros datos mediante las APIs de la 
   plataforma.
   
3. **Generar** los **tokens** de acceso. Este paso requiere la salvaguarda de los tokens 
   en un lugar seguro. Normalmente guardaremos estas claves en un fichero tipo `JSON`.
   
4. [Opcional] **Autenticar** las peticiones HTTP. Algunas APIs requerirán que además 
   autoricemos las peticiones HTTP mediante una cabecera (típicamente `Bearer Token`).
   
5. [Opcional] **Seleccionar los permisos** correctos. Algunas APIs están desarrolladas con
   el concepto de permisos multicapa/multinivel. Si es así, nos solicitarán 
   determinar el ámbito (*scope*) de validez de la clave, donde ámbito/scope no es más que
   un conjunto de acciones. Esta granularidad de permisos permite controlar muy bien 
   cualquier fuga indeseada, ya que si la aplicación intentase acceder mediante a un método 
   que no está en el ámbito en el que está autorizada, se le rechazará la petición.
   
6. **Conectar** con la API con los credenciales obtenidos, una vez los pasos anteriores 
   han sido satisfactoriamente.
   
Antes de comenzar con los detalles de conexión con una API real (como por ejemplo la 
[API v2 de Twitter](https://developer.twitter.com/en/docs/twitter-api) 
que vamos a usar de forma extensiva en este curso), podemos ver primero como se utilizará
`OAuth` en la práctica cuando trabajemos con Python. Para ello, podemos comentar
el siguiente código:

```python
import requests

from requests_oauthlib import OAuth1

user_auth = OAuth1(
  client_key="YOUR_APP_KEY",
  client_secret="YOUR_APP_SECRET",
  resource_owner_key="USER_ACCESS_TOKEN",
  resource_owner_secret="USER_ACCESS_SECRET",
)

base_url = "http://the-api-url.com/"

response = requests.get(
  url=f"{base_url}/get",
  auth=user_auth,
)
```

En este ejemplo, hemos creado un objeto de autenticación tipo `OAuth1` utilizando
las claves de acceso obtenidas en la consola de desarrollador (donde hemos creado
la aplicación). Sólo entonces, podremos hacer peticiones a la API (cuya URL aquí
hemos dejado como un ejemplo genérico: `http://the-api-url.com/`) usando la librería
`requests` y los métodos estándares, `get`, `post`, `put`, `delete`, etc.
En particular, en el ejemplo anterior hemos hecho una llamada autorizada con `OAuth1`
de tipo `GET`.