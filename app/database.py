from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

mdp = quote_plus("magne33PA@")

# REMPLACE 'ton_mot_de_passe' par le vrai mot de passe de ton MySQL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://medecin:{mdp}@127.0.0.1:3306/article_app"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # La base pour tes modèles (Point 2)

#fonction pour fournir une session a fastapi
def get_db():
        db = SessionLocal()
        try:
                yield db
        finally:
                db.close()