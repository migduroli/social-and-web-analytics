### Conexión a la API de Facebook

Para poder conectarnos a la API de Facebook, necesitaremos
registrarnos como desarrolladores en su página [web](https://developers.facebook.com/).
Una vez nos registremos, debemos seguir los pasos indicados
en la [web oficial](https://developers.facebook.com/docs/graph-api/get-started):

1. Crear una App - [link](https://developers.facebook.com/docs/development/create-an-app)
2. Abrir [Graph Explorer](https://developers.facebook.com/tools/explorer)
3. Generar el token de acceso
4. Consultar la API para entender el modelo de datos: [link](https://developers.facebook.com/docs/graph-api/overview#nodes)

Para la conexión con la API de Facebook vamos a usar la librería
de `Python` [facebook-sdk](https://facebook-sdk.readthedocs.io/en/latest/api.html#class-facebook-graphapi),
por lo que deberás instalar dicha librería en el entorno de desarrollo,
i.e., ejecutar `pip install facebook-sdk`.

Ahora que tienes preparado el entorno, puedes proceder a explorar el
script de conexión: [link](fb_api.py)
 