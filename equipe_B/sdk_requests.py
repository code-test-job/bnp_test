import requests
import time
from concurrent.futures import ThreadPoolExecutor


def fetch_data(base_url: str, resource: int) -> None:
    # Construire l'URL de la ressource
    url = f"{base_url}/long-calculation?param={resource}"
    print(url)
    try:
        # Effectuer une requête GET à l'API et récupérer les données JSON de la réponse
        response = requests.get(url)
        response.raise_for_status()  # lever une exception si la requête a échoué     
        data = response.json()

        # Exibir os dados da resource
        print(f"--- {resource} ---")
        print(data)
    except requests.exceptions.RequestException as e:
         # Afficher les données de la ressource
        print(f"Erro ao recuperar dados de {resource}: {e}")


# URL de l'API
#base_url = "https://api.haddock.com"
base_url = "http://127.0.0.1:8000"

# Liste de chiffres avec une taille N,  1 < N < 100000000
resources = [4, 10, 6]

# ThreadPoolExecutor pour lancer en parallel
with ThreadPoolExecutor(max_workers=4) as executor:
    for resource in resources:
        executor.submit(fetch_data, base_url, resource)
        time.sleep(0.001)
