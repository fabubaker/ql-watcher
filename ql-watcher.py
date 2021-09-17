import yaml
import click

from lib.scraper import scrape
from lib.notifier import notify

@click.command()
@click.argument('search_term')
@click.option('--state-file', 'state_file',
              help='''File used to track previously seen items. If the file
                      exists, uses it for the current run.''',
              default='./state-file.json', show_default=True,
              type=click.Path(exists=False))
@click.option('--config-file', 'config_file',
              help='''YAML file used to load config data from. Should be cloned from
                      config.yaml.tpl''',
              default='./config.yaml', show_default=True,
              type=click.Path(exists=True))
@click.option('--dry-run',
              help='''Use this option to trigger a dry run of the watcher.
                      In a dry run, new items are fetched but are only
                      printed to STDOUT. Note that the state file is also
                      updated in a dry run.''',
              is_flag=True, default=False)
@click.option('--vehicles',
              help='''By default, ql-watcher scrapes the 'classifieds'
              page of QatarLiving. Use this option to scrape the
              vehicles page instead of the classifieds page.''',
              is_flag=True, default=False)
def main(search_term, state_file, config_file, dry_run, vehicles):
  """
  ql-watcher scrapes the most recent 30 items for sale from QatarLiving.com
  using SEARCH_TERM, and sends you an email with any new items it finds.
  """
  new_items = scrape(search_term, state_file, vehicles)

  if not new_items:
    print(f'No new items found for "{search_term}"! Exiting...')
    return

  print(f'{len(new_items)} new items found for "{search_term}"!')

  if dry_run:
    print(new_items)
  else:
    config = yaml.safe_load(open(config_file))
    notify(new_items, search_term, config)

if __name__=='__main__':
  main()
