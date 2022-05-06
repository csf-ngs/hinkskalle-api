from __future__ import annotations
from dataclasses import dataclass, field
import typing
from datetime import datetime
from humanize import naturalsize




def plainToCollection(json: dict) -> Collection:
  obj = Collection()
  obj.canEdit = bool(json['canEdit']) if json.get('canEdit') is not None else None
  
  obj.containers = json['containers'] if json.get('containers') is not None and isinstance(json['containers'], list) else []
  obj.createdAt = datetime.fromisoformat(json['createdAt']) if json.get('createdAt') is not None else None
  obj.createdBy = json.get('createdBy')
  obj.customData = json.get('customData')
  obj.deleted = bool(json['deleted']) if json.get('deleted') is not None else None
  obj.deletedAt = datetime.fromisoformat(json['deletedAt']) if json.get('deletedAt') is not None else None
  obj.description = json.get('description')
  obj.entity = json.get('entity')
  obj.entityName = json.get('entityName')
  obj.id = json.get('id')
  obj.name = json.get('name')
  obj.private = bool(json['private']) if json.get('private') is not None else None
  obj.size = json.get('size')
  obj.updatedAt = datetime.fromisoformat(json['updatedAt']) if json.get('updatedAt') is not None else None
  obj.usedQuota = json.get('usedQuota')
  
  return obj

def serializeCollection(obj: Collection) -> dict:
  json = {}
  json['createdBy'] = obj.createdBy
  json['customData'] = obj.customData
  json['description'] = obj.description
  json['entity'] = obj.entity
  json['name'] = obj.name
  json['private'] = obj.private
  
  return json

@dataclass
class Collection:
  canEdit: typing.Optional[bool] = None
  containers: list[str] = field(default_factory=list)
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
  obj.canEdit = bool(json['canEdit']) if json.get('canEdit') is not None else None
  obj.collection = json.get('collection')
  obj.collectionName = json.get('collectionName')
  obj.createdAt = datetime.fromisoformat(json['createdAt']) if json.get('createdAt') is not None else None
  obj.createdBy = json.get('createdBy')
  obj.customData = json.get('customData')
  obj.deleted = bool(json['deleted']) if json.get('deleted') is not None else None
  obj.deletedAt = datetime.fromisoformat(json['deletedAt']) if json.get('deletedAt') is not None else None
  obj.description = json.get('description')
  obj.downloadCount = json.get('downloadCount')
  obj.entity = json.get('entity')
  obj.entityName = json.get('entityName')
  obj.fullDescription = json.get('fullDescription')
  obj.id = json.get('id')
  obj.imageTags = json.get('imageTags')
  
  obj.images = json['images'] if json.get('images') is not None and isinstance(json['images'], list) else []
  obj.name = json.get('name')
  obj.private = bool(json['private']) if json.get('private') is not None else None
  obj.readOnly = bool(json['readOnly']) if json.get('readOnly') is not None else None
  obj.size = json.get('size')
  obj.stars = json.get('stars')
  obj.type = json.get('type')
  obj.updatedAt = datetime.fromisoformat(json['updatedAt']) if json.get('updatedAt') is not None else None
  obj.usedQuota = json.get('usedQuota')
  obj.vcsUrl = json.get('vcsUrl')
  
  return obj

def serializeContainer(obj: Container) -> dict:
  json = {}
  json['collection'] = obj.collection
  json['createdBy'] = obj.createdBy
  json['customData'] = obj.customData
  json['description'] = obj.description
  json['fullDescription'] = obj.fullDescription
  json['name'] = obj.name
  json['private'] = obj.private
  json['readOnly'] = obj.readOnly
  json['vcsUrl'] = obj.vcsUrl
  
  return json

