// ==================== Transit Navigation Link ====================
// Real bus/subway/taxi time+fare would need either ODsay+Kakao Mobility
// (both REST-only, need a backend this static site doesn't have — ODsay
// also requires a fixed outbound IP) or Google Maps' DirectionsService
// (client-side, no backend, but no driving/taxi directions in Korea at all,
// weaker transit data, and requires a billing-enabled Google Cloud account
// that auto-charges past its free usage — decided against that risk).
// So this just links out to real navigation instead of showing numbers.

// Real Kakao Map route-planner deep link (no API key needed, plain URL
// scheme — verified against a live route: opens with origin/destination
// pre-filled and 자동차/대중교통/도보 mode tabs the user can switch between
// for live turn-by-turn navigation, including public transit).
function kakaoRouteUrl(origin, dest) {
    const enc = s => encodeURIComponent(s);
    return `https://map.kakao.com/link/from/${enc(origin.name)},${origin.lat},${origin.lng}/to/${enc(dest.name)},${dest.lat},${dest.lng}`;
}
