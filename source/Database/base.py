from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db_string = "postgresql://root:root@database:5432/database"
engine = create_engine(db_string)

Session = sessionmaker(bind=engine)

Base = declarative_base()



if __name__ == "__main__":
    pass
