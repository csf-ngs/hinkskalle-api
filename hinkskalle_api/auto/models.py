from __future__ import annotations
from dataclasses import dataclass, field
import typing
from datetime import datetime
from humanize import naturalsize




def plainToCollection(json: dict) -> Collection:
  obj = Collection()
  obj.containers = json.get('containers')
  obj.createdAt = datetime.fromisoformat(json['createdAt']) if json.get('createdAt') else None
  obj.createdBy = json.get('createdBy')
  obj.customData = json.get('customData')
  obj.deleted = bool(json['deleted']) if json.get('deleted') else None
  obj.deletedAt = datetime.fromisoformat(json['deletedAt']) if json.get('deletedAt') else None
  obj.description = json.get('description')
  obj.entity = json.get('entity')
  obj.entityName = json.get('entityName')
  obj.id = json.get('id')
  obj.name = json.get('name')
  obj.private = bool(json['private']) if json.get('private') else None
  obj.size = json.get('size')
  obj.updatedAt = datetime.fromisoformat(json['updatedAt']) if json.get('updatedAt') else None
  obj.usedQuota = json.get('usedQuota')
  
  return obj

def serializeCollection(obj: Collection) -> dict:
  json = {}
  json['containers'] = obj.containers
  json['createdAt'] = obj.createdAt.isoformat() if obj.createdAt else None
  json['createdBy'] = obj.createdBy
  json['customData'] = obj.customData
  json['deleted'] = obj.deleted
  json['deletedAt'] = obj.deletedAt.isoformat() if obj.deletedAt else None
  json['description'] = obj.description
  json['entity'] = obj.entity
  json['entityName'] = obj.entityName
  json['id'] = obj.id
  json['name'] = obj.name
  json['private'] = obj.private
  json['size'] = obj.size
  json['updatedAt'] = obj.updatedAt.isoformat() if obj.updatedAt else None
  json['usedQuota'] = obj.usedQuota
  
  return json

@dataclass
class Collection:
  containers: typing.Optional[str] = None
  createdAt: typing.Optional[datetime] = None
  createdBy: typing.Optional[str] = None
  customData: typing.Optional[str] = None
  deleted: typing.Optional[bool] = None
  deletedAt: typing.Optional[datetime] = None
  description: typing.Optional[str] = None
  entity: typing.Optional[str] = None
  entityName: typing.Optional[str] = None
  id: typing.Optional[str] = None
  name: typing.Optional[str] = None
  private: typing.Optional[bool] = None
  size: typing.Optional[int] = None
  updatedAt: typing.Optional[datetime] = None
  usedQuota: typing.Optional[int] = None
  

  def __str__(self):
    return f"""- name: {self.name}
  description: {self.description}
  size: {self.size}
  usedQuota: {naturalsize(self.usedQuota)}
"""



def plainToContainer(json: dict) -> Container:
  obj = Container()
  obj.archTags = json.get('archTags')
  obj.collection = json.get('collection')
  obj.collectionName = json.get('collectionName')
  obj.createdAt = datetime.fromisoformat(json['createdAt']) if json.get('createdAt') else None
  obj.createdBy = json.get('createdBy')
  obj.customData = json.get('customData')
  obj.deleted = bool(json['deleted']) if json.get('deleted') else None
  obj.deletedAt = datetime.fromisoformat(json['deletedAt']) if json.get('deletedAt') else None
  obj.description = json.get('description')
  obj.downloadCount = json.get('downloadCount')
  obj.entity = json.get('entity')
  obj.entityName = json.get('entityName')
  obj.fullDescription = json.get('fullDescription')
  obj.id = json.get('id')
  obj.imageTags = json.get('imageTags')
  obj.images = json.get('images')
  obj.name = json.get('name')
  obj.private = bool(json['private']) if json.get('private') else None
  obj.readOnly = bool(json['readOnly']) if json.get('readOnly') else None
  obj.size = json.get('size')
  obj.stars = json.get('stars')
  obj.type = json.get('type')
  obj.updatedAt = datetime.fromisoformat(json['updatedAt']) if json.get('updatedAt') else None
  obj.usedQuota = json.get('usedQuota')
  obj.vcsUrl = json.get('vcsUrl')
  
  return obj

