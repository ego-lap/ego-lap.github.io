const navLinks = [...document.querySelectorAll('.nav-links a[href^="#"]')];
const sectionObserver = new IntersectionObserver(entries => { for (const entry of entries) if (entry.isIntersecting) navLinks.forEach(link => { const active = link.hash === '#' + entry.target.id; link.classList.toggle('active', active); if (active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current'); }); }, {rootMargin: '-15% 0px -60% 0px'});
document.querySelectorAll('section[id]').forEach(section => sectionObserver.observe(section));
document.querySelector('#copy-citation').addEventListener('click', async () => { const status = document.querySelector('#copy-status'); try { await navigator.clipboard.writeText(document.querySelector('#bibtex').textContent); status.textContent = 'Citation copied.'; } catch { status.textContent = 'Select the citation above and copy it.'; } });
const video = document.querySelector('#demo-video');
const playButton = document.querySelector('#toggle-play');
const progress = document.querySelector('#video-progress');
const speed = document.querySelector('#video-speed');
const view = document.querySelector('#camera-view');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
let selected = 0;
let clips = [];
function applyView(value) { document.querySelector('.video-viewport').dataset.view = value; document.querySelector('.demo-player').classList.toggle('single-view', value !== 'all'); view.value = value; }
applyView(matchMedia('(max-width: 600px)').matches ? 'base' : 'all');
view.addEventListener('change', () => applyView(view.value));
function updatePlayButton() { playButton.textContent = video.paused ? '▶' : 'Ⅱ'; playButton.setAttribute('aria-label', video.paused ? 'Play video' : 'Pause video'); }
playButton.addEventListener('click', () => { if (video.paused) video.play().catch(() => {}); else video.pause(); });
video.addEventListener('play', updatePlayButton);
video.addEventListener('pause', updatePlayButton);
video.addEventListener('timeupdate', () => { progress.value = Number.isFinite(video.duration) ? video.currentTime / video.duration * 100 : 0; document.querySelector('#video-time').textContent = Math.floor(video.currentTime / 60) + ':' + String(Math.floor(video.currentTime % 60)).padStart(2, '0'); });
progress.addEventListener('input', () => { if (Number.isFinite(video.duration)) video.currentTime = progress.value / 100 * video.duration; });
speed.addEventListener('change', () => video.playbackRate = Number(speed.value));
document.querySelector('#fullscreen').addEventListener('click', () => { if (video.requestFullscreen) video.requestFullscreen().catch(() => {}); else if (video.webkitEnterFullscreen) video.webkitEnterFullscreen(); });
function selectClip(index, play = true) { selected = index; const clip = clips[index]; video.pause(); video.src = 'assets/videos/' + clip.file; video.poster = 'assets/videos/' + clip.poster; video.setAttribute('aria-label', clip.title + ', three camera views'); video.playbackRate = Number(speed.value); document.querySelector('#clip-title').textContent = clip.title; document.querySelector('#clip-index').textContent = String(index + 1).padStart(2, '0') + ' / ' + String(clips.length).padStart(2, '0'); document.querySelectorAll('.clip-button').forEach((button, i) => button.setAttribute('aria-pressed', String(i === index))); progress.value = 0; document.querySelector('#video-time').textContent = '0:00'; video.load(); if (play) video.play().catch(() => {}); }
fetch('assets/videos/manifest.json').then(response => { if (!response.ok) throw Error('Cannot load demonstrations'); return response.json(); }).then(items => { clips = items; if (!clips.length) return; const selector = document.querySelector('#clip-selector'); clips.forEach((clip, index) => { const button = document.createElement('button'); button.type = 'button'; button.className = 'clip-button'; button.setAttribute('aria-pressed', String(index === selected)); button.setAttribute('aria-label', clip.title); const thumb = document.createElement('span'); thumb.className = 'thumb-wrap'; const image = document.createElement('img'); image.src = 'assets/videos/' + clip.poster; image.alt = ''; image.loading = 'lazy'; const label = document.createElement('strong'); label.textContent = clip.title; thumb.append(image); button.append(thumb, label); button.addEventListener('click', () => selectClip(index)); selector.append(button); }); selectClip(0, !reducedMotion); }).catch(() => { document.querySelector('.demo-caption').textContent = 'Use the playback controls to explore this demonstration.'; });
const mediaObserver = new IntersectionObserver(entries => { if (!entries[0].isIntersecting) video.pause(); }, {threshold: 0});
mediaObserver.observe(video);
document.addEventListener('visibilitychange', () => { if (document.hidden) video.pause(); });

document.addEventListener('fullscreenchange', () => { video.controls = document.fullscreenElement === video; });
