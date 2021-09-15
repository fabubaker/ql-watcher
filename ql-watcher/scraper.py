import json
import requests

QL_URL = 'https://www.qatarliving.com/backend/api/classified/search'

def scrape(search_term, state_file):
  current_items = _get_current_items(search_term)
  seen_items = _get_seen_items(state_file)
  new_items = _get_new_items(current_items, seen_items)
  # Merge current_items with seen_items.
  updated_seen_items = {**seen_items, **current_items}

  _save_items_as_seen(updated_seen_items, state_file)

  return new_items

def _get_new_items(current_items, seen_items):
  new_items = {}

  for _id, item in current_items.items():
    if _id not in seen_items:
      new_items[_id] = item

  return new_items

def _get_current_items(search_term):
  response = requests.post(QL_URL, data={'title': search_term})
  items = response.json()['classified']
  current_items = {}

  # Massage the response a bit, we don't need everything it returns.
  for item in items:
    _id = item['_id']
    current_items[_id] = {
      'title': item['_source']['title'],
      'price': item['_source']['price']
    }

  return current_items

def _get_seen_items(state_file):
  try:
    with open(state_file, 'r') as state_file_handle:
      return json.load(state_file_handle)
  except FileNotFoundError:
    return {}

def _save_items_as_seen(items, state_file):
  with open(state_file, 'w+') as state_file_handle:
    json.dump(items, state_file_handle, indent=4)
