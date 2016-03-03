from points import P
from math import *
from line import *
pi2 = pi*2

class Arc():
	def __init__(self,st,end,c,a,r=None) :
		#debugger.add_debugger_to_class(self.__class__)
		# a - arc's angle, it's not defining actual angle before now, but defines direction so it's value does not mather matters only the sign.
		if st.__class__ == P :  st = st.to_list()
		if end.__class__ == P : end = end.to_list()
		if c.__class__ == P :   c = c.to_list()
		self.st = P(st)
		self.end = P(end)
		self.c = P(c)
		if r == None : self.r = (P(st)-P(c)).mag()
		else: self.r = r
		self.a = ( (self.st-self.c).angle() - (self.end-self.c).angle() ) % pi2
		if a>0 : self.a -= pi2
		self.a *= -1.
		self.cp = (self.st-self.c).rot(self.a/2)+self.c # central point of an arc

	def __repr__(self) :
		return "Arc: s%s e%s c%s r%.2f a%.2f (l=%.3f) " % (self.st,self.end,self.c,self.r,self.a,self.length())


	def clip(self, x,y,x1,y1):
		t = []
		t.append(self.get_t_at_x(x))
		t.append(self.get_t_at_x(x1))
		t.append(self.get_t_at_y(y))
		t.append(self.get_t_at_y(y1))
		t = [i for i in t if 0<i<1] 
		t.sort()
		t = [0] + t + [1]
		t = [self.at_t(i) for i in t]
		res = []
		for i in range(len(t)-1):
			res.append( Arc(t[i], t[i+1], self.c, self.a ) )
		
		def inside(p) :
			return x<p.x<x1 and y<p.y<y1 
		
		res = [  a if (x<a.cp.x<x1 and y<a.cp.y<y1) else Line(a.st,a.end)  
					for a in res ]
		for l in res :
			if l.__class__ == Line :
				l.st.x = x1 if l.st.x>x1 else ( x if l.st.x<x else l.st.x) 
				l.st.y = y1 if l.st.y>y1 else ( y if l.st.y<y else l.st.y) 
				l.end.x = x1 if l.end.x>x1 else ( x if l.end.x<x else l.end.x) 
				l.end.y = y1 if l.end.y>y1 else ( y if l.end.y<y else l.end.y) 
			
		res = [  a for a in res if a.__class__== Arc or a.l2>0 ]

		return res

	def allowance(self,x=None,y=None,r=None) :
		#TODO radius allowance
		if x!=None :
			self.st.x += x
			self.end.x += x
			self.c.x += x
			self.cp.x += x
		if y!=None :
			self.st.y+= y
			self.end.y += y
			self.c.y += y
			self.cp.y += y

	def copy(self) :
		return Arc(self.st,self.end,self.c,self.a,self.r)	

	def rebuild(self,st=None,end=None,c=None,a=None,r=None) : 
		if st==None: st=self.st
		if end==None: end=self.end
		if c==None: c=self.c
		if a==None: a=self.a
		if r==None: r=self.r
		self.__init__(st,end,c,a,r)
	
	def at_t(self, t) :
		return (self.st-self.c).rot(self.a*t)+self.c

	def get_t_at_point(self, p, y=None) :
		if y!=None : p = P(p,y)
		if not self.point_inside_angle(p) : return -1.
		return abs( acos( (self.st-self.c).dot((p-self.c))/(self.r**2) )/pi ) # consuming all arcs les than 180 deg

	def get_t_at_x(self,x) :
		if self.r<abs(self.c.x-x) or self.a == 0 :
			return []
		y = sqrt( self.r**2 - (self.c.x-x)**2 )
		a = [P(x-self.c.x,y).angle(), P(x-self.c.x,-y).angle() ] if y!=0 else [P(x-self.c.x,0).angle()]
		s = (self.st-self.c).angle()
		a = [ ( i-(self.st-self.c).angle() )/self.a for i in a]
		return a
			
	def get_t_at_y(self,y) :
		if self.r<abs(self.c.y-y) or self.a == 0 :
			return []
		x = sqrt( self.r**2 - (self.c.y-y)**2 )
		a = [P(x,y-self.c.y).angle(), P(x,y-self.c.y).angle() ] if y!=0 else [P(0,y-self.c.y).angle()]
		s = (self.st-self.c).angle()
		a = [ ( i-(self.st-self.c).angle() )/self.a for i in a]
		return a
		
	def point_inside_angle(self,p,y=None) :  # TODO need to be done faster! 
		if y!=None : p = P(p,y)
		if (p-self.c).l2() != self.r**2 :  # p is not on the arc, lets move it there
			p = self.c+(p-self.c).unit()*self.r
		#warn( (self.cp-self.c).dot(p-self.c),self.r**2, (self.cp-self.c).dot(p-self.c)/self.r**2)
		try:
			abs(  acos( (self.cp-self.c).dot(p-self.c) /self.r**2  )  )  <  abs(self.a/2)
		except :
			self.draw()
			return True	 
		return abs(  acos( (self.cp-self.c).dot(p-self.c) /self.r**2  )  )  <  abs(self.a/2) 

	def bounds(self) : 
		# first get bounds of start/end 
		x1,y1, x2,y2 =  ( min(self.st.x,self.end.x),min(self.st.y,self.end.y),
						  max(self.st.x,self.end.x),max(self.st.y,self.end.y) )
		# Then check 0,pi/2,pi and 2pi angles. 
		if self.point_Gde_angle(self.c+P(0,self.r)) :
			y2 = max(y2, self.c.y+self.r)
		if self.point_inside_angle(self.c+P(0,-self.r)) :
			y1 = min(y1, self.c.y-self.r)
		if self.point_inside_angle(self.c+P(-self.r,0)) :
			x1 = min(x1, self.c.x-self.r)
		if self.point_inside_angle(self.c+P(self.r,0)) :
			x2 = max(x2, self.c.x+self.r)
		return x1,y1, x2,y2

	def head(self,p):
		self.rebuild(end=p)

	def tail(self,p):
		self.rebuild(st=p)

	def offset(self, r):
		oldr = self.r
		if self.a>0 :
			self.r = self.r + r
		else :
			self.r = self.r - r
		
		if self.r != 0 :
			self.st = self.c + (self.st-self.c)*self.r/oldr
			self.end = self.c + (self.end-self.c)*self.r/oldr
		self.rebuild()	
			
	def length(self):
		return abs(self.a*self.r)
	

	def draw(self, group=None, style=None, layer=None, transform=None, num = 0, reverse_angle = None, color=None, width=None):
		pass
	
	def check_intersection(self, points): 
		res = []
 		for p in points :
 			if self.point_inside_angle(p) :
 				res.append(p)
		return res		
		
	def intersect(self,b) :
		if b.__class__ == Line :
			return b.intersect(self)
		else : 
			# taken from http://paulbourke.net/geometry/2circle/
			if (self.st-b.st).l2()<1e-10 and (self.end-b.end).l2()<1e-10 : return [self.st,self.end]
			r0 = self.r 
			r1 = b.r
			P0 = self.c
			P1 = b.c
			d2 = (P0-P1).l2() 
			d = sqrt(d2)
			if d>r0+r1  or r0+r1<=0 or d2<(r0-r1)**2 :
				return []
			if d2==0 and r0==r1 :
				return self.check_intersection( b.check_intersection(
					[self.st, self.end, b.st, b.end] ) )
			if d == r0+r1  :
				return self.check_intersection( b.check_intersection(
								[P0 + (P1 - P0)*r0/(r0+r1)]  ) )
			else: 
				a = (r0**2 - r1**2 + d2)/(2.*d)
				P2 = P0 + a*(P1-P0)/d
				h = r0**2-a**2
				h = sqrt(h) if h>0 else 0. 
				return self.check_intersection(b.check_intersection( [
							P([P2.x+h*(P1.y-P0.y)/d, P2.y-h*(P1.x-P0.x)/d]),
							P([P2.x-h*(P1.y-P0.y)/d, P2.y+h*(P1.x-P0.x)/d]),
						] ))

	def point_d2(self, p):
		if self.point_inside_angle(p) :
			l = (p-self.c).mag()
			if l == 0 : return self.r**2
			else : return ((p-self.c)*(1 - self.r/l)).l2()
		else :
			return min( (p-self.st).l2(), (p-self.end).l2() )	


