ee = null;

function TString() {
	this.x = "";
	this.z = "";
	this.chamfer = "";
	this.i = "";
	this.k = "";
	this.r = "";
	this.ccw = "";

	this.start_x = 0;
	this.start_z = 0;
	this.end_x = 0;
	this.end_z = 0;

	function focus_next(el){
		$(el).next("input").focus();
	}

	function focus_prev(el){
		$(el).prev("input").focus();
	}

	function focus_up(el){
		cl = $(el).attr('class');
		st = $(el).parent().prev(".TString");
		$("."+cl, st).focus();
	}

	function focus_down(el){
		cl = $(el).attr('class');
		st = $(el).parent().next(".TString");
		if (st.length != 0){
			$("."+cl, st).focus();
		} else {
			s = new TString();
			sk = $(el).closest("#sketch");			
			$(sk).append(s.create());
			$(".TString ."+cl, sk).last().focus();
		}		
		
	}

	this.create = function() {
		root = $("<div class='TString'><div>");
		root.append("<input type='text' class='x'>");
		root.append("<input type='text' class='z'>");
		root.append("<input type='text' class='chamfer'>");
		root.append("<input type='text' class='i'>");
		root.append("<input type='text' class='k'>");
		root.append("<input type='text' class='r'>");
		root.append("<input type='checkbox' class='ccw'>");		
		
		this.root = root;

		$("input",root).keyup(function(event){
		if(event.keyCode == 13 || event.keyCode == 39){
				if ($(this).hasClass("chamfer") & event.keyCode == 13) 
				{
					focus_down(this, "x");
					$("input", $(':focus').parent()).first().focus();
				} else {
					focus_next(this);
				}
				sketch.update();
			}
		else if(event.keyCode == 37){
				focus_prev(this);
			}
		else if(event.keyCode == 38){
				focus_up(this);
			}
		else if(event.keyCode == 40){
				focus_down(this);
			}
		});

		return root;
	}

};

function Sketch(){

	this.create = function(){ 
		this.root = $("<div id='sketch'></div>");
		s = new TString();
		this.root.append(s.create());
		return this.root;
	}

	this.update = function (){
		result = []		
		$("#sketch .TString").each(function (){
			res = [];
			res.push($(".x",this).val());
			res.push($(".z",this).val());
			res.push($(".chamfer",this).val());
			res.push($(".i",this).val());
			res.push($(".k",this).val());
			res.push($(".r",this).val());
			res.push($(".ccw",this).val());
			result.push(res);
		});		
		console.log(result);
		this.result = result;
		this.draw2d();
	}


	this.draw2d = function (){
		x0 = 100;
		z0 = 150;
		canvas = $("#canvas")[0];
		context = canvas.getContext("2d");
		context.clearRect(0, 0, canvas.width, canvas.height);		
		
		console.log(this.result.length);
		x=0;
		z=0;
		context.beginPath();
		context.moveTo(z0+z,x0-x);

		for (num=0; num<this.result.length; num++)
			{
				st = this.result[num];
				xl = x;
				zl = z;
				
				// X
				s = st[0];
				s = s.replace(/u/gi,"X+");
				s = s.replace(/w/gi,"Z+");
				s = s.replace(/x/gi,x);
				s = s.replace(/z/gi,z);
				s = s.replace(/d/gi,"2*");
				s = s.replace(/\+\-/gi,"-");
				s = s.replace(/2\*\-/gi,"(-2)*");
				//console.log(s)				
				s = eval(s)
				if (s != NaN & s != undefined & s != Infinity) 
				{x = s;}
				
				// Z			
				s = st[1];
				s = s.replace(/u/gi,"X+");
				s = s.replace(/w/gi,"Z+");
				s = s.replace(/x/gi,x);
				s = s.replace(/z/gi,z);
				s = s.replace(/d/gi,"2*");
				s = s.replace(/\+\-/gi,"-");
				s = s.replace(/2\*\-/gi,"(-2)*");
				//console.log(s)
				s = eval(s)
				if (s != NaN & s != undefined & s != Infinity) 
				{z = s;}
				//console.log(x,z)
				
				
				if (st[3] != "" || st[4] != "" || st[5] != "") // it's an arc
				{
					console.log(st);
					s = st[3];
					// I
					s = s.replace(/u/gi,"X+");
					s = s.replace(/w/gi,"Z+");
					s = s.replace(/x/gi,x);
					s = s.replace(/z/gi,z);
					s = s.replace(/d/gi,"2*");
					s = s.replace(/\+\-/gi,"-");
					s = s.replace(/2\*\-/gi,"(-2)*");
					//console.log(s)
					s = eval(s)
					if (s != NaN & s != undefined & s != Infinity) 
					{i = s;} else {i = 0;}
					
					// J
					s = st[4];
					s = s.replace(/u/gi,"X+");
					s = s.replace(/w/gi,"Z+");
					s = s.replace(/x/gi,x);
					s = s.replace(/z/gi,z);
					s = s.replace(/d/gi,"2*");
					s = s.replace(/\+\-/gi,"-");
					s = s.replace(/2\*\-/gi,"(-2)*");
					//console.log(s)
					s = eval(s)
					if (s != NaN & s != undefined & s != Infinity) 
					{k = s;} else {k = 0;}
					
					// R
					s = st[5];
					s = s.replace(/u/gi,"X+");
					s = s.replace(/w/gi,"Z+");
					s = s.replace(/x/gi,x);
					s = s.replace(/z/gi,z);
					s = s.replace(/d/gi,"2*");
					s = s.replace(/\+\-/gi,"-");
					s = s.replace(/2\*\-/gi,"(-2)*");
					//console.log(s)
					s = eval(s)
					if (s != NaN & s != undefined & s != Infinity) 
					{r = s;} else {r = 0;}
								
					if (r == 0) {
						r = Math.sqrt(i^2+k^2);
					}
					else {

						p1 = new Vector(xl,zl);
						p2 = new Vector(x,z);
						p3 = p2.clone().subtract(p1).divide(2);
						console.log(p3.x,p3.y);
						l = Math.sqrt(r*r-p3.l2());
						console.log(l);
						p4 = p3.clone().ccw().unit().multiply(l);
						console.log(p4.x,p4.y);
						c = p3.clone().add(p4);
						console.log(c.x,c.y)
					}
//					a_st = 
					
					
//					x	The x-coordinate of the center of the circle	Play it »
//					y	The y-coordinate of the center of the circle	Play it »
//					r	The radius of the circle	Play it »
//					sAngle	The starting angle, in radians (0 is at the 3 o'clock position of the arc's circle)	Play it »
//					eAngle	The ending angle, in radians	Play it »
//					counterclockwise	Optional. Specifies whether the drawing should be counterclockwise or clockwise. False is default, and indicates clockwise, while true indicates counter-clockwise.
					
					
				}
				
				else // it's a line
				{
					context.lineTo(z0+z,x0-x);
				}

								
				
				
				
				
				
				
			}

	
		//context.arc(95, 85, 40, 0, 2*Math.PI);
		//context.closePath();
		context.lineWidth = 2;
		context.stroke();
}

}


