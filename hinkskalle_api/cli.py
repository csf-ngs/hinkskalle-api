"""Console script for hinkskalle_api."""
import sys
import click
import click_log
import logging
from hinkskalle_api import HinkApi

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.group()
@click_log.simple_verbosity_option(logger)
@click.option('--base', help='API Base URL')
@click.option('--key', help='Your access token')
@click.pass_context
def cli(ctx, base, key):
    """Hinkli - talking to Hinkskalle"""
    ctx.obj = HinkApi(base, key)
    return 0

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
  el = container.split('/')
  if len(el) == 3:
    tags = obj.list_tags(entity=el[0], collection=el[1], container=el[2])
  elif len(el) == 2:
    tags = obj.list_tags(entity=None, collection=el[0], container=el[1])
  else:
    tags = obj.list_tags(entity=None, collection='default', container=container)
  
  click.echo_via_pager(f"{t}\n" for t in tags)

@cli.command(short_help='list downloads')
@click.argument('container')
@click.pass_obj
def list_downloads(obj: HinkApi, container: str):
  el = container.split('/')
  if len(el) == 3:
    manifests = obj.list_manifests(entity=el[0], collection=el[1], container=el[2])
  elif len(el) == 2:
    manifests = obj.list_manifests(entity=None, collection=el[0], container=el[1])
  else:
    manifests = obj.list_manifests(entity=None, collection='default', container=container)
  
  manifests = [ m for m in manifests if m.type=='oras' and m.filename!='(none)' and m.filename != '(multiple)']
  
  click.echo_via_pager(f"{m}\n" for m in manifests)

if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
