/* ============================================================================
 * deckChrome.js — SAS-AM deck-stage v2 chrome (vanilla, no framework)
 * Pairs with engine/deckStage.js and engine/deckChrome.css.
 *
 * Wires, on DOMContentLoaded:
 *   - Theme toggle (light <-> dark), persisted to localStorage
 *   - Count-up animation for [data-count] on the active slide
 *   - Icon navigation rail, built generically from each slide's data-label
 *     (+ optional data-nav-icon), tracking the active slide
 *   - Presenter camera cameo: draggable / resizable / zoom / blur / mirror /
 *     camera-swap / pin, position persisted. Includes a secure-context
 *     preflight, a diagnostic placeholder, and named getUserMedia error
 *     messages (ported from the Mainstream 2026 spineDeck, which learned the
 *     hard way that Safari treats http://localhost as INSECURE — the cameo
 *     needs https, e.g. an mkcert dev cert, on any non-Chrome browser).
 *
 * Opt-outs / config (attributes on <html> or <body>):
 *   data-default-theme="light|dark"  (default: dark)
 *   data-motion="off"                 disable entrance animations + count-ups
 *
 * All state is DOM + localStorage; every hook here uses only the public
 * deck-stage API (the `slidechange` event, deck.goTo, deck.index, deck.length).
 * ==========================================================================*/
