// ==================== API Configuration ====================
const API_BASE_URL = "/api/v1";
const AUTH_TOKEN_KEY = "travel_planner_token";

// ==================== Modal Functions ====================
// Removed: Login and Register modal functionality

// ==================== Authentication Functions ====================
async function login(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem(AUTH_TOKEN_KEY, data.access_token);
            alert("로그인 성공!");
            closeLoginModal();
            location.reload();
        } else {
            alert("로그인 실패: 이메일 또는 비밀번호를 확인하세요.");
        }
    } catch (error) {
        console.error("Login error:", error);
        alert("로그인 중 오류가 발생했습니다.");
    }
}

async function register(email, username, password, passwordConfirm) {
    if (password !== passwordConfirm) {
        alert("비밀번호가 일치하지 않습니다.");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/users/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, username, password })
        });

        if (response.ok) {
            alert("회원가입 성공! 로그인해주세요.");
            closeRegisterModal();
            showLoginModal();
        } else {
            const data = await response.json();
            alert(`회원가입 실패: ${data.detail || "다시 시도해주세요."}`);
        }
    } catch (error) {
        console.error("Register error:", error);
        alert("회원가입 중 오류가 발생했습니다.");
    }
}

function logout() {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    alert("로그아웃 되었습니다.");
    location.reload();
}

function isAuthenticated() {
    return localStorage.getItem(AUTH_TOKEN_KEY) !== null;
}

function getAuthToken() {
    return localStorage.getItem(AUTH_TOKEN_KEY);
}

// ==================== Form Event Listeners ====================
// Removed: Login and Register form event listeners

// ==================== API Helper Functions ====================
async function fetchAPI(endpoint, options = {}) {
    const headers = {
        "Content-Type": "application/json",
        ...options.headers
    };

    // Add authorization token if available
    const token = getAuthToken();
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers
        });

        if (!response.ok) {
            if (response.status === 401) {
                logout();
                throw new Error("세션이 만료되었습니다. 다시 로그인해주세요.");
            }
            throw new Error(`API error: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error("API error:", error);
        throw error;
    }
}

// ==================== Utility Functions ====================
function showLoading() {
    const loader = document.createElement("div");
    loader.className = "spinner";
    loader.id = "loadingSpinner";
    document.body.appendChild(loader);
}

function hideLoading() {
    const loader = document.getElementById("loadingSpinner");
    if (loader) {
        loader.remove();
    }
}

function showNotification(message, type = "info") {
    const notification = document.createElement("div");
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function formatDate(date) {
    return new Date(date).toLocaleDateString("ko-KR");
}

function formatCurrency(amount, currency = "KRW") {
    if (currency === "KRW") {
        return `₩${amount.toLocaleString("ko-KR")}`;
    }
    return `${amount.toLocaleString("en-US")} ${currency}`;
}

// ==================== QR Code Scanner ====================
function scanQRCode() {
    if (typeof QRCode !== "undefined") {
        alert("QR 코드 스캐너 기능이 아직 구현되지 않았습니다.");
    }
}

// ==================== Page Initialization ====================
document.addEventListener("DOMContentLoaded", () => {
    // Initialize page-specific functions
    initializePage();
});

// Page-specific initialization (override in each page)
function initializePage() {
    // To be overridden in specific pages
}

// ==================== Export for use in other pages ====================
// These functions are available globally for use in other HTML files
window.logout = logout;
window.fetchAPI = fetchAPI;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.showNotification = showNotification;
window.formatDate = formatDate;
window.formatCurrency = formatCurrency;
window.isAuthenticated = isAuthenticated;
