import sqlalchemy
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey, UnicodeText, MetaData, Sequence, DateTime
from sqlalchemy.ext.declarative import DeclarativeMeta
from MethodWrapper import Method

UnicodeText = UnicodeText
DateTime = DateTime

Table = Table
Column = Column
Integer = Integer
String = String
Float = Float

exists = exists

relationship = relationship

Sequence = Sequence
ForeignKey = ForeignKey
MetaData = MetaData

DeclarativeMeta = DeclarativeMeta

DEFAULT_LOCAL_STORAGE_NAME = 'LocalStorage'

KW_API = 'api'
KW_NAME = 'name'
KW_MAIN_URL = 'main-url'

KW_REPOSITORY = 'repository'
KW_REPOSITORY_DIALECT = 'dialect'
KW_REPOSITORY_USER = 'user'
KW_REPOSITORY_PASSWORD = 'password'
KW_REPOSITORY_HOST = 'host'
KW_REPOSITORY_PORT = 'port'
KW_REPOSITORY_DATABASE = 'database'

MANY_TO_MANY = '''And'''
ID = '''Id'''
SEQ = '''Seq'''
LIST = '''List'''

@Method
def getNewModel() :
    return declarative_base()

@Method
def attributeIt(modelName) :
    return f'{modelName[0].lower()}{modelName[1:]}'

@Method
def getManyToMany(sisters, brothers, refferenceModel) :
    # skillList = relationship(SKILL, secondary=skillToOwnerAssociation, back_populates=attributeIt(f'{__tablename__}{LIST}'))
    # ownerList = relationship(OWNER, secondary=skillToOwnerAssociation, back_populates=attributeIt(f'{__tablename__}{LIST}'))
    manySonToManyFather = Table(f'{sisters}{MANY_TO_MANY}{brothers}', refferenceModel.metadata,
        Column(f'{attributeIt(sisters)}{ID}', Integer, ForeignKey(f'{sisters}.{ID.lower()}')),
        Column(f'{attributeIt(brothers)}{ID}', Integer, ForeignKey(f'{brothers}.{ID.lower()}')))
    brotherList = relationship(brothers, secondary=manySonToManyFather, back_populates=attributeIt(f'{sisters}{LIST}'))
    sisterList = relationship(sisters, secondary=manySonToManyFather, back_populates=attributeIt(f'{brothers}{LIST}'))
    ### sisters recieves the brotherList
    ### brothers recieves the sisterList
    return fatherList, manySonToManyFather, sonList

@Method
def getOneToMany(owner, pet, refferenceModel) :
    return relationship(pet, back_populates=attributeIt(f'{owner}'))

@Method
def getManyToOne(pet, owner, refferenceModel) :
    ownerId = Column(Integer(), ForeignKey(f'{owner}.{ID.lower()}'))
    owner = relationship(owner, back_populates=attributeIt(f'{pet}{LIST}'))
    return owner, ownerId

@Method
def getOneToOne(owner, pet, refferenceModel) :
    return relationship(pet, back_populates=attributeIt(owner))

@Method
def getOneToOne(woman, man, refferenceModel) :
    manId = Column(Integer(), ForeignKey(f'{man}.{ID.lower()}'))
    manList = relationship(man, back_populates=attributeIt(woman), uselist=False)
    return manId, manList

@Method
def getOneToOne__forDebug(man, woman, refferenceModel) :
    womanId = Column(Integer(), ForeignKey(f'{woman}.{ID.lower()}'))
    womanList = relationship(woman, back_populates=attributeIt(man))
    return womanId, womanList

