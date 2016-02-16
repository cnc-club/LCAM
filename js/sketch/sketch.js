var ee;



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
		var root = $(el).closest(".TString");
		var i = $("input[type=text],input[type=checkbox]",root).index(el);
		$("input[type=text],input[type=checkbox]",root)[i+1].focus();
	}

	function focus_prev(el){
		var root = $(el).closest(".TString");
		var i = $("input[type=text],input[type=checkbox]",root).index(el);
		$("input[type=text],input[type=checkbox]",root)[i-1].focus();
	}

	function focus_up(el){
		cl = $(el).attr('class');
		st = $(el).closest(".TString").prev(".TString");
		$("."+cl, st).focus();
	}

	function focus_down(el){
		cl = $(el).attr('class');
		st = $(el).closest(".TString").next(".TString");
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
		root.append("	<input type='text' class='x'>");
		root.append("<input type='text' class='z'>");
		root.append("<input type='text' class='chamfer'>");
		root.append("<input type='checkbox' class='arc'>");
		root.append("<input type='button' class='add' value='+'>");
		root.append("<input type='button' class='del' value='-'>");
		
		div = $("<div class='arc'></div>");
		div.append("<span>i</span><input type='text' class='i'>");
		div.append("<span>k</span><input type='text' class='k'>");
		div.append("<span>r</span><input type='text' class='r'>");
		div.append("<span>ccw</span><input type='checkbox' class='ccw'>");		
		root.append(div);
		div.hide();
		this.root = root;
		
		$("input",root).change(function(event){
				el = event.target;
				if ($(el).hasClass("arc"))
				{
					if (el.checked){
						$(el).closest(".TString").find("div.arc").show();
					}else 
					{
						$(el).closest(".TString").find("div.arc").hide();
					}
				}
				
				
				sketch.update();
			}
		)
		
		$("input ",root).keyup(function(event){
		if(event.keyCode == 13 || event.keyCode == 39){
				if ($(this).hasClass("chamfer") & event.keyCode == 13) 
				{
					focus_down(this, "x");
					$("input", $(':focus').parent()).first().focus();
				} else {
					if ( this.type == "checkbox" || (this.selectionStart == this.value.length && end_of_input )){
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

		if ( this.type == "text" && this.selectionStart == this.value.length )
			{end_of_input = true;}
		else
			{end_of_input = false;}


		});


		return root;
	}

};

var end_of_input;

function Sketch(){

	this.create = function(){ 
		this.root = $(
			"<div id='sketch'>"+
				"<div class='header'><span class='x'>x</span><span class='z'>z</span><span class='chamfer'>chamfer</span><span class='arc'>arc</span></div>"+
			"</div>"
		);
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


	this.draw2d_grid = function(context,w,h,x0,y0,size){
		
		canvas = $("#canvas")[0];
		context = canvas.getContext("2d");
		context.beginPath();
		context.moveTo(x0,0);
		context.lineTo(x0,h);
		context.moveTo(0,y0);
		context.lineTo(w,y0);
		context.lineWidth = .5;		
		context.strokeStyle="#aa0000";	
		context.stroke();	
		
		for (i=0; i<=w/size; i++){
			x = (x0%size) + i*size;
			context.moveTo(x,0);
			context.lineTo(x,h);
		}
		for (i=0; i<=h/size; i++){
			y = (y0%size) + i*size;
			context.moveTo(0,y);
			context.lineTo(w,y);
		}
		
		
		context.lineWidth = .2;		
		context.strokeStyle="#aaa";	
		context.stroke();	


	}

	this.draw2d = function (){
		w = $("#canvas").width();
		h = $("#canvas").height();
		x0 = w/2;
		y0 = h/2;

		canvas = $("#canvas")[0];
		context = canvas.getContext("2d");
		context.clearRect(0, 0, canvas.width, canvas.height);		

		this.draw2d_grid(context,w,h,x0,y0,10);
		
		context.beginPath();
		context.moveTo(x0,y0);

		for (num=0; num<this.shape.length; num++)
			{
				console.log(this.shape[num]);
				this.shape[num].draw(context,x0,y0);
			}
		context.lineWidth = 2;
		context.strokeStyle="#590";			
		context.stroke();
	}

}

