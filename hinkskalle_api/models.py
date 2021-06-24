from humanize import naturalsize
import typing

class BaseModel:
  def __init__(self, name: str, description: str, size: int = 0, usedQuota: int = 0):
    self.name = name
    self.description = description
    self.size = size
    self.usedQuota = usedQuota

  def __str__(self):
    return f"""- name: {self.name}
  description: {self.description}
  size: {self.size}
  usedQuota: {naturalsize(self.usedQuota)}
"""

class User:
  def __init__(self, username: str, is_admin: bool):
    self.username = username
    self.is_admin = is_admin

class Entity(BaseModel):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

class Collection(BaseModel):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

class Container(BaseModel):
  def __init__(self, type: str, **kwargs):
    super().__init__(**kwargs)
    self.type=type

  def __str__(self):
    out = super().__str__()
    out += f"  type: {self.type}\n"
    return out

class Tag:
  def __init__(self, name: str, arch: str = None):
    self.name=name
    self.arch=arch
  def __str__(self):
    return f"""- name: {self.name}
  arch: {self.arch}
"""

class Manifest:
  def __init__(self, id: int, hash: str, filename: str, type: str, total_size: str, tags: typing.List[Tag], image_hash=None):
    self.id = id
    self.hash = hash
    self.filename = filename
    self.type = type
    self.total_size = total_size
    self.tags = tags
    self.image_hash = image_hash

  def __str__(self):
    return f"""- filename: {self.filename}
  size: {naturalsize(self.total_size)}
  tags: {','.join([ t.name for t in self.tags ])}
"""
