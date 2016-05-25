# Slack Scheduler

Periodically posts reminders in your Slack chat to remind users of events from your Google Calendar. Reminders can be scheduled daily, weekly, and/or monthly.

## Installation

1. Follow steps 1 and 2 of the [Google Calendar API Python Quickstart](https://developers.google.com/google-apps/calendar/quickstart/python#prerequisites). Move the `client_secret.json` to the same folder as `slack_scheduler.py`
2. Install required libraries
    ```
    pip install pytz
    
    pip install slackclient
    
    pip install schedule
    ```
3. [Generate](https://api.slack.com/docs/oauth-test-tokens) a token for your Slack team 
4. Find the Slack channel ID for the channel you would like to post reminders in
    <pre>
    https://<b><i>YOUR SLACK TEAM URL</i></b>.slack.com/api/channels.list?token=<b><i>SLACK TEAM TOKEN</i></b>
    </pre>
    
## Usage

There are **three** required command line arguments:

1. The Google Calendar you would like the reminders set for (primary, work, etc.)
2. The token of your Slack team
3. The Slack channel ID you would like the reminders to be posted into

###Flags

**-d** - set a daily reminder in the Slack channel

**-w** - set a weekly reminder in the Slack channel

**-m** - set a monthly reminder in the Slack channel

**-r** - set a time for the reminder in _military time_ (if no reminder is set, reminder time defaults to 0:00)

**-dt** - display the events happening today in the terminal

**-dw** - display the events happening this week in the terminal

**-dm** - display the events happening this month in the terminal

**Daily, weekly, and monthly reminders to the selected Slack channel will fire at 13:00**
```shell
$ python slack-scheduler.py [<calendar>][<token>][<channelID>] -d -w -m -r 13:00
```
**Daily reminders will fire at midnight**
```shell
$ python slack-scheduler.py [<calendar>][<token>][<channelID>] -d
```
## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## TODO
- [ ] Detect users time zone (Unfortunately, it only works for eastern time zone currently)

