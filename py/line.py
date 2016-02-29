from points import P
from math import *
pi2 = pi*2

class Line():

	def __init__(self,st,end):
		if st.__class__ == P :  st = st.to_list()
		if end.__class__ == P :	end = end.to_list()
		self.st = P(st)
		self.end = P(end)
		self.l = self.length() 
		if self.l != 0 :
			self.n = ((self.end-self.st)/self.l).ccw()
		else: 
			self.n = [0,1]

	def allowance(self,x=None,y=None,r=None) :
		#TODO radius allowance
		if x!=None :
			self.st.x += x
			self.end.x += x
		if y!=None :
			self.st.y += y
			self.end.y += y

	
	def get_t_at_point(self,p) :
		if self.st.x-self.end.x != 0 :
			return (self.st.x-p.x)/(self.st.x-self.end.x)
		else :
			return (self.st.y-p.y)/(self.st.y-self.end.y)
			
	def __repr__(self) :
		return "Line: %s %s (l=%.3f) " % (self.st,self.end,self.l)
				
	def copy(self) : 
		return Line(self.st,self.end)
	
	def rebuild(self,st=None,end=None) : 
		if st==None: st=self.st
		if end==None: end=self.end
		self.__init__(st,end)
	
	def bounds(self) :
		return  ( min(self.st.x,self.end.x),min(self.st.y,self.end.y),
				  max(self.st.x,self.end.x),max(self.st.y,self.end.y) )
	
	def head(self,p):
		self.rebuild(end=p)

	def tail(self,p):
		self.rebuild(st=p)

	def offset(self, r):
		self.st -= self.n*r
		self.end -= self.n*r
		self.rebuild()
		
	def l2(self): return (self.st-self.end).l2()
	def length(self): return (self.st-self.end).mag()
	
	def draw(self, group=None, style=None, layer=None, transform=None, num = 0, reverse_angle = None, color = None, width=None) :
		pass
	
	def intersect(self,b, false_intersection = False, ray = False) :
		# ray = return including false-self intersections 
		if b.__class__ == Line :
			if self.l < 10e-8 or b.l < 10e-8 : return []
			v1 = self.end - self.st
			v2 = b.end - b.st
			x = v1.x*v2.y - v2.x*v1.y 
			if x == 0 :
				# lines are parallel
				res = []

				if (self.st.x-b.st.x)*v1.y - (self.st.y-b.st.y)*v1.x  == 0:
					# lines are the same
					if ray : 
						return [b.st,b.end]
					elif v1.x != 0 :
						if 0<=(self.st.x-b.st.x)/v2.x<=1 :  res.append(self.st)
						if 0<=(self.end.x-b.st.x)/v2.x<=1 :  res.append(self.end)
						if 0<=(b.st.x-self.st.x)/v1.x<=1 :  res.append(b.st)
						if 0<=(b.end.x-b.st.x)/v1.x<=1 :  res.append(b.end)
					else :
						if 0<=(self.st.y-b.st.y)/v2.y<=1 :  res.append(self.st)
						if 0<=(self.end.y-b.st.y)/v2.y<=1 :  res.append(self.end)
						if 0<=(b.st.y-self.st.y)/v1.y<=1 :  res.append(b.st)
						if 0<=(b.end.y-b.st.y)/v1.y<=1 :  res.append(b.end)
				return res
			else :
				t1 = ( v2.x*(self.st.y-b.st.y) - v2.y*(self.st.x-b.st.x) ) / x
				t2 = ( v1.x*(self.st.y-b.st.y) - v1.y*(self.st.x-b.st.x) ) / x
				
				if ray and 0<=t2<=1 : return  [ self.st+v1*t1 ]
				elif 0<=t1<=1 and 0<=t2<=1 or false_intersection : return [ self.st+v1*t1 ]	
				else : return []					
		else: 
			# taken from http://mathworld.wolfram.com/Circle-LineIntersection.html
			x1 = self.st.x - b.c.x
			x2 = self.end.x - b.c.x
			y1 = self.st.y - b.c.y
			y2 = self.end.y - b.c.y
			dx = x2-x1
			dy = y2-y1
			D = x1*y2-x2*y1
			dr = dx*dx+dy*dy
			descr = b.r**2*dr-D*D
			if descr<0 : return []
			if descr==0 :
				res = [ P([D*dy/dr+b.c.x,-D*dx/dr+b.c.y]) ]
				if false_intersection :
					return res
				res = b.check_intersection(res)
				if ray :
					return res  
				return self.check_intersection(res)
			sign = -1. if dy<0 else 1.
			descr = sqrt(descr)
			res = [
						 P( [ (D*dy+sign*dx*descr)/dr+b.c.x, (-D*dx+abs(dy)*descr)/dr+b.c.y ] ), 
						 P( [ (D*dy-sign*dx*descr)/dr+b.c.x, (-D*dx-abs(dy)*descr)/dr+b.c.y ] )
					]
			if false_intersection :
				return res
			res = b.check_intersection(res)
			if ray :
				return res  
			return self.check_intersection(res)

	def check_intersection(self, points):
		res = []
		for p in points :
			if ((self.st.x-1e-7<=p.x<=self.end.x+1e-7 or self.end.x-1e-7<=p.x<=self.st.x+1e-7)
				and 
				(self.st.y-1e-7<=p.y<=self.end.y+1e-7 or self.end.y-1e-7<=p.y<=self.st.y+1e-7)) :
			   		res.append(p)
		return res
	
	def point_d2(self, p) : 
		w0 = p - self.st
		v = self.end - self.st
		c1 = w0.dot(v)
		if c1 <= 0 :
			return w0.l2()
		c2 = v.dot(v)
		if c2 <= c1 :	
			return (p-self.end).l2()
			
		return ((self.st+c1/c2*v)-p).l2()


