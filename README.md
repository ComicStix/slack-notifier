# Slack Notifier

Periodically posts reminders in your Slack chat to remind users of events from your Google Calendar. Reminders can be scheduled daily, weekly, and/or monthly.

## Installation

1. Follow steps 1 and 2 of the [Google Calendar API Python Quickstart](https://developers.google.com/google-apps/calendar/quickstart/python#prerequisites). Move the `client_secret.json` to the same folder as `slack-notifier.py`
2. Install required libraries (pytz, slack client, and schedule)
    ```
    python setup.py install
    pip install slackclient
    pip install schedule
    ```
3. [Generate](https://api.slack.com/docs/oauth-test-tokens) a token for your Slack team 
4. Find the Slack channel ID for the channel you would like to post reminders in
    `https://**YOUR SLACK TEAM URL**/api/channels.list?token=**SLACK TEAM TOKEN**`
    
## Usage

TODO: Write usage instructions

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

TODO: Write history

## Credits

TODO: Write credits

## License

TODO: Write license

