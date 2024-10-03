# Proyecto de Scraping Qualifinds

Kevin Portugal

Este repositorio contiene soluciones a dos problemas de scraping. A continuación se describen las carpetas y cómo ejecutar cada problema.

## Estructura de Carpetas

- **Carpeta 1**:
  - Es necesario instalar la biblioteca `requests`. Puedes hacerlo con el siguiente comando:
    ```bash
    pip install requests
    ```
  - Para ejecutarlo, simplemente navega a la carpeta y ejecuta:
    ```bash
    python3 main.py
    ```
- **Carpeta 2**:

  - Es necesario instalar los paquetes necesarios, que están listados en el archivo `requirements.txt`.  
    Instálalos con:
    ```bash
    pip install -r requirements.txt
    ```
  - Para ejecutar el servicio localmente, puedes usar FastAPI de la siguiente manera:
    ```bash
    fastapi dev main.py
    ```
  - Alternativamente, puedes ejecutar:

    ```bash
    uvicorn main:app --reload
    ```

    ## Documentación

    La aplicación FastAPI expone una ruta de documentación en [/docs](http://127.0.0.1:8000/docs), donde podrás encontrar el endpoint que puedes probar.
    En este caso el endpoint de scraping es un POST llamado Scrape Jumbo.

    ## Docker

    Para ejecutar el proyecto en Docker, asegúrate de construir la imagen con el siguiente comando:

    ```bash
    docker build --platform linux/amd64 -t <NAME> .
    ```

    Es importante especificar la opción --platform linux/amd64 para poder ejecutar los drivers de Firefox correctamente.
    Alternativamente, puedes usar esta imagen:

    ```bash
    docker pull kevinportugalmx/scrapper-test:latest
    ```

    ```bash
    docker run -p 8000:8000 kevinportugalmx/scrapper-test:latest
    ```

    ## Notas

    Al ejecutar las peticiones localmente en mi equipo y mi internet, el tiempo promedio por solicitud era de alrededor de 3 segundos. Sin embargo, al ejecutar en la imagen de Docker, los tiempos fueron considerablemente más altos. Esto lo atribuyo a que mi equipo es ARM64 (macOS) y la imagen se construyó para AMD64, dadas las necesidades del driver de Firefox, lo que podría haber causado ciertas ineficiencias. Probablemente se pudo optimizar mucho más, pero estos son los tiempos que se pudieron lograr en las condiciones actuales.
    Cabe mencionar tambien que es la primera vez que trabajo con Selenium.
    Espero poder obtener un feedback al respecto, y sobre todo el proyecto. Gracias!