(function () {
  'use strict';

  var LS_THEME = 'sasdeck.theme';
  var LS_CAMEO = 'sasdeck.cameo';

  function ready(fn) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  ready(function () {
    var root = document.documentElement;

    // ---- Theme -------------------------------------------------------------
    var stored = null;
    try { stored = localStorage.getItem(LS_THEME); } catch (e) {}
    var def = root.getAttribute('data-default-theme') || 'dark';
    root.setAttribute('data-theme', stored || def);

    var motionOff = (root.getAttribute('data-motion') || document.body.getAttribute('data-motion')) === 'off';
    if (motionOff) root.setAttribute('data-no-motion', '');

    var themeBtn = document.querySelector('[data-theme-toggle]');
    if (themeBtn) themeBtn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem(LS_THEME, next); } catch (e) {}
    });

    var deck = document.querySelector('deck-stage');

    // ---- Count-up ----------------------------------------------------------
    function animateCounts(slide) {
      if (!slide || !slide.querySelectorAll) return;
      var reduce = motionOff || (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
      slide.querySelectorAll('[data-count]').forEach(function (el) {
        var to = parseFloat(el.getAttribute('data-count'));
        var dec = parseInt(el.getAttribute('data-decimals') || '0', 10);
        var pre = el.getAttribute('data-prefix') || '';
        var suf = el.getAttribute('data-suffix') || '';
        if (isNaN(to)) return;
        if (reduce || typeof performance === 'undefined' || typeof requestAnimationFrame === 'undefined') {
          el.textContent = pre + to.toFixed(dec) + suf; return;
        }
        var start = performance.now(), dur = 1150;
        var tick = function (now) {
          var p = Math.min((now - start) / dur, 1);
          var eased = 0.5 - Math.cos(Math.PI * p) / 2;
          el.textContent = pre + (to * eased).toFixed(dec) + suf;
          if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      });
    }

    // ---- Icon navigation rail ---------------------------------------------
    var ICONS = {
      home:'<path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/>',
      list:'<path d="M8 6h13M8 12h13M8 18h13"/><path d="M3 6h.01M3 12h.01M3 18h.01"/>',
      tag:'<path d="M20.6 13.4l-7.2 7.2a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><path d="M7 7h.01"/>',
      bookmark:'<path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>',
      help:'<path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>',
      target:'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.6"/>',
      grid:'<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>',
      bar:'<path d="M4 20V10"/><path d="M10 20V4"/><path d="M16 20v-7"/><path d="M2 20h20"/>',
      trend:'<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
      pie:'<path d="M21.2 15.9A10 10 0 1 1 8.1 2.8"/><path d="M22 12A10 10 0 0 0 12 2v10z"/>',
      split:'<path d="M4 6h6M14 6h6M4 12h6M14 12h6M4 18h6M14 18h6"/>',
      image:'<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 15l5-5 4 4 3-3 6 6"/><circle cx="8.5" cy="8.5" r="1.4"/>',
      quote:'<path d="M7 7H4a1 1 0 0 0-1 1v4a1 1 0 0 0 1 1h3v3H4"/><path d="M20 7h-3a1 1 0 0 0-1 1v4a1 1 0 0 0 1 1h3v3h-3"/>',
      columns:'<rect x="4" y="3" width="7" height="18"/><rect x="13" y="3" width="7" height="18"/>',
      route:'<circle cx="6" cy="18" r="2"/><circle cx="18" cy="6" r="2"/><path d="M8 18h6a3 3 0 0 0 0-6H10a3 3 0 0 1 0-6h6"/>',
      crosshair:'<circle cx="12" cy="12" r="3"/><path d="M12 2v5M12 17v5M2 12h5M17 12h5"/>',
      book:'<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5V4.5A2.5 2.5 0 0 1 6.5 2z"/>',
      flag:'<path d="M4 22V4"/><path d="M4 4h13l-2 4 2 4H4"/>'
    };
    var navDots = null;

    function slideEls() {
      if (!deck) return [];
      return Array.prototype.slice.call(deck.querySelectorAll(':scope > section'))
        .filter(function (s) { return !s.hasAttribute('data-deck-skip'); });
    }

    function initRail(tries) {
      var rail = document.querySelector('[data-nav-rail]');
      if (!rail || rail.childElementCount) return;
      var slides = slideEls();
      if (!slides.length) { if ((tries || 0) < 30) return setTimeout(function () { initRail((tries || 0) + 1); }, 150); return; }
      slides.forEach(function (s, i) {
        var label = s.getAttribute('data-label') || ('Slide ' + (i + 1));
        var icon = ICONS[s.getAttribute('data-nav-icon')] || ICONS.bookmark;
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'nav-dot';
        b.setAttribute('aria-label', label);
        b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + icon + '</svg>' +
          '<span class="pill">' + String(i + 1).padStart(2, '0') + ' · ' + label + '</span>';
        b.addEventListener('click', function () { if (deck && deck.goTo) deck.goTo(i); });
        rail.appendChild(b);
      });
      navDots = Array.prototype.slice.call(rail.children);
      updateRail(deck && typeof deck.index === 'number' ? deck.index : 0);
    }

    function updateRail(idx) {
      if (!navDots) return;
      navDots.forEach(function (b, i) {
        b.classList.toggle('current', i === idx);
        b.classList.toggle('passed', i < idx);
      });
    }

    // ---- Slide change wiring ----------------------------------------------
    document.addEventListener('slidechange', function (e) {
      if (!e.detail) return;
      if (e.detail.slide) animateCounts(e.detail.slide);
      if (typeof e.detail.index === 'number') updateRail(e.detail.index);
    });

    initRail();
    // The first active slide may exist before our listener attached.
    setTimeout(function () {
      var active = document.querySelector('[data-deck-active]');
      if (active) animateCounts(active);
    }, 350);

    // ---- Presenter camera cameo -------------------------------------------
    new Cameo();
  });

  // ==========================================================================
  // Cameo — draggable / resizable webcam PiP with secure-context handling.
  // ==========================================================================
  function Cameo() {
    var self = this;
    this.stream = null; this.el = null; this.video = null; this.cams = []; this.deviceId = null;
    this.cam = this.load();

    var btn = document.querySelector('[data-cameo-toggle]');
    if (btn) btn.addEventListener('click', function () {
      if (self.cam.on) self.stop(); else self.start();
    });
    this.syncBtn();
  }

  Cameo.prototype.defaults = function () {
    return { x: null, y: null, w: 240, h: 240, shape: 0, zoom: 1, blur: 0, mirror: true, pinned: false, on: false };
  };
  Cameo.prototype.load = function () {
    var s = this.defaults();
    try { var raw = localStorage.getItem('sasdeck.cameo'); if (raw) s = Object.assign(s, JSON.parse(raw)); } catch (e) {}
    s.on = false; // never auto-start; getUserMedia requires a user gesture
    return s;
  };
  Cameo.prototype.save = function () {
    try { var c = Object.assign({}, this.cam); delete c.on; localStorage.setItem('sasdeck.cameo', JSON.stringify(c)); } catch (e) {}
  };

  // -- Secure-context preflight (the spineDeck lesson) -----------------------
  Cameo.prototype.diagnose = function () {
    // Returns a human message if the camera cannot possibly start, else null.
    if (!window.isSecureContext) {
      return 'Insecure context<br><span class="hint">' + location.protocol + '//' + location.host +
        '</span><br><span class="hint">Serve over https:// (mkcert) or use Chrome on localhost</span>';
    }
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      return 'Camera API missing<br><span class="hint">secureContext: <b>' + window.isSecureContext + '</b></span>' +
        '<br><span class="hint">Quit &amp; reopen Safari, or use Chrome</span>';
    }
    return null;
  };
  Cameo.prototype.errorFor = function (err) {
    var map = {
      NotAllowedError: 'Camera permission denied',
      NotFoundError: 'No camera found',
      NotReadableError: 'Camera in use by another app',
      OverconstrainedError: 'No matching camera',
      SecurityError: 'Blocked — use https:// or localhost'
    };
    return (err && map[err.name]) || 'Camera unavailable';
  };

  Cameo.prototype.start = function () {
    var self = this;
    this.build();                       // ensure the cameo frame exists (so we can show diagnostics)
    this.el.cameo.style.display = 'block';
    var pre = this.diagnose();
    if (pre) { this.showDiag(pre); this.cam.on = true; this.syncBtn(); return; }
    this.el.cameo.classList.remove('diag');
    var go = function (deviceId) {
      var constraints = { audio: false, video: deviceId ? { deviceId: { exact: deviceId } } : { facingMode: 'user', width: { ideal: 1280 } } };
      navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
        self.stream = stream;
        self.video.srcObject = stream;
        self.video.play().catch(function () {});
        self.cam.on = true;
        self.syncBtn();
        navigator.mediaDevices.enumerateDevices().then(function (ds) {
          self.cams = ds.filter(function (d) { return d.kind === 'videoinput'; });
        }).catch(function () {});
      }).catch(function (err) {
        self.showDiag(self.errorFor(err));
        self.cam.on = true; self.syncBtn();
      });
    };
    go(this.deviceId);
  };
  Cameo.prototype.showDiag = function (html) {
    if (!this.el) return;
    this.el.diag.innerHTML = html;
    this.el.cameo.classList.add('diag');
  };
  Cameo.prototype.stop = function () {
    if (this.stream) { this.stream.getTracks().forEach(function (t) { t.stop(); }); this.stream = null; }
    if (this.el && this.el.cameo) { this.el.cameo.style.display = 'none'; this.el.cameo.classList.remove('diag'); }
    this.cam.on = false;
    this.syncBtn();
  };
  Cameo.prototype.syncBtn = function () {
    var btn = document.querySelector('[data-cameo-toggle]');
    if (!btn) return;
    var on = !!(this.cam && this.cam.on);
    btn.setAttribute('data-on', on ? '1' : '0');
    btn.innerHTML = on ? '◉  Camera on' : '◉  Camera';
  };

  Cameo.prototype.icon = function (name) {
    var P = {
      shape:'<rect x="3" y="3" width="18" height="18" rx="5"/>',
      mirror:'<path d="M12 3v18"/><path d="M8 7L4 12l4 5"/><path d="M16 7l4 5-4 5"/>',
      swap:'<path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/><path d="M3 21v-5h5"/>',
      pin:'<path d="M12 17v5"/><path d="M9 2h6l-1 7 3 3v2H7v-2l3-3-1-7z"/>',
      close:'<path d="M18 6L6 18M6 6l12 12"/>'
    };
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + (P[name] || '') + '</svg>';
  };

  Cameo.prototype.build = function () {
    if (this.el && this.el.cameo) return;
    var self = this;
    var cameo = document.createElement('div');
    cameo.setAttribute('data-cameo', '');
    cameo.innerHTML =
      '<div class="cam-frame">' +
        '<video playsinline autoplay muted></video>' +
        '<div class="cam-diag"></div>' +
        '<div class="cam-resize" data-cam-resize></div>' +
        '<div class="cam-bar">' +
          '<button data-cam="shape" title="Crop shape">' + this.icon('shape') + '</button>' +
          '<button data-cam="mirror" title="Mirror">' + this.icon('mirror') + '</button>' +
          '<button data-cam="swap" title="Switch camera">' + this.icon('swap') + '</button>' +
          '<div class="div"></div>' +
          '<label class="sld"><span>Zoom</span><input type="range" data-cam="zoom" min="1" max="3" step="0.02"></label>' +
          '<label class="sld"><span>Blur</span><input type="range" data-cam="blur" min="0" max="20" step="1"></label>' +
          '<div class="div"></div>' +
          '<button data-cam="pin" title="Keep controls open">' + this.icon('pin') + '</button>' +
          '<button data-cam="close" title="Turn off camera">' + this.icon('close') + '</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(cameo);
    this.el = { cameo: cameo, frame: cameo.querySelector('.cam-frame'), diag: cameo.querySelector('.cam-diag') };
    this.video = cameo.querySelector('video');
    if (this.cam.x === null || this.cam.y === null) {
      this.cam.x = Math.max(20, window.innerWidth - this.cam.w - 70);
      this.cam.y = Math.max(20, window.innerHeight - this.cam.h - 90);
    }
    this.wire();
    this.apply();
  };

  Cameo.prototype.wire = function () {
    var self = this, cameo = this.el.cameo, frame = this.el.frame;
    frame.addEventListener('pointerdown', function (e) {
      if (e.target.closest('.cam-bar') || e.target.closest('[data-cam-resize]')) return;
      e.preventDefault();
      cameo.classList.add('dragging');
      var sx = e.clientX, sy = e.clientY, ox = self.cam.x, oy = self.cam.y;
      var mv = function (ev) {
        self.cam.x = Math.min(Math.max(0, ox + ev.clientX - sx), window.innerWidth - self.cam.w);
        self.cam.y = Math.min(Math.max(0, oy + ev.clientY - sy), window.innerHeight - self.cam.h);
        self.apply();
      };
      var up = function () { cameo.classList.remove('dragging'); window.removeEventListener('pointermove', mv); window.removeEventListener('pointerup', up); self.save(); };
      window.addEventListener('pointermove', mv); window.addEventListener('pointerup', up);
    });
    cameo.querySelector('[data-cam-resize]').addEventListener('pointerdown', function (e) {
      e.preventDefault(); e.stopPropagation();
      var sx = e.clientX, sy = e.clientY, ow = self.cam.w, oh = self.cam.h;
      var mv = function (ev) {
        self.cam.w = Math.min(Math.max(120, ow + ev.clientX - sx), window.innerWidth * 0.7);
        self.cam.h = Math.min(Math.max(120, oh + ev.clientY - sy), window.innerHeight * 0.9);
        self.apply();
      };
      var up = function () { window.removeEventListener('pointermove', mv); window.removeEventListener('pointerup', up); self.save(); };
      window.addEventListener('pointermove', mv); window.addEventListener('pointerup', up);
    });
    cameo.querySelector('.cam-bar').addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      var a = b.getAttribute('data-cam');
      if (a === 'shape') self.cam.shape = (self.cam.shape + 1) % 4;
      else if (a === 'mirror') self.cam.mirror = !self.cam.mirror;
      else if (a === 'swap') return self.swap();
      else if (a === 'pin') { self.cam.pinned = !self.cam.pinned; cameo.classList.toggle('pinned', self.cam.pinned); }
      else if (a === 'close') return self.stop();
      self.apply(); self.save();
    });
    var zoom = cameo.querySelector('[data-cam="zoom"]');
    var blur = cameo.querySelector('[data-cam="blur"]');
    zoom.addEventListener('input', function () { self.cam.zoom = parseFloat(zoom.value); self.apply(); });
    zoom.addEventListener('change', function () { self.save(); });
    blur.addEventListener('input', function () { self.cam.blur = parseFloat(blur.value); self.apply(); });
    blur.addEventListener('change', function () { self.save(); });
    this.el.zoom = zoom; this.el.blur = blur;
  };

  Cameo.prototype.swap = function () {
    if (!this.cams || this.cams.length < 2) return;
    var cur = this.deviceId;
    var i = Math.max(0, this.cams.findIndex(function (d) { return d.deviceId === cur; }));
    this.deviceId = this.cams[(i + 1) % this.cams.length].deviceId;
    if (this.stream) { this.stream.getTracks().forEach(function (t) { t.stop(); }); this.stream = null; }
    var on = this.cam.on; this.cam.on = false;
    if (on) this.start();
  };

  Cameo.prototype.apply = function () {
    if (!this.el) return;
    var c = this.cam, cameo = this.el.cameo;
    cameo.style.left = c.x + 'px'; cameo.style.top = c.y + 'px';
    cameo.style.width = c.w + 'px'; cameo.style.height = c.h + 'px';
    var radii = ['50%', '22px', '999px', '8px'];
    this.el.frame.style.borderRadius = radii[c.shape];
    var sx = c.mirror ? -c.zoom : c.zoom;
    this.video.style.transform = 'scale(' + sx + ',' + c.zoom + ')';
    this.video.style.filter = c.blur ? 'blur(' + c.blur + 'px)' : 'none';
    cameo.classList.toggle('pinned', !!c.pinned);
    if (this.el.zoom) this.el.zoom.value = c.zoom;
    if (this.el.blur) this.el.blur.value = c.blur;
  };
})();
