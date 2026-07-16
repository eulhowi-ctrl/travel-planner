// ==================== Weather Module (demo-mode pattern) ====================
// Set WEATHER_CONFIG.apiKey to switch from demo data to live OpenWeather calls.
// No code changes needed elsewhere when a real key is added.
const WEATHER_CONFIG = {
    apiKey: '', // OpenWeather API key. Empty = demo mode.
    demoMode: true,
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

async function getWeather(city) {
    if (WEATHER_CONFIG.demoMode || !WEATHER_CONFIG.apiKey) {
        return DEMO_WEATHER[city] || DEMO_WEATHER['서울'];
    }
    try {
        const res = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&appid=${WEATHER_CONFIG.apiKey}&units=metric&lang=kr`);
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
        return DEMO_WEATHER[city] || DEMO_WEATHER['서울'];
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
