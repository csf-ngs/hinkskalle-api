import requests
import yaml
import os
import os.path
import typing
import click
import logging
import hashlib
import json
import io
import tarfile
import tempfile
import shutil
import re
from humanize import naturalsize
from calendar import timegm
from datetime import datetime, timedelta

logger = logging.getLogger()

from .auto.models import *

class HinkApi:
  config_file = '~/.hink_api.yml'
  def __init__(self, base=None, key=None):
    if not base:
      base = os.environ.get('HINK_API_BASE')
    if not key:
      key = os.environ.get('HINK_API_KEY')
    self.config_file = os.environ.get('HINK_API_CFG', self.config_file)
    try:
      with open(os.path.expanduser(self.config_file), 'r') as yml:
        cfg = yaml.load(yml, Loader=yaml.SafeLoader)
    except FileNotFoundError:
      cfg={}

    if not base:
      base=cfg.get('hink_api_base')
    if not key:
      key=cfg.get('hink_api_key')
    if not base:
      raise Exception("Please configure HINK_API_BASE!")

    self.base: str = base
    self.key: typing.Optional[str] = key
    self.staging_path: typing.Optional[str] = cfg.get('hink_api_staging_path')
    if self.base.endswith('/'):
      self.base = self.base[:-1]
    
    self.user: typing.Optional[User] = None

  def handle_error(self, r):
    try:
      json: dict = r.json()
    except:
      return r.raise_for_status()
    if 'errors' in json and type(json['errors']) is list:
      raise Exception(f"HINK-ERROR: {json['errors'][0]['detail']}")
    elif 'errors' in json and type(json['errors']) is dict:
      raise Exception(f"HINK-ERROR: {json['errors']}")
    elif 'message' in json:
      raise Exception(f"HINK-ERROR: {json['message']}")
    else:
      r.raise_for_status()
  
  def _make_headers(self, hdr: dict = {}) -> dict:
    if not self.key:
      raise Exception("Not authenticated, please login or provide a token")
    hdr['Authorization'] = f"Bearer {self.key}"
    return hdr
  
  def get(self, route, **kwargs):
    r = requests.get(self.base+route, headers=self._make_headers(), **kwargs)
    if r.status_code != requests.codes.ok:
      self.handle_error(r)
    return r.json().get('data', r.json())
  
  def post(self, route, data, **kwargs):
    r = requests.post(self.base+route, headers=self._make_headers(), json=data, **kwargs)
    if r.status_code != requests.codes.ok:
      self.handle_error(r)
    return r.json().get('data', r.json())
  
  def put(self, route, data, **kwargs):
    r = requests.put(self.base+route, headers=self._make_headers(), json=data, **kwargs)
    if r.status_code != requests.codes.ok:
      self.handle_error(r)
    return r.json().get('data', r.json())

  def get_current_user(self) -> User:
    ret = self.get('/v1/token-status')
    self.user = User(username=ret.get('username'), isAdmin=ret.get('isAdmin'))
    return self.user
  
  def _get_entity(self, entity: str = None) -> str:
    if not self.user:
      self.get_current_user()
    if not entity and self.user:
      entity = typing.cast(str, self.user.username)
    return typing.cast(str, entity)

  def get_token(self, username: str, password: str):
    ret = requests.post(f'{self.base}/v1/get-token', json={'username': username, 'password': password })
    if ret.status_code != requests.codes.ok:
      self.handle_error(ret)
    token = ret.json().get('data')
    try:
      with open(os.path.expanduser(self.config_file), 'r') as yml:
        cfg = yaml.load(yml, Loader=yaml.SafeLoader)
    except FileNotFoundError:
      cfg={}
    cfg['hink_api_key']=token.get('token')
    cfg['hink_api_base']=self.base
    with open(os.path.expanduser(self.config_file), 'w') as cfgfh:
      yaml.dump(cfg, cfgfh)
    self.token=plainToToken(token.get('token'))


  def list_collections(self, entity: str=None) -> typing.List[Collection]:
    entity = self._get_entity(entity)

    colls = self.get(f'/v1/collections/{entity}')
    return [ plainToCollection(c) for c in colls ]
  
  def get_collection(self, collection: str, entity: str=None) -> Collection:
    entity = self._get_entity(entity)
    coll = self.get(f'/v1/collections/{entity}/{collection}')
    return plainToCollection(coll)

  def create_collection(self, collection: Collection) -> Collection:
    coll = self.post(f'/v1/collections', serializeCollection(collection))
    return plainToCollection(coll)

  def update_collection(self, collection: Collection) -> Collection:
    coll = self.put(f'/v1/collections/{collection.entityName}/{collection.name}', serializeCollection(collection))
    return plainToCollection(coll)

  def list_containers(self, collection: str='default', entity: str=None) -> typing.List[Container]:
    entity = self._get_entity(entity)

    containers = self.get(f'/v1/containers/{entity}/{collection}')
    return [ plainToContainer(c) for c in containers ]
  
  def get_container(self, container: str, collection: str='default', entity: str=None) -> Container:
    entity = self._get_entity(entity)

    cont = self.get(f'/v1/containers/{entity}/{collection}/{container}')
    return plainToContainer(cont)
  
  def create_container(self, container: Container) -> Container:
    cont = self.post(f'/v1/containers', serializeContainer(container))
    return plainToContainer(cont)

  def update_container(self, container: Container) -> Container:
    cont = self.put(f'/v1/containers/{container.entityName}/{container.collectionName}/{container.name}', serializeContainer(container))  
    return plainToContainer(cont)


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
    ret: typing.List[Manifest] = []
    for m in manifests:
      mani = plainToManifest(m)
      mani.image_hash = m.get('images', [None])
      ret.append(mani)
    return ret
    
  def get_manifest(self, container: str, collection: str='default', entity: str=None, tag: str=None, hash: str=None) -> Manifest:
    entity = self._get_entity(entity)
    manifests = self.list_manifests(container, collection, entity)
    to_fetch: typing.Optional[Manifest] = None
    if not tag and not hash:
      raise Exception(f"Need either hash or tag")
    for m in manifests:
      if tag and tag in m.tags:
        to_fetch = m
        break
      elif hash and m.hash == hash:
        to_fetch = m
        break
    if not to_fetch:
      raise Exception(f"Manifest {entity}/{collection}/{container}:{tag}/{hash} not found")
    return to_fetch

  def fetch_blob(self, container: str, collection: str='default', entity: str=None, tag: str=None, hash: str=None, out: str = None, progress=False) -> str:
    to_fetch = self.get_manifest(container=container, collection=collection, entity=entity, tag=tag, hash=hash)

    ret = requests.get(f'{self.base}/v1/manifests/{to_fetch.id}/download', headers=self._make_headers(), stream=True)
    if ret.status_code != requests.codes.ok:
      self.handle_error(ret)
    
    if not to_fetch.filename:
      raise Exception('blob filename unset')
    outfn = to_fetch.filename
    if out and os.path.isdir(out):
      outfn = os.path.join(out, outfn)
    elif out:
      outfn = out
    logger.debug(f"will fetch {naturalsize(int(ret.headers.get('Content-Length', -1)))} to {outfn}")
    
    if progress:
      prog = click.progressbar(length=int(ret.headers.get('Content-Length', -1)), label='🥤 Slurping:')
    else:
      prog = None
    
    hl = hashlib.sha256()
    with open(os.path.basename(outfn), 'wb') as outfh:
      for chunk in ret.iter_content(chunk_size=65535): 
        outfh.write(chunk)
        if prog:
          prog.update(len(chunk))
        hl.update(chunk)
    if progress:
      print()

    if f"sha256:{hl.hexdigest()}" != ret.headers.get('Docker-Content-Digest'):
      raise Exception(f"Checksum mismatch: {hl.hexdigest()} != {ret.headers.get('Docker-Content-Digest')}")
    else:
      logger.info("Checksum ok.")

    return outfn
    
  def push_file(self, tag: str, container: str, filename: str, collection: str = 'default', entity: str = None, progress=False, excludes: typing.List[typing.Union[typing.Pattern, str]]=[], private=False) -> str:
    entity = self._get_entity(entity)
    is_tar = False
    orig_filename = filename
    if os.path.isdir(filename):
      if orig_filename.endswith('/'):
        orig_filename = orig_filename[:-1]
      is_tar = True
      filename = self._create_tar(filename, progress=progress, excludes=excludes)

    logging.info(f"⏳ Uploading file to {entity}/{collection}/{container}:{tag}...")
    with open(filename, 'rb') as infh:
      image_hash, image_size = self.push_blob(data=infh, entity=entity, collection=collection, container=container, progress=progress, private=private)

    logging.info("⏳ Uploading image config...")
    cfg=b'{}'
    with io.BytesIO(cfg) as cfgfh:
      cfg_hash, cfg_size = self.push_blob(data=cfgfh, entity=entity, collection=collection, container=container, progress=progress, private=private)
    
    manifest = {
      'schemaVersion': 2,
      "config": {
        'mediaType': 'application/vnd.unknown.config.v1+json',
        'digest': f'sha256:{cfg_hash}',
        'size': cfg_size,
      },
      "layers": [{
        "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip" if is_tar else "application/vnd.oci.image.layer.v1.tar",
        "digest": f"sha256:{image_hash}",
        "size": image_size,
        "annotations":{
          "io.deis.oras.content.unpack": "true" if is_tar else "false",
          "org.opencontainers.image.title": orig_filename,
        }
      }]
    }
    logging.info("⏳ Pushing manifest...")
    self.push_manifest(manifest=manifest, tag=tag, entity=entity, container=container, collection=collection)
    if is_tar:
      os.unlink(filename)
    return image_hash


  def push_manifest(self, manifest: dict, tag: str, container: str, collection: str = 'default', entity: str = None) -> str:
    json_manifest = json.dumps(manifest).encode('utf8')
    hl = hashlib.sha256()
    hl.update(json_manifest)
    manifest_hash = hl.hexdigest()

    ret = requests.put(f"{self.base}/v2/{entity}/{collection}/{container}/manifests/{tag}", data=json_manifest, headers=self._make_headers())
    if ret.status_code != requests.codes.ok:
      self.handle_error(ret)
    upload_hash = ret.headers.get('Docker-Content-Digest')
    if f"sha256:{manifest_hash}" != upload_hash:
      raise Exception(f"Manifest checksum mismatch: {manifest_hash} != {upload_hash}")
    return manifest_hash

  def _create_tar(self, directory: str, progress=False, excludes: typing.List[typing.Union[typing.Pattern, str]]=[]) -> str:
    tmpdir = tempfile.mkdtemp()
    tmptar = os.path.join(tmpdir, f"{directory.replace('/', '_')}.tar")
    tmp = open(tmptar, 'wb')
    tar = tarfile.open(fileobj=tmp, mode='w:gz')
    totar = []
    total_size = 0
    def is_match(fullpath: str) -> bool:
      skip = False
      for pat in excludes:
        if re.search(pat, fullpath):
          logger.debug(f"excluding {fullpath}, match with {pat}")
          print(f"excluding {fullpath}, match with {pat}")
          skip=True
          break
      return skip

    for root, dirs, files in os.walk(directory, topdown=True):
      dirs[:] = [ d for d in dirs if not is_match(os.path.join(root, d)) ]
      for f in files:
        fullpath = os.path.join(root, f)
        if is_match(fullpath):
          continue

        total_size+=os.path.getsize(fullpath)
        totar.append(fullpath)
    if progress:
      prog = click.progressbar(length=total_size, label='📦 Tarring:')
      prog.update(1)
    else:
      prog = None
    for f in sorted(totar):
      tar.add(f, recursive=False)
      if prog:
        prog.update(os.path.getsize(f))
    if progress:
      click.echo("")
    tar.close()
    tmp.close()
    return tmptar

  def push_blob(self, container: str, data: typing.BinaryIO, collection: str = 'default', entity: str = None, progress=False, private=False) -> typing.Tuple[str, int]:
    hl = hashlib.sha256()
    if progress:
      prog = click.progressbar(length=os.path.getsize(data.name) if hasattr(data, 'name') else 0,label='👀 Checksumming:')
    else:
      prog = None
    size = 0
    while True:
      chunk = data.read(65535)
      if len(chunk)==0:
        break
      size += len(chunk)
      hl.update(chunk)
      if prog:
        prog.update(len(chunk))
    data.seek(0)
    if progress:
      click.echo("")
    
    image_hash = hl.hexdigest()
    check = requests.head(f"{self.base}/v2/{entity}/{collection}/{container}/blobs/sha256:{image_hash}", headers=self._make_headers())
    if check.status_code == requests.codes.ok:
      if not check.headers.get('Docker-Content-Digest'):
        raise Exception("something went wrong - no content digest header!")
      logger.info(f"😎 File already on server, skipping upload.")
      return image_hash, size
    
    if size > 100*1024*1024 and self.staging_path:
      logger.info(f"📥 switching to staged upload")
      staged_fn = os.path.join(self.staging_path, f"sha256.{image_hash}")
      os.makedirs(self.staging_path, exist_ok=True)
      with open(staged_fn, 'wb') as staged_fh:
        shutil.copyfileobj(data, staged_fh)
      ret = requests.post(f"{self.base}/v2/{entity}/{collection}/{container}/blobs/uploads/", params={ 'staged': 1, 'digest': f'sha256:{image_hash}', 'private': private }, headers=self._make_headers({ 'Content-Type': 'application/octet-stream' }))
      if ret.status_code != requests.codes.ok:
        self.handle_error(ret)
      return image_hash, size


    class MonitoredFile(io.BytesIO):
      def __init__(self, hdl: typing.BinaryIO, length: int):
        self.hdl = hdl
        self.hdl.seek(0)
        self.length = length
        self.prog = None
        if progress:
          self.prog = click.progressbar(length=length, label='🚀 Pushing:')
      
      def read(self, size=-1) -> bytes:
        if self.prog:
          self.prog.update(size)
        return self.hdl.read(size)

      def __len__(self):
        return self.length

    ret = requests.post(f"{self.base}/v2/{entity}/{collection}/{container}/blobs/uploads/", params={ 'digest': f'sha256:{image_hash}', 'private': private }, data=MonitoredFile(data, size), headers=self._make_headers({ 'Content-Type': 'application/octet-stream' }))
    if ret.status_code != requests.codes.ok:
      self.handle_error(ret)
    if progress:
      click.echo("")
    return image_hash, size

  def get_download_token(self, manifest: typing.Optional[Manifest]=None, tag: str = None, container: str = None, collection: str = 'default', entity: str = None, expiration=None, username=None) -> str:
    if not manifest:
      entity = self._get_entity(entity)
      if not container or not tag:
        raise Exception(f"container and tag are required")

      to_fetch = self.get_manifest(tag=tag, container=container, collection=collection, entity=entity)
    else:
      to_fetch = manifest

    post_data = {
      'type': 'manifest',
      'id': to_fetch.id,
    }
    if not self.user:
      raise Exception("user not defined")
    if self.user.isAdmin:
      if not username:
        if entity == 'default':
          username = self.user.username
        else:
          username = entity

      if not expiration:
        expiration = 14
      try:
        expiration = timegm((datetime.utcnow() + timedelta(days=int(expiration))).utctimetuple())
      except ValueError:
        raise Exception("expiration must be a int (days)")

      post_data['username'] = username
      post_data['exp'] = expiration

    ret = self.post('/v1/get-download-token', data=post_data)
    return ret['location']