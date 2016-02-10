

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
		
		$("input",root).change(function(event){
				
				
				sketch.update();
			}
		)
		
		$("input",root).keyup(function(event){
		if(event.keyCode == 13 || event.keyCode == 39){
				if ($(this).hasClass("chamfer") & event.keyCode == 13) 
				{
					focus_down(this, "x");
					$("input", $(':focus').parent()).first().focus();
				} else {
					if ( this.type == "checkbox" || this.selectionStart == this.value.length){
						focus_next(this);
						}
				}
				sketch.update();
			}
		else if(event.keyCode == 37){
				if (this.type == "checkbox" || this.selectionStart == 0){
					focus_prev(this);
				}
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
			res.push($(".ccw",this)[0].checked);
			result.push(res);
		});		
		this.array_value = result; 
		this.get_shape();
		this.draw2d();
	}

	this.process_str = function(s){
		s = s.replace(/u/gi,"X+");
		s = s.replace(/w/gi,"Z+");
		s = s.replace(/x/gi,x);
		s = s.replace(/z/gi,z);
		s = s.replace(/d/gi,"2*");
		s = s.replace(/\+\-/gi,"-");
		s = s.replace(/2\*\-/gi,"(-2)*");
		//console.log(s)				
		s = eval(s)
		return s
	}

	this.get_shape = function (){
		this.shape = [];
		x = 0;
		z = 0;  	
		for (num=0; num<this.array_value.length; num++)
		{
				st = this.array_value[num];
				xl = x;
				zl = z;
				// X
				s = this.process_str(st[0]);
				if (s != NaN & s != undefined & s != Infinity) 
				{x = s;}
				// Z
				s = this.process_str(st[1]);
				if (s != NaN & s != undefined & s != Infinity) 
				{z = s;}
				
				if (st[3] != "" || st[4] != "" || st[5] != "") // it's an arc
				{
					// I
					s = this.process_str(st[3]);
					if (s != NaN & s != undefined & s != Infinity) 
					{i = s;} else {i = 0;}
					// K
					s = this.process_str(st[4]);
					if (s != NaN & s != undefined & s != Infinity) 
					{k = s;} else {k = 0;}
					// R
					s = this.process_str(st[5]);
					if (s != NaN & s != undefined & s != Infinity) 
					{r = s;} else {r = 0;}
					
					if (r == 0) {
						a = new Arc(new Vector(xl,zl), new Vector(x,z), new Vector(xl+i,zl+k), st[6])
					}
					else {
						a = new Arc(new Vector(xl,zl), new Vector(x,z), r, st[6])
					}
					
					this.shape.push(a);
				}
				
				else // it's a line
				{
					this.shape.push(  new Line(new Vector(xl,zl), new Vector(x,z))   );
				}

		}
		console.log(this.shape);

	}


	this.draw2d = function (){
	
		
		x0 = 100;
		y0 = 150;
		canvas = $("#canvas")[0];
		context = canvas.getContext("2d");
		context.clearRect(0, 0, canvas.width, canvas.height);		
		
		context.beginPath();
		context.moveTo(x0,y0);

		for (num=0; num<this.shape.length; num++)
			{
				console.log(this.shape[num]);
				this.shape[num].draw(context,x0,y0);
			}
		context.lineWidth = 1;
		context.stroke();
	}

}


