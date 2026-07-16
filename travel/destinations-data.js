// ==================== TRAVEL Destination Dataset Generator ====================
// Generates ~8-10 destinations per country from real city coordinates.
// Mirrors the local_setup/generate_destinations.py pattern: seed table -> expand.

const COUNTRY_SEEDS = [
    { country: '대한민국', emoji: '🇰🇷', region: 'asia', cities: [
        ['서울', 37.5665, 126.9780], ['부산', 35.1796, 129.0756], ['제주도', 33.4996, 126.5312],
        ['강릉', 37.7519, 128.8761], ['여수', 34.7604, 127.6622], ['경주', 35.8562, 129.2247],
        ['속초', 38.2070, 128.5918], ['전주', 35.8242, 127.1480], ['통영', 34.8544, 128.4331],
    ]},
    { country: '일본', emoji: '🇯🇵', region: 'asia', cities: [
        ['도쿄', 35.6762, 139.6503], ['오사카', 34.6937, 135.5023], ['교토', 35.0116, 135.7681],
        ['삿포로', 43.0618, 141.3545], ['후쿠오카', 33.5904, 130.4017], ['나고야', 35.1815, 136.9066],
        ['오키나와', 26.2124, 127.6809], ['요코하마', 35.4437, 139.6380], ['하코네', 35.2324, 139.1069],
    ]},
    { country: '중국', emoji: '🇨🇳', region: 'asia', cities: [
        ['베이징', 39.9042, 116.4074], ['상하이', 31.2304, 121.4737], ['시안', 34.3416, 108.9398],
        ['청두', 30.5728, 104.0668], ['구이린', 25.2736, 110.2900], ['항저우', 30.2741, 120.1551],
        ['광저우', 23.1291, 113.2644], ['홍콩', 22.3193, 114.1694],
    ]},
    { country: '태국', emoji: '🇹🇭', region: 'asia', cities: [
        ['방콕', 13.7563, 100.5018], ['치앙마이', 18.7883, 98.9853], ['푸켓', 7.8804, 98.3923],
        ['파타야', 12.9236, 100.8825], ['끄라비', 8.0863, 98.9063], ['코사무이', 9.5120, 100.0136],
        ['아유타야', 14.3532, 100.5680],
    ]},
    { country: '베트남', emoji: '🇻🇳', region: 'asia', cities: [
        ['하노이', 21.0278, 105.8342], ['다낭', 16.0544, 108.2022], ['호치민', 10.8231, 106.6297],
        ['호이안', 15.8801, 108.3380], ['나트랑', 12.2388, 109.1967], ['달랏', 11.9404, 108.4583],
        ['하롱베이', 20.9101, 107.1839],
    ]},
    { country: '싱가포르', emoji: '🇸🇬', region: 'asia', cities: [
        ['마리나베이', 1.2836, 103.8607], ['센토사', 1.2494, 103.8303], ['오차드로드', 1.3048, 103.8318],
        ['차이나타운', 1.2827, 103.8440], ['부기스', 1.3006, 103.8559],
    ]},
    { country: '말레이시아', emoji: '🇲🇾', region: 'asia', cities: [
        ['쿠알라룸푸르', 3.1390, 101.6869], ['페낭', 5.4141, 100.3288], ['랑카위', 6.3500, 99.8000],
        ['코타키나발루', 5.9804, 116.0735], ['말라카', 2.1896, 102.2501],
    ]},
    { country: '인도네시아', emoji: '🇮🇩', region: 'asia', cities: [
        ['발리', -8.3405, 115.0920], ['자카르타', -6.2088, 106.8456], ['족자카르타', -7.7956, 110.3695],
        ['롬복', -8.6500, 116.3249], ['코모도', -8.5833, 119.4833],
    ]},
    { country: '필리핀', emoji: '🇵🇭', region: 'asia', cities: [
        ['보라카이', 11.9674, 121.9248], ['세부', 10.3157, 123.8854], ['마닐라', 14.5995, 120.9842],
        ['팔라완', 9.8349, 118.7384], ['보홀', 9.8500, 124.1435],
    ]},
    { country: '대만', emoji: '🇹🇼', region: 'asia', cities: [
        ['타이베이', 25.0330, 121.5654], ['가오슝', 22.6273, 120.3014], ['타이중', 24.1477, 120.6736],
        ['화롄', 23.9871, 121.6015], ['지우펀', 25.1093, 121.8446],
    ]},
    { country: '인도', emoji: '🇮🇳', region: 'asia', cities: [
        ['뉴델리', 28.6139, 77.2090], ['뭄바이', 19.0760, 72.8777], ['자이푸르', 26.9124, 75.7873],
        ['아그라', 27.1767, 78.0081], ['고아', 15.2993, 74.1240],
    ]},
    { country: '프랑스', emoji: '🇫🇷', region: 'europe', cities: [
        ['파리', 48.8566, 2.3522], ['니스', 43.7102, 7.2620], ['리옹', 45.7640, 4.8357],
        ['마르세유', 43.2965, 5.3698], ['보르도', 44.8378, -0.5792], ['스트라스부르', 48.5734, 7.7521],
    ]},
    { country: '영국', emoji: '🇬🇧', region: 'europe', cities: [
        ['런던', 51.5074, -0.1278], ['에든버러', 55.9533, -3.1883], ['맨체스터', 53.4808, -2.2426],
        ['바스', 51.3811, -2.3590], ['옥스포드', 51.7520, -1.2577],
    ]},
    { country: '이탈리아', emoji: '🇮🇹', region: 'europe', cities: [
        ['로마', 41.9028, 12.4964], ['베니스', 45.4408, 12.3155], ['피렌체', 43.7696, 11.2558],
        ['밀라노', 45.4642, 9.1900], ['나폴리', 40.8518, 14.2681], ['친퀘테레', 44.1461, 9.6438],
    ]},
    { country: '스페인', emoji: '🇪🇸', region: 'europe', cities: [
        ['바르셀로나', 41.3874, 2.1686], ['마드리드', 40.4168, -3.7038], ['세비야', 37.3891, -5.9845],
        ['그라나다', 37.1773, -3.5986], ['발렌시아', 39.4699, -0.3763],
    ]},
    { country: '독일', emoji: '🇩🇪', region: 'europe', cities: [
        ['베를린', 52.5200, 13.4050], ['뮌헨', 48.1351, 11.5820], ['프랑크푸르트', 50.1109, 8.6821],
        ['함부르크', 53.5511, 9.9937], ['드레스덴', 51.0504, 13.7373],
    ]},
    { country: '스위스', emoji: '🇨🇭', region: 'europe', cities: [
        ['취리히', 47.3769, 8.5417], ['인터라켄', 46.6863, 7.8632], ['루체른', 47.0502, 8.3093],
        ['체르마트', 46.0207, 7.7491], ['제네바', 46.2044, 6.1432],
    ]},
    { country: '네덜란드', emoji: '🇳🇱', region: 'europe', cities: [
        ['암스테르담', 52.3676, 4.9041], ['로테르담', 51.9244, 4.4777], ['헤이그', 52.0705, 4.3007],
        ['위트레흐트', 52.0907, 5.1214],
    ]},
    { country: '그리스', emoji: '🇬🇷', region: 'europe', cities: [
        ['아테네', 37.9838, 23.7275], ['산토리니', 36.3932, 25.4615], ['미코노스', 37.4467, 25.3289],
        ['크레타', 35.2401, 24.8093],
    ]},
    { country: '포르투갈', emoji: '🇵🇹', region: 'europe', cities: [
        ['리스본', 38.7223, -9.1393], ['포르투', 41.1579, -8.6291], ['알가르베', 37.0179, -7.9307],
    ]},
    { country: '오스트리아', emoji: '🇦🇹', region: 'europe', cities: [
        ['비엔나', 48.2082, 16.3738], ['잘츠부르크', 47.8095, 13.0550], ['인스브루크', 47.2692, 11.4041],
    ]},
    { country: '체코', emoji: '🇨🇿', region: 'europe', cities: [
        ['프라하', 50.0755, 14.4378], ['체스키크룸로프', 48.8127, 14.3175],
    ]},
    { country: '미국', emoji: '🇺🇸', region: 'americas', cities: [
        ['뉴욕', 40.7128, -74.0060], ['로스앤젤레스', 34.0522, -118.2437], ['라스베가스', 36.1699, -115.1398],
        ['샌프란시스코', 37.7749, -122.4194], ['마이애미', 25.7617, -80.1918], ['하와이', 21.3069, -157.8583],
        ['시카고', 41.8781, -87.6298], ['시애틀', 47.6062, -122.3321],
    ]},
    { country: '캐나다', emoji: '🇨🇦', region: 'americas', cities: [
        ['밴쿠버', 49.2827, -123.1207], ['토론토', 43.6532, -79.3832], ['몬트리올', 45.5017, -73.5673],
        ['밴프', 51.1784, -115.5708], ['퀘벡시티', 46.8139, -71.2080],
    ]},
    { country: '멕시코', emoji: '🇲🇽', region: 'americas', cities: [
        ['칸쿤', 21.1619, -86.8515], ['멕시코시티', 19.4326, -99.1332], ['플라야델카르멘', 20.6296, -87.0739],
    ]},
    { country: '브라질', emoji: '🇧🇷', region: 'americas', cities: [
        ['리우데자네이루', -22.9068, -43.1729], ['상파울루', -23.5505, -46.6333],
    ]},
    { country: '아르헨티나', emoji: '🇦🇷', region: 'americas', cities: [
        ['부에노스아이레스', -34.6037, -58.3816], ['바릴로체', -41.1335, -71.3103],
    ]},
    { country: '호주', emoji: '🇦🇺', region: 'oceania', cities: [
        ['시드니', -33.8688, 151.2093], ['멜버른', -37.8136, 144.9631], ['골드코스트', -28.0167, 153.4000],
        ['케언즈', -16.9186, 145.7781], ['퍼스', -31.9505, 115.8605],
    ]},
    { country: '뉴질랜드', emoji: '🇳🇿', region: 'oceania', cities: [
        ['오클랜드', -36.8485, 174.7633], ['퀸스타운', -45.0312, 168.6626], ['로토루아', -38.1368, 176.2497],
    ]},
    { country: '아랍에미리트', emoji: '🇦🇪', region: 'middle-east', cities: [
        ['두바이', 25.2048, 55.2708], ['아부다비', 24.4539, 54.3773],
    ]},
    { country: '터키', emoji: '🇹🇷', region: 'middle-east', cities: [
        ['이스탄불', 41.0082, 28.9784], ['카파도키아', 38.6431, 34.8283], ['안탈리아', 36.8969, 30.7133],
    ]},
    { country: '이집트', emoji: '🇪🇬', region: 'africa', cities: [
        ['카이로', 30.0444, 31.2357], ['룩소르', 25.6872, 32.6396], ['샤름엘셰이크', 27.9158, 34.3300],
    ]},
    { country: '모로코', emoji: '🇲🇦', region: 'africa', cities: [
        ['마라케시', 31.6295, -7.9811], ['카사블랑카', 33.5731, -7.5898], ['페스', 34.0181, -5.0078],
    ]},
    { country: '남아프리카공화국', emoji: '🇿🇦', region: 'africa', cities: [
        ['케이프타운', -33.9249, 18.4241], ['요하네스버그', -26.2041, 28.0473],
    ]},
    { country: '몰디브', emoji: '🇲🇻', region: 'asia', cities: [
        ['말레', 4.1755, 73.5093], ['아리환초', 3.9000, 72.8333],
    ]},
];

