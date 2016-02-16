// File:src/extras/helpers/GridHelper.js

/**
 * @author mrdoob / http://mrdoob.com/
 */

THREE.GridHelper = function ( size, step, normal_to ) {

	var geometry = new THREE.Geometry();
	var material = new THREE.LineBasicMaterial( { vertexColors: THREE.VertexColors } );

	this.color0 = new THREE.Color( 0x666666 );
	this.color1 = new THREE.Color( 0x333333 );
	this.color2 = new THREE.Color( 0x662222 );
	normal_to = normal_to.toUpperCase()
	for ( var i = - size; i <= size; i += step ) {
	if (normal_to == "X")
		{
			a = new THREE.Vector3( 0, - size, i ),
			b = new THREE.Vector3( 0, size, i ),
			c = new THREE.Vector3( 0,  i, - size ), 
			d = new THREE.Vector3( 0, i, size )
		}
	if (normal_to == "Y")
		{
			a = new THREE.Vector3( - size, 0, i ), 
			b = new THREE.Vector3( size, 0, i ),
			c = new THREE.Vector3( i, 0, - size ), 
			d = new THREE.Vector3( i, 0, size )
		}
	if (normal_to == "Z")
		{
			a = new THREE.Vector3( - size, i, 0 ), 
			b = new THREE.Vector3( size, i, 0 ),
			c = new THREE.Vector3( i, - size, 0 ), 
			d = new THREE.Vector3( i, size, 0 )
		}

		geometry.vertices.push(a,b,c,d);

		var color = (i === 0 ? this.color2 : (i%5 == 0 ? this.color1 : this.color0));

		geometry.colors.push( color, color, color, color );

	}
	material.opacity = 0.5;
	material.transparent = true;
	THREE.LineSegments.call( this, geometry, material );

};

THREE.GridHelper.prototype = Object.create( THREE.LineSegments.prototype );
THREE.GridHelper.prototype.constructor = THREE.GridHelper;

THREE.GridHelper.prototype.setColors = function( colorCenterLine, colorGrid ) {

	this.color1.set( colorCenterLine );
	this.color2.set( colorGrid );

	this.geometry.colorsNeedUpdate = true;

};

