// ==================== Exchange Rate Module (live-fetch + cache fallback) ====================
// Free, keyless API. On failure/offline, falls back to the last cached rates
// (same fallback pattern as weather-api.js's demo mode).
const EXCHANGE_CONFIG = {
    apiUrl: 'https://open.er-api.com/v6/latest/KRW',
    currencies: ['USD', 'JPY', 'CNY', 'THB', 'EUR'],
};

const STATIC_FALLBACK_RATES = { USD: 0.00072, JPY: 0.11, CNY: 0.0052, THB: 0.026, EUR: 0.00067 };

async function getExchangeRates() {
    try {
        const res = await fetch(EXCHANGE_CONFIG.apiUrl);
        if (!res.ok) throw new Error('exchange rate api request failed');
        const data = await res.json();
        const rates = {};
        EXCHANGE_CONFIG.currencies.forEach(c => { rates[c] = data.rates[c]; });
        const payload = { rates, timestamp: Date.now(), live: true };
        setLS('exchangeRatesCache', payload);
        return payload;
    } catch (e) {
        const cached = getLS('exchangeRatesCache', null);
        if (cached) return { ...cached, live: false };
        return { rates: STATIC_FALLBACK_RATES, timestamp: null, live: false };
    }
}

function convertFromKRW(amountKRW, currency, rates) {
    const rate = rates[currency];
    if (!rate) return null;
    return amountKRW * rate;
}
