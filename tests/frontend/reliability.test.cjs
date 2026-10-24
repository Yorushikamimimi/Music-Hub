const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const projectRoot = path.resolve(__dirname, '../..');
const readScript = (name) => fs.readFileSync(
    path.join(projectRoot, 'static', name),
    'utf8'
);

class FakeClassList {
    constructor() { this.values = new Set(); }
    add(value) { this.values.add(value); }
    remove(value) { this.values.delete(value); }
    contains(value) { return this.values.has(value); }
    toggle(value, force) {
        const shouldAdd = force === undefined ? !this.contains(value) : force;
        if (shouldAdd) this.add(value);
        else this.remove(value);
        return shouldAdd;
    }
    replace(oldValue, newValue) {
        if (!this.values.has(oldValue)) return false;
        this.values.delete(oldValue);
        this.values.add(newValue);
        return true;
    }
}

class FakeElement {
    constructor(id = '') {
        this.id = id;
        this.dataset = {};
        this.classList = new FakeClassList();
        this.style = {};
        this.attributes = {};
        this.listeners = new Map();
        this.children = [];
        this.textContent = '';
        this.value = '';
        this.paused = true;
        this.ended = false;
        this.volume = 1;
        this.muted = false;
        this.currentTime = 0;
        this.failPlay = false;
    }
    addEventListener(type, callback) {
        const callbacks = this.listeners.get(type) || [];
        callbacks.push(callback);
        this.listeners.set(type, callbacks);
    }
    async emit(type, event = {}) {
        const callbacks = this.listeners.get(type) || [];
        for (const callback of callbacks) await callback({target: this, ...event});
    }
    async click() { return this.emit('click', {preventDefault() {}, stopPropagation() {}}); }
    setAttribute(key, value) { this.attributes[key] = String(value); }
    getAttribute(key) { return this.attributes[key] || (key === 'src' ? '/cover.svg' : null); }
    hasAttribute(key) { return Object.hasOwn(this.attributes, key); }
    removeAttribute(key) { delete this.attributes[key]; }
    querySelector(selector) {
        if (!this.queryBySelector) this.queryBySelector = new Map();
        if (!this.queryBySelector.has(selector)) {
            this.queryBySelector.set(selector, new FakeElement(`${this.id}:${selector}`));
        }
        return this.queryBySelector.get(selector);
    }
    querySelectorAll() { return this.children; }
    append(...items) { this.children.push(...items); }
    appendChild(item) { this.children.push(item); return item; }
    replaceChildren(...items) { this.children = items; }
}

const createTimerApi = () => {
    let nextId = 1;
    const timeouts = new Map();
    const intervals = new Map();
    return {
        timeouts,
        intervals,
        setTimeout(callback, delay) {
            const id = nextId++;
            timeouts.set(id, {callback, delay});
            return id;
        },
        clearTimeout(id) { timeouts.delete(id); },
        setInterval(callback, delay) {
            const id = nextId++;
            intervals.set(id, {callback, delay});
            return id;
        },
        runTimeout(id) {
            const timer = timeouts.get(id);
            assert.ok(timer, `timeout ${id} exists`);
            timeouts.delete(id);
            return timer.callback();
        },
    };
};

const flush = async () => new Promise((resolve) => setImmediate(resolve));

function createRadioHarness({storageThrows = false, responses = []} = {}) {
    const ids = [
        'global-radio-dock', 'global-radio-audio', 'global-radio-title',
        'global-radio-artist', 'global-radio-progress', 'global-radio-progress-fill',
        'global-radio-time', 'global-radio-toggle', 'global-radio-mute',
        'global-radio-volume', 'global-radio-artwork', 'global-radio-artwork-map',
        'radio-playback-status',
    ];
    const elements = new Map(ids.map((id) => [id, new FakeElement(id)]));
    const dock = elements.get('global-radio-dock');
    dock.dataset.radioSchedule = '/hls/radio-schedule.json';
    const audio = elements.get('global-radio-audio');
    const playCalls = [];
    audio.play = async () => {
        playCalls.push(true);
        if (audio.failPlay) throw new Error('network unavailable');
        audio.paused = false;
        await audio.emit('play');
        await audio.emit('playing');
    };
    audio.load = () => { audio.paused = true; };
    audio.pause = async () => {
        audio.paused = true;
        await audio.emit('pause');
    };

    const documentListeners = new Map();
    const document = {
        getElementById: (id) => elements.get(id) || null,
        querySelector: () => null,
        addEventListener(type, callback) {
            const callbacks = documentListeners.get(type) || [];
            callbacks.push(callback);
            documentListeners.set(type, callbacks);
        },
    };
    const timers = createTimerApi();
    let fetchCount = 0;
    const fetch = async (_url, options = {}) => {
        fetchCount += 1;
        const response = responses.shift();
        if (response instanceof Error) throw response;
        if (typeof response === 'function') return response(options);
        return response || scheduleResponse();
    };
    const storage = {
        getItem() {
            if (storageThrows) throw new Error('StorageError');
            return null;
        },
        setItem() {
            if (storageThrows) throw new Error('StorageError');
        },
    };
    const window = {
        location: {origin: 'https://example.test'},
        setTimeout: timers.setTimeout,
        clearTimeout: timers.clearTimeout,
        setInterval: timers.setInterval,
    };
    const context = vm.createContext({
        document, window, localStorage: storage, fetch, URL, Date, Number,
        AbortController,
        Math, String, Array, JSON, console: {warn() {}}, navigator: {},
    });
    vm.runInContext(readScript('radio.js'), context);
    return {
        elements, audio, dock, timers, playCalls,
        get fetchCount() { return fetchCount; },
        async clickPlay() { await elements.get('global-radio-toggle').click(); },
        async dispatchDocument(type) {
            for (const callback of documentListeners.get(type) || []) await callback();
        },
    };
}

