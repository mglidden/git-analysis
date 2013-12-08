import config

from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy

Base = declarative_base()

engine = sqlalchemy.create_engine(config.DB_URL, echo=False)

Session = sqlalchemy.orm.sessionmaker(bind=engine)
