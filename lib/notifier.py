import smtplib

from email.message import EmailMessage

def notify(items, search_term, config):
  smtp = config['smtp']

  server = smtplib.SMTP_SSL(smtp['host'], smtp['port'])
  server.ehlo()
  server.login(smtp['username'], smtp['password'])

  mail = _create_notification_email(
    items, search_term, smtp['username'], smtp['recepients']
  )

  print(f"Sending mail to {smtp['recepients']}...")
  server.sendmail(smtp['username'], smtp['recepients'], mail.as_string())


def _create_notification_email(items, search_term, sender, recepients):
  mail = EmailMessage()
  item_count = len(items)
  formatted_items = _format_items_for_email(items)

  mail['Subject'] = f'[ql-watcher] {item_count} new items \
                      found for "{search_term}"'
  mail['From'] = sender
  mail['To'] = ', '.join(recepients)
  mail.set_content(formatted_items)

  return mail

def _format_items_for_email(items):
  text = ''

  for _id, item in items.items():
    text += f"id: {_id}\n"

    for key, value in item.items():
      text += f"{key}: {value}\n"

    text += '\n'

  return text