const THEMES = ['family', 'couple', 'solo', 'friends', 'business'];
const SEASONS = ['spring', 'summer', 'autumn', 'winter'];
const TAG_POOL = ['자연', '휴양', '역사', '쇼핑', '맛집', '야경', '해변', '액티비티', '사진명소', '문화'];
const TRANSPORT_POOL = ['flight', 'train', 'rental-car', 'transit', 'ferry'];
const ACCESSIBILITY_POOL = ['parking', 'wheelchair'];

// Simple seeded pseudo-random so the dataset is stable across reloads.
function seededRandom(seed) {
    let x = Math.sin(seed) * 10000;
    return x - Math.floor(x);
}

function pick(arr, seed) {
    return arr[Math.floor(seededRandom(seed) * arr.length)];
}

const PACKAGE_STYLES = [
    { suffix: ' 시티 투어', focus: ['역사', '문화'] },
    { suffix: ' 미식 여행', focus: ['맛집', '쇼핑'] },
    { suffix: ' 자연 힐링', focus: ['자연', '휴양'] },
];

function generateDestinations() {
    const list = [];
    let id = 1;
    COUNTRY_SEEDS.forEach(country => {
        country.cities.forEach(([name, lat, lng]) => {
            // Each city yields the base destination plus themed package variants
            // (mirrors local_setup's per-country generation pattern, scaled to 300+ total).
            const variantCount = country.cities.length >= 6 ? 2 : 3;
            for (let v = 0; v < variantCount; v++) {
                const seed = id * 7.13;
                const style = v === 0 ? null : PACKAGE_STYLES[(v - 1) % PACKAGE_STYLES.length];
                const theme = pick(THEMES, seed);
                const season = pick(SEASONS, seed + 1);
                const price = Math.round((30 + seededRandom(seed + 2) * 250) / 5) * 5;
                const rating = (4.2 + seededRandom(seed + 3) * 0.8).toFixed(1);
                const tags = style ? style.focus : [pick(TAG_POOL, seed + 4), pick(TAG_POOL, seed + 5)].filter((v, i, a) => a.indexOf(v) === i);
                const transport = TRANSPORT_POOL.filter((_, i) => seededRandom(seed + id + i) > 0.4);
                const accessibility = ACCESSIBILITY_POOL.filter((_, i) => seededRandom(seed + id + i + 50) > 0.5);
                list.push({
                    id: id++,
                    name: style ? name + style.suffix : name,
                    baseCity: name,
                    country: country.country, region: country.region,
                    lat, lng, theme, price, duration: pick(['day', '1n2d', '2n3d', '3n+'], seed + 6),
                    transport: transport.length ? transport : ['transit'],
                    accessibility,
                    season, tags: tags.length ? tags : ['여행'],
                    emoji: country.emoji, rating: Number(rating),
                });
            }
        });
    });
    return list;
}

const DESTINATIONS_FULL = generateDestinations();
