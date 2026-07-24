// ==================== Transit Duration (Google Maps, demo-mode pattern) ====================
// Real bus/subway/taxi numbers ran into two dead ends: ODsay (transit
// routing) enforces a fixed outbound IP this static site can't provide
// without a dedicated backend, and Kakao Mobility (driving, for a taxi
// estimate) is REST-only (no CORS) so it needs one too. Google Maps'
// JavaScript SDK's DirectionsService, by contrast, runs entirely client-side
// (script-tag load, like Kakao's Places SDK) — no backend needed — but
// Google has no driving/taxi directions in Korea at all (regulatory
// restriction, see project notes) and its Korean transit data is weaker
// than Kakao/Naver's (walking-to-station legs are straight lines, not real
// routes). So: bus/subway duration only, no taxi, no fare (Google rarely has
// Korean transit fare data) — everything else falls back to just the real
// Kakao Map route link below, same as before.
const GOOGLE_MAPS_CONFIG = {
    jsKey: '__GOOGLE_MAPS_JS_KEY__',
};

function isGoogleMapsConfigured() {
    return !!GOOGLE_MAPS_CONFIG.jsKey && !GOOGLE_MAPS_CONFIG.jsKey.startsWith('__');
}

let googleMapsSdkLoadPromise = null;

function loadGoogleMapsSdk() {
    if (!isGoogleMapsConfigured()) return Promise.resolve(false);
    if (googleMapsSdkLoadPromise) return googleMapsSdkLoadPromise;
    googleMapsSdkLoadPromise = new Promise(resolve => {
        const script = document.createElement('script');
        script.src = `https://maps.googleapis.com/maps/api/js?key=${GOOGLE_MAPS_CONFIG.jsKey}&loading=async`;
        script.onload = () => resolve(true);
        script.onerror = () => resolve(false);
        document.head.appendChild(script);
    });
    return googleMapsSdkLoadPromise;
}

// origin/dest: {lat, lng}. Returns { minutes } or null (not configured, SDK
// failed to load, or no transit route found — Google's Korea transit
// coverage is patchy outside major cities).
async function fetchTransitDuration(origin, dest) {
    const ready = await loadGoogleMapsSdk();
    if (!ready) return null;
    return new Promise(resolve => {
        try {
            const service = new google.maps.DirectionsService();
            service.route({
                origin: { lat: origin.lat, lng: origin.lng },
                destination: { lat: dest.lat, lng: dest.lng },
                travelMode: google.maps.TravelMode.TRANSIT,
            }, (result, status) => {
                if (status !== google.maps.DirectionsStatus.OK || !result.routes.length) {
                    resolve(null);
                    return;
                }
                const leg = result.routes[0].legs[0];
                resolve({ minutes: Math.round(leg.duration.value / 60) });
            });
        } catch (e) {
            resolve(null);
        }
    });
}

// Real Kakao Map route-planner deep link (no API key needed, plain URL
// scheme — verified against a live route: opens with origin/destination
// pre-filled and 자동차/대중교통/도보 mode tabs the user can switch between
// for live turn-by-turn navigation — including taxi/driving fare, which
// Google can't provide in Korea at all).
function kakaoRouteUrl(origin, dest) {
    const enc = s => encodeURIComponent(s);
    return `https://map.kakao.com/link/from/${enc(origin.name)},${origin.lat},${origin.lng}/to/${enc(dest.name)},${dest.lat},${dest.lng}`;
}
