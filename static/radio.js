(() => {
    const page = document.querySelector('.radio-player-card');
    const audio = document.getElementById('radio-audio');
    const equalizer = document.getElementById('radio-equalizer');
    const title = document.getElementById('radio-track-title');
    const artist = document.getElementById('radio-track-artist');
    const nextTitle = document.getElementById('radio-next-title');
    const elapsed = document.getElementById('radio-elapsed');
    const duration = document.getElementById('radio-duration');
    const progressTrack = document.getElementById('radio-progress-track');
    const progressFill = document.getElementById('radio-progress-fill');
    const playbackStatus = document.getElementById('radio-playback-status');

    if (!page || !audio || !equalizer || !title || !artist || !nextTitle) return;

    let schedule = null;
    let serverClockOffset = 0;
    const stationName = page.dataset.stationName || 'Yorushika Radio';

    const formatTime = (seconds) => {
        const safeSeconds = Math.max(0, Math.floor(Number(seconds) || 0));
        const minutes = Math.floor(safeSeconds / 60);
        return `${minutes}:${String(safeSeconds % 60).padStart(2, '0')}`;
    };

    const setPlaybackState = (isPlaying, message) => {
        equalizer.classList.toggle('is-playing', isPlaying);
        if (playbackStatus) playbackStatus.textContent = message;
    };

    const renderSchedule = () => {
        if (!schedule || !Array.isArray(schedule.tracks) || schedule.tracks.length === 0) return;

        const totalDuration = schedule.tracks.reduce(
            (total, track) => total + Number(track.duration || 0),
            0
        );
        if (totalDuration <= 0) return;

        const serverNow = (Date.now() / 1000) + serverClockOffset;
        const liveSeconds = Math.max(
            0,
            serverNow - Number(schedule.startedAt || 0) - Number(schedule.bufferDelaySeconds || 0)
        );
        let position = liveSeconds % totalDuration;
        let currentIndex = 0;

        for (let index = 0; index < schedule.tracks.length; index += 1) {
            const trackDuration = Number(schedule.tracks[index].duration || 0);
            if (position < trackDuration) {
                currentIndex = index;
                break;
            }
            position -= trackDuration;
        }

        const currentTrack = schedule.tracks[currentIndex];
        const upcomingTrack = schedule.tracks[(currentIndex + 1) % schedule.tracks.length];
        const trackDuration = Number(currentTrack.duration || 0);
        const percentage = trackDuration > 0
            ? Math.min(100, Math.max(0, (position / trackDuration) * 100))
            : 0;

        title.textContent = currentTrack.title || 'Unknown track';
        artist.textContent = currentTrack.artist || stationName;
        nextTitle.textContent = `${upcomingTrack.title || 'Unknown track'} · ${upcomingTrack.artist || stationName}`;
        if (elapsed) elapsed.textContent = formatTime(position);
        if (duration) duration.textContent = formatTime(trackDuration);
        if (progressFill) progressFill.style.width = `${percentage}%`;
        if (progressTrack) {
            progressTrack.setAttribute('aria-valuenow', String(Math.round(percentage)));
            progressTrack.setAttribute(
                'aria-valuetext',
                `${currentTrack.title || 'Unknown track'}, ${formatTime(position)} of ${formatTime(trackDuration)}`
            );
        }
    };

    const loadSchedule = async () => {
        try {
            const scheduleUrl = new URL(page.dataset.radioSchedule, window.location.origin);
            scheduleUrl.searchParams.set('v', String(Date.now()));
            const response = await fetch(scheduleUrl, {cache: 'no-store'});
            if (!response.ok) throw new Error(`Schedule request failed with ${response.status}`);

            const serverDate = response.headers.get('Date');
            if (serverDate) {
                serverClockOffset = (new Date(serverDate).getTime() - Date.now()) / 1000;
            }

            schedule = await response.json();
            renderSchedule();
            window.setInterval(renderSchedule, 1000);
        } catch (error) {
            title.textContent = stationName;
            artist.textContent = 'Live stream';
            nextTitle.textContent = 'Track details temporarily unavailable';
            console.warn('Radio schedule unavailable:', error);
        }
    };

    audio.volume = 0.25;
    audio.addEventListener('loadedmetadata', () => {
        audio.volume = 0.25;
    });
    audio.addEventListener('play', () => setPlaybackState(true, 'Live stream playing'));
    audio.addEventListener('pause', () => {
        setPlaybackState(
            false,
            audio.currentTime > 0 ? 'Playback paused' : 'Click Play when you are ready.'
        );
    });
    audio.addEventListener('waiting', () => setPlaybackState(false, 'Buffering live stream…'));
    audio.addEventListener('playing', () => setPlaybackState(true, 'Live stream playing'));
    audio.addEventListener('error', () => {
        setPlaybackState(false, 'Playback is temporarily unavailable');
    });

    loadSchedule();
})();
