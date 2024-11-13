from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

DATABASE = {
    'driver' :'mysql+pymysql',
    'username' : 'root',
    'password': 'root',
    'host': 'localhost',
    'port':'3306',
    'database': 'progressTracker'

}
def get_db_url():
    return f"{DATABASE['driver']}://{DATABASE['username']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}"

db_url = get_db_url()
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = SessionLocal()