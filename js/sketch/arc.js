
function Arc(st,end,c,ccw) {
	this.st = new Vector(0,0);
	this.end = new Vector(0,0);
	this.c  = new Vector(0,0);;
	this.a = 0;
	this.ccw = false;
	this.r = 0;

	this.get_angle = function(){
		var a = this.end.clone().subtract(this.c).angle() - this.st.clone().subtract(this.c).angle();
		a = a%(2*Math.PI);
		if (a<0){ a+= 2*Math.PI;}
		if (this.ccw){
			a -= 2*Math.PI
		} 
		this.a = -a;		
	}

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
		this.get_angle();
	
	}
	
	this.draw = function (context,x0,y0) {
		a_st = this.st.clone().subtract(this.c).angle();
		a_end = this.end.clone().subtract(this.c).angle();
		
		context.arc(this.c.y + x0, this.c.x + y0, this.r, a_st, a_end, this.ccw)
	}
	

	this.draw3d = function (tess) {
		var points = [this.st.clone()]
		var ast = st.clone().subtract(this.c).angle();
		for (var i=0;i<tess-1;i++)
		{
			var p = this.st.clone();
			p = p.subtract(this.c).rot(this.a/tess*(i+1)).add(this.c);
			points.push(p);
		}
		points.push(this.end.clone())
		console.log("arc", points, tess)
		return points
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


