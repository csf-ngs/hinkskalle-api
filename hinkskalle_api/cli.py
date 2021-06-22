"""Console script for hinkskalle_api."""
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

@cli.command(short_help='download data')
@click.argument('container')
@click.option('--out', help='Filename/directory to save to')
@click.option('--progress/--no-progress', help='Show progress bar', default=True)
@click.pass_obj
def pull(obj: HinkApi, container: str, out: str, progress: bool):
  """CONTAINER is a library path like user.name/collection/container:tag

  user.name can be omitted.
  """
  if not ':' in container:
    tag = 'latest'
  else:
    container, tag = container.split(':')
  
  entity, collection, container = split_container(container)
  out = obj.fetch_blob(entity=entity, collection=collection, container=container, tag=tag, progress=progress)
  click.echo(f"{out}: Download complete")

@cli.command(short_help='upload data')
@click.argument('filename')
@click.argument('container')
@click.option('--progress/--no-progress', help='Show progress bar', default=True)
@click.pass_obj
def push(obj: HinkApi, filename: str, container: str, progress: bool):
  if not ':' in container:
    raise Exception("please provide tag [container]:[tag]")
  container, tag = container.split(':')
  entity, collection, container = split_container(container)
  obj.push_file(entity=entity, collection=collection, container=container, tag=tag, progress=progress, filename=filename)
  click.echo(f"Upload complete! (Take that, server!)")


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
