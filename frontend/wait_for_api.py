import time
import requests
import os
import sys

def wait_for_api(api_url, max_retries=30, retry_interval=2):
    """
    Attend que l'API soit disponible avant de continuer.
    
    Args:
        api_url (str): URL de l'API à vérifier
        max_retries (int): Nombre maximum de tentatives
        retry_interval (int): Intervalle entre les tentatives en secondes
        
    Returns:
        bool: True si l'API est disponible, False sinon
    """
    health_endpoint = f"{api_url}/health"
    print(f"Attente de l'API à {health_endpoint}...")
    
    for i in range(max_retries):
        try:
            response = requests.get(health_endpoint, timeout=3)
            if response.status_code == 200:
                print(f"API disponible après {i+1} tentative(s)!")
                return True
        except requests.RequestException as e:
            print(f"Tentative {i+1}/{max_retries}: API non disponible. Erreur: {str(e)}")
        
        # Attendre avant la prochaine tentative
        time.sleep(retry_interval)
    
    print(f"Échec après {max_retries} tentatives. L'API n'est pas disponible.")
    return False

if __name__ == "__main__":
    api_url = os.getenv("FASTAPI_URL", "http://fastapi:8000")
    success = wait_for_api(api_url)
    if not success:
        sys.exit(1)  # Quitter avec un code d'erreur si l'API n'est pas disponible