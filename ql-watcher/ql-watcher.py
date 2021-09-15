import click
from scraper import get_new_items

@click.command()
@click.argument('search_term')
@click.option('--state-file', 'state_file',
              help='''State file used to track previously seen items. If the file
                      exists, uses it for the current run.''',
              default='./state-file.json', show_default=True,
              type=click.Path(exists=False))
@click.option('--dry-run',
              help='''Use this option to trigger a dry run of the watcher.
                      In a dry run, new items are fetched but are only
                      printed to STDOUT. Note that the state file is also
                      updated in a dry run.''',
              default=False, show_default=True)
def main(search_term, state_file, dry_run):
  """
  ql-watcher scrapes the most recent 30 items for sale from QatarLiving.com
  using SEARCH_TERM, and sends you a text with any new items it finds.
  """
  new_items = get_new_items(search_term, state_file)

  if dry_run:
    print(new_items)


if __name__=='__main__':
  main()
