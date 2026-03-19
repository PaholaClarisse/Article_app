from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta
from app.database import get_db
from app.modeles import Article
from app.schemas import ArticleCreate, ArticleUpdate, ArticleOut

app = FastAPI(title="Blog API", version="1.0")

@app.get("/")
def root():
    return {"bienvenue dans notre apllication de gestion des articles."}
    
#creer un article grace a ces informations
@app.post("/api/articles", status_code=status.HTTP_201_CREATED)
def create_article(article: ArticleCreate,db: Session = Depends(get_db)):
    new_article = Article(title= article.title, content=  article.content,
                  author = article.author, category= article.category, 
                  tags= article.tags)

    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return {"message": "creation de l'article reussie", "id_article": new_article.id}

# lire tout les artiles complets, soit par category, soit le nom de l'auteur, soit par date
@app.get("/api/articles", status_code=status.HTTP_201_CREATED)
def read_article(category: Optional[str] = None,author: Optional[str] = None,
    date: Optional[str] = None,db: Session = Depends(get_db)):
    query = db.query(Article)
    
    # 🔹 Filtre par catégorie
    if category:
        query = query.filter(Article.category == category)

    # 🔹 Filtre par auteur
    if author:
        query = query.filter(Article.author == author)

    # 🔹 Filtre par date
    if date:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            next_day = date_obj + timedelta(days=1)

            query = query.filter(
                Article.created_at >= date_obj,
                Article.created_at < next_day)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Format de date invalide. Utilisez YYYY-MM-DD")

    # Récupération des résultats
    articles = query.all()

    return articles

# afficher un article grace a son id
@app.get("/api/article/{id}", response_model = ArticleOut)
def read_article_id(id: int ,db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    if not article:
        raise HTTPException(status_code=404, detail="article not found")
    return article
    
# modifier un article en utilisannt ces champs
@app.put("/api/articles/{id}")
def update_article(id: int, update: ArticleUpdate, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    if not article:
        raise HTTPException(status_code=404, detail="article not found")

    '''if update.title is not None:
        article.title = update.title
    if update.content is not None:
        article.content = update.content
    if update.category is not None:
        article.category= update.category
    if update.tags is not None:
        article.tags= update.tags'''

    for field, value in update.dict(exclude_unset=True).items():
        if value is not None:
            setattr(article, field, value)

    db.commit()
    db.refresh(article)
    return {"message": "Article mis à jour avec succès",
        "id_article": article.id,
        "title": article.title,
        "content": article.content,
        "category": article.category,
        "tags": article.tags}

#supprimer un article par son id
@app.delete("/api/article/{id}")
def supprimer_article_id(id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    if not Article:
        raise HTTPException(status_code=404, detail="article not found")
    db.delete(article)
    db.commit()
    return {"message": "article supprimé"}

# rechercher des articles par leur champ titre ou content
@app.get("/api/articles/search", response_model = List[ArticleOut])
def rechercher_article(query: str, db: Session = Depends(get_db)):
    """
    Rechercher des articles dont le titre ou le contenu contient le texte fourni.
    """
    articles = db.query(Article).filter(
        (Article.title.contains(query)) | (Article.content.contains(query))
    ).all()
    return articles

# recuperer des articles par categories ou par date de publication
@app.get("/api/articles/categorie", response_model = List[ArticleOut])
def recuperer_article_categorie(category: Optional[str] = None,
    date: Optional[str] = None,db: Session = Depends(get_db)):
    query = db.query(Article)

    if category:
        query = query.filter(Article.category.contains(category))

    if date:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            next_day = date_obj + timedelta(days=1)
            query = query.filter(Article.created_at >= date_obj,
                                 Article.created_at < next_day)
        except ValueError:
            raise HTTPException(status_code=400, detail="Format de date incorrect, utilisez YYYY-MM-DD")

    articles = query.all()
    return articles