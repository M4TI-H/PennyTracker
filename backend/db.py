import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

db_url = f"mysql+pymysql://{"root"}:@{"localhost"}:{"3306"}/{"pennytracker"}"
engine = sa.create_engine(db_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()