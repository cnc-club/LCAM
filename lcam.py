#!/usr/bin/env python

import sys
sys.path.append("./py")
from points import *
from line import *
from arc import *
import json


class Sketch() :
	def __init__(self, s=None):
		s = '[{"st":{"x":0,"y":0},"end":{"x":10,"y":0}},{"st":{"x":10,"y":0},"end":{"x":10,"y":20}},{"st":{"x":10,"y":20},"end":{"x":20,"y":20}},{"st":{"x":20,"y":20},"end":{"x":20,"y":-20}},{"st":{"x":20,"y":-20},"end":{"x":40,"y":-20},"c":{"x":30,"y":-8.819660112501051},"a":1.4594553124539322,"ccw":true,"r":15}]'
		self.shape_from_str(s)
		print self.shape
	def shape_from_str (self, s):
		js = json.loads(s)
		self.shape = []
		for el in js : 
			print el
			if "ccw" in el : # it's an arc
				self.shape.append( Arc( P(el["st"]), P(el["end"]), P(el["c"]), (1 if el["ccw"] else -1)  ) )
			else : 	
				self.shape.append( Line( P(el["st"]), P(el["end"]) ) )
				http://toblerity.org/shapely/manual.html
			
		print self.shape		

if __name__ == "__main__":
	s = Sketch()
	

