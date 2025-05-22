import logging
import os
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, RequestException, Timeout

PREDEFINED_DORKS = [
    "site:{domain} intitle:index.of",
    "site:{domain} ext:pdf OR ext:doc OR ext:xls",
    "site:{domain} inurl:admin",
    "site:{domain} intitle:login",
    "site:{domain} intext:password OR intext:username",
]


# ---------------- Cargar variables de entorno ----------------
def load_env_variables() -> Optional[Dict[str, str]]:
    load_dotenv()
    api_key = os.getenv("API_KEY_SEARCH_GOOGLE")
    search_engine_id = os.getenv("SEARCH_ENGINE_ID")

    if not api_key or not search_engine_id:
        logging.error(
            "API Key o Search Engine ID no encontrados en el " + "archivo .env"
        )
        return None
    logging.info("API Key y Search Engine ID cargados correctamente.")
    return {"api_key": api_key, "search_engine_id": search_engine_id}


# ---------------- Realizar búsqueda en Google ----------------
def perform_google_search(
    api_key: str,
    search_engine_id: str,
    query: str,
    start: int = 1,
    lang: str = "lang_es",
) -> Optional[List[Dict]]:
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": query,
        "start": start,
        "lr": lang,
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Mejora 6: verificar si el API devolvió un error
        if "error" in data:
            logging.error(f"Error de API: {data['error'].get('message')}")
            return []

        return data.get("items", [])

    except ConnectionError:
        logging.error(
            "Error de conexión: no se pudo resolver el nombre del host o no hay red."
        )
    except Timeout:
        logging.error("La solicitud ha superado el tiempo de espera.")
    except RequestException as e:
        logging.error(f"Ocurrió un error en la solicitud HTTP: {e}")
    except ValueError as e:
        logging.error(f"Error al parsear la respuesta JSON: {e}")
    except Exception as e:
        logging.exception("Ocurrió un error inesperado")

    return None


# ---------------- Mostrar resultados ----------------
def display_results(results: List[Dict]) -> None:
    for result in results:
        print("------- Nuevo resultado -------")
        print(f"Título: {result.get('title')}")
        print(f"Descripción: {result.get('snippet')}")
        print(f"Enlace: {result.get('link')}")
        print("-------------------------------")


def parsear_resultado(resultados: List[Dict]):
    lista = []
    for resultado in resultados:
        lista.append(
            {
                "titulo": resultado.get("title"),
                "descripcion": resultado.get("snippet"),
                "enlace": resultado.get("link"),
            }
        )

    return lista


# ---------------- Ejecución Principal ----------------
def busqueda_start(pagina: str):
    env_vars = load_env_variables()
    all_results = []

    for dork_template in PREDEFINED_DORKS:
        query = dork_template.format(domain=pagina)
        results = perform_google_search(
            env_vars["api_key"], env_vars["search_engine_id"], query
        )
        if results:
            all_results.extend(parsear_resultado(results))

    return all_results


if __name__ == "__main__":
    busqueda_start("github.com")
