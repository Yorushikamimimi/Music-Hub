/**
 * favorites.js — 歌曲收藏/心愿单
 * 使用 localStorage 在本地持久化收藏数据，无需后端。
 */

const FAV_KEY = 'yorushika_favorites';
let favoritesReadWarningShown = false;
let favoritesReadFailed = false;

/** 读取所有收藏（返回对象数组） */
function getFavorites() {
    favoritesReadFailed = false;
    try {
        const storedValue = localStorage.getItem(FAV_KEY);
        const value = JSON.parse(storedValue);
        if (storedValue !== null && !Array.isArray(value)) {
            throw new Error('Stored favorites are not a list');
        }
        return Array.isArray(value) ? value : [];
    } catch (error) {
        favoritesReadFailed = true;
        console.warn('Favorites could not be read:', error);
        if (!favoritesReadWarningShown) {
            favoritesReadWarningShown = true;
            showToast('浏览器未能读取已有收藏，收藏列表可能不完整。');
        }
        return [];
    }
}

/** 保存收藏列表 */
function saveFavorites(favs) {
    try {
        localStorage.setItem(FAV_KEY, JSON.stringify(favs));
        return true;
    } catch (error) {
        console.warn('Favorites could not be saved:', error);
        return false;
    }
}

/** 是否已收藏（按 id 或 link 判断） */
function isFavorited(songId) {
    return getFavorites().some(s => s.id === songId);
}

/** 切换收藏状态，返回最新状态 true / false */
function toggleFavorite(song) {
    let favs = getFavorites();
    if (favoritesReadFailed) return null;
    const idx = favs.findIndex(s => s.id === song.id);
    if (idx === -1) {
        favs.push(song);
    } else {
        favs.splice(idx, 1);
    }
    if (!saveFavorites(favs)) return null;
    return idx === -1; // true = 刚被收藏
}

/** 为页面上所有 .fav-btn 绑定事件，并同步初始状态 */
function initFavButtons() {
    document.querySelectorAll('.fav-btn').forEach(btn => {
        if (btn.dataset.favoriteBound === 'true') return;
        btn.dataset.favoriteBound = 'true';
        const id    = btn.dataset.songId;
        const icon  = btn.querySelector('i');
        // 初始状态
        if (isFavorited(id)) {
            btn.classList.add('favorited');
            icon.classList.replace('bi-heart', 'bi-heart-fill');
        }

        btn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            const song = {
                id:     btn.dataset.songId,
                title:  btn.dataset.songTitle,
                album:  btn.dataset.songAlbum,
                link:   btn.dataset.songLink,
                year:   btn.dataset.songYear,
            };
            const added = toggleFavorite(song);
            if (added === null) {
                showToast('浏览器无法读取或保存收藏，请检查存储设置或空间。');
                return;
            }
            if (added) {
                btn.classList.add('favorited');
                icon.classList.replace('bi-heart', 'bi-heart-fill');
                showToast(`已收藏《${song.title}》`);
            } else {
                btn.classList.remove('favorited');
                icon.classList.replace('bi-heart-fill', 'bi-heart');
                showToast(`已取消收藏《${song.title}》`);
            }
            // 如果当前在 about 页面，实时刷新心愿单
            if (typeof window.renderWishlist === 'function') window.renderWishlist();
        });
    });
}

/** 简易 Toast 提示 */
function showToast(msg) {
    let toast = document.getElementById('fav-toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'fav-toast';
        toast.className = 'fav-toast';
        toast.setAttribute('role', 'status');
        toast.setAttribute('aria-live', 'polite');
        document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => toast.classList.remove('show'), 2500);
}

document.addEventListener('DOMContentLoaded', initFavButtons);
document.addEventListener('music-hub:page-load', initFavButtons);