def serializeContainer(obj: Container) -> dict:
  json = {}
  json['archTags'] = obj.archTags
  json['collection'] = obj.collection
  json['collectionName'] = obj.collectionName
  json['createdAt'] = obj.createdAt.isoformat() if obj.createdAt else None
  json['createdBy'] = obj.createdBy
  json['customData'] = obj.customData
  json['deleted'] = obj.deleted
  json['deletedAt'] = obj.deletedAt.isoformat() if obj.deletedAt else None
  json['description'] = obj.description
  json['downloadCount'] = obj.downloadCount
  json['entity'] = obj.entity
  json['entityName'] = obj.entityName
  json['fullDescription'] = obj.fullDescription
  json['id'] = obj.id
  json['imageTags'] = obj.imageTags
  json['images'] = obj.images
  json['name'] = obj.name
  json['private'] = obj.private
  json['readOnly'] = obj.readOnly
  json['size'] = obj.size
  json['stars'] = obj.stars
  json['type'] = obj.type
  json['updatedAt'] = obj.updatedAt.isoformat() if obj.updatedAt else None
  json['usedQuota'] = obj.usedQuota
  json['vcsUrl'] = obj.vcsUrl
  
  return json

@dataclass
class Container:
  archTags: typing.Optional[dict] = None
  collection: typing.Optional[str] = None
  collectionName: typing.Optional[str] = None
  createdAt: typing.Optional[datetime] = None
  createdBy: typing.Optional[str] = None
  customData: typing.Optional[str] = None
  deleted: typing.Optional[bool] = None
  deletedAt: typing.Optional[datetime] = None
  description: typing.Optional[str] = None
  downloadCount: typing.Optional[int] = None
  entity: typing.Optional[str] = None
  entityName: typing.Optional[str] = None
  fullDescription: typing.Optional[str] = None
  id: typing.Optional[str] = None
  imageTags: typing.Optional[dict] = None
  images: typing.Optional[str] = None
  name: typing.Optional[str] = None
  private: typing.Optional[bool] = None
  readOnly: typing.Optional[bool] = None
  size: typing.Optional[int] = None
  stars: typing.Optional[int] = None
  type: typing.Optional[str] = None
  updatedAt: typing.Optional[datetime] = None
  usedQuota: typing.Optional[int] = None
  vcsUrl: typing.Optional[str] = None
  

  def __str__(self):
    return f"""- name: {self.name}
  description: {self.description}
  size: {self.size}
  usedQuota: {naturalsize(self.usedQuota)}
"""



def plainToEntity(json: dict) -> Entity:
  obj = Entity()
  obj.collections = json.get('collections')
  obj.createdAt = datetime.fromisoformat(json['createdAt']) if json.get('createdAt') else None
  obj.createdBy = json.get('createdBy')
  obj.customData = json.get('customData')
  obj.defaultPrivate = bool(json['defaultPrivate']) if json.get('defaultPrivate') else None
  obj.deleted = bool(json['deleted']) if json.get('deleted') else None
  obj.deletedAt = datetime.fromisoformat(json['deletedAt']) if json.get('deletedAt') else None
  obj.description = json.get('description')
  obj.id = json.get('id')
  obj.name = json.get('name')
  obj.quota = json.get('quota')
  obj.size = json.get('size')
  obj.updatedAt = datetime.fromisoformat(json['updatedAt']) if json.get('updatedAt') else None
  obj.usedQuota = json.get('usedQuota')
  
  return obj

def serializeEntity(obj: Entity) -> dict:
  json = {}
  json['collections'] = obj.collections
  json['createdAt'] = obj.createdAt.isoformat() if obj.createdAt else None
  json['createdBy'] = obj.createdBy
  json['customData'] = obj.customData
  json['defaultPrivate'] = obj.defaultPrivate
  json['deleted'] = obj.deleted
  json['deletedAt'] = obj.deletedAt.isoformat() if obj.deletedAt else None
  json['description'] = obj.description
  json['id'] = obj.id
  json['name'] = obj.name
  json['quota'] = obj.quota
  json['size'] = obj.size
  json['updatedAt'] = obj.updatedAt.isoformat() if obj.updatedAt else None
  json['usedQuota'] = obj.usedQuota
  
  return json

@dataclass
class Entity:
  collections: typing.Optional[str] = None
  createdAt: typing.Optional[datetime] = None
  createdBy: typing.Optional[str] = None
  customData: typing.Optional[str] = None
  defaultPrivate: typing.Optional[bool] = None
  deleted: typing.Optional[bool] = None
  deletedAt: typing.Optional[datetime] = None
  description: typing.Optional[str] = None
  id: typing.Optional[str] = None
  name: typing.Optional[str] = None
  quota: typing.Optional[int] = None
  size: typing.Optional[int] = None
  updatedAt: typing.Optional[datetime] = None
  usedQuota: typing.Optional[int] = None
  

  def __str__(self):
    return f"""- name: {self.name}
  description: {self.description}
  size: {self.size}
  usedQuota: {naturalsize(self.usedQuota)}
"""



