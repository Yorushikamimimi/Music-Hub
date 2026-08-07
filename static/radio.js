(() => {
    const dock = document.getElementById('global-radio-dock');
    const audio = document.getElementById('global-radio-audio');
    if (!dock || !audio) return;

    const dockTitle = document.getElementById('global-radio-title');
    const dockArtist = document.getElementById('global-radio-artist');
    const dockProgress = document.getElementById('global-radio-progress');
    const dockProgressFill = document.getElementById(
        'global-radio-progress-fill'
    );
    const dockTime = document.getElementById('global-radio-time');
    const dockToggle = document.getElementById('global-radio-toggle');
    const dockMute = document.getElementById('global-radio-mute');
    const dockVolume = document.getElementById('global-radio-volume');
    const dockArtwork = document.getElementById('global-radio-artwork');
    const artworkMapElement = document.getElementById(
        'global-radio-artwork-map'
    );
    const stationName = dock.dataset.stationName || '夜鹿电台';
    const fallbackArtwork = (
        dockArtwork?.getAttribute('src') || '/static/images/yorushika-eye.svg'
    );
    let artworkByTitle = {};
    let schedule = null;
    let scheduleUnavailable = false;
    let serverClockOffset = 0;
    let renderedTrackKey = '';

    try {
        artworkByTitle = JSON.parse(
            artworkMapElement?.dataset.artworkMap || '{}'
        );
    } catch (error) {
        console.warn('Radio artwork map is invalid:', error);
    }

    const formatTime = (seconds) => {
        const safeSeconds = Math.max(0, Math.floor(Number(seconds) || 0));
        const minutes = Math.floor(safeSeconds / 60);
        return `${minutes}:${String(safeSeconds % 60).padStart(2, '0')}`;
    };

    const pageControls = () => ({
        page: document.querySelector('.radio-player-card'),
        cover: document.getElementById('radio-cover'),
        artwork: document.getElementById('radio-disc-artwork'),
        equalizer: document.getElementById('radio-equalizer'),
        title: document.getElementById('radio-track-title'),
        artist: document.getElementById('radio-track-artist'),
        nextTitle: document.getElementById('radio-next-title'),
        elapsed: document.getElementById('radio-elapsed'),
        duration: document.getElementById('radio-duration'),
        progressTrack: document.getElementById('radio-progress-track'),
        progressFill: document.getElementById('radio-progress-fill'),
        playbackStatus: document.getElementById('radio-playback-status'),
        toggle: document.getElementById('radio-page-toggle'),
        mute: document.getElementById('radio-page-mute'),
        volume: document.getElementById('radio-page-volume'),
    });

    const normalizeTrackTitle = (title) => String(title || '')
        .replace(/\s*[（(]Live[）)]\s*$/i, '')
        .trim();

    const artworkForTrack = (track) => (
        artworkByTitle[
            normalizeTrackTitle(track?.artworkTitle || track?.title)
        ] || fallbackArtwork
    );

    const renderArtwork = (track) => {
        const artwork = artworkForTrack(track);
        if (dockArtwork) dockArtwork.src = artwork;
        const pageArtwork = pageControls().artwork;
        if (pageArtwork) pageArtwork.src = artwork;
    };

    const updateMediaMetadata = (track) => {
        if (!('mediaSession' in navigator) || !('MediaMetadata' in window)) {
            return;
        }
        const trackKey = `${track.title || ''}:${track.artist || ''}`;
        if (trackKey === renderedTrackKey) return;
        renderedTrackKey = trackKey;
        const artwork = artworkForTrack(track);
        navigator.mediaSession.metadata = new MediaMetadata({
            title: track.title || '夜鹿电台',
            artist: track.artist || 'Yorushika',
            album: '夜鹿集 · 私人电台',
            artwork: [
                {
                    src: artwork,
                    sizes: '512x512',
                    type: artwork.endsWith('.webp')
                        ? 'image/webp'
                        : 'image/svg+xml',
                },
            ],
        });
    };

    const setProgress = (percentage, position, trackDuration, trackTitle) => {
        const safePercentage = Math.min(
            100,
            Math.max(0, Number(percentage) || 0)
        );
        if (dockProgressFill) {
            dockProgressFill.style.width = `${safePercentage}%`;
        }
        if (dockProgress) {
            dockProgress.setAttribute(
                'aria-valuenow',
                String(Math.round(safePercentage))
            );
            dockProgress.setAttribute(
                'aria-valuetext',
                `${trackTitle}，${formatTime(position)} / ${formatTime(trackDuration)}`
            );
        }
        if (dockTime) {
            dockTime.textContent = (
                `${formatTime(position)} / ${formatTime(trackDuration)}`
            );
        }

        const page = pageControls();
        if (page.progressFill) {
            page.progressFill.style.width = `${safePercentage}%`;
        }
        if (page.progressTrack) {
            page.progressTrack.setAttribute(
                'aria-valuenow',
                String(Math.round(safePercentage))
            );
            page.progressTrack.setAttribute(
                'aria-valuetext',
                `${trackTitle}，${formatTime(position)} / ${formatTime(trackDuration)}`
            );
        }
        if (page.elapsed) page.elapsed.textContent = formatTime(position);
        if (page.duration) {
            page.duration.textContent = formatTime(trackDuration);
        }
    };

    const renderSchedule = () => {
        if (
            !schedule
            || !Array.isArray(schedule.tracks)
            || schedule.tracks.length === 0
        ) {
            return;
        }

        const totalDuration = schedule.tracks.reduce(
            (total, track) => total + Number(track.duration || 0),
            0
        );
        if (totalDuration <= 0) return;

        const serverNow = (Date.now() / 1000) + serverClockOffset;
        const liveSeconds = Math.max(
            0,
            serverNow
                - Number(schedule.startedAt || 0)
                - Number(schedule.bufferDelaySeconds || 0)
        );
        let position = liveSeconds % totalDuration;
        let currentIndex = 0;

        for (let index = 0; index < schedule.tracks.length; index += 1) {
            const trackDuration = Number(
                schedule.tracks[index].duration || 0
            );
            if (position < trackDuration) {
                currentIndex = index;
                break;
            }
            position -= trackDuration;
        }

        const currentTrack = schedule.tracks[currentIndex];
        const upcomingTrack = schedule.tracks[
            (currentIndex + 1) % schedule.tracks.length
        ];
        const trackDuration = Number(currentTrack.duration || 0);
        const percentage = trackDuration > 0
            ? (position / trackDuration) * 100
            : 0;
        const currentTitle = currentTrack.title || '未知曲目';
        const currentArtist = currentTrack.artist || 'Yorushika';
        const upcomingTitle = upcomingTrack.title || '未知曲目';
        const upcomingArtist = upcomingTrack.artist || 'Yorushika';

        if (dockTitle) dockTitle.textContent = currentTitle;
        if (dockArtist) dockArtist.textContent = currentArtist;

        const page = pageControls();
        if (page.title) page.title.textContent = currentTitle;
        if (page.artist) page.artist.textContent = currentArtist;
        if (page.nextTitle) {
            page.nextTitle.textContent = (
                `${upcomingTitle} · ${upcomingArtist}`
            );
        }
        setProgress(percentage, position, trackDuration, currentTitle);
        renderArtwork(currentTrack);
        updateMediaMetadata(currentTrack);
    };

    const setPlaybackMessage = (message) => {
        const status = pageControls().playbackStatus;
        if (status) status.textContent = message;
    };

    const renderUnavailableSchedule = () => {
        if (dockTitle) dockTitle.textContent = '夜鹿电台';
        if (dockArtist) dockArtist.textContent = '曲目信息暂时不可用';
        const page = pageControls();
        if (page.title) page.title.textContent = '夜鹿电台';
        if (page.artist) page.artist.textContent = '直播音频';
        if (page.nextTitle) {
            page.nextTitle.textContent = '曲目信息暂时不可用';
        }
        renderArtwork(null);
    };

    const updatePlaybackControls = () => {
        const isPlaying = !audio.paused && !audio.ended;
        dock.classList.toggle('is-playing', isPlaying);
        const page = pageControls();
        page.cover?.classList.toggle('is-playing', isPlaying);
        page.equalizer?.classList.toggle('is-playing', isPlaying);

        const updateToggle = (button) => {
            if (!button) return;
            const icon = button.querySelector('i');
            icon?.classList.toggle('bi-play-fill', !isPlaying);
            icon?.classList.toggle('bi-pause-fill', isPlaying);
            button.setAttribute(
                'aria-label',
                isPlaying ? '暂停夜鹿电台' : '播放夜鹿电台'
            );
            const label = button.querySelector('span');
            if (label) label.textContent = isPlaying ? '暂停播放' : '开始收听';
        };
        updateToggle(dockToggle);
        updateToggle(page.toggle);
    };

    const updateVolumeControls = () => {
        const effectiveMuted = audio.muted || audio.volume === 0;
        [dockMute, pageControls().mute].forEach((button) => {
            if (!button) return;
            const icon = button.querySelector('i');
            icon?.classList.toggle('bi-volume-up-fill', !effectiveMuted);
            icon?.classList.toggle('bi-volume-mute-fill', effectiveMuted);
            button.setAttribute(
                'aria-label',
                effectiveMuted ? '恢复声音' : '静音'
            );
        });
        [dockVolume, pageControls().volume].forEach((slider) => {
            if (slider) slider.value = String(audio.volume);
        });
    };

    const togglePlayback = async () => {
        if (audio.paused) {
            setPlaybackMessage('正在连接夜鹿电台…');
            try {
                await audio.play();
            } catch (error) {
                setPlaybackMessage('播放未能开始，请稍后再试。');
                console.warn('Radio playback did not start:', error);
            }
        } else {
            audio.pause();
        }
    };

    const bindPageControls = () => {
        const page = pageControls();
        if (!page.page) return;
        page.page.dataset.globalRadioConnected = 'true';

        if (page.toggle && page.toggle.dataset.bound !== 'true') {
            page.toggle.dataset.bound = 'true';
            page.toggle.addEventListener('click', togglePlayback);
        }
        if (page.mute && page.mute.dataset.bound !== 'true') {
            page.mute.dataset.bound = 'true';
            page.mute.addEventListener('click', () => {
                audio.muted = !audio.muted;
            });
        }
        if (page.volume && page.volume.dataset.bound !== 'true') {
            page.volume.dataset.bound = 'true';
            page.volume.addEventListener('input', () => {
                audio.muted = false;
                audio.volume = Number(page.volume.value);
            });
        }
        updatePlaybackControls();
        updateVolumeControls();
        renderSchedule();
        if (scheduleUnavailable) renderUnavailableSchedule();
        setPlaybackMessage(
            audio.paused
                ? '准备好后，点击“开始收听”。'
                : '夜鹿电台正在播放。'
        );
    };

    const loadSchedule = async () => {
        try {
            const scheduleUrl = new URL(
                dock.dataset.radioSchedule,
                window.location.origin
            );
            scheduleUrl.searchParams.set('v', String(Date.now()));
            const response = await fetch(scheduleUrl, {cache: 'no-store'});
            if (!response.ok) {
                throw new Error(
                    `Schedule request failed with ${response.status}`
                );
            }

            const serverDate = response.headers.get('Date');
            if (serverDate) {
                serverClockOffset = (
                    new Date(serverDate).getTime() - Date.now()
                ) / 1000;
            }

            schedule = await response.json();
            renderSchedule();
            window.setInterval(renderSchedule, 1000);
        } catch (error) {
            scheduleUnavailable = true;
            renderUnavailableSchedule();
            console.warn('Radio schedule unavailable:', error);
        }
    };

    const savedVolumeSetting = localStorage.getItem('radio-volume');
    const savedVolume = Number(savedVolumeSetting);
    audio.volume = savedVolumeSetting !== null
        && Number.isFinite(savedVolume)
        && savedVolume >= 0
        && savedVolume <= 1
        ? savedVolume
        : 0.25;

    dockToggle?.addEventListener('click', togglePlayback);
    dockMute?.addEventListener('click', () => {
        audio.muted = !audio.muted;
    });
    dockVolume?.addEventListener('input', () => {
        audio.muted = false;
        audio.volume = Number(dockVolume.value);
    });

    audio.addEventListener('play', () => {
        updatePlaybackControls();
        setPlaybackMessage('夜鹿电台正在播放。');
    });
    audio.addEventListener('pause', () => {
        updatePlaybackControls();
        setPlaybackMessage(
            audio.currentTime > 0
                ? '播放已暂停。'
                : '准备好后，点击“开始收听”。'
        );
    });
    audio.addEventListener('waiting', () => {
        dock.classList.remove('is-playing');
        pageControls().cover?.classList.remove('is-playing');
        pageControls().equalizer?.classList.remove('is-playing');
        setPlaybackMessage('正在缓冲直播音频…');
    });
    audio.addEventListener('playing', () => {
        updatePlaybackControls();
        setPlaybackMessage('夜鹿电台正在播放。');
    });
    audio.addEventListener('volumechange', () => {
        localStorage.setItem('radio-volume', String(audio.volume));
        updateVolumeControls();
    });
    audio.addEventListener('error', () => {
        updatePlaybackControls();
        setPlaybackMessage('音频暂时无法播放，请稍后再试。');
    });

    if ('mediaSession' in navigator) {
        try {
            navigator.mediaSession.setActionHandler('play', () => audio.play());
            navigator.mediaSession.setActionHandler('pause', () => audio.pause());
        } catch (error) {
            console.warn('Media Session controls unavailable:', error);
        }
    }

    document.addEventListener('music-hub:page-load', bindPageControls);
    document.addEventListener('DOMContentLoaded', bindPageControls);
    updatePlaybackControls();
    updateVolumeControls();
    loadSchedule();
})();