function scheduleResponse(payload = {
    startedAt: Date.now() / 1000,
    bufferDelaySeconds: 16,
    tracks: [{title: '晴る', artist: 'Yorushika', duration: 210}],
}) {
    return {
        ok: true,
        headers: {get: (name) => name === 'Date' ? new Date().toUTCString() : null},
        json: async () => payload,
    };
}

test('radio tolerates StorageError and keeps the default volume', async () => {
    const radio = createRadioHarness({storageThrows: true});
    await flush();
    assert.equal(radio.audio.volume, 0.25);
    radio.audio.volume = 0.6;
    await radio.audio.emit('volumechange');
    assert.equal(radio.elements.get('global-radio-volume').value, '0.6');
});

test('radio retries a failed stream, but a manual pause cancels recovery', async () => {
    const radio = createRadioHarness();
    await flush();
    radio.audio.failPlay = true;
    await radio.clickPlay();
    assert.equal(radio.playCalls.length, 1);
    assert.equal(radio.timers.timeouts.size, 1);
    const retryId = [...radio.timers.timeouts.keys()][0];
    assert.equal(radio.timers.timeouts.get(retryId).delay, 1000);

    radio.audio.failPlay = false;
    await radio.timers.runTimeout(retryId);
    await flush();
    assert.equal(radio.audio.paused, false);

    await radio.audio.emit('error');
    assert.equal(radio.timers.timeouts.size, 1);
    await radio.clickPlay();
    assert.equal(radio.timers.timeouts.size, 0);
    assert.equal(radio.audio.paused, true);
});

test('radio recovery button cancels retries while audio remains paused', async () => {
    const radio = createRadioHarness();
    await flush();
    radio.audio.failPlay = true;
    await radio.clickPlay();
    const toggle = radio.elements.get('global-radio-toggle');
    assert.equal(toggle.getAttribute('aria-label'), '取消夜鹿电台重连');
    assert.equal(toggle.querySelector('span').textContent, '取消重连');
    assert.equal(radio.timers.timeouts.size, 1);

    await radio.clickPlay();
    assert.equal(radio.timers.timeouts.size, 0);
    assert.equal(radio.audio.paused, true);
    assert.equal(toggle.getAttribute('aria-label'), '播放夜鹿电台');
});

test('late play events after cancellation pause audio and restore the ready message', async () => {
    const radio = createRadioHarness();
    await flush();
    let resolvePlay;
    radio.audio.play = () => new Promise((resolve) => { resolvePlay = resolve; });
    const pendingPlay = radio.clickPlay();
    await flush();
    await radio.clickPlay();
    assert.equal(radio.audio.paused, true);

    radio.audio.paused = false;
    await radio.audio.emit('play');
    await radio.audio.emit('playing');
    assert.equal(radio.audio.paused, true);
    assert.equal(
        radio.elements.get('radio-playback-status').textContent,
        '准备好后，点击“开始收听”。'
    );
    resolvePlay();
    await pendingPlay;
    assert.equal(radio.audio.paused, true);
});

test('radio gives up after a bounded number of failed recovery attempts', async () => {
    const radio = createRadioHarness();
    await flush();
    radio.audio.failPlay = true;
    await radio.clickPlay();
    for (let attempt = 0; attempt < 5; attempt += 1) {
        const retryId = [...radio.timers.timeouts.keys()][0];
        assert.ok(retryId);
        await radio.timers.runTimeout(retryId);
        await flush();
    }
    assert.equal(radio.playCalls.length, 6);
    assert.equal(radio.timers.timeouts.size, 0);
    assert.equal(
        radio.elements.get('radio-playback-status').textContent,
        '电台暂时无法恢复，请点击播放重试。'
    );
    radio.audio.failPlay = false;
    await radio.clickPlay();
    assert.equal(radio.audio.paused, false);
});

