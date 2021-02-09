from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///contatos.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = 'contatos'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    dominio = Column(String, nullable=False)

    def __init__(self, email, dominio):
        self.email = email
        self.dominio = dominio

    def save(self):
        db_session.add(self)
        db_session.commit()

    def __repr__(self):
        return '<Usuario {}>'.format(self.email)


def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()