def plainToUser(json: dict) -> User:
  obj = User()
  obj.createdAt = datetime.fromisoformat(json['createdAt']) if json.get('createdAt') else None
  obj.createdBy = json.get('createdBy')
  obj.deleted = bool(json['deleted']) if json.get('deleted') else None
  obj.deletedAt = datetime.fromisoformat(json['deletedAt']) if json.get('deletedAt') else None
  obj.email = json.get('email')
  obj.firstname = json.get('firstname')
  obj.groups = [ plainToGroup(o) for o in json.get('groups', [])]
  obj.id = json.get('id')
  obj.isActive = bool(json['isActive']) if json.get('isActive') else None
  obj.isAdmin = bool(json['isAdmin']) if json.get('isAdmin') else None
  obj.lastname = json.get('lastname')
  obj.source = json.get('source')
  obj.updatedAt = datetime.fromisoformat(json['updatedAt']) if json.get('updatedAt') else None
  obj.username = json.get('username')
  
  return obj

def serializeUser(obj: User) -> dict:
  json = {}
  json['createdAt'] = obj.createdAt.isoformat() if obj.createdAt else None
  json['createdBy'] = obj.createdBy
  json['deleted'] = obj.deleted
  json['deletedAt'] = obj.deletedAt.isoformat() if obj.deletedAt else None
  json['email'] = obj.email
  json['firstname'] = obj.firstname
  json['groups'] = [ serializeGroup(o) for o in obj.groups ] if obj.groups is not None else []
  json['id'] = obj.id
  json['isActive'] = obj.isActive
  json['isAdmin'] = obj.isAdmin
  json['lastname'] = obj.lastname
  json['source'] = obj.source
  json['updatedAt'] = obj.updatedAt.isoformat() if obj.updatedAt else None
  json['username'] = obj.username
  
  return json

@dataclass
class User:
  createdAt: typing.Optional[datetime] = None
  createdBy: typing.Optional[str] = None
  deleted: typing.Optional[bool] = None
  deletedAt: typing.Optional[datetime] = None
  email: typing.Optional[str] = None
  firstname: typing.Optional[str] = None
  groups: list[Group] = field(default_factory=list)
  id: typing.Optional[str] = None
  isActive: typing.Optional[bool] = None
  isAdmin: typing.Optional[bool] = None
  lastname: typing.Optional[str] = None
  source: typing.Optional[str] = None
  updatedAt: typing.Optional[datetime] = None
  username: typing.Optional[str] = None
  



def plainToGroup(json: dict) -> Group:
  obj = Group()
  obj.createdAt = datetime.fromisoformat(json['createdAt']) if json.get('createdAt') else None
  obj.createdBy = json.get('createdBy')
  obj.deleted = bool(json['deleted']) if json.get('deleted') else None
  obj.deletedAt = datetime.fromisoformat(json['deletedAt']) if json.get('deletedAt') else None
  obj.email = json.get('email')
  obj.id = json.get('id')
  obj.name = json.get('name')
  obj.updatedAt = datetime.fromisoformat(json['updatedAt']) if json.get('updatedAt') else None
  
  return obj

def serializeGroup(obj: Group) -> dict:
  json = {}
  json['createdAt'] = obj.createdAt.isoformat() if obj.createdAt else None
  json['createdBy'] = obj.createdBy
  json['deleted'] = obj.deleted
  json['deletedAt'] = obj.deletedAt.isoformat() if obj.deletedAt else None
  json['email'] = obj.email
  json['id'] = obj.id
  json['name'] = obj.name
  json['updatedAt'] = obj.updatedAt.isoformat() if obj.updatedAt else None
  
  return json

@dataclass
class Group:
  createdAt: typing.Optional[datetime] = None
  createdBy: typing.Optional[str] = None
  deleted: typing.Optional[bool] = None
  deletedAt: typing.Optional[datetime] = None
  email: typing.Optional[str] = None
  id: typing.Optional[str] = None
  name: typing.Optional[str] = None
  updatedAt: typing.Optional[datetime] = None
  



def plainToManifest(json: dict) -> Manifest:
  obj = Manifest()
  obj.collection = json.get('collection')
  obj.collectionName = json.get('collectionName')
  obj.container = json.get('container')
  obj.containerName = json.get('containerName')
  obj.content = json.get('content')
  obj.createdAt = datetime.fromisoformat(json['createdAt']) if json.get('createdAt') else None
  obj.createdBy = json.get('createdBy')
  obj.downloadCount = json.get('downloadCount')
  obj.entity = json.get('entity')
  obj.entityName = json.get('entityName')
  obj.filename = json.get('filename')
  obj.hash = json.get('hash')
  obj.id = json.get('id')
  
  obj.images = json.get('images', [])
  
  obj.tags = json.get('tags', [])
  obj.total_size = json.get('total_size')
  obj.type = json.get('type')
  obj.updatedAt = datetime.fromisoformat(json['updatedAt']) if json.get('updatedAt') else None
  
  return obj

