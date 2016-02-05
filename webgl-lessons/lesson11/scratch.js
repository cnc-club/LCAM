

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
		if(event.keyCode == 13){
				console.log(this);	
				console.log(this.closest(".TString"));
				root = this.closest(".TString");
				if ($(this).hasClass("x")) {
					$(".z").focus();
				}		    	
				if ($(this).hasClass("z")) {
					$(".chamfer").focus();
				}		    	
				if ($(this).hasClass("chamfer")) {
					$(".chamfer").focus();
				}		    	
				
			}
		});

		return root;
	}



  this.update = function(speed) {
  };

  this.stop = function() {
    this.speed = 0;
    alert( this.name + ' стоит' );
  };
};



function scratch_start(){
	root = $("#scratch");
	s = new TString();
	root.append(s.create());
}
