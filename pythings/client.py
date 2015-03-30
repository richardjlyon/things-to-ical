#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
py-things.py

A class for hacking the CultureCode Things database

Created on 29 Mar 2015
@author: Richard Lyon
"""
import sqlite3 as lite
import tempfile
import shutil
from pythings.thing import Thing

class Client(object):
	"""
	A class for representing a Things database
	"""

	def fetch_thing(self, id=None):
		"""Get the thing with Z_PK 'id'"""
		result = None
		if id:
			result = Thing(self, self.con.execute('SELECT * FROM ZTHING WHERE Z_PK = ?', (id,)).fetchone())
		return result

	def _fetch_things(self, query_string):
		"""Return a list of Thing objects from query"""
		rows = self.con.execute(query_string).fetchall()
		return [Thing(self, row=row) for row in rows]

	def __init__(self, path):

		# Things locks the database when active, so work from a temporary copy
		(temphandle, temppath) = tempfile.mkstemp()
		shutil.copyfile(path, temppath)
		self.con = lite.connect(temppath)
		
		# allows access by column name
		self.con.row_factory = lite.Row
		
		#  e.g. { 'ZDUEDATE' : 'TIMESTAMP' } use this in the Thing class to find the right parse function
		self.schema = {row[1]: row[2] for row in self.con.execute("pragma table_info('ZTHING')").fetchall()}
		
		# projects are ZTYPE = 1; todos are ztype 1 
		self.scheduled_todos = self._fetch_things('SELECT * FROM ZTHING WHERE ZTYPE = "0" AND ZTRASHED <> "1" AND ZSTARTDATE IS NOT NULL')
		# self.things = self._fetch_things('SELECT * FROM ZTHING')
		# self.areas = self._fetch_things('SELECT * FROM ZTHING WHERE ZFOCUSLEVEL1 = "2"')
		# self.projects = self._fetch_things('SELECT * FROM ZTHING WHERE ZTYPE = "1" AND ZTRASHED <> "1"')
		# self.todos = self._fetch_things('SELECT * FROM ZTHING WHERE ZTYPE = "0" AND ZTRASHED <> "1"')
		# self.due_todos = self._fetch_things('SELECT * FROM ZTHING WHERE ZTYPE = "0" AND ZTRASHED <> "1" AND ZDUEDATE IS NOT NULL')
