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


### APIs: Tipos, autenticación, conexión y limitaciones

Para una discusión formal sobre la definición de API, referimos al siguiente [enlace](https://www.redhat.com/en/topics/api/what-are-application-programming-interfaces).
En esta sección vamos a ser bastante más prácticos, y por ello vamos a adoptar la definición
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

*REST* proviene de la definición inglesa: *Representational State Transfer*, una 
arquitectura de diseño de API que impone una política de mínimos en cuanto a 
acuerdo cliente-servidor, y es por ello por lo que se ha hecho tan popular, por
su flexibilidad. Estos mínimos que debe cumplir una API para considerarse 
RESTful son ([referencia](https://www.redhat.com/es/topics/api/what-are-application-programming-interfaces)):
 
- Arquitectura cliente-servidor, y administración de solicitudes con protocolo `HTTP`.

- Sistema sin estado (*Stateless*): la información sobre el estado de la sesión es responsabilidad del cliente

- Capacidad de almacenamiento en caché

- Sistema en capas: Las interacciones cliente-servidor pueden estar mediadas por capas adicionales. Estas capas pueden ofrecer funcionalidades adicionales, e.g. seguridad, balanceador de carga, o cachés compartidas.

- Código disponible según se solicite (opcional)
  
- Interfaz uniforme: Fundamental para el diseño, y requiere de:
    - Identificación de los recursos en las solicitudes, y separación de las representaciones devueltas al cliente
    - Gestión de recursos mediante representaciones
    - Respuestas autodescriptivas
    - Debe contener hipertexto o hipervínculos que permita al cliente conocer las acciones disponibles a posteriri de la respuesta

El incremento del uso de APIs ha hecho necesaria la definición de estándares
mínimos. A día de hoy, el estándar *de facto* que se ha propagado exponencialmente
en la comunidad es [**OpenAPI Specification**](https://swagger.io/specification/) 
(OAS) el cual define un estándar para el diseño de APIs tipo RESTful agnóstico al
lenguaje de programación. 