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

<img src="_img/pipeline.png" alt="Pipeline" width="600"/>

### Planificación del proyecto

Como en cualquier otro proyecto de análisis, lo primero que tenemos que hacer es
determinar cuáles son las preguntas que queremos responder. Obviamente, la determinación
de estas preguntas no será algo estático, sino que será modificado iterativamente según
vayamos avanzando en cada una de las etapas del proyecto (metodología [*agile*](https://en.wikipedia.org/wiki/Agile_learning)).
En este proyecto vamos a intentar dar respuesta a las siguientes preguntas "tentativas":

- ¿Qué está publicando la marca seleccionada en Facebook y Twitter?
- ¿Cómo están reaccionando los seguidores de la marca a dichas publicaciones? (likes, shares, comentarios, retweets)
- ¿Qué se comenta sobre la marca en Facebook?
- ¿Qué emociones están surgiendo de las publicaciones?


#### Extracción de datos sociales

En este ejemplo en concreto vamos a explorar la marca `LouisVuitton`. El minado de
posts (Facebook) y Tweets (Twitter) lo vamos a hacer utilizando los siguientes scripts:

- [mine-facebook](social-miner/src/social_miner/facebook.py):

  ```python
    #!/usr/bin/env python
    import json
    import logging
    import sys
    
    import pymongo as pymdb
    import facebook_scraper as fb
    
    logging.basicConfig(level=logging.INFO)
    
    
    default_config = {
        "cookies_path": "COOKIES_FILE_PATH.json",
        "extract_options": {
            "comments": True,
            "allow_extra_requests": True,
            "progress": True,
            "reactors": True
        },
        "db_params": {
            "host": "localhost:27017",
            "collection": "scraping",
        },
        "max_pages": 100_000,
    }
    
    
    class FBScraper:
    
        @staticmethod
        def read_json_file(file):
            with open(file, "r") as input_file:
                return json.load(input_file)
    
        def _read_cookies(self):
            return self.read_json_file(file=self.cookies_path)
    
        def _set_cookies(self):
            self.fb.set_cookies(self.cookies)
    
        def _initialise_mongo(self):
            self.db_client = pymdb.MongoClient(self.db_params["host"])
            self.collection = self.db_client[self.db_params["collection"]]
    
        def _write_post_db(self, post: dict, database: str):
            post_id = post.pop("post_id")
            record = {**post, "_id": post_id}
            self.database = self.collection[database]
            try:
                self.database.insert_one(record)
                logging.info(f"Post inserted: {post_id}")
            except pymdb.errors.DuplicateKeyError:
                logging.info(f"{post_id} is already in our DB: Updating record")
                self.database.update_one(
                    {"_id": post_id},
                    {"$set": record}
                )
    
        def __init__(
                self,
                extract_options: dict,
                db_params: dict,
                max_pages: int = None,
                cookies_path: str = None,
        ):
            self.fb = fb
    
            if cookies_path:
                self.cookies_path = cookies_path
                self.cookies = self._read_cookies()
                self._set_cookies()
    
            self.options = extract_options
            self.max_pages = max_pages
    
            self.db_params = db_params
            self._initialise_mongo()
    
        def mine_posts(self, account):
            posts_iterator = self.fb.get_posts(
                account=account,
                options=self.options,
                extra_info=True,
                pages=self.max_pages
            )
    
            posts = []
            for post in posts_iterator:
                self._write_post_db(post, database=account)
                posts += [post]
    
            return posts
    
        def read_posts(self, account, limit=100):
            collection = self.collection[account]
            cursor = collection.find({})
            if limit:
                cursor = cursor.limit(limit)
    
            posts = []
            for document in cursor:
                posts += [document]
    
            return posts
    
    
    def mine_posts(account: str, config=None):
        if config is None:
            config = default_config
    
        my_scraper = FBScraper(**config)
        my_scraper.mine_posts(account=account)
    
    
    def read_posts(account: str, config=None, limit=100):
        if config is None:
            config = default_config
    
        fb = FBScraper(**config)
        return fb.read_posts(account=account, limit=limit)
    
    
    if __name__ == "__main__":
        brand = sys.argv[1]
        mine_posts(account=brand)
    ```

  Para ejecutar el script, sólo tenemos que cambiar el permiso del fichero (`chmod a+x fb_mining.py`)
  y ejecutar la siguiente línea de comando:
    ```shell
    > ./facebook.py BRAND_PAGE_NAME
    ```
  Donde `BRAND_PAGE_NAME` será el nombre de la página de la marca que queramos minar,
  por ejemplo: `Google`.
  

- [mine-tweets](social-miner/src/social_miner/twitter.py):
  ```python
    #!/usr/bin/env python
    
    import json
    import logging
    import pymongo as pymdb
    import tweepy
    import sys
    
    from enum import Enum
    
    logging.basicConfig(level=logging.INFO)
    
    
    class APIScraper:
    
        @staticmethod
        def read_json_file(file):
            with open(file, "r") as input_file:
                return json.load(input_file)
    
        def _read_credentials(self):
            return self.read_json_file(file=self.credentials_file)
    
        def _initialise_mongo(self):
            self.db_client = pymdb.MongoClient(self.db_params["host"])
            self.collection = self.db_client[self.db_params["collection"]]
    
        def _initialise_api_client(self):
            pass
    
        def _initialise_api(self):
            self._initialise_api_client()
    
        def _save_post(self, post_id: str, post: dict, database: str):
            record = {**post, "_id": post_id}
            self.database = self.collection[database]
            try:
                self.database.insert_one(record)
                logging.info(f"Post inserted: {self.collection.name}:{database}.{post_id}")
            except pymdb.errors.DuplicateKeyError:
                logging.info(f"{self.collection.name}:{database}.{post_id} is already in our DB: Updating record")
                self.database.update_one(
                    {"_id": post_id},
                    {"$set": record}
                )
    
        def __init__(
                self,
                credentials_path: str,
                db_params: dict,
                max_pages: int = None,
                max_items: int = None,
                extract_options: dict = None,
        ):
            self.credentials_file = credentials_path
            self.credentials = self._read_credentials()
    
            self.api = None
            self._initialise_api()
    
            self.options = extract_options
            self.max_pages = max_pages
            self.max_results = max_items
    
            self.db_params = db_params
            self._initialise_mongo()
    
    
    class TwitterVersion(Enum):
        V1 = 1
        V2 = 2
    
    
    class TwitterScraper(APIScraper):
    
        API_VERSION_ERROR_MSG = "The version specified {version} is not yet available..."
        DEFAULT_TWEET_FIELDS = [
            "id", "text", "created_at", "public_metrics", "referenced_tweets",
        ]
    
        def _initialise_api_client(self):
            auth = tweepy.OAuthHandler(
                self.credentials["CONSUMER_KEY"],
                self.credentials["CONSUMER_SECRET"]
            )
            auth.set_access_token(
                self.credentials["ACCESS_TOKEN"],
                self.credentials["ACCESS_SECRET"],
            )
    
            if self.api_version == TwitterVersion.V1:
                self.api = tweepy.API(
                    auth=auth,
                    wait_on_rate_limit=True,
                )
    
            elif self.api_version == TwitterVersion.V2:
                credentials = self.credentials
                self.api = tweepy.Client(
                    bearer_token=credentials["BEARER_TOKEN"],
                    consumer_key=credentials["CONSUMER_KEY"],
                    consumer_secret=credentials["CONSUMER_SECRET"],
                    access_token=credentials["ACCESS_TOKEN"],
                    access_token_secret=credentials["ACCESS_SECRET"],
                    wait_on_rate_limit=True,
                )
    
            else:
                raise NotImplementedError(
                    self.API_VERSION_ERROR_MSG.format(version=self.api_version)
                )
    
        def _get_iterator(self, func, kwargs):
    
            if self.api_version == TwitterVersion.V2:
                return tweepy.Paginator(
                    func,
                    **kwargs,
                    max_results=self.max_results
                ).flatten(limit=self.max_results)
    
            elif self.api_version == TwitterVersion.V1:
                return tweepy.Cursor(
                    func,
                    **kwargs,
                    count=self.max_results
                ).pages(self.max_pages)
    
            else:
                raise NotImplementedError(
                    self.API_VERSION_ERROR_MSG.format(version=self.api_version)
                )
    
        def _get_user_tweets(self, user_name=None, user_id=None, **kwargs):
            if not user_id:
                user = self.api.get_user(
                    username=user_name,
                    user_fields=["id", "public_metrics"]
                ).data
                user_id = user.id
    
            iterator = tweepy.Paginator(
                self.api.get_users_tweets,
                id=user_id,
                **kwargs,
            ).flatten(limit=self.max_results)
    
            return user, iterator
    
        def mine_user_tweets(self, user_name=None, user_id=None, **kwargs):
            if "tweet_fields" not in kwargs.keys():
                kwargs["tweet_fields"] = self.tweet_fields
    
            tweets = []
            user, tweets_iterator = self._get_user_tweets(
                user_name=user_name,
                user_id=user_id,
                **kwargs
            )
    
            for t in tweets_iterator:
                ret_objs = self.api.get_retweeters(
                    id=t.id,
                    user_fields=[
                        "id",
                        "name",
                        "username",
                        "description",
                        "entities",
                        "verified",
                        "public_metrics",
                    ]
                ).data
                try:
                    retweeters = [dict(rt) for rt in ret_objs]
                except:
                    retweeters = []
    
                record = dict(t)
                record = {
                    **record,
                    "user_metrics": user.public_metrics,
                    "retweeters": retweeters
                }
                self._save_post(
                    post_id=t.id,
                    post=record,
                    database=user_name
                )
                tweets.append(t)
            return tweets
    
        def __init__(
                self,
                credentials_path: str,
                db_params: dict,
                api_version: TwitterVersion = TwitterVersion.V2,
                max_pages: int = None,
                max_items: int = None,
                extract_options: dict = None,
                tweet_fields=None
        ):
            if tweet_fields is None:
                tweet_fields = TwitterScraper.DEFAULT_TWEET_FIELDS
    
            self.api_version = api_version
            if self.api_version == TwitterVersion.V1:
                logging.warning(self.API_VERSION_ERROR_MSG)
    
            super().__init__(
                credentials_path,
                db_params,
                max_pages,
                max_items,
                extract_options,
            )
    
            self.tweet_fields = tweet_fields
    
    
    if __name__ == "__main__":
        brand = sys.argv[1]
    
        tw = TwitterScraper(
            credentials_path="auth/private/twitter_credentials.json",
            db_params={
                "host": "localhost:27017",
                "collection": "twitter",
            },
            api_version=TwitterVersion.V2,
            max_items=100_000,
        )
    
        tw.mine_user_tweets(user_name=brand)
  ```
  
  Para ejecutar el script, solo tenemos que cambiar el permiso del fichero (`chmod a+x twitter_mining.py`)
  y ejecutar la siguiente línea de comando:
  ```shell
    > ./twitter.py BRAND_USERNAME
  ```
  Donde `BRAND_USERNAME` será el nombre de la cuenta de Twitter de la marca que queramos minar,
  por ejemplo: `Google`.

‼️ **Nota**: Para que los scripts anteriores funcionen correctamente, deberemos tener 
MongoDB corriendo en nuestro sistema. Para ello recomendamos ejecutar:
```shell
> docker run --name mongodb -d -p 27017:27017 -v LOCAL_PATH_TO_BIND:/data/db mongo
```
Este comando de docker lanzará una imagen de docker de MongoDB que guardará los datos en 
el nuestro directorio local `LOCAL_PATH_TO_BIND` (sustituir con la dirección que nostros
queramos).


El proceso de extracción que se realiza mediante los scripts anteriores consiste en:

- Descargar todos los *posts* que nos permita Facebook de la marca

- Descargar todos los metadatos que nos permita Facebook de estos posts

- Descargar todos los comentarios que nos permita Facebook de estos posts

- Descargar todos los tweets que nos permita la API de Twitter de la marca

- Descargar todos los metadatos que nos permita la API de Twitter de esos tweets

- Descargar todos los datos referentes a los *retweeterers* que nos permita la API de Twitter


Las descargas enunciadas son inmediatamente guardadas en una colección en MongoDB con el 
nombre de la marca. De esta forma, la etapa de procesado y extracción de información puede
ocurrir sin necesidad de conectarnos a la API nuevamente, ya que tenemos los datos en local.

‼️ **Nota 2**: En las prácticas de clase, se han colectado los datos referentes a la marca
*Louis Vuitton*. Los datos colectados han sido compartido a través del grupo de la asignatura
como `data.zip`, que representa la carpeta generada por MongoDB. Para poder trabajar con
esos datos lo único que tienes que hacer es descargar el fichero *.zip*, descomprimirlo en 
el directorio que creas oportuno en tu sistema operativo, y ejecutes:
```shell
> docker run --name mongodb -d -p 27017:27017 -v UNZIP_FILE_PATH:/data/db mongo
```

#### Procesado (*Feature Extraction*)

Una vez hemos descargado los datos que consideramos oportunos a nuestra base de datos, 
procederemos a su procesamiento para extraer la información fundamental que nos permitirá
responder a las cuestiones planteadas anteriormente. En esencia, los pasos que vamos
a seguir son los siguientes:

<img src="_img/pipeline.png" alt="Pipeline" width="600"/>


- Obtener los #hashtags del texto crudo obtenido desde la API/Web: [get_hashtags](social-miner/src/social_miner/pipeline.py):
  ```python
  import re
  def get_hashtags(text: str):
    hashtags = list(set(re.findall(
        pattern=r"#(\w+)",
        string=text
    )))
    return hashtags
  ```
