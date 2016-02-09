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
			sk = el.closest("#sketch");			
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
		root.append("<input type='text' class='j'>");
		root.append("<input type='text' class='r'>");
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
			result.push(res);
		});		
		console.log(result);

	}

}

