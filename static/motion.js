(() => {
    const root = document.documentElement;
    const calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    root.classList.add('motion-ready');

    // site.js swaps #main-content in place on in-site navigation and then fires
    // `music-hub:page-load`, so everything below re-runs for each new page; a
    // flag on the current main element keeps it from running twice on one page.
    const init = () => {
        const main = document.getElementById('main-content') || document.body;
        if (main.dataset.motionReady) return;
        main.dataset.motionReady = '1';

        // Scroll reveal: cards fade up as they enter the viewport, staggered per row.
        const revealTargets = document.querySelectorAll(
            '.featured-track-card, .listening-path-card, .album-thread-row'
        );
        if (calm || !('IntersectionObserver' in window)) {
            revealTargets.forEach((el) => el.classList.add('is-seen'));
        } else {
            const seen = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) return;
                    entry.target.classList.add('is-seen');
                    seen.unobserve(entry.target);
                });
            }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
            revealTargets.forEach((el) => {
                const siblings = [...el.parentElement.children];
                el.style.setProperty('--reveal-i', String(siblings.indexOf(el) % 6));
                seen.observe(el);
            });
        }

        // Gentle 3D tilt on today's card, following the pointer.
        const tiltCard = document.querySelector('.daily-listening-card');
        if (tiltCard && !calm && window.matchMedia('(hover: hover)').matches) {
            tiltCard.addEventListener('pointermove', (event) => {
                const box = tiltCard.getBoundingClientRect();
                const x = (event.clientX - box.left) / box.width - 0.5;
                const y = (event.clientY - box.top) / box.height - 0.5;
                tiltCard.style.transform = `rotateY(${x * 7}deg) rotateX(${-y * 7}deg)`;
            });
            tiltCard.addEventListener('pointerleave', () => {
                tiltCard.style.transform = '';
            });
        }

        // Lists: mark songs that have frames in the local studio ("工房 N").
        const slots = document.querySelectorAll('[data-studio-slug]');
        if (slots.length) {
            fetch('/local/studio/songs', { headers: { Accept: 'application/json' } })
                .then((resp) => (resp.ok ? resp.json() : null))
                .then((data) => {
                    const counts = (data && data.counts) || {};
                    slots.forEach((slot) => {
                        const n = counts[slot.dataset.studioSlug];
                        if (!n) return;
                        slot.textContent = `工房 ${n}`;
                        slot.title = `视觉工房里收藏了这首歌的 ${n} 帧`;
                        slot.hidden = false;
                    });
                })
                .catch(() => {});
        }

        // Song page: frames the owner kept in the local visual studio.
        const studio = document.querySelector('[data-studio-frames]');
        if (!studio) return;

        // Scroll to the block without touching the URL hash (a hash change would
        // make site.js reload the page body).
        document.querySelector('.studio-jump')?.addEventListener('click', (event) => {
            event.preventDefault();
            studio.scrollIntoView({ behavior: calm ? 'auto' : 'smooth', block: 'start' });
        });

        const lyricBox = studio.querySelector('.studio-lyric');
        const strip = studio.querySelector('.studio-strip');
        const count = studio.querySelector('.studio-count');
        let typing = 0;

        const showLyric = (frame) => {
            const text = frame.lyric || `${frame.source}${frame.timecode ? ' · ' + frame.timecode : ''}`;
            lyricBox.classList.toggle('is-meta', !frame.lyric);
            lyricBox.textContent = '';
            const run = ++typing;
            if (calm) {
                lyricBox.textContent = text;
                return;
            }
            [...text].forEach((ch, i) => {
                const span = document.createElement('span');
                span.textContent = ch;
                span.style.animationDelay = `${Math.min(i * 28, 900)}ms`;
                if (run === typing) lyricBox.appendChild(span);
            });
        };

        fetch(studio.dataset.studioFrames, { headers: { Accept: 'application/json' } })
            .then((resp) => (resp.ok ? resp.json() : null))
            .then((data) => {
                if (!data) return;
                if (!data.online) {
                    studio.hidden = false;
                    studio.classList.add('is-offline');
                    return;
                }
                if (!data.frames.length) return;
                data.frames.forEach((frame, i) => {
                    const link = document.createElement('a');
                    link.href = frame.href;
                    link.target = '_blank';
                    link.rel = 'noopener';
                    link.setAttribute('aria-label', `在视觉工房打开这一帧：${frame.source} ${frame.timecode}`);
                    const img = document.createElement('img');
                    img.src = frame.image;
                    img.alt = '';
                    img.loading = 'lazy';
                    img.decoding = 'async';
                    const tag = document.createElement('span');
                    tag.textContent = frame.timecode || frame.source;
                    link.append(img, tag);
                    link.addEventListener('mouseenter', () => showLyric(frame));
                    link.addEventListener('focus', () => showLyric(frame));
                    link.style.setProperty('--reveal-i', String(i % 8));
                    strip.appendChild(link);
                });
                count.textContent = `收藏了 ${data.frames.length} 帧`;
                studio.hidden = false;
                const jump = document.querySelector('.studio-jump');
                if (jump) {
                    jump.querySelector('span').textContent = `工房画面 ${data.frames.length} 帧`;
                    jump.hidden = false;
                }
                showLyric(data.frames.find((f) => f.lyric) || data.frames[0]);
            })
            .catch(() => {});
    };

    init();
    document.addEventListener('music-hub:page-load', init);
})();
