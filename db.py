import  atexit
from sqlalchemy import Column, String, Integer, DateTime, create_engine, func, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

PG_DSN = 'postgresql://app:1234@127.0.0.1:5431/netology'

engine = create_engine(PG_DSN)

Base = declarative_base()
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)

class User(Base):

    __tablename__ = 'app_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())


class Bulletin(Base):

    __tablename__ = 'bulletin'

    id = Column(Integer, primary_key=True, autoincrement=True)
    header = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey('app_users.id'))
    user = relationship('User', backref='bulletin')


Base.metadata.create_all(bind=engine)