import requests
import yaml
import os
import os.path
import typing
from humanize import naturalsize

from .models import *

class HinkApi:
  def __init__(self, base=None, key=None):
    if not base:
      base = os.environ.get('HINK_API_BASE')
    if not key:
      key = os.environ.get('HINK_API_KEY')
    if not base or not key:
      cfgfile = os.environ.get('HINK_API_CFG', '~/.hink_api.yml')
      with open(os.path.expanduser(cfgfile), 'rb') as yml:
          cfg = yaml.load(yml, Loader=yaml.SafeLoader)
      if not base:
          base=cfg.get('hink_api_base')
      if not key:
          key=cfg.get('hink_api_key')
    if not base or not key:
      raise Exception("Please configure HINK_API_BASE and HINK_API_KEY!")
    self.base: str = base
    self.key: str = key    
    if self.base.endswith('/'):
      self.base = self.base[:-1]
    
    self.user: typing.Optional[User] = None

  def handle_error(self, r):
    try:
      json: dict = r.json()
    except:
      return r.raise_for_status()
    if 'message' in json:
      raise Exception(f"HINK-ERROR: {json['message']}")
    else:
      r.raise_for_status()
  
  def _make_headers(self, hdr: dict = {}) -> dict:
    hdr['Authorization'] = f"Bearer {self.key}"
    return hdr
  
  def get(self, route):
    r = requests.get(self.base+route, headers=self._make_headers())
    if r.status_code != requests.codes.ok:
      self.handle_error(r)
    return r.json().get('data')
  
  def post(self, route, data):
    r = requests.post(self.base+route, headers=self._make_headers(), json=data)
    if r.status_code != requests.codes.ok:
      self.handle_error(r)
    return r.json().get('data')

  def get_current_user(self) -> User:
    ret = self.get('/v1/token-status')
    self.user = User(username=ret.get('username'))
    return self.user
  
  def _get_entity(self, entity: str = None) -> str:
    if not self.user:
      self.get_current_user()
    if not entity:
      entity = self.user.username
    return entity


  def list_collections(self, entity: str=None) -> typing.List[Collection]:
    entity = self._get_entity(entity)

    colls = self.get(f'/v1/collections/{entity}')
    return [ Collection(
        name=c.get('name'), 
        description=c.get('description'), 
        size=c.get('size'), 
        usedQuota=c.get('usedQuota')) for c in colls ]

  def list_containers(self, collection: str='default', entity: str=None) -> typing.List[Container]:
    entity = self._get_entity(entity)

    containers = self.get(f'/v1/containers/{entity}/{collection}')
    return [ Container(
        name=c.get('name'), 
        type=c.get('type'), 
        description=c.get('description'), 
        size=c.get('size'), 
        usedQuota=c.get('usedQuota')) for c in containers ]

  def list_tags(self, container: str, collection: str='default', entity: str=None) -> typing.List[Tag]:
    entity = self._get_entity(entity)

    ret = self.get(f'/v1/containers/{entity}/{collection}/{container}')
    tags = self.get(f'/v2/tags/{ret.get("id")}')
    ret = []
    for arch in tags:
      for tag in tags[arch]:
        ret.append(Tag(name=tag, arch=arch))
    return ret

  def list_manifests(self, container: str, collection: str='default', entity: str=None) -> typing.List[Manifest]:
    entity = self._get_entity(entity)

    manifests = self.get(f'/v1/containers/{entity}/{collection}/{container}/manifests')
    return [ Manifest(
        hash=m.get('hash'), 
        filename=m.get('filename'), 
        type=m.get('type'),
        total_size=m.get('total_size'),
        tags=[ Tag(name=t) for t in m.get('tags') ],
      ) for m in manifests ]
