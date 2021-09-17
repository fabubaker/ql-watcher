# ql-watcher

`ql-watcher` scrapes the most recent 30 items from [QatarLiving.com](https://www.qatarliving.com/) for a search term, and sends you an email with any new items it finds.

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
❯ python3 ql-watcher.py "nintendo"
30 new items found for "nintendo"!
...
```

This will fetch the most recent 30 items related to "nintendo" and send them to the recepients you have specified in `config.yaml`. Additionally, it will also save them to `state-file.json`.

Running it again immediately will tell you that it has found no new items (unless someone posted a new item in that small window!):

```
❯ python3 ql-watcher.py "nintendo"
No new items found for "nintendo"! Exiting...
```

### Scheduling `ql-watcher`

`ql-watcher` isn't very useful if you have to keep running it manually every now and then.

Let's schedule it to run every hour using [cron](https://en.wikipedia.org/wiki/Cron).

First, let's add an entry to your crontab for ql-watcher to run every hour. Open up the crontab using `crontab -e` and add the following line:

```
0 * * * * cd /<path-to-ql-watcher>/ql-watcher.py; python3 ql-watcher.py <search-term>
```

This will run the ql-watcher script on the 0th minute of every hour, every day. For more info on crontabs, check this [guide](https://ostechnix.com/a-beginners-guide-to-cron-jobs/).

Of course, the script won't run if your computer is shutdown or asleep when the cron job is triggered. For this reason, you should schedule `ql-watcher` on an external server if you want regular notifications.
