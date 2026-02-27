/**
 * admin_fx.js — WeArtificial Launchpad
 * Sistema de partículas metabola con efecto Liquid Glass.
 *
 * Técnica: CSS filter blur + contrast en el canvas.
 * Cada partícula es un gradiente radial blanco → transparente sobre fondo negro.
 * El blur CSS mezcla los gradientes y el contrast extremo los convierte en
 * formas fusionadas orgánicas (efecto metabola / chicle / mercurio) sin código extra.
 *
 * Módulo IIFE con 'use strict'. No contamina el espacio global.
 *
 * Estructura:
 *   AdminFX
 *   ├── CONFIG              → constantes ajustables
 *   ├── class Particle      → posición, velocidad, radio, ángulo de divagación
 *   │   └── update(bounds)  → movimiento + divagación + fricción + rebote
 *   ├── createCanvas()      → crea <canvas> fixed con CSS filter metabola
 *   ├── resizeCanvas()      → ajusta dimensiones al viewport
 *   ├── spawnParticles()    → instancia las N partículas
 *   ├── tick()              → loop: fondo negro + gradientes radiales
 *   └── init()              → punto de entrada
 */
(function () {
  'use strict';

  /* =========================================================================
     CONFIG — ajusta estos valores para cambiar el comportamiento visual
     ========================================================================= */
  var CONFIG = {
    /** Número total de partículas (pocas, grandes) */
    PARTICLE_COUNT: 12,

    /** Radio mínimo en píxeles */
    MIN_RADIUS: 65,

    /** Radio máximo en píxeles */
    MAX_RADIUS: 115,

    /** Velocidad inicial mínima (px/frame) */
    MIN_SPEED: 0.60,

    /** Velocidad inicial máxima (px/frame) */
    MAX_SPEED: 1.40,

    /** Límite de velocidad en cualquier momento */
    MAX_SPEED_CAP: 1.80,

    /**
     * Factor de rozamiento aplicado cada frame.
     * 1.0 = sin rozamiento. 0.997 = casi nulo (mantienen velocidad).
     */
    FRICTION: 0.997,

    /** Magnitud del impulso de divagación aleatoria por frame */
    WANDER_STRENGTH: 0.040,

    /** Variación máxima del ángulo de divagación por frame (rad) */
    WANDER_DELTA: 0.080,

    /**
     * El gradiente de cada partícula se extiende hasta r * BLOB_RADIUS_FACTOR.
     * Valores mayores → partículas más grandes y zona de fusión más amplia.
     */
    BLOB_RADIUS_FACTOR: 3.5,

    /** Blur CSS en píxeles — controla el rango de fusión entre partículas */
    FILTER_BLUR: 28,

    /**
     * Contraste CSS — umbral de fusión.
     * Valores más altos → bordes más duros y fusión más abrupta (más "mercurio").
     * Valores más bajos → transición más suave (más "niebla").
     */
    FILTER_CONTRAST: 12,

    /** Brillo CSS — intensidad de la luz de las partículas */
    FILTER_BRIGHTNESS: 1.15,

    /** Gravedad permanente hacia el centro (4× más fuerte que v3, supera al wander) */
    CENTER_GRAVITY: 0.025,

    /** Zona de exclusión en bordes: fracción del ancho/alto donde actúa la repulsión extra */
    EDGE_ZONE: 0.05,

    /** Fuerza adicional de repulsión cuando la partícula entra en EDGE_ZONE */
    EDGE_REPULSE: 0.08,

    /** Número de blobs de niebla */
    FOG_COUNT: 5,

    /** Radio mínimo de cada blob de niebla (px) */
    FOG_MIN_RADIUS: 180,

    /** Radio máximo de cada blob de niebla (px) */
    FOG_MAX_RADIUS: 380,

    /** Velocidad base de la niebla (10× más lenta que partículas) */
    FOG_SPEED: 0.10,

    /** Variación angular de la niebla por frame (muy suave) */
    FOG_WANDER: 0.015,

    /** Opacidad mínima de cada blob */
    FOG_OPACITY_MIN: 0.05,

    /** Opacidad máxima de cada blob */
    FOG_OPACITY_MAX: 0.11,

    /** Blur CSS del canvas de niebla */
    FOG_BLUR: 100,

    /** Velocidad mínima; si baja de este valor se activa el impulso de rescate */
    MIN_SPEED_ENFORCE: 0.25,

    /** Magnitud del impulso de rescate hacia el centro */
    CENTER_KICK: 0.45,

    /** Frames en fase de atracción (~4s a 60fps) */
    ATTRACT_PHASE_FRAMES: 240,

    /** Distancia máxima a la que se atraen las partículas entre sí (px) */
    ATTRACT_RADIUS: 450,

    /** Magnitud de la fuerza de atracción inter-partícula */
    ATTRACT_FORCE: 0.08,

    /** Repulsión activa cuando dist < (ri+rj) * factor */
    REPEL_RADIUS_FACTOR: 2.4,

    /** Magnitud de la fuerza de repulsión inter-partícula */
    REPEL_FORCE: 0.22,
  };

  /* =========================================================================
     class Particle — partícula con divagación continua
     ========================================================================= */

  /**
   * @param {number} x   - Posición inicial X
   * @param {number} y   - Posición inicial Y
   * @param {number} r   - Radio en píxeles
   * @param {number} vx  - Velocidad inicial en X
   * @param {number} vy  - Velocidad inicial en Y
   */
  function Particle(x, y, r, vx, vy) {
    this.x  = x;
    this.y  = y;
    this.r  = r;
    this.vx = vx;
    this.vy = vy;

    /** Ángulo actual de divagación (evoluciona cada frame) */
    this.wander = Math.random() * Math.PI * 2;
  }

  /**
   * Actualiza posición y velocidad con divagación, fricción y rebote.
   *
   * @param {{ w: number, h: number }} bounds - Dimensiones del canvas
   */
  Particle.prototype.update = function (bounds, speedCap) {
    // Evolucionar ángulo de divagación aleatoriamente
    this.wander += (Math.random() - 0.5) * CONFIG.WANDER_DELTA;

    // Aplicar impulso de divagación en la dirección actual
    this.vx += Math.cos(this.wander) * CONFIG.WANDER_STRENGTH;
    this.vy += Math.sin(this.wander) * CONFIG.WANDER_STRENGTH;

    // Fricción casi nula
    this.vx *= CONFIG.FRICTION;
    this.vy *= CONFIG.FRICTION;

    // Gravedad permanente hacia el centro — más fuerte durante fase attract
    var toCx = (bounds.w / 2 - this.x) / bounds.w;  // -0.5..0.5
    var toCy = (bounds.h / 2 - this.y) / bounds.h;
    var gravMult = appTime < CONFIG.ATTRACT_PHASE_FRAMES ? 2.5 : 1.0;
    this.vx += toCx * CONFIG.CENTER_GRAVITY * gravMult;
    this.vy += toCy * CONFIG.CENTER_GRAVITY * gravMult;

    // Zona de exclusión en bordes — repulsión adicional cuando la partícula
    // entra en el 18% exterior de cada lado
    var edgeX = bounds.w * CONFIG.EDGE_ZONE;
    var edgeY = bounds.h * CONFIG.EDGE_ZONE;
    if (this.x < edgeX)                 this.vx += CONFIG.EDGE_REPULSE;
    else if (this.x > bounds.w - edgeX) this.vx -= CONFIG.EDGE_REPULSE;
    if (this.y < edgeY)                 this.vy += CONFIG.EDGE_REPULSE;
    else if (this.y > bounds.h - edgeY) this.vy -= CONFIG.EDGE_REPULSE;

    // Clamp de velocidad máxima (usa speedCap dinámico si se pasa)
    var cap = speedCap !== undefined ? speedCap : CONFIG.MAX_SPEED_CAP;
    var speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
    if (speed > cap) {
      var scale = cap / speed;
      this.vx *= scale;
      this.vy *= scale;
    }

    // Impulso de rescate si la partícula casi se ha detenido
    if (speed < CONFIG.MIN_SPEED_ENFORCE) {
      var cx  = bounds.w / 2;
      var cy  = bounds.h / 2;
      var dCx = cx - this.x;
      var dCy = cy - this.y;
      var dLen = Math.sqrt(dCx * dCx + dCy * dCy) || 1;
      this.vx += (dCx / dLen) * CONFIG.CENTER_KICK + (Math.random() - 0.5) * 0.30;
      this.vy += (dCy / dLen) * CONFIG.CENTER_KICK + (Math.random() - 0.5) * 0.30;
    }

    // Integrar posición
    this.x += this.vx;
    this.y += this.vy;

    // Rebote en bordes izquierdo/derecho
    if (this.x - this.r < 0) {
      this.x  = this.r;
      this.vx = Math.abs(this.vx);
    } else if (this.x + this.r > bounds.w) {
      this.x  = bounds.w - this.r;
      this.vx = -Math.abs(this.vx);
    }

    // Rebote en bordes superior/inferior
    if (this.y - this.r < 0) {
      this.y  = this.r;
      this.vy = Math.abs(this.vy);
    } else if (this.y + this.r > bounds.h) {
      this.y  = bounds.h - this.r;
      this.vy = -Math.abs(this.vy);
    }
  };

  /* =========================================================================
     class FogBlob — blob de niebla flotante semitransparente
     ========================================================================= */

  function FogBlob(x, y, r, opacity) {
    this.x       = x;
    this.y       = y;
    this.r       = r;
    this.opacity = opacity;
    this.wander  = Math.random() * Math.PI * 2;
    var spd      = CONFIG.FOG_SPEED * (0.5 + Math.random() * 0.5);
    var ang      = Math.random() * Math.PI * 2;
    this.vx      = Math.cos(ang) * spd;
    this.vy      = Math.sin(ang) * spd;
  }

  FogBlob.prototype.update = function (bounds) {
    this.wander += (Math.random() - 0.5) * CONFIG.FOG_WANDER;
    this.vx += Math.cos(this.wander) * 0.004;
    this.vy += Math.sin(this.wander) * 0.004;
    // Fricción suave
    this.vx *= 0.998;
    this.vy *= 0.998;
    // Clamp velocidad
    var spd = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
    var maxSpd = CONFIG.FOG_SPEED * 1.5;
    if (spd > maxSpd) { this.vx *= maxSpd / spd; this.vy *= maxSpd / spd; }
    // Gravedad suave hacia el centro
    this.vx += (bounds.w / 2 - this.x) / bounds.w * 0.005;
    this.vy += (bounds.h / 2 - this.y) / bounds.h * 0.005;
    // Integrar
    this.x += this.vx;
    this.y += this.vy;
    // Rebote en bordes
    if (this.x - this.r < 0)             { this.x = this.r;          this.vx =  Math.abs(this.vx); }
    else if (this.x + this.r > bounds.w) { this.x = bounds.w - this.r; this.vx = -Math.abs(this.vx); }
    if (this.y - this.r < 0)             { this.y = this.r;          this.vy =  Math.abs(this.vy); }
    else if (this.y + this.r > bounds.h) { this.y = bounds.h - this.r; this.vy = -Math.abs(this.vy); }
  };

  /* =========================================================================
     Funciones privadas del módulo
     ========================================================================= */

  /** @type {HTMLCanvasElement} */
  var canvas;

  /** @type {CanvasRenderingContext2D} */
  var ctx;

  /** @type {Particle[]} */
  var particles = [];

  /** @type {HTMLCanvasElement} */
  var fogCanvas;

  /** @type {CanvasRenderingContext2D} */
  var fogCtx;

  /** @type {FogBlob[]} */
  var fogBlobs = [];

  /** Dimensiones actuales del canvas */
  var bounds = { w: 0, h: 0 };

  /** Contador de frames para la fase de atracción/repulsión */
  var appTime = 0;

  /**
   * Crea el elemento <canvas> fixed que cubre toda la ventana,
   * situado detrás del contenido (z-index: 0), con el CSS filter
   * que implementa el efecto metabola.
   */
  function createCanvas() {
    canvas = document.createElement('canvas');
    canvas.id = 'adminFxCanvas';
    canvas.style.cssText = [
      'position: fixed',
      'top: 0',
      'left: 0',
      'width: 100%',
      'height: 100%',
      'z-index: 0',
      'pointer-events: none',
      'display: block',
    ].join('; ');

    // CSS filter metabola: blur mezcla los gradientes,
    // contrast convierte la zona solapada en blanco puro (efecto chicle/mercurio),
    // brightness amplifica la luz resultante.
    canvas.style.filter =
      'blur(' + CONFIG.FILTER_BLUR + 'px) ' +
      'contrast(' + CONFIG.FILTER_CONTRAST + ') ' +
      'brightness(' + CONFIG.FILTER_BRIGHTNESS + ')';

    document.body.insertBefore(canvas, document.body.firstChild);
    ctx = canvas.getContext('2d');
  }

  /**
   * Crea el canvas de niebla situado encima del canvas de partículas.
   * Solo blur suave — sin contrast — para que los blobs sean niebla, no metabola.
   */
  function createFogCanvas() {
    fogCanvas = document.createElement('canvas');
    fogCanvas.id = 'adminFogCanvas';
    fogCanvas.style.cssText = [
      'position: fixed',
      'top: 0',
      'left: 0',
      'width: 100%',
      'height: 100%',
      'z-index: 0',
      'pointer-events: none',
      'display: block',
    ].join('; ');
    fogCanvas.style.filter = 'blur(' + CONFIG.FOG_BLUR + 'px) brightness(0.9)';
    // Insertar DESPUÉS del canvas de partículas → queda encima visualmente
    document.body.insertBefore(fogCanvas, canvas.nextSibling);
    fogCtx = fogCanvas.getContext('2d');
  }

  /**
   * Ajusta las dimensiones del canvas al viewport actual.
   */
  function resizeCanvas() {
    bounds.w = canvas.width  = window.innerWidth;
    bounds.h = canvas.height = window.innerHeight;
    if (fogCanvas) {
      fogCanvas.width  = bounds.w;
      fogCanvas.height = bounds.h;
    }
  }

  /**
   * Crea todas las partículas con posición, radio y velocidad aleatorios.
   */
  function spawnParticles() {
    particles = [];
    for (var i = 0; i < CONFIG.PARTICLE_COUNT; i++) {
      var r   = CONFIG.MIN_RADIUS + Math.random() * (CONFIG.MAX_RADIUS - CONFIG.MIN_RADIUS);
      var x   = r + Math.random() * (bounds.w - r * 2);
      var y   = r + Math.random() * (bounds.h - r * 2);
      var spd = CONFIG.MIN_SPEED + Math.random() * (CONFIG.MAX_SPEED - CONFIG.MIN_SPEED);
      var ang = Math.random() * Math.PI * 2;
      var vx  = Math.cos(ang) * spd;
      var vy  = Math.sin(ang) * spd;
      particles.push(new Particle(x, y, r, vx, vy));
    }
  }

  /**
   * Crea los blobs de niebla con posición, radio y opacidad aleatorios.
   */
  function spawnFogBlobs() {
    fogBlobs = [];
    for (var i = 0; i < CONFIG.FOG_COUNT; i++) {
      var r  = CONFIG.FOG_MIN_RADIUS + Math.random() * (CONFIG.FOG_MAX_RADIUS - CONFIG.FOG_MIN_RADIUS);
      var x  = r + Math.random() * (bounds.w - r * 2);
      var y  = r + Math.random() * (bounds.h - r * 2);
      var op = CONFIG.FOG_OPACITY_MIN + Math.random() * (CONFIG.FOG_OPACITY_MAX - CONFIG.FOG_OPACITY_MIN);
      fogBlobs.push(new FogBlob(x, y, r, op));
    }
  }

  /**
   * Loop de animación de la niebla (independiente del tick principal).
   * Pinta gradientes radiales blancos semitransparentes sobre fogCanvas.
   * El blur CSS del canvas hace que parezcan manchas de vapor suave.
   */
  function tickFog() {
    fogCtx.clearRect(0, 0, bounds.w, bounds.h);
    for (var i = 0; i < fogBlobs.length; i++) {
      var f = fogBlobs[i];
      f.update(bounds);
      var grad = fogCtx.createRadialGradient(f.x, f.y, 0, f.x, f.y, f.r);
      grad.addColorStop(0.00, 'rgba(255,255,255,' + f.opacity + ')');
      grad.addColorStop(0.45, 'rgba(255,255,255,' + (f.opacity * 0.40).toFixed(3) + ')');
      grad.addColorStop(1.00, 'rgba(255,255,255,0)');
      fogCtx.beginPath();
      fogCtx.arc(f.x, f.y, f.r, 0, Math.PI * 2);
      fogCtx.fillStyle = grad;
      fogCtx.fill();
    }
    requestAnimationFrame(tickFog);
  }

  /**
   * Aplica fuerzas inter-partícula.
   * Fase attract (appTime < ATTRACT_PHASE_FRAMES): atracción entre pares.
   * Fase repel   (appTime >= ATTRACT_PHASE_FRAMES): repulsión cuando están cerca.
   * O(n²) — solo 12 partículas → 66 pares máx, sin impacto en rendimiento.
   */
  function applyParticleForces() {
    var isAttract = appTime < CONFIG.ATTRACT_PHASE_FRAMES;
    for (var i = 0; i < particles.length; i++) {
      for (var j = i + 1; j < particles.length; j++) {
        var a  = particles[i];
        var b  = particles[j];
        var dx = b.x - a.x;
        var dy = b.y - a.y;
        var dist = Math.sqrt(dx * dx + dy * dy) || 1;
        var nx = dx / dist;
        var ny = dy / dist;

        if (isAttract) {
          // Atracción: solo dentro de ATTRACT_RADIUS
          if (dist < CONFIG.ATTRACT_RADIUS) {
            var f = CONFIG.ATTRACT_FORCE * (1 - dist / CONFIG.ATTRACT_RADIUS);
            a.vx += nx * f;
            a.vy += ny * f;
            b.vx -= nx * f;
            b.vy -= ny * f;
          }
        } else {
          // Repulsión: cuando están demasiado cerca
          var repelDist = (a.r + b.r) * CONFIG.REPEL_RADIUS_FACTOR;
          if (dist < repelDist) {
            var rf = CONFIG.REPEL_FORCE * (1 - dist / repelDist);
            a.vx -= nx * rf;
            a.vy -= ny * rf;
            b.vx += nx * rf;
            b.vy += ny * rf;
          }
        }
      }
    }
  }

  /**
   * Loop principal de animación.
   *
   * Cada frame:
   * 1. Fondo negro sólido (imprescindible para que el CSS contrast funcione)
   * 2. Aplicar fuerzas inter-partícula (atracción→repulsión según appTime)
   * 3. Actualizar posición de cada partícula
   * 4. Dibujar gradiente radial blanco→transparente por partícula
   *
   * El CSS filter aplicado al canvas hace el resto: blur solapa los gradientes
   * y contrast los convierte en manchas orgánicas fusionadas.
   */
  function tick() {
    appTime++;

    // Durante fase attract la velocidad máxima es mayor para permitir convergencia rápida
    var dynamicSpeedCap = appTime < CONFIG.ATTRACT_PHASE_FRAMES
      ? CONFIG.MAX_SPEED_CAP * 2.2
      : CONFIG.MAX_SPEED_CAP;

    applyParticleForces();

    // Fondo negro sólido en cada frame
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, bounds.w, bounds.h);

    for (var i = 0; i < particles.length; i++) {
      var p = particles[i];
      p.update(bounds, dynamicSpeedCap);

      // Radio del blob = r * factor (zona de influencia del gradiente)
      var blobR = p.r * CONFIG.BLOB_RADIUS_FACTOR;

      // Gradiente radial puro: blanco opaco en el centro → transparente en el borde
      // Sin borde duro en ningún punto — todo es transición suave
      var grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, blobR);
      grad.addColorStop(0.00, 'rgba(255,255,255,1.00)');
      grad.addColorStop(0.06, 'rgba(255,255,255,0.88)');  // core pequeño (~14px para r=65)
      grad.addColorStop(0.22, 'rgba(255,255,255,0.42)');  // caída rápida
      grad.addColorStop(0.55, 'rgba(255,255,255,0.10)');  // halo suave y amplio
      grad.addColorStop(1.00, 'rgba(255,255,255,0.00)');  // borde completamente transparente

      ctx.beginPath();
      ctx.arc(p.x, p.y, blobR, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();
    }

    requestAnimationFrame(tick);
  }

  /**
   * Punto de entrada del módulo.
   */
  function init() {
    createCanvas();
    createFogCanvas();
    resizeCanvas();
    spawnParticles();
    spawnFogBlobs();

    // Ajustar canvas cuando cambia el tamaño de la ventana
    var resizeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        resizeCanvas();
        // Reposicionar partículas que queden fuera del nuevo bounds
        for (var i = 0; i < particles.length; i++) {
          var p = particles[i];
          if (p.x + p.r > bounds.w) p.x = bounds.w - p.r;
          if (p.y + p.r > bounds.h) p.y = bounds.h - p.r;
        }
      }, 150);
    });

    requestAnimationFrame(tick);
    requestAnimationFrame(tickFog);
  }

  /* =========================================================================
     Arrancar cuando el DOM esté listo
     ========================================================================= */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
