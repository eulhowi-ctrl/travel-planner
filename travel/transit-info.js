// ==================== Transit Navigation Link ====================
// Real bus/subway/taxi time+fare would need ODsay (transit routing) and
// Kakao Mobility (driving distance, for a taxi-fare estimate) — both are
// REST APIs that require a server-side call (Authorization header, no CORS)
// AND, in ODsay's case, a fixed outbound IP registered with the app, which
// this static GitHub Pages site has no way to provide without standing up a
// dedicated backend. Decided against building that for now, so this just
// links out to real navigation instead of showing invented numbers.

// Real Kakao Map route-planner deep link (no API key needed, plain URL
// scheme — verified against a live route: opens with origin/destination
// pre-filled and 자동차/대중교통/도보 mode tabs the user can switch between
// for live turn-by-turn navigation, including public transit).
function kakaoRouteUrl(origin, dest) {
    const enc = s => encodeURIComponent(s);
    return `https://map.kakao.com/link/from/${enc(origin.name)},${origin.lat},${origin.lng}/to/${enc(dest.name)},${dest.lat},${dest.lng}`;
}
