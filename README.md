# Sistemas Distribuidos
> Tarea 3: Scrapping y procesamiento de información


## General Information
- En este proyecto se solicita construir un sistema de monitoreo de tráfico en tiempo real utilizando varias tecnologías de procesamiento y análisis de datos distribuidos
- Luego de establecer la conexión se planea analizar los datos obtenidos durante la ejecución del Scrapping.


<!-- You don't have to answer all the questions - just the ones relevant to your project. -->


## Technologies Used
- Terminal Ubuntu 22.04
- Python-3 o superior, con sus dependencias.
- Apache Kafka
- ElasticSearch
- Kibana
- Apache ZooKeeper
- Apache Cassandra
- Apache Spark
- Contenedores Docker

## Setup
Descargar la carpeta **Distribuidos** para tener todos los archivos necesarios para levantar el sistema.

Antes de establecer la conexión entre los contenedores, se crea el archivo docker-compose.yml, la cual se encarga de hacer correr los múltiples contenedores de Docker para así facilitar el despliegue de los servicios del sistema, asegurando que se inicien, se conecten entre sí a través de una red común y se mantengan operativos.

Se crean los contenedores descritos en el docker-compose.yml:
```diff
sudo docker-compose up --build -d
```
Luego, se comprueba que todos los contenedores estén funcionando con el comando:
```diff
sudo docker-compose ps
```
Luego, se configura Cassandra en su contenedor:
```diff
sudo docker exec -it cassandra cqlsh
```
Después se crea el keyspace:
```diff
CREATE KEYSPACE IF NOT EXISTS traffic_monitoring
WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};
```

Finalmente se crea la tabla "alerts" para almacenar los datos históricos:
```diff
CREATE TABLE IF NOT EXISTS alerts (
    uuid text PRIMARY KEY,
    country text,
    city text,
    reliability int,
    type text,
    speed int,
    subtype text,
    street text,
    id text,
    ncomments int,
    inscale boolean,
    confidence int,
    roadtype int,
    location_x double,
    location_y double,
    pubmillis bigint
);

```
## Usage

Para correr el sistema, se procede a ejecutar el Scrapper dentro de su contenedor.
```diff
sudo docker exec -it scrapper bash
```
```diff
python3 scrapper.py
```

Para visualizar los resultados en el **UI de Kafka**, en un navegador se usa:
```diff
localhost:8080
```
Y para ver los resultados para graficar en Elastic Search, se busca en el navegador:
```diff
localhost:5601
```
Y para ver los datos históricos en **Cassandra**, dentro de su contenedor se usa la query:
```diff
SELECT * FROM alerts LIMIT 10;
```