test('radio schedule refreshes, retries invalid payloads, then clears unavailable state', async () => {
    const radio = createRadioHarness({
        responses: [
            scheduleResponse({
                startedAt: null,
                tracks: [{title: '晴る', duration: 210}],
            }),
            scheduleResponse(),
        ],
    });
    await flush();
    assert.equal(radio.fetchCount, 1);
    assert.equal(radio.elements.get('global-radio-artist').textContent, '曲目信息暂时不可用');
    const retryId = [...radio.timers.timeouts.keys()][0];
    assert.equal(radio.timers.timeouts.get(retryId).delay, 5000);
    await radio.timers.runTimeout(retryId);
    await flush();
    assert.equal(radio.fetchCount, 2);
    assert.equal(radio.elements.get('global-radio-title').textContent, '晴る');
    assert.equal(radio.timers.intervals.size, 2);
    assert.equal(
        [...radio.timers.intervals.values()].filter(({delay}) => delay === 1000).length,
        1
    );
    await radio.dispatchDocument('music-hub:page-load');
    await radio.dispatchDocument('DOMContentLoaded');
    assert.equal(radio.timers.intervals.size, 2);
    await [...radio.timers.intervals.values()]
        .find(({delay}) => delay === 60000).callback();
    await flush();
    assert.equal(radio.fetchCount, 3);
});

test('schedule request timeout releases the in-flight lock for a later refresh', async () => {
    const radio = createRadioHarness({
        responses: [({signal}) => new Promise((_resolve, reject) => {
            signal.addEventListener('abort', () => reject(new Error('request aborted')));
        })],
    });
    await flush();
    const timeoutId = [...radio.timers.timeouts.entries()]
        .find(([, timer]) => timer.delay === 10000)?.[0];
    assert.ok(timeoutId);
    await radio.timers.runTimeout(timeoutId);
    await flush();
    assert.equal(radio.fetchCount, 1);

    const retryId = [...radio.timers.timeouts.keys()][0];
    await radio.timers.runTimeout(retryId);
    await flush();
    assert.equal(radio.fetchCount, 2);
    assert.equal(radio.elements.get('global-radio-title').textContent, '晴る');
});

test('theme initializes and remains usable when storage access throws', () => {
    const root = new FakeElement('root');
    root.setAttribute('data-theme', 'light');
    const toggle = new FakeElement('theme-toggle');
    const listeners = new Map();
    const document = {
        documentElement: root,
        getElementById: (id) => id === 'theme-toggle' ? toggle : null,
        addEventListener(type, callback) { listeners.set(type, callback); },
        dispatchEvent() {},
        querySelectorAll: () => [],
    };
    const context = vm.createContext({
        document,
        window: {addEventListener() {}, location: {href: 'https://example.test/', origin: 'https://example.test', pathname: '/', search: ''}},
        localStorage: {
            getItem() { throw new Error('StorageError'); },
            setItem() { throw new Error('StorageError'); },
        },
        URL, Map, Array, String, CustomEvent: class {}, AbortController,
        console: {warn() {}}, fetch() {}, DOMParser: class {},
    });
    vm.runInContext(readScript('site.js'), context);
    assert.equal(root.getAttribute('data-theme'), 'light');
    toggle.click();
    assert.equal(root.getAttribute('data-theme'), 'dark');
});

test('favorite write failure reports the failure without changing the button', () => {
    const button = new FakeElement('favorite');
    button.dataset = {
        songId: 'haru', songTitle: '晴る', songAlbum: '幻燈',
        songLink: '/songs/haru', songYear: '2024',
    };
    const icon = new FakeElement('heart');
    icon.classList.add('bi-heart');
    button.queryBySelector = new Map([['i', icon]]);
    const listeners = new Map();
    const toast = new FakeElement('fav-toast');
    const document = {
        addEventListener(type, callback) { listeners.set(type, callback); },
        querySelectorAll: () => [button],
        getElementById: (id) => id === 'fav-toast' ? toast : null,
        createElement: () => new FakeElement(),
        body: {appendChild() {}},
    };
    const context = vm.createContext({
        document,
        window: {},
        localStorage: {
            getItem: () => null,
            setItem() { throw new Error('QuotaExceededError'); },
        },
        setTimeout: () => 1,
        clearTimeout() {},
        console: {warn() {}},
    });
    vm.runInContext(readScript('favorites.js'), context);
    listeners.get('DOMContentLoaded')();
    button.click();
    assert.equal(button.classList.contains('favorited'), false);
    assert.equal(icon.classList.contains('bi-heart'), true);
    assert.match(toast.textContent, /无法读取或保存收藏/);
});

