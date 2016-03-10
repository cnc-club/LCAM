#!/usr/bin/env python

import sys
sys.path.append("./py")
from points import *
from line import *
from arc import *
import json

import matplotlib.pyplot as plt
from matplotlib import patches
import matplotlib.lines as lines
class Sketch() :
	def __repr__(self) :
		l = "------ Sketch ------\n"
		for s in self.shape:
			l += "	%s\n"%s 
		l += "------        ------\n\n"
		return l

		
	def __init__(self, s=None):
		self.shape_from_str(s)

	def shape_from_str (self, s):
		js = json.loads(s)
		self.shape = []
		for el in js : 
			#print el
			if "ccw" in el : # it's an arc
				self.shape.append( Arc( P(el["st"]), P(el["end"]), P(el["c"]), (1 if el["ccw"] else -1)  ) )
			else : 	
				self.shape.append( Line( P(el["st"]), P(el["end"]) ) )
				#http://toblerity.org/shapely/manual.html
			


class Tool() :
	def __init__(self) :
		self.angle = 90
		self.speed = 100
		self.init()		
		
	def init(self) :
		pass
	
		
class LatheTool(Tool) :
	def init(self) :
		self.angle = 90
		self.in_angle = -135
		self.in_l = 5
		self.speed = 100
		self.in_p = -P(self.in_l,0).rot(self.in_angle*pi/180.)

	def __repr__(self) :
		l =  "-- Tool --"	
		l+= "ang: %s\n"%self.angle
		l+= "in_p: %s\n"%self.in_p
		l+= "speed: %s\n"%self.speed
		return l 
	
class Geometry() :
	
	def __init__(self) :
		self.g = []
	
	def allowance(self,x=None,z=None,r=None) :
		for g in self.g :
			g.allowance(x,z,r)
	
	def from_sketch(self, sk) :
		for i in sk.shape:
			self.g.append(i.copy())
	
	def copy(self) :
		geom = Geometry()
		for i in self.g : 
			geom.g.append(i.copy())
		return geom	
	
	def clip(self, x,y,x1,y1) :
		x,x1 = min(x,x1),max(x,x1)
		y,y1 = min(y,y1),max(y,y1)

		res = Geometry()
		for e in self.g :	
			res.g += e.clip(x,y,x1,y1)
		return res 			
	
	def __repr__(self) :	
		l = "-- Geometry --\n"
		for e in self.g :
			l += "%s\n"%e
		l += "--          --\n"
		return l

class PostProcessor() :
	def __init__(self) :
		self.operations = [] 
		self.gcode = ""
		self.x = None
		self.feed = None
		self.y = None
		self.before = "G18"
		self.after = "M02"
			
	def comment(self,s) :
		res = ""
		for l in s.split("\n") :
			res += "(" + l.replace("(","[").replace(")","]") + ")\n"
		return res	

	def process(self, t, op) :
		s = ""
		if t.__class__ == Feed :
			s += "G01"
			if t.end.x != self.x :
				s += " X%s"%t.end.x
			if t.end.y != self.y :
				s += " Z%s"%t.end.y
			if self.feed != op.feed :
				s += " F%s"%op.feed
				self.feed = op.feed

		if t.__class__ == FeedIn :
			s += "G01"
			if t.end.x != self.x :
				s += " X%s"%t.end.x
			if t.end.y != self.y :
				s += " Z%s"%t.end.y
			if self.feed != op.feed_in :
				s += " F%s"%op.feed_in
				self.feed = op.feed_in

		if t.__class__ == FeedOut :
			s += "G01"
			if t.end.x != self.x :
				s += " X%s"%t.end.x
			if t.end.y != self.y :
				s += " Z%s"%t.end.y
			if self.feed != op.feed_out :
				s += " F%s"%op.feed_out
				self.feed = op.feed_out
				
		if t.__class__ == Rapid :
			s += "G00"
			if t.end.x != self.x :
				s += " X%s"%t.end.x
			if t.end.y != self.y :
				s += " Z%s"%t.end.y

		if t.__class__ == ArcFeed :
			s += "G02" if t.geom.a > 0 else "G03"
			if t.end.x != self.x :
				s += " X%s"%t.end.x
			if t.end.y != self.y :
				s += " Z%s"%t.end.y
			i = t.geom.c.x-t.st.x 
			if i != 0 :
				s += "I%s"%i
			k = t.geom.c.y-t.st.y 
			if k != 0 :
				s += "K%s"%k
			if self.feed != op.feed :
				s += " F%s"%op.feed
				self.feed = op.feed		

		self.x = t.end.x
		self.y = t.end.y
		s += "\n"
		return s 		

	
	def update(self) :
		gcode = ''
		gcode += self.before
		for op in self.operations :
			gcode += self.comment(op.before())
			for t in op.traj.items :
				gcode += self.process(t, op) 
			gcode += self.comment(op.after())
		gcode += self.after	
		self.gcode = gcode	
		 
		
		
