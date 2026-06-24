# Manual interno de Docker

## Crear una imagen Docker

Para crear una imagen Docker se debe preparar un archivo llamado `Dockerfile`
en la raiz del proyecto. El archivo define la imagen base, las dependencias,
los archivos que se copian y el comando de inicio.

Pasos recomendados:

1. Crear o revisar el `Dockerfile`.
2. Ejecutar `docker build -t nombre-aplicacion:version .` desde la carpeta del
   proyecto.
3. Verificar que la imagen exista con `docker images`.
4. Ejecutar un contenedor de prueba con `docker run --rm nombre-aplicacion:version`.

Si el build falla, se debe revisar el log de la capa que produjo el error y
confirmar que los archivos copiados existan en el contexto de construccion.

## Ejecutar contenedores

Un contenedor se puede iniciar con `docker run`. Para publicar un puerto se usa
`-p puerto_host:puerto_contenedor`. Para variables de entorno se usa `-e`.

Ejemplo:

```bash
docker run --rm -p 8080:80 -e APP_ENV=dev nombre-aplicacion:version
```

## Revisar logs de un contenedor

Los logs se revisan con `docker logs nombre_contenedor`. Para seguirlos en
tiempo real se agrega `-f`.

