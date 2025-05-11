import time
import os
import sys
import pymysql

def wait_for_db(max_retries=30, retry_interval=2):
    """
    Attend que la base de données MySQL soit disponible.
    
    Args:
        max_retries (int): Nombre maximum de tentatives
        retry_interval (int): Intervalle entre les tentatives en secondes
        
    Returns:
        bool: True si la base de données est disponible, False sinon
    """
    # Configuration de la base de données
    DB_HOST = os.getenv("DB_HOST", "mysql")
    DB_USER = os.getenv("DB_USER", "app_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "app_password")
    DB_NAME = os.getenv("DB_NAME", "app_db")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    
    print(f"Attente de la base de données MySQL à {DB_HOST}:{DB_PORT}...")
    
    for i in range(max_retries):
        try:
            connection = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                port=DB_PORT,
                connect_timeout=3
            )
            connection.close()
            print(f"Base de données disponible après {i+1} tentative(s)!")
            return True
        except pymysql.MySQLError as e:
            print(f"Tentative {i+1}/{max_retries}: Base de données non disponible. Erreur: {str(e)}")
        except Exception as e:
            print(f"Erreur inattendue: {str(e)}")
        
        # Attendre avant la prochaine tentative
        time.sleep(retry_interval)
    
    print(f"Échec après {max_retries} tentatives. La base de données n'est pas disponible.")
    return False

if __name__ == "__main__":
    success = wait_for_db()
    if not success:
        sys.exit(1)  # Quitter avec un code d'erreur si la base de données n'est pas disponible