class Trajectory() :	
	def __init__(self) :
		self.st = P(0,0)
		self.items = []
		
	def append(self, item) :
		self.items.append(item)
	
	def pos(self) :
		if len(self.items)> 0 :
			return self.items[-1].end
		else :
			return self.st
			
	def feed(self, x=None, z=None, feed=1 ) :
		p0 = self.pos()
		if x.__class__ == P :
			p = x
		else :
			p = P(   x if x!=None else p0.x,   z if z!=None else p0.y  )
		if feed == 1 :		
			self.append(Feed( Line(p0, p) ))
		elif feed == 2 :
			self.append(FeedIn( Line(p0, p) ))
		elif feed == 3 	:
			self.append(FeedOut( Line(p0, p) ))
		else :
			self.append(Rapid( Line(p0, p) ))

	def feed_in (self, x=None, z=None) :
		self.feed(x,z, feed=2)
	def feed_out(self, x=None, z=None) :
		self.feed(x,z, feed=3)
	def rapid   (self, x=None, z=None) :
		self.feed(x,z, feed=0)

	def arc(self, x) :
		if x.__class__ == Arc :
			self.append(ArcFeed( x ))
			
	def __repr__(self) :
		l =  "------ Trajectory ------\n"
		for s in self.items:
			l += "	%s\n"%s 
		l += "------            ------\n\n"
		return l		
	
	def draw(self, p) :
		for i in self.items :
			i.draw(p)
	
class Tr() :

	def __init__(self,g) :
		self.feed = None
		self.rapid = None		
		self.geom = g
		self.st = g.st.copy()
		self.end = g.end.copy()
		self.update()

		self.color = "b"

		self.init()
		
	def init(self) :
		pass # init Tr by type 
	
	def update(self) :
		pass

	def draw(self, p) :
		l = self.end-self.st
		p.arrow(self.st.y, self.st.x, l.y, l.x, lw = 0.5, head_width=1, head_length=1, fc=self.color, ec=self.color)
	
class Rapid(Tr) :
	def init(self) :
		self.rapid = True
		self.color = "#00aa00"
	def __repr__(self) :
		return "Rapid %s -> %s"%(self.st,self.end)

class Feed(Tr) :
	def init(self) :
		self.color = "#16a0fe"
		self.rapid = False
	def __repr__(self) :
		return "Feed  %s -> %s"%(self.st,self.end)

class ArcFeed(Tr) :
	def init(self) :
		self.rapid = False
		self.color = "#b569d6"
		
	def draw(self, p) :
		if self.geom.a<0 :
			a = 90-(self.geom.st-self.geom.c).angle()/pi*180.		
			arc = patches.Arc([self.geom.c.y,self.geom.c.x], self.geom.r*2, self.geom.r*2, 0, a, a+self.geom.a/pi*180, color=self.color, linewidth='2.5')
		else : 	
			a = 90-(self.geom.end-self.geom.c).angle()/pi*180.		
			arc = patches.Arc([self.geom.c.y,self.geom.c.x], self.geom.r*2, self.geom.r*2, 0, a, a+self.geom.a/pi*180, color=self.color, linewidth='2.5')
		p.add_patch(arc)
		p.plot(	[self.st.y,self.geom.c.y,self.end.y], [self.st.x,self.geom.c.x,self.end.x], linewidth=0.2, color='blue')
#		print ([self.geom.c.x,self.geom.c.y], self.geom.r, self.geom.r, 0, a, a+self.geom.a, self.color,'0.5')


	def __repr__(self) :
		return "Arc   %s -> %s r%.2f"%(self.st,self.end, self.geom.r)
		

