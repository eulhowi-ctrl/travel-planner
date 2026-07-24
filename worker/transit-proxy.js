// ==================== Transit Info Proxy (Cloudflare Worker) ====================
// The travel-planner site (GitHub Pages, static) can't call ODsay's public
// transit API or Kakao Mobility's directions API directly from the browser —
// both require a server-side API key in an Authorization/query param, and
// neither sends CORS headers for arbitrary browser origins. This Worker is
// the minimal proxy: it holds both keys as secrets, makes the real calls
// server-side, and returns just the numbers the itinerary page needs.
//
// GET /transit?originX=&originY=&destX=&destY=
//   (X = longitude, Y = latitude, matching ODsay/Kakao's own convention)
// -> { transit: {minutes, fare, transferCount} | null,
//      taxi: {minutes, fare, approximate: true} | null }
//
// Either half can be null independently (e.g. ODsay has no route, or the
// Kakao Mobility call fails) — the frontend renders whichever came back
// rather than failing the whole segment.

function corsHeaders(env) {
    return {
        'Access-Control-Allow-Origin': env.ALLOWED_ORIGIN,
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Vary': 'Origin',
    };
}

async function fetchTransit(env, originX, originY, destX, destY) {
    const url = `https://api.odsay.com/v1/api/searchPubTransPathT?SX=${originX}&SY=${originY}&EX=${destX}&EY=${destY}&apiKey=${encodeURIComponent(env.ODSAY_API_KEY)}`;
    try {
        const res = await fetch(url);
        if (!res.ok) return null;
        const data = await res.json();
        const paths = data && data.result && data.result.path;
        if (!paths || !paths.length) return null;
        // ODsay returns several route options (subway-only, bus-only, mixed);
        // pick the fastest total door-to-door time.
        const best = paths.reduce((a, b) => (a.info.totalTime <= b.info.totalTime ? a : b));
        return {
            minutes: best.info.totalTime,
            fare: best.info.payment,
            transferCount: (best.info.busTransitCount || 0) + (best.info.subwayTransitCount || 0),
        };
    } catch (e) {
        return null;
    }
}

// Korea has no unified taxi fare API open to third parties, so this derives
// an estimate from real driving distance/time (Kakao Mobility) applied to
// Seoul's published base-fare schedule. It's labeled "approximate" end to
// end (worker response and UI both) since actual metered fare varies by
// city/region and isn't something we can call an API for honestly.
const SEOUL_TAXI_BASE_FARE = 4800; // 기본요금 (~1.6km)
const SEOUL_TAXI_BASE_METERS = 1600;
const SEOUL_TAXI_PER_METER = 100 / 131; // 131m당 100원

function estimateTaxiFare(distanceMeters) {
    if (distanceMeters <= SEOUL_TAXI_BASE_METERS) return SEOUL_TAXI_BASE_FARE;
    return Math.round(SEOUL_TAXI_BASE_FARE + (distanceMeters - SEOUL_TAXI_BASE_METERS) * SEOUL_TAXI_PER_METER);
}

async function fetchTaxiEstimate(env, originX, originY, destX, destY) {
    const url = `https://apis-navi.kakaomobility.com/v1/directions?origin=${originX},${originY}&destination=${destX},${destY}`;
    try {
        const res = await fetch(url, { headers: { Authorization: `KakaoAK ${env.KAKAO_REST_API_KEY}` } });
        if (!res.ok) return null;
        const data = await res.json();
        const summary = data && data.routes && data.routes[0] && data.routes[0].summary;
        if (!summary) return null;
        return {
            minutes: Math.round(summary.duration / 60),
            fare: estimateTaxiFare(summary.distance),
            approximate: true,
        };
    } catch (e) {
        return null;
    }
}

export default {
    async fetch(request, env) {
        const headers = corsHeaders(env);
        if (request.method === 'OPTIONS') return new Response(null, { headers });

        const url = new URL(request.url);
        const originX = url.searchParams.get('originX');
        const originY = url.searchParams.get('originY');
        const destX = url.searchParams.get('destX');
        const destY = url.searchParams.get('destY');
        if (!originX || !originY || !destX || !destY) {
            return new Response(JSON.stringify({ error: 'missing coordinates' }), {
                status: 400, headers: { ...headers, 'Content-Type': 'application/json' },
            });
        }

        const [transit, taxi] = await Promise.all([
            fetchTransit(env, originX, originY, destX, destY),
            fetchTaxiEstimate(env, originX, originY, destX, destY),
        ]);

        return new Response(JSON.stringify({ transit, taxi }), {
            headers: { ...headers, 'Content-Type': 'application/json', 'Cache-Control': 'public, max-age=1800' },
        });
    },
};
