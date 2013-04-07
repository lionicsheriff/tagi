from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from sqlalchemy import event
from sqlalchemy.sql import func, case

import os

Base = declarative_base()
Session = sessionmaker()

class Config(Base):
    __tablename__ = 'config'
    key = Column('key', String, primary_key=True)
    value = Column('value', String)

class Document(Base):
    __tablename__ = 'documents'
    id = Column('id', Integer, primary_key = True)
    path = Column('path', String, index = True, unique = True)
    title = Column('title', String)

    tags = relationship("Tag", backref = "document", cascade='all, delete-orphan')
    
    @property
    def context(self):
        return [tag for tag in self.tags if tag.as_context]

    @property
    def links(self):
        return [tag for tag in self.tags if tag.as_link]

    @classmethod
    def find_or_new(cls,session, path, tags = []):
        return session.query(cls).filter_by(path = path).first() or cls(path, tags)
    
    def __init__(self, path, tags = []):
        self.path = path
        self.tags = tags

    def __repr__(self):
        return '<Document(%s)>' % self.path


class Keyword(Base):
    __tablename__ = 'keywords'
    id = Column('id', Integer, primary_key = True)
    name = Column('name', String, index = True, unique = True)
    
    @classmethod
    def find_or_new(cls, session, name):
        return session.query(Keyword).filter_by(name = name).first() or cls(name)

    def __init__(self, name):
            self.name = name

    def __repr__(self):
        return '<Keyword(%s)>' % self.name


class Tag(Base):
    __tablename__ = 'tags'
    keyword_id = Column(Integer, ForeignKey('keywords.id'), primary_key = True)
    document_id = Column(Integer, ForeignKey('documents.id'), primary_key = True)
    as_context = Column(Boolean, default = False)
    as_link = Column(Boolean, default = False)
    
    keyword = relationship("Keyword")

    def __init__(self, keyword = None, document = None, as_context = None, as_link = None):
        self.keyword = keyword
        self.document = document
        self.as_context = as_context
        self.as_link = as_link
    
    def __repr__(self):
        document = "None"
        if (self.document != None):
            document = self.document.path

        keyword = "None"
        if (self.keyword != None):
            keyword = self.keyword.name

        return '<Tag(%s,%s)>' % (keyword, document)
    
    
    
class Tagi:

    @classmethod
    def find_database(cls,dbname):
        cwd = os.getcwd()
        calling_dir = os.getcwd()
        while True:
            # try to find the database file
            dbpath = os.path.join(cwd,dbname)
            if os.path.isfile(dbpath):
                return dbpath

            # prepare to go up a level
            nwd = os.path.dirname(cwd)

            # could not go up (probably at root)
            if (nwd == cwd or not os.path.isdir(nwd)):
                return calling_dir

            # go up and try again
            cwd = nwd
    

    def create_document(self, path,tags = [], context = [], links = []):
        doc = Document.find_or_new(self.session, path)
        self.session.add(doc)
        self.add_tags(doc,tags)
        self.set_context(doc,context)
        self.set_links(doc,links)

        self.session.commit() # this needs to be at the end otherwise some documents get lost, why?
        return doc

    def add_tags(self, document, tags):
        current_tags = [tag.keyword.name for tag in document.tags]
        for tag in tags:
            if tag not in current_tags:
                keyword = Keyword.find_or_new(self.session, tag)
                document.tags.append(Tag(keyword = keyword))

    def remove_tags(self, document, tags):
        current_tags = [tag for tag in document.tags if tag.keyword.name in tags]
        for tag in current_tags:
            document.tags.remove(tag)



    def set_tags(self, document, tags):
        document.tags = []
        self.add_tags(document, tags)


    def set_context(self, document, context = []):
        self.add_tags(document, context)
        for tag in document.tags:
            if tag.keyword.name in context:
                tag.as_context = True
            else:
                tag.as_context = False
        
    def set_links(self, document, context = []):
        self.add_tags(document, context)
        for tag in document.tags:
            if tag.keyword.name in context:
                tag.as_link = True
            else:
                tag.as_link = False

        
    def find_document(self, path = None, tags = [], context = []):
        documents = self.find_documents(path = path, tags = tags, context = context)
        if documents != None and len(documents) > 0:
            return documents[0]
        else:
            return None

    def find_documents(self, path = None, tags = [], context = []):

        query = self.session.query(Document)

        if path != None:
            query = query.filter_by(path=path)

        if len(tags) > 0:
            query = query.join(Document.tags).\
            join(Tag.keyword).\
            filter(Keyword.name.in_(tags)).\
            group_by(Document.id).\
            having(func.count(Document.id) == len(tags))

        documents = query.order_by(Document.id).all()

        if len(context) > 0:
            # calculate the weight for a document based off the number of context tags the document has
            # this is done in python as it is simpler to retrieve the set of documents that match the tags
            # and then check them agains the context, then doing it in one swoop (the having clause would need to be a lot smarter)

            for doc in documents:
                doc.weight = len(set([tag.keyword.name for tag in doc.tags]) & set(context))

            # sort the most appropriate to the top
            documents.sort(key=lambda x: x.weight, reverse=True)

        return documents

    def __init__(self, dbname = 'tagi.db'):
        self.dbpath = self.find_database(dbname)
        self.wiki_root = os.path.dirname(self.dbpath)
        self.engine = create_engine('sqlite:///%s' % dbname)
        Base.metadata.create_all(self.engine)
        Session.configure(bind=self.engine)
        self.session = Session()