class FeedIn(Feed) :
	def init(self) :
		self.color = "#0161a3"
	def __repr__(self) :
		return "FeedI %s -> %s"%(self.st,self.end)

class FeedOut(Feed) :
	def init(self) :
		self.color = "#80ccfe"
	def __repr__(self) :
		return "FeedO %s -> %s"%(self.st,self.end)

		
class Stock() :
	def __init__(self) :
		self.geometry = []
	
	def get_width(self) :
		x = 0
		for g in self.geom.g :
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
		self.param = {}
		self.init()
		self.traj = Trajectory()
		self.feed = 100
		self.feed_in = 70
		self.feed_out = 400
		
	
	def before(self) :
		s = "Operation %s start\n"%self.__class__.__name__
		s += "%s\n"%self.tool			
		return s 

	def after(self) :
		s = "Operation %s end\n"%self.__class__.__name__
		return s 
	
	def init(self) :
		pass # init operation by type 
		
	def draw(self) :
		for t in self.traj :
			t.draw()

	def to_str(self) :
		res = {}
		for p in self.params :
			res[p] = getattr(self, p)			
		return json.dumps(res)


	def __repr__(self) :
		l =  "====== Operation ======\n"
		l += "Class: %s\n"%self.__class__
		l += "Tool: %s\n"%self.tool
		l += "%s\n"%self.param
		l += "%s"%self.traj
		l += "======           ======\n\n"
		return l		
		
	def draw(self) :
		ax = plt.axes()
		self.traj.draw(ax)	
		ax.set_aspect('equal', 'datalim')
		ax.autoscale_view()
		ax.set_xlim([-100,100])
		ax.set_ylim([-100,100])
		
		plt.show()		
		
class ShapeContour(Operation) : 
	def init(self) :
		self.param = {}
		self.stx = self.param["maxx"] = 10
		self.endx = self.param["minx"] = -5
		self.stz = self.param["maxz"] = 5
		self.endz = self.param["minz"] = -20 
		self.safex = self.param["safex"] = 100 
		self.steps = self.param["steps"] = 2 
		self.step = self.param["step"] = .05 

		self.direction = self.param["direction"] = -135 
		self.dir_p = -P(1,0).rot(self.direction*pi/180.)		
	
		self.fastdist = 5
		self.geom = Geometry()

	def update(self) :
		self.traj.rapid(self.safex)
		for n in range(self.steps) :
			num = self.steps-n-1
			geom = self.geom.copy()
			print self.dir_p,self.dir_p*num*self.step
			geom.allowance((self.dir_p*num*self.step).x, (self.dir_p*num*self.step).y)
			geom.clip(self.stx,self.stz, self.endx, self.endz)
			if len(geom.g) == 0 :
				continue
#			print geom	
			# go inside 
			p = geom.g[0].st 

			self.traj.rapid(None, p.y + self.tool.in_p.y)
			self.traj.rapid(p.x + self.step + self.fastdist + self.tool.in_p.x, None)

			self.traj.feed_in(p.x + self.tool.in_p.x, None)
			self.traj.feed_in(p.x, p.y)	

			for e in geom.g : 
				if e.__class__ == Line :
					self.traj.feed(e.end)
				elif e.__class__ == Arc :
					self.traj.arc(e)
			
			self.traj.feed_out(self.stx, None)
			self.traj.rapid(self.safex)
		
class ShapeRough(Operation) :
	def init(self) :
		self.param = {}
		self.stx = self.param["maxx"] = 5
		self.endx = self.param["minx"] = 0
		self.stz = self.param["maxz"] = 20
		self.endz = self.param["minz"] = -30 
		self.safex = self.param["safex"] = 20 
		
		self.step = .5
		self.fastdist = 5
		self.geom = Geometry()
		
	def prepare(self) :
		pass
	
	def update(self) :
		done = False
		touched = False

		self.traj.rapid(self.safex, None)
		

		x = self.stx - self.step
		while x>self.endx and not done:
			done = False
			#print "X = %s"%x
			r = Ray( P(x, self.stz), P(x,self.endz) )
			#print r
			points = r.intersect_geom(self.geom)
			points = sum(points,[])
			if len(points) == 0 :
				if touched == True :
					done = True
					continue
				else : 
					p = P(x,self.endz)
					
			else :			
				touched = True	
				p = min(points, key=r.get_t_at_point)
				t = r.get_t_at_point(p)
				if t<=0 : 
					done = True
					continue				
			
			p.y = max(p.y, self.endz)
			
			self.traj.rapid(None, self.stz + self.tool.in_p.y)
			self.traj.rapid(x + self.step + self.fastdist + self.tool.in_p.x, None)
			
			self.traj.feed_in(x + self.tool.in_p.x, None)
			self.traj.feed_in(x, self.stz)	

			self.traj.feed(p)

			self.traj.feed_out(self.stx, None)
			self.traj.rapid(self.safex)

			x -= self.step
			