@dataclass
class Container:
  archTags: typing.Optional[dict] = None
  canEdit: typing.Optional[bool] = None
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
  images: list[str] = field(default_factory=list)
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
  obj.canEdit = bool(json['canEdit']) if json.get('canEdit') is not None else None
  
  obj.collections = json['collections'] if json.get('collections') is not None and isinstance(json['collections'], list) else []
  obj.createdAt = datetime.fromisoformat(json['createdAt']) if json.get('createdAt') is not None else None
  obj.createdBy = json.get('createdBy')
  obj.customData = json.get('customData')
  obj.defaultPrivate = bool(json['defaultPrivate']) if json.get('defaultPrivate') is not None else None
  obj.deleted = bool(json['deleted']) if json.get('deleted') is not None else None
  obj.deletedAt = datetime.fromisoformat(json['deletedAt']) if json.get('deletedAt') is not None else None
  obj.description = json.get('description')
  obj.groupRef = json.get('groupRef')
  obj.id = json.get('id')
  obj.isGroup = bool(json['isGroup']) if json.get('isGroup') is not None else None
  obj.name = json.get('name')
  obj.quota = json.get('quota')
  obj.size = json.get('size')
  obj.updatedAt = datetime.fromisoformat(json['updatedAt']) if json.get('updatedAt') is not None else None
  obj.usedQuota = json.get('usedQuota')
  
  return obj

def serializeEntity(obj: Entity) -> dict:
  json = {}
  json['createdBy'] = obj.createdBy
  json['customData'] = obj.customData
  json['defaultPrivate'] = obj.defaultPrivate
  json['description'] = obj.description
  json['name'] = obj.name
  json['quota'] = obj.quota
  
  return json

@dataclass
class Entity:
  canEdit: typing.Optional[bool] = None
  collections: list[str] = field(default_factory=list)
  createdAt: typing.Optional[datetime] = None
  createdBy: typing.Optional[str] = None
  customData: typing.Optional[str] = None
  defaultPrivate: typing.Optional[bool] = None
  deleted: typing.Optional[bool] = None
  deletedAt: typing.Optional[datetime] = None
  description: typing.Optional[str] = None
  groupRef: typing.Optional[str] = None
  id: typing.Optional[str] = None
  isGroup: typing.Optional[bool] = None
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



def plainToImage(json: dict) -> Image:
  obj = Image()
  obj.arch = json.get('arch')
  obj.blob = json.get('blob')
  obj.canEdit = bool(json['canEdit']) if json.get('canEdit') is not None else None
  obj.collection = json.get('collection')
  obj.collectionName = json.get('collectionName')
  obj.container = json.get('container')
  obj.containerDownloads = json.get('containerDownloads')
  obj.containerName = json.get('containerName')
  obj.containerStars = json.get('containerStars')
  obj.createdAt = datetime.fromisoformat(json['createdAt']) if json.get('createdAt') is not None else None
  obj.createdBy = json.get('createdBy')
  obj.customData = json.get('customData')
  obj.deleted = bool(json['deleted']) if json.get('deleted') is not None else None
  obj.deletedAt = datetime.fromisoformat(json['deletedAt']) if json.get('deletedAt') is not None else None
  obj.description = json.get('description')
  obj.downloadCount = json.get('downloadCount')
  obj.encrypted = bool(json['encrypted']) if json.get('encrypted') is not None else None
  obj.entity = json.get('entity')
  obj.entityName = json.get('entityName')
  obj.expiresAt = datetime.fromisoformat(json['expiresAt']) if json.get('expiresAt') is not None else None
  
  obj.fingerprints = json['fingerprints'] if json.get('fingerprints') is not None and isinstance(json['fingerprints'], list) else []
  obj.hash = json.get('hash')
  obj.id = json.get('id')
  obj.signatureVerified = bool(json['signatureVerified']) if json.get('signatureVerified') is not None else None
  obj.signed = bool(json['signed']) if json.get('signed') is not None else None
  obj.size = json.get('size')
  
  obj.tags = json['tags'] if json.get('tags') is not None and isinstance(json['tags'], list) else []
  obj.type = json.get('type')
  obj.updatedAt = datetime.fromisoformat(json['updatedAt']) if json.get('updatedAt') is not None else None
  obj.uploadState = json.get('uploadState')
  
  return obj

def serializeImage(obj: Image) -> dict:
  json = {}
  json['arch'] = obj.arch
  json['blob'] = obj.blob
  json['container'] = obj.container
  json['customData'] = obj.customData
  json['description'] = obj.description
  json['encrypted'] = obj.encrypted
  json['expiresAt'] = obj.expiresAt.isoformat() if obj.expiresAt else None
  json['hash'] = obj.hash
  json['uploadState'] = obj.uploadState
  
  return json

