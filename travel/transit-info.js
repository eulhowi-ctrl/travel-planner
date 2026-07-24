// ==================== Transit Info (live, demo-mode pattern) ====================
// Mirrors weather-api.js / kakao-places.js: set TRANSIT_CONFIG.proxyUrl to
// switch from "no inter-stop transit segment shown" to live bus/subway/taxi
// numbers, fetched from the Cloudflare Worker proxy (worker/transit-proxy.js)
// that holds the ODsay + Kakao Mobility API keys server-side — this site is
// static (GitHub Pages), so those keyed REST calls can't be made directly
// from the browser (no CORS, need an Authorization header).
// The real URL is injected by the GitHub Actions deploy workflow from the
// TRANSIT_PROXY_URL repo secret, so it never appears in source control.
const TRANSIT_CONFIG = {
    proxyUrl: '__TRANSIT_PROXY_URL__',
};

function isTransitConfigured() {
    return !!TRANSIT_CONFIG.proxyUrl && !TRANSIT_CONFIG.proxyUrl.startsWith('__');
}

// origin/dest: {lat, lng}. Returns null (not { transit:null, taxi:null }) if
// the proxy isn't configured or the request itself fails — the per-mode
// nulls inside a successful response are a different, valid case (e.g. no
// bus/subway route exists) that callers still render partially.
async function fetchTransitInfo(origin, dest) {
    if (!isTransitConfigured() || !origin || !dest) return null;
    try {
        const url = `${TRANSIT_CONFIG.proxyUrl}/transit?originX=${origin.lng}&originY=${origin.lat}&destX=${dest.lng}&destY=${dest.lat}`;
        const res = await fetch(url);
        if (!res.ok) return null;
        return await res.json();
    } catch (e) {
        return null;
    }
}

// Real Kakao Map route-planner deep link (no API key needed, plain URL
// scheme — verified against a live route: opens with origin/destination
// pre-filled and 자동차/대중교통/도보 mode tabs the user can switch between
// for live turn-by-turn navigation, including public transit).
function kakaoRouteUrl(origin, dest) {
    const enc = s => encodeURIComponent(s);
    return `https://map.kakao.com/link/from/${enc(origin.name)},${origin.lat},${origin.lng}/to/${enc(dest.name)},${dest.lat},${dest.lng}`;
}
