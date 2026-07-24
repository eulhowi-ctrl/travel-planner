// ==================== TRAVEL Shared Utilities ====================
// Loaded on every page. Provides header/footer rendering (single source of
// truth so all 11 pages share identical nav), toast, and LocalStorage helpers.

const NAV_LINKS = [
    { page: 'home', label: '홈', href: 'index.html' },
    { page: 'search', label: '검색', href: 'search.html' },
    { page: 'wishlist', label: '위시리스트', href: 'wishlist.html' },
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

function getTravelPoints() {
    return getLS('travelPoints', { balance: 0, history: [] });
}

function earnPoints(desc, points) {
    const data = getTravelPoints();
    data.balance += points;
    data.history.unshift({ desc, points, date: new Date().toISOString() });
    setLS('travelPoints', data);
    refreshHeaderPoints();
    return data;
}

// Call after any direct setLS('travelPoints', ...) write (e.g. redemptions)
// that doesn't go through earnPoints, so the header pill stays in sync.
function refreshHeaderPoints() {
    const pill = document.getElementById('headerPointsPill');
    if (pill) pill.textContent = `✨ ${getTravelPoints().balance.toLocaleString()}P`;
}

// ==================== Placeholder Photos ====================
// Real (non-emoji) stock placeholder photos, seeded so the same item always
// gets the same image. Swap for licensed destination photography later.
function photoUrl(seed, w = 400, h = 300) {
    return `https://picsum.photos/seed/${encodeURIComponent(seed)}/${w}/${h}`;
}

// ==================== External Price Check (deep-link, no API) ====================
// We don't have a live flight/hotel pricing API, so these hand off to Naver's
// general search — its own flight/hotel comparison widgets surface from there,
// and unlike a hand-built flight.naver.com URL, this endpoint won't break when
// Naver changes their booking-flow URL scheme.
function naverFlightSearchUrl(cityName) {
    return `https://search.naver.com/search.naver?query=${encodeURIComponent(cityName + ' 항공권')}`;
}

// ==================== Flight Deep Link (real flight.naver.com results) ====================
// Trip dates for the flight link default to "2 weeks out, 3 nights" unless the
// user set real ones on the itinerary page (stored under 'tripDates').
// Naver's own site is blocked for automated browsing (see project notes), so
// this URL shape is unverified against a live response — it matches the one
// real flight.naver.com URL a manual browse turned up, reused for every
// destination via a per-city IATA code (AIRPORT_CODES in destinations-data.js).
function getTripDates() {
    const saved = getLS('tripDates', null);
    if (saved && saved.start && saved.end) return saved;
    const start = new Date();
    start.setDate(start.getDate() + 14);
    const end = new Date(start);
    end.setDate(end.getDate() + 3);
    const fmt = d => d.toISOString().slice(0, 10);
    return { start: fmt(start), end: fmt(end) };
}

function setTripDates(start, end) {
    setLS('tripDates', { start, end });
}

const NAVER_FLIGHT_ORIGIN = 'ICN';

// Falls back to the general search link when the destination has no airport
// code (small towns with no commercial airport) rather than building a
// broken URL for it.
function naverFlightDeepLink(cityName) {
    const destCode = typeof AIRPORT_CODES !== 'undefined' ? AIRPORT_CODES[cityName] : null;
    if (!destCode || destCode === NAVER_FLIGHT_ORIGIN) return naverFlightSearchUrl(cityName);
    const { start, end } = getTripDates();
    const noDash = s => s.replace(/-/g, '');
    return `https://flight.naver.com/flights/international/${NAVER_FLIGHT_ORIGIN}:airport-${destCode}:airport-${noDash(start)}/${destCode}:airport-${NAVER_FLIGHT_ORIGIN}:airport-${noDash(end)}?adult=1&fareType=Y`;
}

// Korean destinations get a real hotels.naver.com deep link straight into the
// domestic accommodation search results (verified working). Overseas cities
// fall back to general search — the overseas path/param shape on
// hotels.naver.com is unverified (naver.com is blocked for automated
// browsing, see project notes), so we don't guess at it.
function naverHotelSearchUrl(cityName, isKorea) {
    if (isKorea) {
        return `https://hotels.naver.com/accommodation/search/${encodeURIComponent(cityName + ' 호텔')}/domestic?sort=POPULAR_DESC&openTarget=checkIn&accommodationTypes=HOTEL%2CRESORT%2CRESIDENCE&adultCnt=2`;
    }
    return `https://search.naver.com/search.naver?query=${encodeURIComponent(cityName + ' 호텔')}`;
}

// Naver blocks automated scraping of cafe/blog reviews (see project notes), so
// we can't pull real review snippets in. This just hands off to a search for
// the actual reviews instead of faking review content.
function naverReviewSearchUrl(query) {
    return `https://search.naver.com/search.naver?query=${encodeURIComponent(query + ' 후기')}`;
}

// Naver Map's POI database only reliably covers Korean businesses — searching
// it for an overseas place (a Rio restaurant, a Paris museum) just falls
// through to Naver's generic web search instead of an actual map pin. Google
// Maps has real worldwide POI coverage, so overseas destinations use this
// deep link instead (see mapSearchUrl in itinerary.html, which picks between
// the two based on country).
function googleMapsSearchUrl(query) {
    return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(query)}`;
}

// Shared by itinerary.html and search.html: Naver Map search only resolves
// real POIs inside Korea, so overseas destinations get the Google Maps link.
function mapSearchUrl(query, country) {
    return country === '대한민국'
        ? `https://map.naver.com/p/search/${encodeURIComponent(query)}`
        : googleMapsSearchUrl(query);
}