def serializeManifest(obj: Manifest) -> dict:
  json = {}
  json['collection'] = obj.collection
  json['collectionName'] = obj.collectionName
  json['container'] = obj.container
  json['containerName'] = obj.containerName
  json['content'] = obj.content
  json['createdAt'] = obj.createdAt.isoformat() if obj.createdAt else None
  json['createdBy'] = obj.createdBy
  json['downloadCount'] = obj.downloadCount
  json['entity'] = obj.entity
  json['entityName'] = obj.entityName
  json['filename'] = obj.filename
  json['hash'] = obj.hash
  json['id'] = obj.id
  json['images'] = obj.images
  json['tags'] = obj.tags
  json['total_size'] = obj.total_size
  json['type'] = obj.type
  json['updatedAt'] = obj.updatedAt.isoformat() if obj.updatedAt else None
  
  return json

@dataclass
class Manifest:
  collection: typing.Optional[str] = None
  collectionName: typing.Optional[str] = None
  container: typing.Optional[str] = None
  containerName: typing.Optional[str] = None
  content: typing.Optional[dict] = None
  createdAt: typing.Optional[datetime] = None
  createdBy: typing.Optional[str] = None
  downloadCount: typing.Optional[int] = None
  entity: typing.Optional[str] = None
  entityName: typing.Optional[str] = None
  filename: typing.Optional[str] = None
  hash: typing.Optional[str] = None
  id: typing.Optional[str] = None
  images: list[str] = field(default_factory=list)
  tags: list[str] = field(default_factory=list)
  total_size: typing.Optional[int] = None
  type: typing.Optional[str] = None
  updatedAt: typing.Optional[datetime] = None
  
  image_hash: typing.Optional[list[str]] = None

  def __str__(self):
    return f"""- filename: {self.filename}
  size: {naturalsize(self.total_size)}
  tags: {','.join(self.tags)}
"""



def plainToTagData(json: dict) -> TagData:
  obj = TagData()
  
  obj.tags = json.get('tags', [])
  
  return obj

def serializeTagData(obj: TagData) -> dict:
  json = {}
  json['tags'] = obj.tags
  
  return json

@dataclass
class TagData:
  tags: list[str] = field(default_factory=list)
  



def plainToToken(json: dict) -> Token:
  obj = Token()
  obj.comment = json.get('comment')
  obj.createdAt = datetime.fromisoformat(json['createdAt']) if json.get('createdAt') else None
  obj.createdBy = json.get('createdBy')
  obj.deleted = bool(json['deleted']) if json.get('deleted') else None
  obj.deletedAt = datetime.fromisoformat(json['deletedAt']) if json.get('deletedAt') else None
  obj.expiresAt = datetime.fromisoformat(json['expiresAt']) if json.get('expiresAt') else None
  obj.id = json.get('id')
  obj.source = json.get('source')
  obj.token = json.get('token')
  obj.updatedAt = datetime.fromisoformat(json['updatedAt']) if json.get('updatedAt') else None
  
  obj.user = plainToUser(json['user']) if json.get('user') else None
  
  return obj

def serializeToken(obj: Token) -> dict:
  json = {}
  json['comment'] = obj.comment
  json['createdAt'] = obj.createdAt.isoformat() if obj.createdAt else None
  json['createdBy'] = obj.createdBy
  json['deleted'] = obj.deleted
  json['deletedAt'] = obj.deletedAt.isoformat() if obj.deletedAt else None
  json['expiresAt'] = obj.expiresAt.isoformat() if obj.expiresAt else None
  json['id'] = obj.id
  json['source'] = obj.source
  json['token'] = obj.token
  json['updatedAt'] = obj.updatedAt.isoformat() if obj.updatedAt else None
  
  json['user'] = serializeUser(obj.user) if obj.user is not None else None
  
  return json

@dataclass
class Token:
  comment: typing.Optional[str] = None
  createdAt: typing.Optional[datetime] = None
  createdBy: typing.Optional[str] = None
  deleted: typing.Optional[bool] = None
  deletedAt: typing.Optional[datetime] = None
  expiresAt: typing.Optional[datetime] = None
  id: typing.Optional[str] = None
  source: typing.Optional[str] = None
  token: typing.Optional[str] = None
  updatedAt: typing.Optional[datetime] = None
  user: typing.Optional[User] = None
  


@dataclass
class Tag:
  name: str
  arch: typing.Optional[str] = None
  def __str__(self):
    return f"""- name: {self.name}
  arch: {self.arch}
"""