test('favorite read failure reports that the displayed list may be incomplete', () => {
    let toast = null;
    const document = {
        addEventListener() {},
        querySelectorAll: () => [],
        getElementById: () => null,
        createElement: () => (toast = new FakeElement('toast')),
        body: {appendChild(element) { toast = element; }},
    };
    const context = vm.createContext({
        document,
        window: {},
        localStorage: {getItem() { throw new Error('StorageError'); }},
        setTimeout: () => 1,
        clearTimeout() {},
        console: {warn() {}},
    });
    vm.runInContext(readScript('favorites.js'), context);
    assert.deepEqual(Array.from(vm.runInContext('getFavorites()', context)), []);
    assert.match(toast.textContent, /未能读取已有收藏/);
});

test('favorite read failure blocks removal and leaves the button unchanged', async () => {
    const button = new FakeElement('favorite');
    button.dataset = {songId: 'haru', songTitle: '晴る'};
    const icon = new FakeElement('heart');
    icon.classList.add('bi-heart');
    button.queryBySelector = new Map([['i', icon]]);
    const toast = new FakeElement('fav-toast');
    const documentListeners = new Map();
    const document = {
        addEventListener(type, callback) { documentListeners.set(type, callback); },
        querySelectorAll: () => [button],
        getElementById: (id) => id === 'fav-toast' ? toast : null,
        createElement: () => new FakeElement(),
        body: {appendChild() {}},
    };
    let writeCalls = 0;
    const context = vm.createContext({
        document,
        window: {},
        localStorage: {
            getItem() { throw new Error('StorageError'); },
            setItem() { writeCalls += 1; },
        },
        setTimeout: () => 1,
        clearTimeout() {},
        console: {warn() {}},
    });
    vm.runInContext(readScript('favorites.js'), context);
    documentListeners.get('DOMContentLoaded')();
    await button.click();

    assert.equal(writeCalls, 0);
    assert.equal(button.classList.contains('favorited'), false);
    assert.equal(icon.classList.contains('bi-heart'), true);
    assert.match(toast.textContent, /无法读取或保存收藏/);
});

test('clearing favorites reports StorageError without claiming success or changing the list', async () => {
    const savedFavorites = JSON.stringify([
        {id: 'haru', title: '晴る', album: '幻燈', link: '/songs/haru', year: '2024'},
    ]);
    const elements = new Map();
    const wishlist = new FakeElement('wishlist-body');
    wishlist.replaceChildren = (...items) => { wishlist.children = items; };
    const clearButton = new FakeElement('clear-favs-btn');
    clearButton.style = {display: ''};
    const pageBody = new FakeElement('body');
    elements.set('wishlist-body', wishlist);
    elements.set('clear-favs-btn', clearButton);
    let removeCalls = 0;
    const documentListeners = new Map();
    const document = {
        addEventListener(type, callback) {
            const callbacks = documentListeners.get(type) || [];
            callbacks.push(callback);
            documentListeners.set(type, callbacks);
        },
        querySelectorAll: () => [],
        getElementById: (id) => elements.get(id) || null,
        createElement: () => new FakeElement(),
        body: {
            appendChild(element) {
                pageBody.appendChild(element);
                if (element.id) elements.set(element.id, element);
            },
        },
    };
    const context = vm.createContext({
        document,
        window: {confirm: () => true, location: {origin: 'https://example.test'}},
        localStorage: {
            getItem: () => savedFavorites,
            setItem() {},
            removeItem() {
                removeCalls += 1;
                throw new Error('StorageError');
            },
        },
        URL,
        setTimeout: () => 1,
        clearTimeout() {},
        console: {warn() {}},
    });
    vm.runInContext(readScript('favorites.js'), context);
    vm.runInContext(readScript('about.js'), context);
    for (const callback of documentListeners.get('DOMContentLoaded') || []) callback();
    const rowBeforeClear = wishlist.children[0];
    assert.ok(rowBeforeClear);

    await clearButton.click();

    assert.equal(removeCalls, 1);
    assert.equal(wishlist.children[0], rowBeforeClear);
    assert.equal(clearButton.style.display, '');
    assert.equal(elements.get('fav-toast').textContent, '浏览器未能清空收藏，请检查存储设置。');
    assert.notEqual(elements.get('fav-toast').textContent, '收藏已清空。');
});
