#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
things_to_ical.py

A script that reads a Culturedcode Things database and makes a calendar feed of todos.
Todos with the tag 'event' are created as events, otherwise todos.

Created on 29 Mar 2015
@author: Richard Lyon
"""

from icalendar import Calendar, Event, Todo, vText
from pythings.client import Client
import os
import datetime

home = os.path.expanduser("~")
thingsdb = 'Library/Containers/com.culturedcode.things/Data/Library/Application Support/Cultured Code/Things/ThingsLibrary.db'
thingsdb_path = os.path.join(home, thingsdb)
client = Client(thingsdb_path)

def makeEvent(thing):
	"""Make an iCal event from the thing name and due/activation date"""
	event = Event()
	event.add('summary', thing.ZTITLE.capitalize())
	event.add('dtstart', thing.ZSTARTDATE.date())
	event.add('dtend', thing.ZSTARTDATE.date() + datetime.timedelta(days=1))
	if thing.ZPROJECT: 
		event['location'] = vText(client.fetch_thing(thing.ZPROJECT).ZTITLE)
	return event

def makeTodo(thing):
	"""Make an iCal reminder """
	todo = Todo()
	todo.add('summary', thing.ZTITLE.capitalize())
	todo.add('due', thing.ZSTARTDATE)
	if thing.ZSTOPPEDDATE:
		todo.add('completed', thing.ZSTOPPEDDATE)
	if thing.ZPROJECT: 
		todo['location'] = vText(client.fetch_thing(thing.ZPROJECT).ZTITLE)
	return todo

def main():

	# initialise the calendar
	cal = Calendar()
	cal.add('prodid', '-//My calendar product//mxm.dk//')
	cal.add('version', '2.0')

	# add the events to the calendar
	dated_todos = client.scheduled_todos
	for todo in dated_todos:
		if "event" in todo.get_tags():
			cal.add_component(makeEvent(todo))
		else:
			cal.add_component(makeTodo(todo))
		print todo

	# save the calendar
	directory = "/Applications/MAMP/htdocs"
	f = open(os.path.join(directory, 'things.ics'), 'wb')
	f.write(cal.to_ical())
	f.close()

if __name__ == "__main__":
	main()