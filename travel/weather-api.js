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

const DEMO_WEATHER = {
    '서울': { temp: 27, condition: '맑음', icon: '☀️', rainChance: 10, uvIndex: 6, hourly: [
        { time: '09:00', temp: 24, icon: '☀️' }, { time: '12:00', temp: 28, icon: '☀️' },
        { time: '15:00', temp: 29, icon: '🌤️' }, { time: '18:00', temp: 25, icon: '🌥️' },
    ]},
    '부산': { temp: 29, condition: '구름 조금', icon: '🌤️', rainChance: 20, uvIndex: 8, hourly: [
        { time: '09:00', temp: 26, icon: '🌤️' }, { time: '12:00', temp: 30, icon: '☀️' },
        { time: '15:00', temp: 31, icon: '☀️' }, { time: '18:00', temp: 27, icon: '🌤️' },
    ]},
    '제주도': { temp: 26, condition: '흐림', icon: '☁️', rainChance: 65, uvIndex: 4, hourly: [
        { time: '09:00', temp: 24, icon: '☁️' }, { time: '12:00', temp: 26, icon: '🌧️' },
        { time: '15:00', temp: 25, icon: '🌧️' }, { time: '18:00', temp: 23, icon: '☁️' },
    ]},
    '도쿄': { temp: 30, condition: '맑음', icon: '☀️', rainChance: 5, uvIndex: 9, hourly: [
        { time: '09:00', temp: 27, icon: '☀️' }, { time: '12:00', temp: 31, icon: '☀️' },
        { time: '15:00', temp: 32, icon: '☀️' }, { time: '18:00', temp: 28, icon: '🌤️' },
    ]},
    '방콕': { temp: 34, condition: '한낮 소나기', icon: '⛈️', rainChance: 70, uvIndex: 10, hourly: [
        { time: '09:00', temp: 31, icon: '🌤️' }, { time: '12:00', temp: 35, icon: '⛈️' },
        { time: '15:00', temp: 33, icon: '⛈️' }, { time: '18:00', temp: 29, icon: '🌦️' },
    ]},
    '파리': { temp: 22, condition: '맑음', icon: '🌤️', rainChance: 15, uvIndex: 5, hourly: [
        { time: '09:00', temp: 18, icon: '🌤️' }, { time: '12:00', temp: 23, icon: '☀️' },
        { time: '15:00', temp: 24, icon: '☀️' }, { time: '18:00', temp: 20, icon: '🌤️' },
    ]},
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

async function getWeather(city) {
    if (WEATHER_CONFIG.demoMode || !WEATHER_CONFIG.apiKey || WEATHER_CONFIG.apiKey === '__OPENWEATHER_API_KEY__') {
        return DEMO_WEATHER[city] || { unavailable: true };
    }
    try {
        const coords = lookupCityCoords(city);
        const url = coords
            ? `https://api.openweathermap.org/data/2.5/weather?lat=${coords[0]}&lon=${coords[1]}&appid=${WEATHER_CONFIG.apiKey}&units=metric&lang=kr`
            : `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&appid=${WEATHER_CONFIG.apiKey}&units=metric&lang=kr`;
        const res = await fetch(url);
        if (!res.ok) throw new Error('weather api request failed');
        const data = await res.json();
        return {
            temp: Math.round(data.main.temp),
            condition: data.weather[0].description,
            icon: '🌤️',
            rainChance: 0,
            uvIndex: 0,
            hourly: [],
        };
    } catch (e) {
        return DEMO_WEATHER[city] || { unavailable: true };
    }
}

function getWeatherTips(weather) {
    const tips = [];
    if (weather.rainChance > 60) tips.push('☔ 강수 확률이 높아요. 실내 위주 일정을 추천해요.');
    if (weather.temp > 30) tips.push('🏊 무더운 날씨예요. 물놀이 명소가 좋아요.');
    if (weather.uvIndex > 7) tips.push('🧴 자외선이 강해요. 선크림을 꼭 발라주세요.');
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
