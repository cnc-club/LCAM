
function Arc(st,end,c,ccw) {
	this.st = new Vector(0,0);
	this.end = new Vector(0,0);
	this.c  = new Vector(0,0);;
	this.ccw = false;
	this.r = 0;

	this.createFrom = function(st,end,c,ccw){
		this.st = st.clone();
		this.end = end.clone();
		if (c instanceof Vector) 
		{
			this.c = c.clone();
			this.r = c.clone().subtract(this.st).l();
		} else {
			this.r = c;
			p3 = end.clone().subtract(st).divide(2);
			l = Math.sqrt(this.r*this.r-p3.l2());
			p4 = p3.clone().ccw().unit().multiply(l);
			this.c = p3.clone().add(p4).add(st);
		}	
		this.ccw = ccw;
	}
	
	this.draw = function (context,x0,y0) {
		a_st = this.st.clone().subtract(this.c).angle();
		a_end = this.end.clone().subtract(this.c).angle();
		
		context.arc(this.c.y + x0, this.c.x + y0, this.r, a_st, a_end, this.ccw)
	}
	

	this.draw3d = function (tess) {
		p = [this.st]
		ast = Math.atan2(st);
		a = Math.atan2(end)-Math.atan2(st);
		for (var i=0;i<tess;i++)
		{
			p = this.st.clone()
			p = p.subtract(this.c).rot(ast+a/tess*(i+1)).add(this.c);
			p.push(p);
		}
		return p
	}

	this.create = function(st,end,c,ccw) {
		// start - vector
		// end - vector
		// c - center vector OR radius
		// ccw - ccw or cw
		this.createFrom(st,end,c,ccw);
	}

	this.createFrom(st,end,c,ccw);

};


