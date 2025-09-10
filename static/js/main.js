(function () {
    const htmlEl = document.documentElement;
    const themeToggle = document.getElementById('themeToggle');
    const mobileBtn = document.getElementById('mobileMenuBtn');
    const mobilePanel = document.getElementById('mobileMenuPanel');
    const mobileOverlay = document.getElementById('mobileOverlay');
    const mobileCloseBtn = document.getElementById('mobileCloseBtn');
    const iconMenu = document.getElementById('iconMenu');
    const iconClose = document.getElementById('iconClose');
    const canvas = document.getElementById('bg-canvas');

    // Theme persistence
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        htmlEl.classList.add('dark');
    } else {
        htmlEl.classList.remove('dark');
    }
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            htmlEl.classList.toggle('dark');
            localStorage.setItem('theme', htmlEl.classList.contains('dark') ? 'dark' : 'light');
        });
    }

    if (mobileBtn && mobilePanel && mobileOverlay) {
        const themeToggleMobile = document.getElementById('themeToggleMobile');
        const openPanel = () => {
            mobilePanel.classList.remove('translate-x-full');
            mobileOverlay.classList.remove('pointer-events-none');
            mobileOverlay.classList.add('opacity-100');
            document.body.style.overflow = 'hidden';
            mobileBtn.setAttribute('aria-expanded', 'true');
            if (iconMenu && iconClose) { iconMenu.classList.add('hidden'); iconClose.classList.remove('hidden'); }
        };
        const closePanel = () => {
            mobilePanel.classList.add('translate-x-full');
            mobileOverlay.classList.add('pointer-events-none');
            mobileOverlay.classList.remove('opacity-100');
            document.body.style.overflow = '';
            mobileBtn.setAttribute('aria-expanded', 'false');
            if (iconMenu && iconClose) { iconMenu.classList.remove('hidden'); iconClose.classList.add('hidden'); }
        };
        mobileBtn.addEventListener('click', () => {
            const expanded = mobileBtn.getAttribute('aria-expanded') === 'true';
            expanded ? closePanel() : openPanel();
        });
        if (mobileCloseBtn) mobileCloseBtn.addEventListener('click', closePanel);
        mobileOverlay.addEventListener('click', closePanel);
        document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closePanel(); });
        if (themeToggleMobile) {
            themeToggleMobile.addEventListener('click', () => {
                htmlEl.classList.toggle('dark');
                localStorage.setItem('theme', htmlEl.classList.contains('dark') ? 'dark' : 'light');
            });
        }
    }

    // Animated background - flowing neon blobs
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let width, height, dpr;
        const blobs = [];
        // Blob count adapts to screen size for mobile performance
        let NUM_BLOBS = 24;

        function resize() {
            width = window.innerWidth;
            height = window.innerHeight;
            dpr = window.devicePixelRatio || 1;
            canvas.style.width = width + 'px';
            canvas.style.height = height + 'px';
            canvas.width = Math.floor(width * dpr);
            canvas.height = Math.floor(height * dpr);
            ctx.setTransform(1, 0, 0, 1, 0, 0);
            ctx.scale(dpr, dpr);
        }

        function rand(min, max) { return Math.random() * (max - min) + min; }

        function initBlobs() {
            blobs.length = 0;
            const count = Math.max(10, Math.round(Math.min(width, height) / 60));
            NUM_BLOBS = count;
            for (let i = 0; i < NUM_BLOBS; i++) {
                blobs.push({
                    x: rand(0, width),
                    y: rand(0, height),
                    r: rand(40, 140),
                    dx: rand(-0.6, 0.6),
                    dy: rand(-0.6, 0.6),
                    c1: `hsl(${rand(250, 290)}, 80%, 60%)`,
                    c2: `hsl(${rand(300, 330)}, 80%, 60%)`
                });
            }
        }

        function draw() {
            ctx.clearRect(0, 0, width, height);
            for (const b of blobs) {
                const grd = ctx.createRadialGradient(b.x, b.y, 0, b.x, b.y, b.r);
                grd.addColorStop(0, b.c1);
                grd.addColorStop(1, 'transparent');
                ctx.globalCompositeOperation = 'lighter';
                ctx.fillStyle = grd;
                ctx.beginPath();
                ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
                ctx.fill();

                b.x += b.dx; b.y += b.dy;
                if (b.x < -b.r) b.x = width + b.r;
                if (b.x > width + b.r) b.x = -b.r;
                if (b.y < -b.r) b.y = height + b.r;
                if (b.y > height + b.r) b.y = -b.r;
            }
            requestAnimationFrame(draw);
        }

        window.addEventListener('resize', () => { resize(); initBlobs(); });
        resize();
        initBlobs();
        requestAnimationFrame(draw);
    }
})(); 