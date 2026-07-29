(() => {
    const body = document.getElementById('wishlist-body');
    const clearButton = document.getElementById('clear-favs-btn');
    if (!body || !clearButton || typeof getFavorites !== 'function') return;

    const safeExternalUrl = (value) => {
        try {
            const url = new URL(value, window.location.origin);
            return ['https:', 'http:'].includes(url.protocol) ? url.href : '#';
        } catch {
            return '#';
        }
    };

    const emptyState = () => {
        const wrapper = document.createElement('div');
        wrapper.className = 'text-center py-4 text-muted';

        const icon = document.createElement('i');
        icon.className = 'bi bi-music-note-list display-4 opacity-25';
        icon.setAttribute('aria-hidden', 'true');

        const text = document.createElement('p');
        text.className = 'mt-3 small';
        text.textContent = '还没有收藏任何歌曲，去首页点 ❤ 吧！';

        wrapper.append(icon, text);
        return wrapper;
    };

    const favoriteRow = (song) => {
        const row = document.createElement('div');
        row.className = 'wishlist-item d-flex align-items-center justify-content-between';

        const details = document.createElement('div');
        details.className = 'd-flex align-items-center gap-3';
        const noteIcon = document.createElement('i');
        noteIcon.className = 'bi bi-music-note-beamed text-danger';
        noteIcon.setAttribute('aria-hidden', 'true');

        const text = document.createElement('div');
        const link = document.createElement('a');
        link.className = 'fw-bold text-decoration-none wishlist-link';
        link.href = safeExternalUrl(song.link);
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.textContent = song.title || '未命名曲目';

        const metadata = document.createElement('div');
        metadata.className = 'small text-muted';
        metadata.textContent = [song.album, song.year].filter(Boolean).join(' · ');
        text.append(link, metadata);
        details.append(noteIcon, text);

        const favoriteButton = document.createElement('button');
        favoriteButton.className = 'fav-btn favorited';
        favoriteButton.dataset.songId = String(song.id || '');
        favoriteButton.dataset.songTitle = song.title || '';
        favoriteButton.dataset.songAlbum = song.album || '';
        favoriteButton.dataset.songLink = safeExternalUrl(song.link);
        favoriteButton.dataset.songYear = song.year || '';
        favoriteButton.title = `取消收藏 ${song.title || ''}`;
        favoriteButton.setAttribute('aria-label', favoriteButton.title);
        const heart = document.createElement('i');
        heart.className = 'bi bi-heart-fill';
        heart.setAttribute('aria-hidden', 'true');
        favoriteButton.append(heart);

        row.append(details, favoriteButton);
        return row;
    };

    window.renderWishlist = () => {
        const favorites = getFavorites();
        body.replaceChildren();

        if (favorites.length === 0) {
            clearButton.style.display = 'none';
            body.append(emptyState());
            return;
        }

        clearButton.style.display = '';
        favorites.forEach((song) => body.append(favoriteRow(song)));
        initFavButtons();
    };

    clearButton.addEventListener('click', () => {
        if (window.confirm('确认清空全部收藏吗？')) {
            localStorage.removeItem(FAV_KEY);
            window.renderWishlist();
            showToast('收藏已清空。');
        }
    });

    window.renderWishlist();
})();
