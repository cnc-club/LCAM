function Vector(x, y) {
  this.x = x || 0;
  this.y = y || 0;
}

Vector.prototype = {
  negative: function() {
    return new Vector(-this.x, -this.y);
  },
  add: function(v) {
    if (v instanceof Vector) return new Vector(this.x + v.x, this.y + v.y);
    else return new Vector(this.x + v, this.y + v);
  },
  subtract: function(v) {
    if (v instanceof Vector) return new Vector(this.x - v.x, this.y - v.y);
    else return new Vector(this.x - v, this.y - v);
  },
  multiply: function(v) {
    if (v instanceof Vector) return new Vector(this.x * v.x, this.y * v.y);
    else return new Vector(this.x * v, this.y * v);
  },
  divide: function(v) {
    if (v instanceof Vector) return new Vector(this.x / v.x, this.y / v.y);
    else return new Vector(this.x / v, this.y / v);
  },
  equals: function(v) {
    return this.x == v.x && this.y == v.y;
  },
  dot: function(v) {
    return this.x * v.x + this.y * v.y;
  },
  cross: function(v) {
    return new Vector(
      this.x * v.y - this.y * v.x
    );
  },
  length: function() {
    return Math.sqrt(this.dot(this));
  },
  l: function() {
    return Math.sqrt(this.dot(this));
  },
  l2: function() {
    return this.dot(this);
  },
  unit: function() {
    return this.divide(this.length());
  },
  min: function() {
    return Math.min(this.x, this.y);
  },
  max: function() {
    return Math.max(this.x, this.y);
  },
  angle: function() {
      return Math.atan2(this.x, this.y)
  },
  angleTo: function(a) {
    return Math.acos(this.dot(a) / (this.length() * a.length()));
  },
  toArray: function(n) {
    return [this.x, this.y].slice(0, n || 2);
  },
  clone: function() {
    return new Vector(this.x, this.y);
  },
  init: function(x, y) {
    this.x = x; this.y = y;
    return this;
  },
  ccw: function() {
  	t = this.x; this.x = -this.y; this.y = t;
    return this;
  },
  cw: function() {
  	t = this.x; this.x = this.y; this.y = -t;
    return this;
  }
  
  
};