// Google search deep link for reviews — the Google-based equivalent of
// naverReviewSearchUrl, used for destinations where Naver's Korean-blogger-
// centric review corpus is less useful (see project notes on overseas coverage).
function googleReviewSearchUrl(query) {
    return `https://www.google.com/search?q=${encodeURIComponent(query + ' 후기')}`;
}

// map.naver.com/p/search needs an exact POI business name match (e.g. Seoul has
// no single business literally named "서울 시외버스터미널" — it's split across
// 서울고속버스터미널/센트럴시티/남부터미널). For destinations where we've verified
// the real terminal name (and, importantly, which one — several of these cities
// have two separate terminals in different locations for 고속버스 vs 시외버스, and
// the Seoul-departing route only serves one of them), we use it for a direct
// map.naver.com POI link. Anything else falls back to search.naver.com's fuzzy
// general search, same as the other deep links above.
const BUS_TERMINAL_NAMES = {
    '부산': '부산종합버스터미널',
    '강릉': '강릉고속버스터미널', // not 강릉시외버스터미널 — separate building, Seoul route goes here
    '여수': '여수종합버스터미널',
    '경주': '경주고속버스터미널', // not 경주시외버스터미널 — different operator/location, that one serves 포항·울산·대구
    '속초': '속초고속버스터미널', // not 속초시외버스터미널 — separate, unintegrated terminal
    '전주': '전주고속버스터미널', // not 전주시외버스공용터미널 — adjacent but separate
    '통영': '통영종합버스터미널',
};

function naverBusTerminalSearchUrl(cityName) {
    const exactName = BUS_TERMINAL_NAMES[cityName];
    if (exactName) {
        return `https://map.naver.com/p/search/${encodeURIComponent(exactName)}`;
    }
    return `https://search.naver.com/search.naver?query=${encodeURIComponent(cityName + ' 시외버스터미널')}`;
}

// Naver Map directions need internal per-POI IDs we have no way to look up
// (naver.com blocks scraping, see project notes), so real turn-by-turn
// directions there are a dead end. Google's Directions URL API takes plain
// place-name text for origin/destination and geocodes it itself — no ID
// lookup needed — so this is the one place we can offer an actual route
// instead of just a map search. Only destinations with a verified exact
// terminal name (BUS_TERMINAL_NAMES) get this button.
const SEOUL_TERMINAL_NAME = '서울고속버스터미널';

function terminalDirectionsUrl(cityName) {
    const exactName = BUS_TERMINAL_NAMES[cityName];
    if (!exactName) return null;
    const params = new URLSearchParams({
        api: '1',
        origin: SEOUL_TERMINAL_NAME,
        destination: exactName,
        travelmode: 'driving',
    });
    return `https://www.google.com/maps/dir/?${params.toString()}`;
}

// Korail's own site doesn't reflect search params (station/date) in the URL —
// it's session-based — so there's no way to deep-link a filled-in result.
// This just hands off to their generic ticket search entry point.
const KORAIL_SEARCH_URL = 'https://www.korail.com/ticket/search/list';

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

    const points = getTravelPoints();

    const navHtml = NAV_LINKS.map(link =>
        `<a href="${link.href}" class="${link.page === activePage ? 'active' : ''}">${link.label}</a>`
    ).join('');

    root.innerHTML = `
        <header class="site-header">
            <div class="container">
                <a href="index.html" class="brand">TRA<span>VEL</span></a>
                <nav class="main-nav">${navHtml}</nav>
                <div class="header-actions">
                    <a href="rewards.html" class="points-pill" id="headerPointsPill">✨ ${points.balance.toLocaleString()}P</a>
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
                        <h4>TRAVEL</h4>
                        <p style="font-size:13px;">AI 개인화 여행 계획</p>
                    </div>
                    <div>
                        <h4>둘러보기</h4>
                        <a href="search.html">여행지 검색</a>
                        <a href="wishlist.html">위시리스트</a>
                        <a href="packages.html">패키지</a>
                        <a href="chatbot.html">AI 챗봇</a>
                    </div>
                    <div>
                        <h4>여행 카페</h4>
                        <a href="https://cafe.naver.com/firstlove" target="_blank" rel="noopener">네이버 여행 카페 모음</a>
                    </div>
                </div>
                <div class="footer-bottom">© 2026 TRAVEL. All rights reserved.</div>
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
