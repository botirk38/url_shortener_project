from sqlalchemy.orm import Session
from . import models, schemas,keygenerator

def create_db_url(db: Session, url: schemas.URLBase,custom_key: str=None) -> models.URL:

    if custom_key is not None:
        if get_db_url_by_key(db,custom_key):
            raise HTTPException(
                status_code=400,
                detail="The custom key you provided is already in use",
            )
        else:
            key = custom_key
            secret_key = f"{key}_{keygenerator.create_random_key(length=8)}"
            db_url = models.URL(
                target_url=url.target_url, key=key, secret_key=secret_key
            )
            db.add(db_url)
            db.commit()
            db.refresh(db_url)
            return db_url
            
    else:
        key = keygenerator.create_unique_random_key(db)
        secret_key = f"{key}_{keygenerator.create_random_key(length=8)}"
        db_url = models.URL(
            target_url=url.target_url, key=key, secret_key=secret_key
        )
        db.add(db_url)
        db.commit()
        db.refresh(db_url)
        return db_url


def get_db_url_by_key(db: Session, url_key: str) -> models.URL:
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )


def update_db_clicks(db: Session, db_url: schemas.URL) -> models.URL:
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url

def deactivate_url(db: Session, secret_key: str) -> models.URL:
    url = get_db_url_by_secret_key(db, secret_key)
    url.is_active = False
    db.add(url)
    db.commit()
    db.refresh(url)
    return url

def get_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    return db.query(models.URL).filter(models.URL.secret_key == secret_key).first()


