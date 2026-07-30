(() => {
    const root = document.documentElement;
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = themeToggle?.querySelector('i');
    const navToggle = document.getElementById('mobile-nav-toggle');
    const navPanel = document.getElementById('site-nav');
    let activeNavigation = null;

    const updateThemeControl = (theme) => {
        if (!themeToggle || !themeIcon) return;
        const isDark = theme === 'dark';
        themeIcon.classList.toggle('bi-sun-fill', isDark);
        themeIcon.classList.toggle('bi-moon-stars-fill', !isDark);
        themeToggle.setAttribute(
            'aria-label',
            isDark ? '切换为浅色主题' : '切换为深色主题'
        );
    };

    const savedTheme = localStorage.getItem('theme');
    const initialTheme = savedTheme === 'dark' ? 'dark' : 'light';
    root.setAttribute('data-theme', initialTheme);
    updateThemeControl(initialTheme);

    themeToggle?.addEventListener('click', () => {
        const nextTheme = root.getAttribute('data-theme') === 'light'
            ? 'dark'
            : 'light';
        root.setAttribute('data-theme', nextTheme);
        localStorage.setItem('theme', nextTheme);
        updateThemeControl(nextTheme);
    });

    const setNavigationOpen = (isOpen) => {
        if (!navToggle || !navPanel) return;
        navPanel.classList.toggle('is-open', isOpen);
        navToggle.setAttribute('aria-expanded', String(isOpen));
        navToggle.setAttribute(
            'aria-label',
            isOpen ? '关闭导航菜单' : '打开导航菜单'
        );
        const icon = navToggle.querySelector('i');
        icon?.classList.toggle('bi-list', !isOpen);
        icon?.classList.toggle('bi-x-lg', isOpen);
    };

    navToggle?.addEventListener('click', () => {
        setNavigationOpen(navToggle.getAttribute('aria-expanded') !== 'true');
    });

    navPanel?.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', () => setNavigationOpen(false));
    });

    const updateShellMetadata = (nextDocument) => {
        document.title = nextDocument.title;
        const currentDescription = document.querySelector(
            'meta[name="description"]'
        );
        const nextDescription = nextDocument.querySelector(
            'meta[name="description"]'
        );
        if (currentDescription && nextDescription) {
            currentDescription.content = nextDescription.content;
        }

        const nextLinks = new Map(
            Array.from(nextDocument.querySelectorAll(
                '#site-nav a, .nav-search-link'
            )).map((link) => [link.getAttribute('href'), link])
        );
        document.querySelectorAll('#site-nav a, .nav-search-link').forEach(
            (link) => {
                const nextLink = nextLinks.get(link.getAttribute('href'));
                link.classList.toggle(
                    'active',
                    Boolean(nextLink?.classList.contains('active'))
                );
                if (nextLink?.hasAttribute('aria-current')) {
                    link.setAttribute(
                        'aria-current',
                        nextLink.getAttribute('aria-current')
                    );
                } else {
                    link.removeAttribute('aria-current');
                }
            }
        );
    };

    const pageReady = () => {
        document.dispatchEvent(new CustomEvent('music-hub:page-load'));
    };

    const navigate = async (
        destination,
        {pushHistory = true, focusMain = true} = {}
    ) => {
        const url = new URL(destination, window.location.href);
        if (activeNavigation) activeNavigation.abort();
        const navigationController = new AbortController();
        activeNavigation = navigationController;

        const currentMain = document.getElementById('main-content');
        currentMain?.setAttribute('aria-busy', 'true');
        document.body.classList.add('is-page-loading');

        try {
            const response = await fetch(url, {
                credentials: 'same-origin',
                headers: {'X-Music-Hub-Navigation': '1'},
                signal: navigationController.signal,
            });
            const contentType = response.headers.get('content-type') || '';
            if (!response.ok || !contentType.includes('text/html')) {
                throw new Error(`Navigation failed with ${response.status}`);
            }

            const html = await response.text();
            const nextDocument = new DOMParser().parseFromString(
                html,
                'text/html'
            );
            const nextMain = nextDocument.getElementById('main-content');
            if (!nextMain) throw new Error('Response did not include main content');

            currentMain?.replaceWith(nextMain);
            updateShellMetadata(nextDocument);
            setNavigationOpen(false);

            if (pushHistory) {
                window.history.pushState(
                    {musicHubShell: true},
                    '',
                    response.url
                );
            }

            if (focusMain) {
                window.scrollTo({top: 0, behavior: 'auto'});
                nextMain.focus({preventScroll: true});
            }
            pageReady();
        } catch (error) {
            if (error.name === 'AbortError') return;
            window.location.assign(url.href);
        } finally {
            if (activeNavigation === navigationController) {
                document.body.classList.remove('is-page-loading');
                document.getElementById('main-content')?.removeAttribute(
                    'aria-busy'
                );
                activeNavigation = null;
            }
        }
    };

    const isShellNavigation = (link, event) => {
        if (
            event.defaultPrevented
            || event.button !== 0
            || event.metaKey
            || event.ctrlKey
            || event.shiftKey
            || event.altKey
            || link.hasAttribute('download')
            || (link.target && link.target !== '_self')
        ) {
            return false;
        }

        const url = new URL(link.href, window.location.href);
        if (url.origin !== window.location.origin) return false;
        if (url.pathname.startsWith('/static/') || url.pathname.startsWith('/hls/')) {
            return false;
        }
        if (
            url.pathname === window.location.pathname
            && url.search === window.location.search
            && url.hash
        ) {
            return false;
        }
        return true;
    };

    document.addEventListener('click', (event) => {
        const link = event.target.closest('a[href]');
        if (!link || !isShellNavigation(link, event)) return;
        event.preventDefault();
        navigate(link.href);
    });

    document.addEventListener('submit', (event) => {
        const form = event.target;
        if (
            !(form instanceof HTMLFormElement)
            || form.method.toUpperCase() !== 'GET'
        ) {
            return;
        }
        const action = new URL(form.action, window.location.href);
        if (action.origin !== window.location.origin) return;

        event.preventDefault();
        const values = new FormData(form);
        action.search = '';
        values.forEach((value, key) => {
            if (String(value).trim()) action.searchParams.append(key, value);
        });
        navigate(action.href);
    });

    window.addEventListener('popstate', () => {
        navigate(window.location.href, {
            pushHistory: false,
            focusMain: false,
        });
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') setNavigationOpen(false);
    });

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', pageReady, {once: true});
    } else {
        pageReady();
    }
})();
