// ==================== QR Code Helper ====================
// Assembles api.qrserver.com URLs client-side. No backend/key needed.
function buildQrUrl(data, size = 180) {
    return `https://api.qrserver.com/v1/create-qr-code/?size=${size}x${size}&data=${encodeURIComponent(data)}`;
}

function buildWifiQrData(ssid, password, encryption = 'WPA') {
    return `WIFI:T:${encryption};S:${ssid};P:${password};;`;
}

function buildContactQrData({ name, phone, email }) {
    return `BEGIN:VCARD\nVERSION:3.0\nN:${name}\nTEL:${phone}\nEMAIL:${email}\nEND:VCARD`;
}