class Ray(Line) :
	def __init__(self, st, end) :
		self.st = st.copy()
		self.end = end.copy() 
	
	def __repr__(self) :
		return "Ray %s -> %s a=%s"%(self.st,self.end, (self.end-self.st).angle()/pi*180 )
		
	def intersect_geom(self, geom, true = True) :
		self.l = Line(self.st,self.end)
		res = []
		for g in geom.g : 
			res.append(self.intersect_g(g))
		return res		
	def intersect_g(self, g) :
		res = self.l.intersect(g,ray = True)
		return res
class Postprocessor() :
	pass
	
	
def run() :
	s = Sketch()
		
	

if __name__ == "__main__":
	s = Sketch(
				#'[{"st":{"x":0,"y":0},"end":{"x":0,"y":0}},{"st":{"x":0,"y":0},"end":{"x":1.25,"y":-2}},{"st":{"x":1.25,"y":-2},"end":{"x":1.25,"y":-3.5},"c":{"x":4.154737509655563,"y":-2.75},"a":0.5053605102841576,"ccw":true,"r":3},{"st":{"x":1.25,"y":-3.5},"end":{"x":1.25,"y":-5.5}},{"st":{"x":1.25,"y":-5.5},"end":{"x":1.25,"y":-7},"c":{"x":4.154737509655563,"y":-6.25},"a":0.5053605102841576,"ccw":true,"r":3},{"st":{"x":1.25,"y":-7},"end":{"x":1.25,"y":-9}},{"st":{"x":1.25,"y":-9},"end":{"x":2.5,"y":-11}},{"st":{"x":2.5,"y":-11},"end":{"x":2.5,"y":-13}},{"st":{"x":2.5,"y":-13},"end":{"x":2,"y":-13}},{"st":{"x":2,"y":-13},"end":{"x":2,"y":-20}}]'
				
			   '[{"st":{"x":0,"y":0},"end":{"x":1,"y":-0.5}},{"st":{"x":1,"y":-0.5},"end":{"x":1.25,"y":-2}},{"st":{"x":1.25,"y":-2},"end":{"x":1.25,"y":-3.5},"c":{"x":5.179058411375427,"y":-2.75},"a":0.37723277235080843,"ccw":true,"r":4},{"st":{"x":1.25,"y":-3.5},"end":{"x":1.25,"y":-5.5}},{"st":{"x":1.25,"y":-5.5},"end":{"x":1.25,"y":-7},"c":{"x":5.179058411375427,"y":-6.25},"a":0.37723277235080843,"ccw":true,"r":4},{"st":{"x":1.25,"y":-7},"end":{"x":1.25,"y":-9}},{"st":{"x":1.25,"y":-9},"end":{"x":2.5,"y":-11}},{"st":{"x":2.5,"y":-11},"end":{"x":2.5,"y":-13}},{"st":{"x":2.5,"y":-13},"end":{"x":2,"y":-13}},{"st":{"x":2,"y":-13},"end":{"x":2,"y":-20}}]'  
				)
	#print s
	p = PostProcessor()

	m = ShapeRough()	
	m.tool = LatheTool()
	m.geom.from_sketch(s) 
	m.update()
	p.operations.append(m)

#	print m
	m = ShapeContour()	
	m.tool = LatheTool()
	m.geom.from_sketch(s) 
	m.update()
	p.operations.append(m)

	p.update()
	open("/home/nick1/linuxcnc/nc_files/out.ngc","w").write(p.gcode)
	#print m.tool
