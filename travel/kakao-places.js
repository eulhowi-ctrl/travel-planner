// ==================== Kakao Local Places (live search, demo-mode pattern) ====================
// Mirrors weather-api.js: set KAKAO_CONFIG.jsKey to switch itinerary items
// with a `liveQuery` from their hand-written venue to a live Kakao Local
// keyword search, so the recommendation stays current instead of being
// frozen at whatever was true when the itinerary was written.
// The real key is injected by the GitHub Actions deploy workflow (see
// .github/workflows/pages.yml) from the KAKAO_JS_KEY repo secret, so it
// never appears in source control. Locally, this placeholder is left as-is
// and callers get null (fall back to the hand-written venue).
//
// This uses the Kakao Maps JS SDK's Places service (loaded as a <script>
// tag), not a raw fetch() to Kakao's REST API — the REST API requires an
// Authorization header and doesn't allow direct browser calls (CORS), which
// would need a backend proxy this static site doesn't have. The JS SDK path
// works CORS-free with a domain-restricted JavaScript key registered in the
// Kakao Developers console.
const KAKAO_CONFIG = {
    jsKey: '__KAKAO_JS_KEY__',
};

function isKakaoConfigured() {
    return !!KAKAO_CONFIG.jsKey && !KAKAO_CONFIG.jsKey.startsWith('__');
}

let kakaoSdkLoadPromise = null;

function loadKakaoSdk() {
    if (!isKakaoConfigured()) return Promise.resolve(false);
    if (kakaoSdkLoadPromise) return kakaoSdkLoadPromise;
    kakaoSdkLoadPromise = new Promise(resolve => {
        const script = document.createElement('script');
        script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_CONFIG.jsKey}&libraries=services&autoload=false`;
        script.onload = () => window.kakao.maps.load(() => resolve(true));
        script.onerror = () => resolve(false);
        document.head.appendChild(script);
    });
    return kakaoSdkLoadPromise;
}

// Returns the single highest-relevance live result for a keyword search, or
// null if Kakao isn't configured, the SDK fails to load, or nothing matches.
// Kakao's keyword search sorts by accuracy (관련도) by default, so results[0]
// out of the requested top-3 is the "most accurate of the top matches" pick.
async function kakaoTopPlace(query) {
    const ready = await loadKakaoSdk();
    if (!ready) return null;
    return new Promise(resolve => {
        try {
            const places = new kakao.maps.services.Places();
            places.keywordSearch(query, (results, status) => {
                if (status !== kakao.maps.services.Status.OK || !results.length) {
                    resolve(null);
                    return;
                }
                const top = results[0];
                resolve({
                    name: top.place_name,
                    address: top.road_address_name || top.address_name,
                    url: top.place_url,
                    lat: Number(top.y),
                    lng: Number(top.x),
                });
            }, { size: 3 });
        } catch (e) {
            resolve(null);
        }
    });
}
