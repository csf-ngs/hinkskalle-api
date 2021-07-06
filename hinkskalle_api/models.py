from humanize import naturalsize
from dataclasses import dataclass, field
import typing

@dataclass
class BaseModel:
  name: str 
  description: str
  size: int = 0
  usedQuota: int = 0

  def __str__(self):
    return f"""- name: {self.name}
  description: {self.description}
  size: {self.size}
  usedQuota: {naturalsize(self.usedQuota)}
"""

@dataclass
class User:
  username: str
  is_admin: bool

@dataclass
class Entity(BaseModel):
  pass

@dataclass
class Collection(BaseModel):
  pass

@dataclass
class Container(BaseModel):
  type: typing.Optional[str] = None

  def __str__(self):
    out = super().__str__()
    out += f"  type: {self.type}\n"
    return out

@dataclass
class Tag:
  name: str
  arch: typing.Optional[str] = None
  def __str__(self):
    return f"""- name: {self.name}
  arch: {self.arch}
"""


@dataclass
class Manifest:
  id: int
  hash: str
  filename: str
  type: str
  total_size: str
  tags: typing.List[Tag] = field(default_factory=list)
  image_hash: typing.Optional[str] = None

  def __str__(self):
    return f"""- filename: {self.filename}
  size: {naturalsize(self.total_size)}
  tags: {','.join([ t.name for t in self.tags ])}
"""
