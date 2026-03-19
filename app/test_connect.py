from database import engine
from sqlalchemy import text

def test_mysql_connection():
    print("🔍 Tentative de connexion à MySQL...")
    try:
        # On essaie d'ouvrir une connexion et d'exécuter une petite commande
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ SUCCÈS : La connexion entre l'application et MySQL est fonctionnelle !")
    except Exception as e:
        print("❌ ÉCHEC : Impossible de se connecter à la base de données.")
        print(f"L'erreur est : {e}")

if __name__ == "__main__":
    test_mysql_connection()