class SqlAlchemyHelper:

    TOKEN_WITHOUT_NAME = '__TOKEN_WITHOUT_NAME__'
    DEFAULT_LOCAL_NAME = DEFAULT_LOCAL_STORAGE_NAME

    DEFAULT_DATABASE_TYPE = 'sqlite'
    BAR = '''/'''
    COLON = ''':'''
    ARROBA = '''@'''
    DOUBLE_BAR = 2 * BAR
    TRIPLE_BAR = 3 * BAR

    NOTHING = ''

    EXTENSION = 'db'

    def __init__(self,
            localName = TOKEN_WITHOUT_NAME,
            dialect = None,
            user = None,
            password = None,
            host = None,
            port = None,
            model = None,
            globals = None,
            echo = False,
            checkSameThread = False
        ):

        self.sqlalchemy = sqlalchemy

        if not dialect and globals :
            self.dialect = globals.getApiSetting(f'{KW_API}.{KW_REPOSITORY}.{KW_REPOSITORY_DIALECT}')
        else :
            self.dialect = dialect

        if not dialect and globals :
            self.user = globals.getApiSetting(f'{KW_API}.{KW_REPOSITORY}.{KW_REPOSITORY_USER}')
        else :
            self.user = user

        if not dialect and globals :
            self.password = globals.getApiSetting(f'{KW_API}.{KW_REPOSITORY}.{KW_REPOSITORY_PASSWORD}')
        else :
            self.password = password

        if not dialect and globals :
            self.host = globals.getApiSetting(f'{KW_API}.{KW_REPOSITORY}.{KW_REPOSITORY_HOST}')
        else :
            self.host = host

        if not dialect and globals :
            self.port = globals.getApiSetting(f'{KW_API}.{KW_REPOSITORY}.{KW_REPOSITORY_PORT}')
        else :
            self.port = port

        if localName == self.TOKEN_WITHOUT_NAME and globals :
            databaseName = globals.getApiSetting(f'{KW_API}.{KW_REPOSITORY}.{KW_REPOSITORY_DATABASE}')
            if databaseName and not 'None' == databaseName :
                self.name = databaseName
            else :
                self.name = 'DefaultLocalName'
        else :
            self.name = localName

        if globals :
            globals.debug(f'Repository configuration:')
            globals.debug(f'{globals.TAB_UNITS * globals.SPACE}dialect = {self.dialect}')
            globals.debug(f'{globals.TAB_UNITS * globals.SPACE}user = wops!')
            globals.debug(f'{globals.TAB_UNITS * globals.SPACE}password = wops!')
            globals.debug(f'{globals.TAB_UNITS * globals.SPACE}host = {self.host}')
            globals.debug(f'{globals.TAB_UNITS * globals.SPACE}port = {self.port}')
            globals.debug(f'{globals.TAB_UNITS * globals.SPACE}name = {self.name}')

        user_password_host = self.NOTHING
        if self.user and self.password :
            user_password_host += f'{self.user}{self.COLON}{self.password}'
        if self.host :
            user_password_host += f'{self.ARROBA}{self.host}{self.COLON}{self.port}'
        user_password_host += self.BAR

        if user_password_host == self.BAR :
            self.name = f'{self.name}.{self.EXTENSION}'

        if not self.dialect :
            self.dialect = self.DEFAULT_DATABASE_TYPE

        self.databaseUrl = f'{self.dialect}:{self.DOUBLE_BAR}{user_password_host}{self.name}'

        self.engine = create_engine(self.databaseUrl, echo=echo, connect_args={"check_same_thread": checkSameThread})
        self.session = scoped_session(sessionmaker(self.engine)) ###- sessionmaker(bind=self.engine)()
        self.model = model
        self.model.metadata.bind = self.engine

        self.run()

    @Method
    def run(self):
        self.model.metadata.create_all(self.engine)

    @Method
    def commit(self):
        self.session.commit()

    @Method
    def saveNewAndCommit(self,*args):
        model = args[-1]
        return self.saveAndCommit(model(*args[:-1]))

    @Method
    def saveAndCommit(self,instance):
        self.session.add(instance)
        self.session.commit()
        return instance

    @Method
    def saveAllAndCommit(self,instanceList):
        self.session.add_all(instanceList)
        self.session.commit()
        return instanceList

    @Method
    def findAllAndCommit(self,model):
        objectList = self.session.query(model).all()
        self.session.commit()
        return objectList

    @Method
    def findByIdAndCommit(self,id,model):
        object = self.session.query(model).filter(model.id == id).first()
        self.session.commit()
        return object

    @Method
    def existsByIdAndCommit(self,id,model):
        # ret = Session.query(exists().where(and_(Someobject.field1 == value1, Someobject.field2 == value2)))
        objectExists = self.session.query(exists().where(model.id == id)).one()[0]
        self.session.commit()
        return objectExists

    @Method
    def findByKeyAndCommit(self,key,model):
        object = self.session.query(model).filter(model.key == key).first()
        self.session.commit()
        return object

    @Method
    def existsByKeyAndCommit(self,key,model):
        objectExists = self.session.query(exists().where(model.key == key)).one()[0]
        self.session.commit()
        return objectExists

    @Method
    def findByStatusAndCommit(self,status,model):
        object = self.session.query(model).filter(model.status == status).first()
        self.session.commit()
        return object

    @Method
    def findAllByQueryAndCommit(self,query,model):
        objectList = []
        if query :
            objectList = self.session.query(model).filter_by(**query).all()
        self.session.commit()
        return objectList

    @Method
    def deleteByKeyAndCommit(self,key,model):
        if self.session.query(exists().where(model.key == key)).one()[0] :
            object = self.session.query(model).filter(model.key == key).first()
            self.session.delete(object)
        self.session.commit()
