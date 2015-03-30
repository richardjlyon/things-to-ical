#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
thing.py

This object is a base class that represents a Thing in the Things database.

Created on 29 Mar 2015
@author: Richard Lyon
"""
import datetime

def parseInteger(data):
	return data

def parseTimestamp(data):
	"""Timestamps in Things database are too old by OFFSET seconds. Correct"""
	result = None
	OFFSET = 978307370
	if data:
		result = datetime.datetime.fromtimestamp(data) + datetime.timedelta(seconds=OFFSET)
	return result

def parseFloat(data):
	return data

def parseVarchar(data):
	"""Encode in UTF-8"""
	result = None
	if data:
		result = data.encode('UTF-8')
	return result

def parseBlob(data):
	return data

parseMap = {"INTEGER" 	: parseInteger,
			"TIMESTAMP"	: parseTimestamp,
			"FLOAT"		: parseFloat,
			"VARCHAR"	: parseVarchar,
			"BLOB"		: parseBlob}


class Thing(object):

	def __init__(self, client, row=None, id=None):
		"""Create an attribute for each column from parsed data"""
		super(Thing, self).__init__()
		self.client = client
		keys = row.keys()
		ind = 0
		for data in row:
			parseFunc = parseMap[client.schema[keys[ind]]]
			setattr(self, keys[ind], parseFunc(data))
			ind += 1

	def get_tags(self):
		"""Return list of tag names"""
		result = []
		if id:
			tags = self.client.con.execute('SELECT Z_14TAGS FROM Z_12TAGS WHERE Z_12NOTES = ?', (self.Z_PK,)).fetchall()
			result = [self.client.fetch_thing(tag[0]).ZTITLE for tag in tags]
		return result

	def get_area(self):
		"""Return Area as string"""
		area_id = self.client.con.execute('SELECT ZAREA FROM ZTHING WHERE Z_PK = ?', (self.Z_PK,)).fetchone()[0]
		return self.client.fetch_thing(area_id).ZTITLE

	def get_project(self):
		"""Return Project as string"""
		project_id = self.client.con.execute('SELECT ZPROJECT FROM ZTHING WHERE Z_PK = ?', (self.Z_PK,)).fetchone()[0]
		return self.client.fetch_thing(project_id).ZTITLE	

	def __repr__(self):
		thestring = ""
		thestring += '-'*80 + '\n'
		thestring += "TASK:    %s\n" % self.ZTITLE
		thestring += "CREATED: %s\n" % self.ZCREATIONDATE
		thestring += "DUE:     %s\n" % self.ZDUEDATE
		thestring += "START:   %s\n" % self.ZSTARTDATE

		if self.client.fetch_thing(id = self.ZAREA):
			thestring += "AREA   : %s\n" % self.get_area()
		if self.client.fetch_thing(id = self.ZPROJECT):
			thestring += "PROJECT: %s\n" % self.get_project()
		if self.get_tags():
			thestring += "TAGS   : %s\n" % self.get_tags()

		return thestring