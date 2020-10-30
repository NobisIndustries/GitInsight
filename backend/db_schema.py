from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.schema import ForeignKey


Base = declarative_base()


class SqlCommitMetadata(Base):
    __tablename__ = 'commits'
    
    hash = Column(String(40), index=True, primary_key=True)
    authored_timestamp = Column(Integer)
    author = Column(Text)
    message = Column(Text)
    number_affected_files = Column(Integer)


class SqlAffectedFile(Base):
    __tablename__ = 'affected_files'

    hash = Column(String(40), ForeignKey('commits.hash'), index=True, primary_key=True)
    file_id = Column(String(36), primary_key=True)  # UUID4
    old_path = Column(Text)
    new_path = Column(Text)
    change_type = Column(String(1))


class SqlCurrentFilePath(Base):
    __tablename__ = 'current_file_paths'

    branch = Column(Text, index=True, primary_key=True)
    file_id = Column(String(36), ForeignKey('affected_files.file_id'), index=True, primary_key=True)
    current_path = Column(Text)


def get_engine():
    return create_engine('sqlite:///test.db')


def get_session():
    Session = sessionmaker(bind=get_engine())
    return Session()


def create_tables(clean_before=False):
    if clean_before:
         Base.metadata.drop_all(get_engine())
    Base.metadata.create_all(get_engine())
