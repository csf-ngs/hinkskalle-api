"""Console script for hinkskalle_api."""
import re
import sys
import click
import click_log
import logging
import typing

logger = logging.getLogger()
click_log.basic_config(logger)
from hinkskalle_api import HinkApi


@click.group()
@click_log.simple_verbosity_option(logger)
@click.option('--base', help='API Base URL')
@click.option('--key', help='Your access token')
@click.pass_context
def cli(ctx, base, key):
    """Hinkli - talking to Hinkskalle"""
    ctx.obj = HinkApi(base, key)
    return 0

@cli.command(short_help='get token')
@click.option('--user', help='Username', prompt=True)
@click.option('--password', help='Password', prompt=True, hide_input=True)
@click.pass_obj
def login(obj: HinkApi, user: str, password: str):
  obj.get_token(username=user, password=password)
  click.echo(f"Token stored in {obj.config_file}")

@cli.command(short_help='list collections')
@click.argument('entity', required=False)
@click.pass_obj
def list_collections(obj: HinkApi, entity: str):
  colls = obj.list_collections(entity)
  if len(colls) == 0:
    click.echo("No collections, you should definitely make some.")
  click.echo_via_pager(f"{c}\n" for c in colls)

@cli.command(short_help='list containers')
@click.argument('collection')
@click.pass_obj
def list_containers(obj: HinkApi, collection: str):
  if '/' in collection:
    entity, collection = collection.split('/')
  else:
    entity=None

  containers = obj.list_containers(collection, entity)
  if len(containers) == 0:
    click.echo("No containers, did you forget to push some?")
  click.echo_via_pager(f"{c}\n" for c in containers)

@cli.command(short_help='list tags')
@click.argument('container')
@click.pass_obj
def list_tags(obj: HinkApi, container: str):
  entity, collection, container = split_container(container)
  tags = obj.list_tags(entity=entity, collection=collection, container=container)
  
  click.echo_via_pager(f"{t}\n" for t in tags)

@cli.command(short_help='list downloads')
@click.argument('container')
@click.pass_obj
def list_downloads(obj: HinkApi, container: str):
  entity, collection, container = split_container(container)
  manifests = obj.list_manifests(entity=entity, collection=collection, container=container)
  
  manifests = [ m for m in manifests if m.type=='oras' and m.filename!='(none)' and m.filename != '(multiple)']
  
  click.echo_via_pager(f"{m}\n" for m in manifests)

@cli.command(short_help='get download token')
@click.argument('container')
@click.option('--expiration', help='Expiration time in days', default=14)
@click.pass_obj
def download_token(obj: HinkApi, container: str, expiration: int):
  entity, collection, container, tag = split_tagged_container(container)
  if not tag:
    raise click.ClickException("Please provide container:tag")
  link = obj.get_download_token(entity=entity, collection=collection, container=container, tag=tag, expiration=expiration)
  click.echo("There you go:")
  click.echo(f"curl -fOJ {link}")
  

@cli.command(short_help='download data')
@click.argument('container')
@click.option('--out', help='Filename/directory to save to')
@click.option('--progress/--no-progress', help='Show progress bar', default=True)
@click.pass_obj
def pull(obj: HinkApi, container: str, out: str, progress: bool):
  """CONTAINER is a library path like user.name/collection/container:tag

  user.name can be omitted, tag defaults to 'latest'
  """
  entity, collection, container, tag = split_tagged_container(container)
  if not tag:
    tag = 'latest'
  
  out = obj.fetch_blob(entity=entity, collection=collection, container=container, tag=tag, progress=progress)
  click.echo(f"{out}: Download complete")

@cli.command(short_help='upload data')
@click.argument('filename')
@click.argument('container')
@click.option('--exclude', '-e', help='When creating tar, exclude files matching these regexes', multiple=True)
@click.option('--exclude-file', help='Read exclude patterns from this file (one per line)', type=click.File())
@click.option('--private/--no-private', help='Set private flag on container', default=False)
@click.option('--progress/--no-progress', help='Show progress bar', default=True)
@click.pass_obj
def push(obj: HinkApi, filename: str, container: str, progress: bool, exclude: typing.Tuple, exclude_file: typing.TextIO, private: bool):
  entity, collection, container, tag = split_tagged_container(container)
  if exclude_file:
    exclude = exclude + tuple([ l.rstrip() for l in exclude_file.readlines() if not l.startswith('#') ])
  
  exclude_regexes: typing.List[typing.Union[typing.Pattern, str]] = []
  for l in exclude:
    try:
      exclude_regexes.append(re.compile(l))
    except re.error as rerr:
      raise click.ClickException(f"pattern `{l}` invalid: {rerr}")

  if not tag:
    raise click.ClickException("Please provide container:tag")
  obj.push_file(entity=entity, collection=collection, container=container, tag=tag, progress=progress, filename=filename, excludes=exclude_regexes, private=private)
  click.echo(f"Upload complete! (Take that, server!)")


def split_tagged_container(container: str) -> typing.Tuple[typing.Optional[str], str, str, typing.Optional[str]]:
  if ':' in container:
    container, tag = container.split(':')
  else:
    tag = None
  entity, collection, container = split_container(container)
  return entity, collection, container, tag

def split_container(container: str) -> typing.Tuple[typing.Optional[str], str, str]:
  el = container.split('/')
  if len(el) == 3:
    return el[0], el[1], el[2]
  elif len(el) == 2:
    return None, el[0], el[1]
  else:
    return None, 'default', container


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
