
function Canvas3d(){
	if ( ! Detector.webgl ) Detector.addGetWebGLMessage();

	this.tess = -1;	// force initialization

	// allocate these just once
	this.diffuseColor = new THREE.Color();
	this.specularColor = new THREE.Color();

	this.init = function() {

		this.container = $( '#canvas3d' );

		this.w = this.container.width();
		this.h = this.container.height();
	
		// CAMERA
		this.camera = new THREE.PerspectiveCamera( 10, this.w / this.w, 1, 80000 );

		this.camera.position.set( -600, 550, 1300 );

		// LIGHTS
		this.ambientLight = new THREE.AmbientLight( 0x333333 );	// 0.2

		this.light = new THREE.DirectionalLight( 0xFFFFFF, 1.0 );
		// direction is set in GUI

		// RENDERER
		this.renderer = new THREE.WebGLRenderer( { antialias: true } );
		this.renderer.setClearColor( 0xAAAAAA );
		this.renderer.setPixelRatio( this.container.devicePixelRatio );
		this.renderer.setSize( this.w, this.h );
		this.renderer.gammaInput = true;
		this.renderer.gammaOutput = true;
		this.container.append( this.renderer.domElement );
		// EVENTS
		this.container.resize(	function() {
											this.onWindowResize();
								}.bind(this), false );
		// CONTROLS
		this.cameraControls = new THREE.OrbitControls( this.camera, this.renderer.domElement );
		this.cameraControls.target.set( 0, 0, 0 );
		this.cameraControls.addEventListener( 'change',
												function() {
													this.render();
												}.bind(this)
										);

		// MATERIALS
		var materialColor = new THREE.Color();
		materialColor.setRGB( 1.0, 0.5, 1.0 );

		this.wireMaterial = new THREE.MeshBasicMaterial( { color: 0xFFFFFF, wireframe: true } ) ;
		this.flatMaterial = new THREE.MeshPhongMaterial( { color: materialColor, specular: 0x0, shading: THREE.FlatShading, side: THREE.DoubleSide } );
		this.gouraudMaterial = new THREE.MeshLambertMaterial( { color: materialColor, side: THREE.DoubleSide } );
		this.phongMaterial = new THREE.MeshPhongMaterial( { color: materialColor, shading: THREE.SmoothShading, side: THREE.DoubleSide } );

		// SKYBOX
		var shader = THREE.ShaderLib[ "cube" ];
		var skyboxMaterial = new THREE.ShaderMaterial( {
			fragmentShader: shader.fragmentShader,
			vertexShader: shader.vertexShader,
			uniforms: shader.uniforms,
			depthWrite: false,
			side: THREE.BackSide
		} );

		this.skybox = new THREE.Mesh( new THREE.BoxGeometry( 5000, 5000, 5000 ), skyboxMaterial );

		// skybox scene - keep camera centered here
		this.sceneCube = new THREE.Scene();
		this.sceneCube.add( this.skybox );

		// scene itself
		this.scene = new THREE.Scene();

		this.scene.add( this.ambientLight );
		this.scene.add( this.light );

		// GUI
		this.setupGui();
		this.init_helpers();
		
		this.render();
	}

	// EVENT HANDLERS
	this.onWindowResize = function() {
		this.w = this.container.width();
		this.h = this.container.height();
		this.renderer.setSize( this.w, this.h );
		this.camera.aspect = this.w / this.h;
		this.camera.updateProjectionMatrix();
		this.render();
	}

	this.setupGui = function() {
		effectController = {
			newTess: 30,
			newShading: "glossy",
			newEdgesHelper: false
		};

		var h;

		var gui = new dat.GUI({ autoPlace: false, closed: true });
		gui.close();
		// material (attributes)
		h = gui.add( effectController, "newTess", [ 6, 8, 10, 15, 20, 30, 40, 50 ] ).name( "Tessellation Level" ).onChange( render_func );
		h = gui.add( effectController, "newShading", [ "wireframe", "flat", "smooth", "glossy" ] ).name( "Shading" ).onChange( render_func );
		h = gui.add( effectController, "newEdgesHelper" ).name( "Display wireframe" ).onChange( render_func );	
		this.container.append(gui.domElement);	
	}
		
	this.update_camera = function(ev,me){
		me.render();
	}
	
	render_func = function() {
		this.render();
	}.bind(this)
	
	this.render = function() {
		if ( effectController.newTess !== this.tess ||
			effectController.newShading !== this.shading ||
			effectController.newEdgesHelper !== this.edgesHelper
			 )
		{
			this.tess = effectController.newTess;
			this.shading = effectController.newShading;
			this.edgesHelper = effectController.newEdgesHelper;
			this.createScene();
		}

		this.renderer.autoClear = true;
		this.renderer.render( this.scene, this.camera );
	}

	this.createScene = function() {

		if ( this.obj !== undefined ) {

			this.obj.geometry.dispose();
			this.scene.remove( this.obj );
		}

		var points = [];
		for ( var i = 0; i < 10; i ++ ) {
			points.push( new THREE.Vector2( Math.random() * 15 + 50, ( i - 5 ) * 2 ) );
		}
		var geometry = new THREE.LatheGeometry( points, this.tess );

		this.obj = new THREE.Mesh(
			geometry,
			this.shading === "wireframe" ? this.wireMaterial : (
			this.shading === "flat" ? this.flatMaterial : (
			this.shading === "smooth" ? this.gouraudMaterial : (
			this.shading === "glossy" ? this.phongMaterial : this.phongMaterial
								) ) ) );	// if no match, pick Phong

		//scene.add( teapot );
		this.scene.add( this.obj );

		if ( this.edges != undefined){
			this.edges.geometry.dispose();
			this.scene.remove(this.edges);
		}
		if ( this.edgesHelper )
		{
			this.edges = new THREE.EdgesHelper( this.obj, 0xaa0000 );
			this.scene.add( this.edges );
		}
	}
			
			
	this.init_helpers = function() {
	
		var axisHelper = new THREE.AxisHelper( 5 );
		this.scene.add( axisHelper );


		var size = 100;
		var step = 1;

		var gridHelper = new THREE.GridHelper( size, step, "Y" );
		this.scene.add( gridHelper );

	}
	
				
}			

