from sqlalchemy import create_engine

DEBUG = True

# database engine. Use sqlite3 for debug
engine = create_engine('sqlite:///foo.db', echo=DEBUG)