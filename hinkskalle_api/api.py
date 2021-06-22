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
from humanize import naturalsize

logger = logging.getLogger()

from .models import *

class HinkApi:
  config_file = '~/.hink_api.yml'
  def __init__(self, base=None, key=None):
    if not base:
      base = os.environ.get('HINK_API_BASE')
    if not key:
      key = os.environ.get('HINK_API_KEY')
    if not base or not key:
      self.config_file = os.environ.get('HINK_API_CFG', self.config_file)
      with open(os.path.expanduser(self.config_file), 'r') as yml:
          cfg = yaml.load(yml, Loader=yaml.SafeLoader)
      if not base:
          base=cfg.get('hink_api_base')
      if not key:
          key=cfg.get('hink_api_key')
    if not base:
      raise Exception("Please configure HINK_API_BASE!")
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
    if 'errors' in json:
      raise Exception(f"HINK-ERROR: {json['errors'][0]['detail']}")
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
    r = requests.get(self.base+route, headers=self._make_headers())
    if r.status_code != requests.codes.ok:
      self.handle_error(r)
    return r.json().get('data', **kwargs)
  
  def post(self, route, data, **kwargs):
    r = requests.post(self.base+route, headers=self._make_headers(), json=data, **kwargs)
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

  def get_token(self, username: str, password: str):
    ret = requests.post(f'{self.base}/v1/get-token', json={'username': username, 'password': password })
    if ret.status_code != requests.codes.ok:
      self.handle_error(ret)
    token = ret.json().get('data')
    with open(os.path.expanduser(self.config_file), 'r') as yml:
      cfg = yaml.load(yml, Loader=yaml.SafeLoader)
    cfg['hink_api_key']=token.get('token')
    with open(os.path.expanduser(self.config_file), 'w') as cfgfh:
      yaml.dump(cfg, cfgfh)


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
        id=m.get('id'),
        hash=m.get('hash'), 
        filename=m.get('filename'), 
        type=m.get('type'),
        total_size=m.get('total_size'),
        tags=[ Tag(name=t) for t in m.get('tags') ],
      ) for m in manifests ]
    
  def fetch_blob(self, container: str, collection: str='default', entity: str=None, tag: str=None, hash: str=None, out: str = None, progress=False) -> str:
    manifests = self.list_manifests(container, collection, entity)
    to_fetch: typing.Optional[Manifest] = None
    if not tag and not hash:
      raise Exception(f"Need either hash or tag")
    for m in manifests:
      if tag and tag in [ t.name for t in m.tags ]:
        to_fetch = m
        break
      elif hash and m.hash == hash:
        to_fetch = m
        break
    if not to_fetch:
      raise Exception("Manifest not found")

    ret = requests.get(f'{self.base}/v1/manifests/{m.id}/download', headers=self._make_headers(), stream=True)
    if ret.status_code != requests.codes.ok:
      self.handle_error(ret)
    
    outfn = to_fetch.filename
    if out and os.path.isdir(out):
      outfn = os.path.join(out, outfn)
    elif out:
      outfn = out
    logger.debug(f"will fetch {naturalsize(int(ret.headers.get('Content-Length', -1)))} to {outfn}")
    
    if progress:
      prog = click.progressbar(length=int(ret.headers.get('Content-Length', -1)), label='🥤 Slurping:')
    
    hl = hashlib.sha256()
    with open(outfn, 'wb') as outfh:
      for chunk in ret.iter_content(chunk_size=65535): 
        outfh.write(chunk)
        if progress:
          prog.update(len(chunk))
        hl.update(chunk)
    if progress:
      print()

    if f"sha256:{hl.hexdigest()}" != ret.headers.get('Docker-Content-Digest'):
      raise Exception(f"Checksum mismatch: {hl.hexdigest()} != {ret.headers.get('Docker-Content-Digest')}")
    else:
      logger.info("Checksum ok.")

    return outfn
    
  def push_file(self, tag: str, container: str, filename: str, collection: str = 'default', entity: str = None, progress=False):
    entity = self._get_entity(entity)
    logging.info("🚀 Uploading file...")
    is_tar = False
    orig_filename = filename
    if os.path.isdir(filename):
      if orig_filename.endswith('/'):
        orig_filename = orig_filename[:-1]
      is_tar = True
      filename = self._create_tar(filename, progress=progress)

    with open(filename, 'rb') as infh:
      image_hash, image_size = self.push_blob(data=infh, entity=entity, collection=collection, container=container, progress=progress)

    logging.info("🚀 Uploading image config")
    cfg=b'{}'
    with io.BytesIO(cfg) as cfgfh:
      cfg_hash, cfg_size = self.push_blob(data=cfgfh, entity=entity, collection=collection, container=container, progress=progress)
    
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
          "org.opencontainers.image.title": os.path.basename(orig_filename)},
        }
      ]
    }
    logging.info("🚀 Pushing manifest")
    self.push_manifest(manifest=manifest, tag=tag, entity=entity, container=container, collection=collection)
    if is_tar:
      os.unlink(filename)


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

  def _create_tar(self, directory: str, progress=False) -> str:
    tmpdir = tempfile.mkdtemp()
    tmptar = os.path.join(tmpdir, f"{directory}.tar")
    tmp = open(tmptar, 'wb')
    tar = tarfile.open(fileobj=tmp, mode='w:gz')
    totar = []
    total_size = 0
    for root, dirs, files in os.walk(directory, topdown=True):
      for f in files:
        fullpath = os.path.join(root, f)
        total_size+=os.path.getsize(fullpath)
        totar.append(fullpath)
    if progress:
      prog = click.progressbar(length=total_size, label='📦 Tarring:')
    for f in sorted(totar):
      tar.add(f, recursive=False)
      if progress:
        prog.update(os.path.getsize(f))
    if progress:
      click.echo("")
    tar.close()
    tmp.close()
    return tmptar

  def push_blob(self, container: str, data: typing.Optional[typing.IO[typing.Any]] = None, collection: str = 'default', entity: str = None, progress=False) -> typing.Tuple[str, int]:
    hl = hashlib.sha256()
    if progress:
      prog = click.progressbar(length=os.path.getsize(data.name) if hasattr(data, 'name') else 0,label='👀 Checksumming:')
    size = 0
    while True:
      chunk = data.read(65535)
      if len(chunk)==0:
        break
      size += len(chunk)
      hl.update(chunk)
      if progress:
        prog.update(len(chunk))
    data.seek(0)
    if progress:
      click.echo("")
    
    image_hash = hl.hexdigest()
    check = requests.head(f"{self.base}/v2/{entity}/{collection}/{container}/blobs/sha256:{image_hash}", headers=self._make_headers())
    if check.status_code == requests.codes.ok:
      logger.info(f"File already on server, skipping upload.")
      return image_hash, size
    ret = requests.post(f"{self.base}/v2/{entity}/{collection}/{container}/blobs/uploads/", params={ 'digest': f'sha256:{image_hash}'}, data=data, headers=self._make_headers({ 'Content-Type': 'application/octet-stream' }))
    if ret.status_code != requests.codes.ok:
      self.handle_error(ret)
    return image_hash, size



