import requests
import yaml
import os
import os.path

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
    if not self.base.endswith('/'):
      self.base += '/'

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
    r = requests.get(self.base+route)
    if r.status_code != requests.codes.ok:
      self.handle_error(r)
    return r.json()
  
  def post(self, route, data):
    r = requests.post(self.base+route, headers=self._make_headers(), json=data)
    if r.status_code != requests.codes.ok:
      self.handle_error(r)
    return r.json()



