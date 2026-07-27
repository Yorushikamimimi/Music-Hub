(() => {
    const root = document.documentElement;
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = themeToggle?.querySelector('i');
    const navToggle = document.getElementById('mobile-nav-toggle');
    const navPanel = document.getElementById('site-nav');

    const updateThemeControl = (theme) => {
        if (!themeToggle || !themeIcon) return;
        const isDark = theme === 'dark';
        themeIcon.classList.toggle('bi-sun-fill', isDark);
        themeIcon.classList.toggle('bi-moon-stars-fill', !isDark);
        themeToggle.setAttribute('aria-label', isDark ? '切换为浅色主题' : '切换为深色主题');
    };

    const savedTheme = localStorage.getItem('theme');
    const initialTheme = savedTheme === 'light' ? 'light' : 'dark';
    root.setAttribute('data-theme', initialTheme);
    updateThemeControl(initialTheme);

    themeToggle?.addEventListener('click', () => {
        const nextTheme = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
        root.setAttribute('data-theme', nextTheme);
        localStorage.setItem('theme', nextTheme);
        updateThemeControl(nextTheme);
    });

    const setNavigationOpen = (isOpen) => {
        if (!navToggle || !navPanel) return;
        navPanel.classList.toggle('is-open', isOpen);
        navToggle.setAttribute('aria-expanded', String(isOpen));
        navToggle.setAttribute('aria-label', isOpen ? '关闭导航菜单' : '打开导航菜单');
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

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') setNavigationOpen(false);
    });
})();
