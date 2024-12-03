import json
import os
import time
import requests
from kafka import KafkaProducer

# Configuración de Kafka
KAFKA_BROKER = 'kafka1:9092'

# Inicializar productor de Kafka
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

keys_to_remove = [
    "comments",
    "reportDescription",
    "nThumbsUp",
    "reportBy",
    "reportByMunicipalityUser",
    "reportRating",
    "reportMood",
    "fromNodeId",
    "toNodeId",
    "magvar",
    "additionalInfo",
    "wazeData"
]

def remove_keys_from_dict(data, keys_to_remove):
    """Función recursiva para eliminar claves específicas de un diccionario."""
    if isinstance(data, list):
        for item in data:
            remove_keys_from_dict(item, keys_to_remove)
    elif isinstance(data, dict):
        for key in keys_to_remove:
            if key in data:
                del data[key]

        for key in data:
            if isinstance(data[key], (dict, list)):
                remove_keys_from_dict(data[key], keys_to_remove)

def scrape_traffic_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la respuesta contiene un estado HTTP de error
        data = response.json()

        # Eliminar los atributos innecesarios
        remove_keys_from_dict(data, keys_to_remove=keys_to_remove)

        return data

    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud a {url}: {e}")
        return {}

def main():
    # Establecer la URL predeterminada
    default_url = "https://www.waze.com/live-map/api/georss?top=-33.37380423388275&bottom=-33.418863153828454&left=-70.73255538940431&right=-70.54201126098634&env=row&types=alerts,traffic"

    url = default_url  # Asignar directamente la URL predeterminada

    print(f"Scrapeando datos de la URL: {url}")

    while True:
        try:
            print("Extrayendo datos de tráfico...")
            traffic_data = scrape_traffic_data(url)

            # Separar los datos en dos partes: alerts y jams
            alerts_data = traffic_data.get("alerts", [])

            # Enviar los datos de "alerts" al tópico "alerts"
            for alert in alerts_data:
                producer.send('alerts', alert)
                print(f"Alerta enviada a Kafka: {alert}")

            time.sleep(10)  # Esperar 10 segundos antes de la próxima extracción
        except Exception as e:
            print(f"Error en el scraper: {e}")
            time.sleep(2)  # Esperar 2 segundos antes de reintentar

if __name__ == "__main__":
    main()

