// /*
//  (c) 2014, Vladimir Agafonkin
//  simpleheat, a tiny JavaScript library for drawing heatmaps with Canvas
//  https://github.com/mourner/simpleheat
// */
// !function(){"use strict";function t(i){return this instanceof t?(this._canvas=i="string"==typeof i?document.getElementById(i):i,this._ctx=i.getContext("2d"),this._width=i.width,this._height=i.height,this._max=1,void this.clear()):new t(i)}t.prototype={defaultRadius:25,defaultGradient:{.4:"blue",.6:"cyan",.7:"lime",.8:"yellow",1:"red"},data:function(t,i){return this._data=t,this},max:function(t){return this._max=t,this},add:function(t){return this._data.push(t),this},clear:function(){return this._data=[],this},radius:function(t,i){i=i||15;var a=this._circle=document.createElement("canvas"),s=a.getContext("2d"),e=this._r=t+i;return a.width=a.height=2*e,s.shadowOffsetX=s.shadowOffsetY=200,s.shadowBlur=i,s.shadowColor="black",s.beginPath(),s.arc(e-200,e-200,t,0,2*Math.PI,!0),s.closePath(),s.fill(),this},gradient:function(t){var i=document.createElement("canvas"),a=i.getContext("2d"),s=a.createLinearGradient(0,0,0,256);i.width=1,i.height=256;for(var e in t)s.addColorStop(e,t[e]);return a.fillStyle=s,a.fillRect(0,0,1,256),this._grad=a.getImageData(0,0,1,256).data,this},draw:function(t){this._circle||this.radius(this.defaultRadius),this._grad||this.gradient(this.defaultGradient);var i=this._ctx;i.clearRect(0,0,this._width,this._height);for(var a,s=0,e=this._data.length;e>s;s++)a=this._data[s],i.globalAlpha=Math.max(a[2]/this._max,t||.05),i.drawImage(this._circle,a[0]-this._r,a[1]-this._r);var n=i.getImageData(0,0,this._width,this._height);return this._colorize(n.data,this._grad),i.putImageData(n,0,0),this},_colorize:function(t,i){for(var a,s=3,e=t.length;e>s;s+=4)a=4*t[s],a&&(t[s-3]=i[a],t[s-2]=i[a+1],t[s-1]=i[a+2])}},window.simpleheat=t}(),/*
//  (c) 2014, Vladimir Agafonkin
//  Leaflet.heat, a tiny and fast heatmap plugin for Leaflet.
//  https://github.com/Leaflet/Leaflet.heat
// */
// L.HeatLayer=(L.Layer?L.Layer:L.Class).extend({initialize:function(t,i){this._latlngs=t,L.setOptions(this,i)},setLatLngs:function(t){return this._latlngs=t,this.redraw()},addLatLng:function(t){return this._latlngs.push(t),this.redraw()},setOptions:function(t){return L.setOptions(this,t),this._heat&&this._updateOptions(),this.redraw()},redraw:function(){return!this._heat||this._frame||this._map._animating||(this._frame=L.Util.requestAnimFrame(this._redraw,this)),this},onAdd:function(t){this._map=t,this._canvas||this._initCanvas(),t._panes.overlayPane.appendChild(this._canvas),t.on("moveend",this._reset,this),t.options.zoomAnimation&&L.Browser.any3d&&t.on("zoomanim",this._animateZoom,this),this._reset()},onRemove:function(t){t.getPanes().overlayPane.removeChild(this._canvas),t.off("moveend",this._reset,this),t.options.zoomAnimation&&t.off("zoomanim",this._animateZoom,this)},addTo:function(t){return t.addLayer(this),this},_initCanvas:function(){var t=this._canvas=L.DomUtil.create("canvas","leaflet-heatmap-layer leaflet-layer"),i=L.DomUtil.testProp(["transformOrigin","WebkitTransformOrigin","msTransformOrigin"]);t.style[i]="50% 50%";var a=this._map.getSize();t.width=a.x,t.height=a.y;var s=this._map.options.zoomAnimation&&L.Browser.any3d;L.DomUtil.addClass(t,"leaflet-zoom-"+(s?"animated":"hide")),this._heat=simpleheat(t),this._updateOptions()},_updateOptions:function(){this._heat.radius(this.options.radius||this._heat.defaultRadius,this.options.blur),this.options.gradient&&this._heat.gradient(this.options.gradient),this.options.max&&this._heat.max(this.options.max)},_reset:function(){var t=this._map.containerPointToLayerPoint([0,0]);L.DomUtil.setPosition(this._canvas,t);var i=this._map.getSize();this._heat._width!==i.x&&(this._canvas.width=this._heat._width=i.x),this._heat._height!==i.y&&(this._canvas.height=this._heat._height=i.y),this._redraw()},_redraw:function(){var t,i,a,s,e,n,h,o,r,d=[],_=this._heat._r,l=this._map.getSize(),m=new L.Bounds(L.point([-_,-_]),l.add([_,_])),c=void 0===this.options.max?1:this.options.max,u=void 0===this.options.maxZoom?this._map.getMaxZoom():this.options.maxZoom,f=1/Math.pow(2,Math.max(0,Math.min(u-this._map.getZoom(),12))),g=_/2,p=[],v=this._map._getMapPanePos(),w=v.x%g,y=v.y%g;for(t=0,i=this._latlngs.length;i>t;t++)if(a=this._map.latLngToContainerPoint(this._latlngs[t]),m.contains(a)){e=Math.floor((a.x-w)/g)+2,n=Math.floor((a.y-y)/g)+2;var x=void 0!==this._latlngs[t].alt?this._latlngs[t].alt:void 0!==this._latlngs[t][2]?+this._latlngs[t][2]:1;r=x*f,p[n]=p[n]||[],s=p[n][e],s?(s[0]=(s[0]*s[2]+a.x*r)/(s[2]+r),s[1]=(s[1]*s[2]+a.y*r)/(s[2]+r),s[2]+=r):p[n][e]=[a.x,a.y,r]}for(t=0,i=p.length;i>t;t++)if(p[t])for(h=0,o=p[t].length;o>h;h++)s=p[t][h],s&&d.push([Math.round(s[0]),Math.round(s[1]),Math.min(s[2],c)]);this._heat.data(d).draw(this.options.minOpacity),this._frame=null},_animateZoom:function(t){var i=this._map.getZoomScale(t.zoom),a=this._map._getCenterOffset(t.center)._multiplyBy(-i).subtract(this._map._getMapPanePos());L.DomUtil.setTransform?L.DomUtil.setTransform(this._canvas,a,i):this._canvas.style[L.DomUtil.TRANSFORM]=L.DomUtil.getTranslateString(a)+" scale("+i+")"}}),L.heatLayer=function(t,i){return new L.HeatLayer(t,i)};


