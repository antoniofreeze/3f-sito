(function () {
  var testata = document.querySelector('[data-testata]');
  if (testata && testata.classList.contains('su-foto')) {
    var aggiorna = function () { testata.classList.toggle('piena', window.scrollY > 40); };
    aggiorna(); window.addEventListener('scroll', aggiorna, { passive: true });
  }

  var bott = document.querySelector('[data-menu]'), menu = document.getElementById('menu');
  if (bott && menu) bott.addEventListener('click', function () {
    var ap = menu.classList.toggle('aperto');
    bott.setAttribute('aria-expanded', ap); bott.firstElementChild.textContent = ap ? 'Chiudi' : 'Menu';
    testata.classList.toggle('aperta', ap);
  });

  // Le foto si accendono e il filo scende quando entrano nello schermo
  var el = document.querySelectorAll('.accende, .filo');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (voci) {
      voci.forEach(function (v) { if (v.isIntersecting) { v.target.classList.add('in'); io.unobserve(v.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    el.forEach(function (x) { io.observe(x); });
  } else el.forEach(function (x) { x.classList.add('in'); });

  // Foto ingrandita
  var box = document.querySelector('[data-box]'), lk = Array.prototype.slice.call(document.querySelectorAll('[data-luce]'));
  if (box && box.showModal && lk.length) {
    var im = box.querySelector('img'), dida = box.querySelector('[data-didascalia]'), i = 0;
    var mostra = function (n) {
      i = (n + lk.length) % lk.length;
      var t = lk[i].querySelector('img');
      im.src = lk[i].getAttribute('href'); im.alt = t.alt; dida.textContent = t.alt;
    };
    lk.forEach(function (a, n) { a.addEventListener('click', function (ev) { ev.preventDefault(); mostra(n); box.showModal(); }); });
    box.querySelector('[data-chiudi]').addEventListener('click', function () { box.close(); });
    box.querySelector('[data-prec]').addEventListener('click', function () { mostra(i - 1); });
    box.querySelector('[data-succ]').addEventListener('click', function () { mostra(i + 1); });
    box.addEventListener('click', function (ev) { if (ev.target === box) box.close(); });
    box.addEventListener('keydown', function (ev) { if (ev.key === 'ArrowLeft') mostra(i - 1); if (ev.key === 'ArrowRight') mostra(i + 1); });
    var x0 = null;
    box.addEventListener('touchstart', function (ev) { x0 = ev.touches[0].clientX; }, { passive: true });
    box.addEventListener('touchend', function (ev) { if (x0 === null) return; var d = ev.changedTouches[0].clientX - x0; if (Math.abs(d) > 50) mostra(i + (d < 0 ? 1 : -1)); x0 = null; });
  }

  // Mappa solo a richiesta
  var bm = document.querySelector('[data-apri-mappa]');
  if (bm) bm.addEventListener('click', function () {
    var m = document.querySelector('[data-mappa]'), f = document.createElement('iframe');
    f.src = m.getAttribute('data-src'); f.title = 'Mappa dello showroom'; f.loading = 'lazy'; f.referrerPolicy = 'no-referrer-when-downgrade';
    m.textContent = ''; m.classList.add('aperta'); m.appendChild(f);
  });

  // Modulo: controlla i campi, invia, e in caso di problemi offre email e telefono
  var mod = document.querySelector('[data-modulo]');
  if (mod) {
    var esito = mod.querySelector('[data-esito]');
    var errore = function (c, msg) {
      var w = c.closest('.campo'); if (!w) return;
      var vec = w.querySelector('.errore-testo'); if (vec) vec.remove();
      w.classList.toggle('errore', !!msg);
      if (msg) { var s = document.createElement('span'); s.className = 'errore-testo'; s.textContent = msg; w.appendChild(s); c.setAttribute('aria-invalid', 'true'); }
      else c.removeAttribute('aria-invalid');
    };
    var controlla = function () {
      var ok = true, primo = null;
      var seg = function (c, m) { errore(c, m); if (m) { ok = false; primo = primo || c; } };
      seg(mod.nome, mod.nome.value.trim() ? '' : 'Scrivi il tuo nome.');
      seg(mod.email, /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(mod.email.value.trim()) ? '' : 'Controlla l’indirizzo email.');
      seg(mod.messaggio, mod.messaggio.value.trim() ? '' : 'Scrivi di cosa hai bisogno.');
      if (!mod.privacy.checked) { ok = false; primo = primo || mod.privacy; esito.textContent = 'Per inviare devi confermare di aver letto la privacy policy.'; } else esito.textContent = '';
      if (primo) primo.focus();
      return ok;
    };
    mod.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (!controlla()) return;
      var b = mod.querySelector('button[type=submit]'), t = b.textContent;
      b.disabled = true; b.textContent = 'Invio in corso…'; esito.textContent = '';
      fetch(mod.action, { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(mod) })
        .then(function (r) { return r.json().then(function (j) { if (!r.ok || String(j.success) !== 'true') throw 0; }); })
        .then(function () { mod.reset(); esito.textContent = 'Grazie, abbiamo ricevuto la tua richiesta. Ti ricontatteremo al più presto.'; esito.focus(); })
        .catch(function () { esito.innerHTML = 'Non siamo riusciti a inviare il messaggio. Scrivici a <a href="mailto:3filluminazione@libero.it">3filluminazione@libero.it</a> o chiama lo <a href="tel:+390956730772">095 673 0772</a>.'; esito.focus(); })
        .then(function () { b.disabled = false; b.textContent = t; });
    });
  }
})();