@dataclass
class Image:
  arch: typing.Optional[str] = None
  blob: typing.Optional[str] = None
  canEdit: typing.Optional[bool] = None
  collection: typing.Optional[str] = None
  collectionName: typing.Optional[str] = None
  container: typing.Optional[str] = None
  containerDownloads: typing.Optional[int] = None
  containerName: typing.Optional[str] = None
  containerStars: typing.Optional[int] = None
  createdAt: typing.Optional[datetime] = None
  createdBy: typing.Optional[str] = None
  customData: typing.Optional[str] = None
  deleted: typing.Optional[bool] = None
  deletedAt: typing.Optional[datetime] = None
  description: typing.Optional[str] = None
  downloadCount: typing.Optional[int] = None
  encrypted: typing.Optional[bool] = None
  entity: typing.Optional[str] = None
  entityName: typing.Optional[str] = None
  expiresAt: typing.Optional[datetime] = None
  fingerprints: list[str] = field(default_factory=list)
  hash: typing.Optional[str] = None
  id: typing.Optional[str] = None
  signatureVerified: typing.Optional[bool] = None
  signed: typing.Optional[bool] = None
  size: typing.Optional[int] = None
  tags: list[str] = field(default_factory=list)
  type: typing.Optional[str] = None
  updatedAt: typing.Optional[datetime] = None
  uploadState: typing.Optional[str] = None
  



def plainToUser(json: dict) -> User:
  obj = User()
  obj.canEdit = bool(json['canEdit']) if json.get('canEdit') is not None else None
  obj.createdAt = datetime.fromisoformat(json['createdAt']) if json.get('createdAt') is not None else None
  obj.createdBy = json.get('createdBy')
  obj.deleted = bool(json['deleted']) if json.get('deleted') is not None else None
  obj.deletedAt = datetime.fromisoformat(json['deletedAt']) if json.get('deletedAt') is not None else None
  obj.email = json.get('email')
  obj.firstname = json.get('firstname')
  obj.id = json.get('id')
  obj.isActive = bool(json['isActive']) if json.get('isActive') is not None else None
  obj.isAdmin = bool(json['isAdmin']) if json.get('isAdmin') is not None else None
  obj.lastname = json.get('lastname')
  obj.source = json.get('source')
  obj.updatedAt = datetime.fromisoformat(json['updatedAt']) if json.get('updatedAt') is not None else None
  obj.username = json.get('username')
  
  return obj

def serializeUser(obj: User) -> dict:
  json = {}
  json['email'] = obj.email
  json['firstname'] = obj.firstname
  json['isActive'] = obj.isActive
  json['isAdmin'] = obj.isAdmin
  json['lastname'] = obj.lastname
  json['source'] = obj.source
  json['username'] = obj.username
  
  return json

@dataclass
class User:
  canEdit: typing.Optional[bool] = None
  createdAt: typing.Optional[datetime] = None
  createdBy: typing.Optional[str] = None
  deleted: typing.Optional[bool] = None
  deletedAt: typing.Optional[datetime] = None
  email: typing.Optional[str] = None
  firstname: typing.Optional[str] = None
  id: typing.Optional[str] = None
  isActive: typing.Optional[bool] = None
  isAdmin: typing.Optional[bool] = None
  lastname: typing.Optional[str] = None
  source: typing.Optional[str] = None
  updatedAt: typing.Optional[datetime] = None
  username: typing.Optional[str] = None
  

  @property
  def is_admin(self) -> bool:
    return self.isAdmin if self.isAdmin is not None else False



def plainToGroup(json: dict) -> Group:
  obj = Group()
  obj.canEdit = bool(json['canEdit']) if json.get('canEdit') is not None else None
  obj.collections = json.get('collections')
  obj.createdAt = datetime.fromisoformat(json['createdAt']) if json.get('createdAt') is not None else None
  obj.createdBy = json.get('createdBy')
  obj.deleted = bool(json['deleted']) if json.get('deleted') is not None else None
  obj.deletedAt = datetime.fromisoformat(json['deletedAt']) if json.get('deletedAt') is not None else None
  obj.description = json.get('description')
  obj.email = json.get('email')
  obj.entityRef = json.get('entityRef')
  obj.id = json.get('id')
  obj.name = json.get('name')
  obj.updatedAt = datetime.fromisoformat(json['updatedAt']) if json.get('updatedAt') is not None else None
  obj.users = [ 
    plainToGroupMember(o) for o in (json['users'] if json.get('users') is not None and isinstance(json['users'], list) else [])
  ]
  
  return obj

