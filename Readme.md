##-----  Blog API ------

#API REST pour gérer des articles de blog (création, lecture, mise à jour, suppression, recherche).

#Technologies utilisées

Python 3.8+

FastAPI

SQLAlchemy

MySQL / MariaDB

Alembic (pour les migrations)

Uvicorn (serveur ASGI)

#Structure du projet
article_app/
│
├── app/
│   ├── main.py            # Points d'entrée FastAPI
│   ├── modeles.py          # Modèles SQLAlchemy
│   ├── schemas.py         # Schémas Pydantic
│   ├── database.py        # Configuration DB
│
├── alembic/               # Migrations Alembic
├── alembic.ini
├── requirements.txt
├── .env                   # Variables sensibles (non push sur GitHub)
├── .gitignore
├── Procfile               # Pour déploiement (Render/Heroku)
└── README.md

##Installation et configuration

Créer un environnement virtuel et l’activer :

python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

##Installer les dépendances :

pip install -r requirements.txt

Créer un fichier .env pour tes variables sensibles :

DB_USER=ton_utilisateur_mysql
DB_PASSWORD=ton_mot_de_passe
DB_HOST=127.0.0.1
DB_NAME=nom_de_ta_base

Appliquer les migrations Alembic :

alembic upgrade head

Lancer le serveur FastAPI :

uvicorn app.main:app --reload

L’API sera disponible sur : http://127.0.0.1:8000

##Documentation API

FastAPI génère automatiquement la documentation Swagger :

Swagger UI : http://127.0.0.1:8000/docs

Redoc : http://127.0.0.1:8000/redoc

🔹 Endpoints principaux
Méthode	Endpoint	Description
POST	/api/articles	Créer un article
GET	/api/articles	Lire tous les articles, possibilité de filtrer par category, author, date
GET	/api/articles/{id}	Lire un article par son ID
PUT	/api/articles/{id}	Mettre à jour un article par son ID
DELETE	/api/articles/{id}	Supprimer un article par son ID
GET	/api/articles/search?query=...	Rechercher articles par titre ou contenu
GET	/api/articles/categorie?query=...	Rechercher articles par catégorie ou date

## Exemple de requêtes

Créer un article :

POST /api/articles
{
    "title": "Mon premier article",
    "content": "Contenu de l'article...",
    "author": "pahola",
    "category": "Tech",
    "tags": "python,fastapi"
}

Réponse :

{
    "message": "Création de l'article réussie",
    "id_article": 1
}

Mettre à jour un article :

PUT /api/articles/1
{
    "title": "Titre mis à jour"
}

Réponse :

{
    "message": "Article mis à jour avec succès",
    "id_article": 1,
    "title": "Titre mis à jour",
    "content": "Contenu précédent",
    "category": "Tech",
    "tags": "python,fastapi"
}
