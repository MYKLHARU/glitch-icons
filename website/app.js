'use strict';
(() => {
  const icons = window.GLITCH_CATALOG || [];
  const config = window.GLITCH_CONFIG || {};
  const repository = /^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(config.repository || '') ? config.repository : 'mickyharu-dot/glitch-icons';
  const repoURL = `https://github.com/${repository}`;
  const assetName = (value, fallback) => /^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(value || '') ? value : fallback;
  const apkAsset = assetName(config.apkAsset, 'Glitch-Reflections-TV-2.0.3.apk');
  const packAsset = assetName(config.packAsset, 'Icons-glitch-2.0.3.zip');
  document.querySelectorAll('.repository-link').forEach(link => { link.href = repoURL; });
  document.querySelectorAll('.apk-download').forEach(link => { link.href = `${repoURL}/releases/latest/download/${apkAsset}`; });
  document.querySelectorAll('.pack-download').forEach(link => { link.href = `downloads/${packAsset}`; });
  document.querySelectorAll('.releases-link').forEach(link => { link.href = `${repoURL}/releases`; });

  const featuredNames = ['netflix.png','disneyplus.png','primevideo.png','appletv.png','youtube.png','spotify.png','plex.png','kodi.png','jellyfin.png','vlc.png','twitch.png','hbomax.png','crunchyroll.png','paramount+.png','stremio.png','10play.png','7+.png','9now.png','plutotv.png','tubi.png'];
  const featured = featuredNames.map(name => icons.find(icon => icon.file === name)).filter(Boolean);
  const rank = new Map(featuredNames.map((name,index) => [name,index]));
  const grid = document.getElementById('icon-grid');
  const search = document.getElementById('search');
  const sort = document.getElementById('sort');
  const dialog = document.getElementById('icon-dialog');
  const dialogImage = document.getElementById('dialog-image');
  const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
  let playing = !motionPreference.matches;
  let userSelectedMotion = false;
  let page = 0;
  let filtered = [];
  const pageSize = 20;
  const path = (icon, animate = playing) => `${animate ? 'icons' : 'stills'}/${encodeURIComponent(icon.file)}`;
  const normalize = value => value.toLocaleLowerCase().normalize('NFKD').replace(/[^a-z0-9+]/g, '');

  function openIcon(icon) {
    document.getElementById('dialog-title').textContent = icon.name;
    document.getElementById('dialog-filename').textContent = icon.file;
    dialogImage.dataset.file = icon.file;
    dialogImage.src = path(icon);
    dialogImage.alt = `${icon.name} ${playing ? 'animated' : 'still'} icon preview`;
    const download = document.getElementById('icon-download');
    download.href = path(icon, true);
    download.download = icon.file;
    dialog.showModal();
    document.body.classList.add('dialog-open');
  }

  function makeImage(icon) {
    const image = document.createElement('img');
    image.src = path(icon);
    image.dataset.file = icon.file;
    image.alt = '';
    image.width = 320;
    image.height = 180;
    image.loading = 'lazy';
    image.decoding = 'async';
    return image;
  }

  function renderPreview() {
    const board = document.getElementById('preview-board');
    featured.forEach(icon => {
      const tile = document.createElement('button');
      tile.className = 'preview-tile';
      tile.type = 'button';
      tile.setAttribute('aria-label', `Preview ${icon.name}`);
      tile.title = icon.name;
      tile.append(makeImage(icon));
      tile.addEventListener('click', () => openIcon(icon));
      board.append(tile);
    });
  }

  function updateMotion() {
    document.querySelectorAll('img[data-file]').forEach(image => {
      if (image === dialogImage && !dialog.open) return;
      image.src = path({file:image.dataset.file});
    });
    document.querySelectorAll('.motion-toggle').forEach(button => {
      button.setAttribute('aria-pressed', String(!playing));
      button.querySelector('.motion-label').textContent = playing ? 'Pause animations' : 'Play animations';
      button.querySelector('.motion-symbol').textContent = playing ? 'Ⅱ' : '▷';
    });
    document.getElementById('preview-state').textContent = playing ? 'LIVE PREVIEW' : 'STILL PREVIEW';
  }

  function renderCollection() {
    const query = normalize(search.value);
    filtered = icons.filter(icon => normalize(`${icon.name} ${icon.file}`).includes(query));
    filtered.sort((a,b) => compareGlitchIcons(a, b, sort.value, rank));
    const pages = Math.max(1, Math.ceil(filtered.length / pageSize));
    page = Math.min(Math.max(0,page), pages - 1);
    grid.replaceChildren();
    filtered.slice(page * pageSize, (page + 1) * pageSize).forEach(icon => {
      const card = document.createElement('button');
      card.type = 'button';
      card.className = 'icon-card';
      card.setAttribute('aria-label', `Preview and download ${icon.name}`);
      card.append(makeImage(icon));
      const label = document.createElement('span');
      label.className = 'card-label';
      const name = document.createElement('span');
      name.className = 'name';
      name.textContent = icon.name;
      const arrow = document.createElement('span');
      arrow.className = 'arrow';
      arrow.textContent = '↗';
      arrow.setAttribute('aria-hidden','true');
      label.append(name, arrow);
      card.append(label);
      card.addEventListener('click', () => openIcon(icon));
      grid.append(card);
    });
    const first = filtered.length ? page * pageSize + 1 : 0;
    const last = Math.min((page + 1) * pageSize, filtered.length);
    document.getElementById('results-count').textContent = `${first.toLocaleString()}–${last.toLocaleString()} of ${filtered.length.toLocaleString()} icons`;
    document.getElementById('page-label').textContent = `Page ${page + 1} of ${pages}`;
    document.getElementById('previous').disabled = page === 0;
    document.getElementById('next').disabled = page >= pages - 1;
    document.getElementById('empty-message').hidden = filtered.length !== 0;
    document.querySelector('.pagination').hidden = filtered.length === 0;
  }

  search.addEventListener('input', () => { page = 0; renderCollection(); });
  sort.addEventListener('change', () => { page = 0; renderCollection(); });
  ['previous','next'].forEach(id => document.getElementById(id).addEventListener('click', () => {
    page += id === 'next' ? 1 : -1;
    renderCollection();
    document.querySelector('.search-row').scrollIntoView({behavior:motionPreference.matches ? 'instant' : 'smooth',block:'start'});
  }));
  document.querySelectorAll('.motion-toggle').forEach(button => button.addEventListener('click', () => {
    userSelectedMotion = true;
    playing = !playing;
    updateMotion();
  }));
  motionPreference.addEventListener('change', event => {
    if (!userSelectedMotion) { playing = !event.matches; updateMotion(); }
  });
  document.getElementById('close-dialog').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if(event.target === dialog) {const bounds = dialog.getBoundingClientRect();if(event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();} });
  dialog.addEventListener('close', () => { document.body.classList.remove('dialog-open'); dialogImage.removeAttribute('src'); });
  document.addEventListener('keydown', event => {
    if(event.key === '/' && !dialog.open && !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)) {event.preventDefault(); search.focus();}
  });
  renderPreview();
  renderCollection();
  updateMotion();
})();
