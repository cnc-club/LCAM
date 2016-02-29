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
				#http://toblerity.org/shapely/manual.html
			
		print self.shape		


class Tool() :
	self.angle = 90
	self.speed = 100
	
	
class Geometry() :
	
	def __init__(self) :
		self.geom = []
	
	def allowance(self,x=None,z=None,r=None) :
		for g in self.geom :
			g.allowance(x,z,r)
	
	def from_sketch(self, sk) :
		for i in sk.shape:
			self.geom.append(i.copy())
	
		
class Trajectory() :	
	self.traj = []

class Tr() :
	def __init__(self,t) :
		self.feed = None
		self.rapid = None		
		self.t = t
		self.st = t.st.copy()
		self.end = t.end.copy()
		self.update()
	
	def update(self) :
		pass
		
		
	
class Rapid(Tr) :
	def update(self) :	
		self.rapid = True

class Cut(Tr) :
	pass

class CutArc(Tr) :
	pass
		
class Stock() :
	self.geometry = []
	
	def get_width(self) :
		x = 0
		for geom in self.geometry :
			for g in self.geom :
				b = g.bounds()
				x = max(x,	b[3])
		return x
	
	def add_cylinder(self, r,l,z=0) :
		g = Geometry()
		g.geom.append(Line(z,0))
		g.geom.append(Line(z,r))
		g.geom.append(Line(z-l,r))
		g.geom.append(Line(z-l,0))
		self.geometry.append(g)
				
		
class Operation() :
	def __init__(self) :
		self.tool = Tool()		
		self.geometry = []
		self.stock = Stock()
		self.allowance = [0,0,0]

	def draw(self) :
		for t in self.traj :
			t.draw()

	def to_str(self) :
		res = {}
		for p in self.params :
			res[p] = getattr(self, p)			
		return json.dumps(res)
		
		
class Shape(Operation) :
	def __init__(self) :
		self.step = 1
		self.startx = 20
		self.safex = 50
		self.endx = 0
	def prepare(self) :
		pass
	
	
	def run(self) :
		done == False
		x = self.startx - step
		while x>self.endx and not done:
			done = True
			
class Ray() :
	def __init__(self, st, end) :
		self.st = st.copy()
		self.end = end.copy() 
	def intersect_geom(self, geom) :
		self.l = Line(self.st,self.end)
		for g in geom : 
			self.intersect_g(g)	
	def intersect_g(self, g)
		r = self.l.intersect(g,ray = True)
		for p in r :
			#TODO
			
class Postprocessor() :
	pass
	

if __name__ == "__main__":
	s = Sketch()
	m = Shape()	
	print m.tool