/*
* Leaflet Heatmap Overlay
*
* Copyright (c) 2008-2016, Patrick Wied (https://www.patrick-wied.at)
* Dual-licensed under the MIT (http://www.opensource.org/licenses/mit-license.php)
* and the Beerware (http://en.wikipedia.org/wiki/Beerware) license.
*/
;(function (name, context, factory) {
    // Supports UMD. AMD, CommonJS/Node.js and browser context
    if (typeof module !== "undefined" && module.exports) {
      module.exports = factory(
        require('heatmap.js'),
        require('leaflet')
      );
    } else if (typeof define === "function" && define.amd) {
      define(['heatmap.js', 'leaflet'], factory);
    } else {
      // browser globals
      if (typeof window.h337 === 'undefined') {
        throw new Error('heatmap.js must be loaded before the leaflet heatmap plugin');
      }
      if (typeof window.L === 'undefined') {
        throw new Error('Leaflet must be loaded before the leaflet heatmap plugin');
      }
      context[name] = factory(window.h337, window.L);
    }
  
  })("HeatmapOverlay", this, function (h337, L) {
    'use strict';
  
    // Leaflet < 0.8 compatibility
    if (typeof L.Layer === 'undefined') {
      L.Layer = L.Class;
    }
  
    var HeatmapOverlay = L.Layer.extend({
  
      initialize: function (config) {
        this.cfg = config;
        this._el = L.DomUtil.create('div', 'leaflet-zoom-hide');
        this._data = [];
        this._max = 1;
        this._min = 0;
        this.cfg.container = this._el;
      },
  
      onAdd: function (map) {
        var size = map.getSize();
  
        this._map = map;
  
        this._width = size.x;
        this._height = size.y;
  
        this._el.style.width = size.x + 'px';
        this._el.style.height = size.y + 'px';
        this._el.style.position = 'absolute';
  
        this._origin = this._map.layerPointToLatLng(new L.Point(0, 0));
  
        map.getPanes().overlayPane.appendChild(this._el);
  
        if (!this._heatmap) {
          this._heatmap = h337.create(this.cfg);
        } 
  
        // this resets the origin and redraws whenever
        // the zoom changed or the map has been moved
        map.on('moveend', this._reset, this);
        this._draw();
      },
  
      addTo: function (map) {
        map.addLayer(this);
        return this;
      },
  
      onRemove: function (map) {
        // remove layer's DOM elements and listeners
        map.getPanes().overlayPane.removeChild(this._el);
  
        map.off('moveend', this._reset, this);
      },
      _draw: function() {
        if (!this._map) { return; }
        
        var mapPane = this._map.getPanes().mapPane;
        var point = mapPane._leaflet_pos;      
  
        // reposition the layer
        this._el.style[HeatmapOverlay.CSS_TRANSFORM] = 'translate(' +
          -Math.round(point.x) + 'px,' +
          -Math.round(point.y) + 'px)';
  
        this._update();
      },
      _update: function() {
        var bounds, zoom, scale;
        var generatedData = { max: this._max, min: this._min, data: [] };
  
        bounds = this._map.getBounds();
        zoom = this._map.getZoom();
        scale = Math.pow(2, zoom);
  
        if (this._data.length == 0) {
          if (this._heatmap) {
            this._heatmap.setData(generatedData);
          }
          return;
        }
  
  
        var latLngPoints = [];
        var radiusMultiplier = this.cfg.scaleRadius ? scale : 1;
        var localMax = 0;
        var localMin = 0;
        var valueField = this.cfg.valueField;
        var len = this._data.length;
      
        while (len--) {
          var entry = this._data[len];
          var value = entry[valueField];
          var latlng = entry.latlng;
  
  
          // we don't wanna render points that are not even on the map ;-)
          if (!bounds.contains(latlng)) {
            continue;
          }
          // local max is the maximum within current bounds
          localMax = Math.max(value, localMax);
          localMin = Math.min(value, localMin);
  
          var point = this._map.latLngToContainerPoint(latlng);
          var latlngPoint = { x: Math.round(point.x), y: Math.round(point.y) };
          latlngPoint[valueField] = value;
  
          var radius;
  
          if (entry.radius) {
            radius = entry.radius * radiusMultiplier;
          } else {
            radius = (this.cfg.radius || 2) * radiusMultiplier;
          }
          latlngPoint.radius = radius;
          latLngPoints.push(latlngPoint);
        }
        if (this.cfg.useLocalExtrema) {
          generatedData.max = localMax;
          generatedData.min = localMin;
        }
  
        generatedData.data = latLngPoints;
  
        this._heatmap.setData(generatedData);
      },
      setData: function(data) {
        this._max = data.max || this._max;
        this._min = data.min || this._min;
        var latField = this.cfg.latField || 'lat';
        var lngField = this.cfg.lngField || 'lng';
        var valueField = this.cfg.valueField || 'value';
      
        // transform data to latlngs
        var data = data.data;
        var len = data.length;
        var d = [];
      
        while (len--) {
          var entry = data[len];
          var latlng = new L.LatLng(entry[latField], entry[lngField]);
          var dataObj = { latlng: latlng };
          dataObj[valueField] = entry[valueField];
          if (entry.radius) {
            dataObj.radius = entry.radius;
          }
          d.push(dataObj);
        }
        this._data = d;
      
        this._draw();
      },
      // experimential... not ready.
      addData: function(pointOrArray) {
        if (pointOrArray.length > 0) {
          var len = pointOrArray.length;
          while(len--) {
            this.addData(pointOrArray[len]);
          }
        } else {
          var latField = this.cfg.latField || 'lat';
          var lngField = this.cfg.lngField || 'lng';
          var valueField = this.cfg.valueField || 'value';
          var entry = pointOrArray;
          var latlng = new L.LatLng(entry[latField], entry[lngField]);
          var dataObj = { latlng: latlng };
          
          dataObj[valueField] = entry[valueField];
          this._max = Math.max(this._max, dataObj[valueField]);
          this._min = Math.min(this._min, dataObj[valueField]);
  
          if (entry.radius) {
            dataObj.radius = entry.radius;
          }
          this._data.push(dataObj);
          this._draw();
        }
      },
      _reset: function () {
        this._origin = this._map.layerPointToLatLng(new L.Point(0, 0));
        
        var size = this._map.getSize();
        if (this._width !== size.x || this._height !== size.y) {
          this._width  = size.x;
          this._height = size.y;
  
          this._el.style.width = this._width + 'px';
          this._el.style.height = this._height + 'px';
  
          this._heatmap._renderer.setDimensions(this._width, this._height);
        }
        this._draw();
      } 
    });
  
    HeatmapOverlay.CSS_TRANSFORM = (function() {
      var div = document.createElement('div');
      var props = [
        'transform',
        'WebkitTransform',
        'MozTransform',
        'OTransform',
        'msTransform'
      ];
  
      for (var i = 0; i < props.length; i++) {
        var prop = props[i];
        if (div.style[prop] !== undefined) {
          return prop;
        }
      }
      return props[0];
    })();
  
    return HeatmapOverlay;
  });