from __future__ import print_function
from slackclient import SlackClient
import schedule
import time
import argparse
import sys,getopt
import dateutil.parser
import httplib2
import os
import requests
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Slack Scheduler'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)

    return credentials

def get_todays_events(token, channelID, service, calendar):

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    today = datetime.date.today()
    midnight = datetime.datetime.combine(today, datetime.time.max)
    midnight = midnight.isoformat() + 'Z'
    todaysResults = service.events().list(
            calendarId=calendar, timeMin=now, orderBy='startTime', singleEvents=True,
            timeMax=midnight).execute()
    todays_events = todaysResults.get('items',[])

    postNotification(token, channelID, todays_events, "today")
        
def get_weeks_events(token, channelID, service, calendar):
    
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    today = datetime.datetime.today()
    weekday = today.isoweekday();
    this_sunday = today + datetime.timedelta(days= 7 - weekday)
    this_sunday = this_sunday.isoformat() + 'Z'

    weekResults = service.events().list(
            calendarId=calendar, timeMin=now, orderBy='startTime', singleEvents=True,
            timeMax=this_sunday).execute()
    weeks_events = weekResults.get('items',[])

    postNotification(token, channelID, weeks_events, "this week")
        
def get_months_events(token, channelID, service, calendar):

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    today = datetime.datetime.today()
    next_month = today.replace(day=28) + datetime.timedelta(days=4)
    end_of_month = next_month - datetime.timedelta(days=next_month.day)
    end_of_month = end_of_month.isoformat() + 'Z'
    monthResults = service.events().list(
            calendarId=calendar, timeMin=now, orderBy='startTime', singleEvents=True,
            timeMax=end_of_month).execute()
    months_events = monthResults.get('items',[])
    
    postNotification(token, channelID, months_events, "this month")
    
def postNotification(token, channelID, events, timePeriod):

    message = ""
    sc = SlackClient(token)

    if not events:
        period = "*_No events scheduled for " + timePeriod + " :sleepy:  _*\n"
    for event in events:
        period = "*_Here are the events happening " + timePeriod + " :smile: _*\n"
        start_date = dateutil.parser.parse(event['start'].get('dateTime'))
        start_date = start_date.strftime("%A, %B %d %Y @ %I:%M %p")
        end_date = dateutil.parser.parse(event['end'].get('dateTime'))
        end_date = end_date.strftime("%A, %B %d %Y @ %I:%M %p")
        message += "\n - " + "*" + event['summary'] + "*" + "\n"+ start_date + " to " + end_date + "\n" + "*Where:* " + event['location'] + "\n" + "*Description:* " + event['description'] + "\n" + event['htmlLink'] + "\n"
        
    sc.api_call("chat.postMessage",username="Slack Notifier",channel=channelID,text=period + message)
    
def main(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument("calendar",help="input the calendar you would like to set notifications for",type=str)
    parser.add_argument("token",help="input the token for your Slack team",type=str)
    parser.add_argument("channelID",help="input the channel you would like the bot to post in",type=str)
    parser.add_argument("-d","--daily",help="set a daily reminder",action="store_true")
    parser.add_argument("-w","--weekly",help="set a weekly reminder",action="store_true")
    parser.add_argument("-m","--monthly",help="set a monthly reminder",action="store_true")
    parser.add_argument("-dt","--displayToday",help="display today's events",action="store_true")
    parser.add_argument("-dw","--displayWeek",help="display this week's events",action="store_true")
    parser.add_argument("-dm","--displayMonth",help="display this month's events",action="store_true")
    parser.add_argument("-r","--reminder",help="set time of Slack channel event notifications (if not set, notification time defaults to midnight)",type=str)
    
    args = parser.parse_args()
    calendar = args.calendar
    notificationTime = "0:00"
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    
    try:
        cal = service.calendars().get(calendarId=calendar).execute()
    except Exception as exc:
        if exc.resp['status'] == '404':
            print("Calendar %s not found" % calendar)
        else:
            print(exc.message)
        sys.exit()

    if args.reminder:
        notificationTime = args.reminder
        print("Reminder set for", args.reminder)
    if args.displayToday:
        get_todays_events(args.token, args.channelID, service, calendar)
    if args.displayWeek:
        get_weeks_events(args.token, args.channelID, service, calendar)
    if args.displayMonth:
        get_months_events(args.token, args.channelID, service, calendar)
    if args.daily:
        schedule.every().day.at(notificationTime).do(get_todays_events, args.token, args.channelID, service, calendar)
        print("Daily reminder is on")
    if args.weekly:
        schedule.every().monday.at(notificationTime).do(get_weeks_events, args.token, args.channelID, service, calendar)
        print("Weekly reminder is on")
    if args.monthly:
        print("Monthly reminder is on")

    while True:
        if args.monthly:
            today = datetime.datetime.now().replace(microsecond=0)
            first_of_month = datetime.datetime(today.year, today.month, 1, 0, 0, 0)
            if today == first_of_month:
                get_months_events(args.token,args.channelID,service,calendar)
        schedule.run_pending()
        time.sleep(1)
        
if __name__ == '__main__':
    main(sys.argv[1:])
