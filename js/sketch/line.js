
function Line(st,end) {

	this.clone = function(){
		return new Line(this.st,this.end);
	}
	
	this.createFrom = function(st,end){
		this.st = st.clone();
		this.end = end.clone();
	}
		
	this.draw = function (context,x0,y0) {
		context.moveTo(this.st.y + x0, this.st.x + y0);
		context.lineTo(this.end.y + x0, this.end.x + y0);
	}
	

	this.create = function(st,end) {
		// start - vector
		// end - vector
		this.createFrom(st,end);
	}
	this.createFrom(st,end);
	
	this.draw3d = function() {
		return [this.st,this.end];
	}


};


