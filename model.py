from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime #SQL alchemy datatypes
from sqlalchemy import ForeignKey, Table


from sqlalchemy import create_engine
ENGINE = create_engine('postgresql://katiecheng:password@localhost/publications', echo=False)
session = scoped_session(sessionmaker(bind=ENGINE,
                                      autocommit = False,
                                      autoflush = False))
Base = declarative_base()
Base.query = session.query_property()

### START SQLAlchemy class declarations

class Journal(Base):
    __tablename__ = "journals"

    id = Column(Integer, primary_key = True)
    name = Column(String(100))

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key = True)
    name = Column(String(100))

references = Table("references", Base.metadata,
    Column("parent_pub_id", Integer, ForeignKey("publications.id"), primary_key=True),
    Column("child_pub_id", Integer, ForeignKey("publications.id"), primary_key=True))

class Publication(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key = True)
    eric_id = Column(String(20), nullable=False)
    title = Column(String(500))
    source_id = Column(Integer, ForeignKey('sources.id'))
    full_desc = Column(String(5000))
    url = Column(String(100))
    abstract = Column(String(3000))
    month = Column(Integer)
    year = Column(Integer)
    journal_id = Column(Integer, ForeignKey('journals.id'))
    volume = Column(Integer)
    issue = Column(Integer)
    start_page = Column(Integer)
    end_page = Column(Integer)

    journal = relationship("Journal", 
        backref = backref("publications", order_by=id))

    source = relationship("Source", 
        backref = backref("publications", order_by=id))

    referenced_by = relationship("Publication",
        secondary=references,
        primaryjoin=id==references.c.child_pub_id,
        secondaryjoin=id==references.c.parent_pub_id,
        backref="references")

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key = True)
    first_name = Column(String(30))
    middle_name = Column(String(30))
    last_name = Column(String(30))
    credential = Column(String(30))
    position = Column(String(50))
    institution_id = Column(Integer, ForeignKey('institutions.id'))
    department_id = Column(Integer, ForeignKey('departments.id'))

    institution = relationship("Institution", 
        backref = backref("authors", order_by=id))

    department = relationship("Department", 
        backref = backref("authors", order_by=id))

class Descriptor(Base):
    __tablename__ = "descriptors"

    id = Column(Integer, primary_key = True)
    phrase = Column(String(100))

class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key = True)
    phrase = Column(String(100))

class CommonWord(Base):
    __tablename__ = "common_words"

    id = Column(Integer, primary_key = True)
    word = Column(String(20))

class Institution(Base):
    __tablename__ = "institutions"

    id = Column(Integer, primary_key = True)
    name = Column(String(100))

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key = True)
    name = Column(String(100))

### Pivot Tables

class pubAuth(Base):
    __tablename__ = "pub_auth"

    id = Column(Integer, primary_key = True)
    pub_id = Column(Integer, ForeignKey('publications.id'), nullable=False)
    auth_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

    publication = relationship("Publication", 
        backref = backref("pub_auth", order_by=id))

    author = relationship("Author", 
        backref = backref("pub_auth", order_by=id))

class pubDesc(Base):
    __tablename__ = "pub_desc"

    id = Column(Integer, primary_key = True)

    pub_id = Column(Integer, ForeignKey('publications.id'), nullable=False)
    desc_id = Column(Integer, ForeignKey('descriptors.id'), nullable=False)

    publication = relationship("Publication", 
        backref = backref("pub_desc", order_by=id))

    descriptor = relationship("Descriptor", 
        backref = backref("pub_desc", order_by=id))

class pubKey(Base):
    __tablename__ = "pub_key"

    id = Column(Integer, primary_key = True)
    pub_id = Column(Integer, ForeignKey('publications.id'), nullable=False)
    key_id = Column(Integer, ForeignKey('keywords.id'), nullable=False)

    publication = relationship("Publication", 
        backref = backref("pub_key", order_by=id))

    keywords = relationship("Keyword", 
        backref = backref("pub_key", order_by=id))

class pubCommon(Base):
    __tablename__ = "pub_common"

    id = Column(Integer, primary_key = True)
    pub_id = Column(Integer, ForeignKey('publications.id'), nullable=False)
    common_id = Column(Integer, ForeignKey('common_words.id'), nullable=False)

    publication = relationship("Publication", 
        backref = backref("pub_common", order_by=id))

    common_word = relationship("CommonWord", 
        backref = backref("pub_common", order_by=id))

### END SQLAlchemy class declarations

def create_tables():
    global ENGINE
    Base.metadata.create_all(ENGINE)

def drop_tables():
    global ENGINE
    Base.metadata.drop_all(ENGINE)

def main():
    pass

if __name__ == "__main__":
    main()