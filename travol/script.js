// ==================== TRAVOL Shared Utilities ====================
// Loaded on every page. Provides header/footer rendering (single source of
// truth so all 11 pages share identical nav), toast, and LocalStorage helpers.

const NAV_LINKS = [
    { page: 'home', label: '홈', href: 'index.html' },
    { page: 'search', label: '검색', href: 'search.html' },
    { page: 'wishlist', label: '위시리스트', href: 'wishlist.html' },
    { page: 'community', label: '커뮤니티', href: 'community.html' },
    { page: 'chatbot', label: 'AI 챗봇', href: 'chatbot.html' },
    { page: 'packages', label: '패키지', href: 'packages.html' },
    { page: 'budget', label: '예산관리', href: 'budget.html' },
    { page: 'rewards', label: '포인트', href: 'rewards.html' },
];

// ==================== LocalStorage Helpers ====================
function getLS(key, fallback) {
    try {
        const raw = localStorage.getItem(key);
        if (raw === null) return fallback;
        return JSON.parse(raw);
    } catch (e) {
        return fallback;
    }
}

function setLS(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}

// Escape user-entered text before interpolating into innerHTML templates.
function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str ?? '';
    return div.innerHTML;
}

function getTravolPoints() {
    return getLS('travolPoints', { balance: 0, history: [] });
}

function earnPoints(desc, points) {
    const data = getTravolPoints();
    data.balance += points;
    data.history.unshift({ desc, points, date: new Date().toISOString() });
    setLS('travolPoints', data);
    return data;
}

// ==================== Toast ====================
function showToast(message, type = 'default', duration = 2600) {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = `toast${type !== 'default' ? ' toast-' + type : ''}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), duration);
}

// ==================== Header / Footer ====================
function renderHeader(activePage) {
    const root = document.getElementById('header-root');
    if (!root) return;

    const points = getTravolPoints();

    const navHtml = NAV_LINKS.map(link =>
        `<a href="${link.href}" class="${link.page === activePage ? 'active' : ''}">${link.label}</a>`
    ).join('');

    root.innerHTML = `
        <header class="site-header">
            <div class="container">
                <a href="index.html" class="brand">TRA<span>VOL</span></a>
                <nav class="main-nav">${navHtml}</nav>
                <div class="header-actions">
                    <a href="rewards.html" class="points-pill">✨ ${points.balance.toLocaleString()}P</a>
                    <button class="btn btn-primary btn-small nav-toggle" id="navToggleBtn">☰</button>
                </div>
            </div>
        </header>
    `;

    const toggleBtn = document.getElementById('navToggleBtn');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            const nav = root.querySelector('.main-nav');
            nav.style.display = nav.style.display === 'flex' ? 'none' : 'flex';
            if (nav.style.display === 'flex') {
                nav.style.cssText += 'position:absolute;top:var(--header-height);left:0;right:0;background:#fff;flex-direction:column;padding:12px;box-shadow:var(--shadow-md);';
            }
        });
    }
}

function renderFooter() {
    const root = document.getElementById('footer-root');
    if (!root) return;

    root.innerHTML = `
        <footer class="site-footer">
            <div class="container">
                <div class="footer-grid">
                    <div>
                        <h4>TRAVOL</h4>
                        <p style="font-size:13px;">AI 개인화 여행 계획 + 커뮤니티</p>
                    </div>
                    <div>
                        <h4>둘러보기</h4>
                        <a href="search.html">여행지 검색</a>
                        <a href="wishlist.html">위시리스트</a>
                        <a href="packages.html">패키지</a>
                    </div>
                    <div>
                        <h4>커뮤니티</h4>
                        <a href="community.html">Q&A / 여행기</a>
                        <a href="chatbot.html">AI 챗봇</a>
                    </div>
                    <div>
                        <h4>여행 카페</h4>
                        <a href="https://cafe.naver.com/firstlove" target="_blank" rel="noopener">네이버 여행 카페 모음</a>
                    </div>
                </div>
                <div class="footer-bottom">© 2026 TRAVOL. All rights reserved.</div>
            </div>
        </footer>
    `;
}

// ==================== Init ====================
document.addEventListener('DOMContentLoaded', () => {
    const activePage = document.body.dataset.page || '';
    renderHeader(activePage);
    renderFooter();
});
