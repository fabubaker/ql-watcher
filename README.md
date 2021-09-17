# ql-watcher

`ql-watcher` scrapes the most recent 30 items from QatarLiving.com for a search term, and sends you an email with any new items it finds.

## Install

Install dependencies using:

```
pip install -r requirements.txt
```

## Usage

### Pre-requisites

In order for `ql-watcher` to send you emails, you need to fill out a config file with your SMTP settings:

First, copy the existing config template:

```
cp config.yaml.tpl config.yaml
```

Then fill out the relevant SMTP settings. Here's an example for gmail:

```
smtp:
  host: 'smtp.gmail.com'
  port: '465'
  username: 'example@gmail.com'
  password: 'examplepassword'
  recepients:
    - 'recepient@gmail.com'

```

Note that for using SMTP with gmail, you will need to create an [app password](https://www.febooti.com/products/automation-workshop/tutorials/enable-google-app-passwords-for-smtp.html) and use this instead of your actual password.

### Running

Once `config.yaml` has been filled out, you are ready to run `ql-watcher`.

`ql-watcher` uses a file to keep track of items it has seen before. Let's perform an initial run to generate this file:

```
❯ python3 ql-watcher/ql-watcher.py "nintendo"
30 new items found for "nintendo"!
...
```

This will fetch the most recent 30 items related to "nintendo" and send them to the recepients you have specified in `config.yaml`. Additionally, it will also save them to `state-file.json`.

Running it again immediately will tell you that it has found no new items (unless someone posted a new item in that small window!):

```
❯ python3 ql-watcher/ql-watcher.py "nintendo"
No new items found for "nintendo"! Exiting...
```