def serializeGroup(obj: Group) -> dict:
  json = {}
  json['createdBy'] = obj.createdBy
  json['description'] = obj.description
  json['email'] = obj.email
  json['name'] = obj.name
  
  return json

@dataclass
class Group:
  canEdit: typing.Optional[bool] = None
  collections: typing.Optional[int] = None
  createdAt: typing.Optional[datetime] = None
  createdBy: typing.Optional[str] = None
  deleted: typing.Optional[bool] = None
  deletedAt: typing.Optional[datetime] = None
  description: typing.Optional[str] = None
  email: typing.Optional[str] = None
  entityRef: typing.Optional[str] = None
  id: typing.Optional[str] = None
  name: typing.Optional[str] = None
  updatedAt: typing.Optional[datetime] = None
  users: list[GroupMember] = field(default_factory=list)
  



def plainToGroupMember(json: dict) -> GroupMember:
  obj = GroupMember()
  obj.role = json.get('role')
  
  obj.user = plainToUser(json['user']) if json.get('user') is not None else None
  
  return obj

def serializeGroupMember(obj: GroupMember) -> dict:
  json = {}
  json['role'] = obj.role
  
  json['user'] = serializeUser(obj.user) if obj.user is not None else None
  
  return json

@dataclass
class GroupMember:
  role: typing.Optional[str] = None
  user: typing.Optional[User] = None
  



def plainToManifest(json: dict) -> Manifest:
  obj = Manifest()
  obj.collection = json.get('collection')
  obj.collectionName = json.get('collectionName')
  obj.container = json.get('container')
  obj.containerName = json.get('containerName')
  obj.content = json.get('content')
  obj.createdAt = datetime.fromisoformat(json['createdAt']) if json.get('createdAt') is not None else None
  obj.createdBy = json.get('createdBy')
  obj.downloadCount = json.get('downloadCount')
  obj.entity = json.get('entity')
  obj.entityName = json.get('entityName')
  obj.filename = json.get('filename')
  obj.hash = json.get('hash')
  obj.id = json.get('id')
  
  obj.images = json['images'] if json.get('images') is not None and isinstance(json['images'], list) else []
  
  obj.tags = json['tags'] if json.get('tags') is not None and isinstance(json['tags'], list) else []
  obj.total_size = json.get('total_size')
  obj.type = json.get('type')
  obj.updatedAt = datetime.fromisoformat(json['updatedAt']) if json.get('updatedAt') is not None else None
  
  return obj

def serializeManifest(obj: Manifest) -> dict:
  json = {}
  json['collection'] = obj.collection
  json['container'] = obj.container
  json['content'] = obj.content
  json['entity'] = obj.entity
  json['hash'] = obj.hash
  
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
  
  obj.tags = json['tags'] if json.get('tags') is not None and isinstance(json['tags'], list) else []
  
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
  obj.createdAt = datetime.fromisoformat(json['createdAt']) if json.get('createdAt') is not None else None
  obj.createdBy = json.get('createdBy')
  obj.deleted = bool(json['deleted']) if json.get('deleted') is not None else None
  obj.deletedAt = datetime.fromisoformat(json['deletedAt']) if json.get('deletedAt') is not None else None
  obj.expiresAt = datetime.fromisoformat(json['expiresAt']) if json.get('expiresAt') is not None else None
  obj.generatedToken = json.get('generatedToken')
  obj.id = json.get('id')
  obj.key_uid = json.get('key_uid')
  obj.source = json.get('source')
  obj.updatedAt = datetime.fromisoformat(json['updatedAt']) if json.get('updatedAt') is not None else None
  
  obj.user = plainToUser(json['user']) if json.get('user') is not None else None
  
  return obj

def serializeToken(obj: Token) -> dict:
  json = {}
  json['comment'] = obj.comment
  json['expiresAt'] = obj.expiresAt.isoformat() if obj.expiresAt else None
  
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
  generatedToken: typing.Optional[str] = None
  id: typing.Optional[str] = None
  key_uid: typing.Optional[str] = None
  source: typing.Optional[str] = None
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