// ==================== Weather Module (demo-mode pattern) ====================
// Set WEATHER_CONFIG.apiKey to switch from demo data to live OpenWeather calls.
// No code changes needed elsewhere when a real key is added.
// The real key is injected by the GitHub Actions deploy workflow (see
// .github/workflows/pages.yml) from the OPENWEATHER_API_KEY repo secret, so it
// never appears in source control. Locally, this placeholder is left as-is and
// the app runs in demo mode.
const WEATHER_CONFIG = {
    apiKey: '__OPENWEATHER_API_KEY__',
    demoMode: false,
};

// OpenWeather's q= param doesn't resolve Korean city names, so cities are looked
// up by lat/lon instead. A handful of demo cities are hardcoded below; every
// other destination's coordinates come from destinations-data.js's
// DESTINATIONS_FULL (already has lat/lng per city), so live lookups work across
// the whole destination catalog, not just these six.
const CITY_COORDS = {
    '서울': [37.5665, 126.9780], '부산': [35.1796, 129.0756], '제주도': [33.4996, 126.5312],
    '도쿄': [35.6762, 139.6503], '방콕': [13.7563, 100.5018], '파리': [48.8566, 2.3522],
};

function lookupCityCoords(city) {
    if (CITY_COORDS[city]) return CITY_COORDS[city];
    if (typeof DESTINATIONS_FULL !== 'undefined') {
        const match = DESTINATIONS_FULL.find(d => d.baseCity === city || d.name === city);
        if (match) return [match.lat, match.lng];
    }
    return null;
}

// Maps OpenWeather's icon codes (e.g. "10d") to an emoji by their 2-digit condition prefix.
const WEATHER_ICON_MAP = {
    '01': '☀️', '02': '🌤️', '03': '⛅', '04': '☁️',
    '09': '🌦️', '10': '🌧️', '11': '⛈️', '13': '❄️', '50': '🌫️',
};
function weatherIconEmoji(code) {
    return WEATHER_ICON_MAP[(code || '').slice(0, 2)] || '🌤️';
}

async function getWeather(city) {
    // Checked via startsWith rather than an exact-match placeholder string:
    // the deploy workflow's sed does a literal find/replace across the whole
    // file, so a second copy of the exact placeholder text here would also
    // get substituted with the real key, turning this into an always-true
    // "key === itself" check that silently disables live weather forever.
    if (WEATHER_CONFIG.demoMode || !WEATHER_CONFIG.apiKey || WEATHER_CONFIG.apiKey.startsWith('__')) {
        return { unavailable: true };
    }
    try {
        const coords = lookupCityCoords(city);
        const query = coords
            ? `lat=${coords[0]}&lon=${coords[1]}`
            : `q=${encodeURIComponent(city)}`;
        const [currentRes, forecastRes] = await Promise.all([
            fetch(`https://api.openweathermap.org/data/2.5/weather?${query}&appid=${WEATHER_CONFIG.apiKey}&units=metric&lang=kr`),
            fetch(`https://api.openweathermap.org/data/2.5/forecast?${query}&appid=${WEATHER_CONFIG.apiKey}&units=metric&lang=kr`),
        ]);
        if (!currentRes.ok) throw new Error('weather api request failed');
        const data = await currentRes.json();
        // The 5-day/3-hour forecast endpoint doubles as our short-term "hourly"
        // view and is the only free source of rain probability (pop). If it
        // fails, rainChance stays unknown (null) rather than a fake 0/no-rain.
        const forecast = forecastRes.ok ? await forecastRes.json() : null;
        const upcoming = forecast ? forecast.list.slice(0, 4) : [];
        return {
            temp: Math.round(data.main.temp),
            condition: data.weather[0].description,
            icon: weatherIconEmoji(data.weather[0].icon),
            rainChance: upcoming.length ? Math.round(Math.max(...upcoming.map(f => f.pop || 0)) * 100) : null,
            hourly: upcoming.map(f => ({
                time: f.dt_txt.slice(11, 16),
                temp: Math.round(f.main.temp),
                icon: weatherIconEmoji(f.weather[0].icon),
            })),
        };
    } catch (e) {
        return { unavailable: true };
    }
}

// No free/confirmed-working OpenWeather endpoint currently supplies UV index
// (the old uvi endpoint is deprecated), so tips are based only on data we
// actually have — no fabricated UV warning.
function getWeatherTips(weather) {
    const tips = [];
    if (weather.rainChance > 60) tips.push('☔ 강수 확률이 높아요. 실내 위주 일정을 추천해요.');
    if (weather.temp > 30) tips.push('🏊 무더운 날씨예요. 물놀이 명소가 좋아요.');
    if (!tips.length) tips.push('🙂 야외 활동하기 좋은 날씨예요.');
    return tips;
}

function renderWeatherWidget(containerId, city) {
    const el = document.getElementById(containerId);
    if (!el) return;
    getWeather(city).then(weather => {
        if (weather.unavailable) {
            el.innerHTML = `
                <div class="card" style="padding:24px;">
                    <p class="text-muted" style="margin:0;">🌤️ ${city}의 실시간 날씨 정보를 아직 준비하지 못했어요.</p>
                </div>
            `;
            return;
        }
        const tips = getWeatherTips(weather);
        el.innerHTML = `
            <div class="card" style="padding:24px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:20px;">
                <div class="flex gap-16" style="align-items:center;">
                    <div style="font-size:48px;">${weather.icon}</div>
                    <div>
                        <div style="font-size:26px; font-weight:700;">${weather.temp}°C</div>
                        <div class="text-muted">${city} · ${weather.condition}</div>
                    </div>
                </div>
                <div class="flex gap-16">
                    ${weather.hourly.map(h => `
                        <div class="text-center">
                            <div style="font-size:12px; color:var(--color-gray-500);">${h.time}</div>
                            <div style="font-size:20px;">${h.icon}</div>
                            <div style="font-size:13px; font-weight:600;">${h.temp}°</div>
                        </div>
                    `).join('')}
                </div>
                <div style="min-width:220px;">
                    ${tips.map(t => `<div style="font-size:13px; margin-bottom:4px;">${t}</div>`).join('')}
                </div>
            </div>
        `;
    });
}
