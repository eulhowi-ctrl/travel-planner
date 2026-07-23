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
    { country: '네팔', emoji: '🇳🇵', region: 'asia', cities: [
        ['카트만두', 27.7172, 85.3240], ['포카라', 28.2096, 83.9856],
    ]},
    { country: '스리랑카', emoji: '🇱🇰', region: 'asia', cities: [
        ['콜롬보', 6.9271, 79.8612], ['캔디', 7.2906, 80.6337], ['갈레', 6.0535, 80.2210],
    ]},
    { country: '캄보디아', emoji: '🇰🇭', region: 'asia', cities: [
        ['씨엠립', 13.3671, 103.8448], ['프놈펜', 11.5564, 104.9282],
    ]},
    { country: '라오스', emoji: '🇱🇦', region: 'asia', cities: [
        ['루앙프라방', 19.8856, 102.1347], ['비엔티안', 17.9757, 102.6331],
    ]},
    { country: '미얀마', emoji: '🇲🇲', region: 'asia', cities: [
        ['양곤', 16.8409, 96.1735], ['바간', 21.1717, 94.8600],
    ]},
    { country: '몽골', emoji: '🇲🇳', region: 'asia', cities: [
        ['울란바토르', 47.8864, 106.9057],
    ]},
    { country: '부탄', emoji: '🇧🇹', region: 'asia', cities: [
        ['파로', 27.4305, 89.6237],
    ]},
    { country: '우즈베키스탄', emoji: '🇺🇿', region: 'asia', cities: [
        ['타슈켄트', 41.2995, 69.2401], ['사마르칸트', 39.6270, 66.9750],
    ]},
    { country: '아이슬란드', emoji: '🇮🇸', region: 'europe', cities: [
        ['레이캬비크', 64.1466, -21.9426], ['블루라군', 63.8804, -22.4495], ['바트나이외쿠틀', 64.4000, -16.9000],
    ]},
    { country: '노르웨이', emoji: '🇳🇴', region: 'europe', cities: [
        ['오슬로', 59.9139, 10.7522], ['베르겐', 60.3913, 5.3221], ['트롬쇠', 69.6492, 18.9553],
    ]},
    { country: '스웨덴', emoji: '🇸🇪', region: 'europe', cities: [
        ['스톡홀름', 59.3293, 18.0686], ['예테보리', 57.7089, 11.9746],
    ]},
    { country: '덴마크', emoji: '🇩🇰', region: 'europe', cities: [
        ['코펜하겐', 55.6761, 12.5683],
    ]},
    { country: '핀란드', emoji: '🇫🇮', region: 'europe', cities: [
        ['헬싱키', 60.1699, 24.9384], ['로바니에미', 66.5039, 25.7294],
    ]},
    { country: '아일랜드', emoji: '🇮🇪', region: 'europe', cities: [
        ['더블린', 53.3498, -6.2603],
    ]},
    { country: '폴란드', emoji: '🇵🇱', region: 'europe', cities: [
        ['바르샤바', 52.2297, 21.0122], ['크라쿠프', 50.0647, 19.9450],
    ]},
    { country: '헝가리', emoji: '🇭🇺', region: 'europe', cities: [
        ['부다페스트', 47.4979, 19.0402],
    ]},
    { country: '크로아티아', emoji: '🇭🇷', region: 'europe', cities: [
        ['두브로브니크', 42.6507, 18.0944], ['자그레브', 45.8150, 15.9819], ['스플리트', 43.5081, 16.4402],
    ]},
    { country: '러시아', emoji: '🇷🇺', region: 'europe', cities: [
        ['모스크바', 55.7558, 37.6173], ['상트페테르부르크', 59.9311, 30.3609],
    ]},
    { country: '벨기에', emoji: '🇧🇪', region: 'europe', cities: [
        ['브뤼셀', 50.8503, 4.3517],
    ]},
    { country: '슬로베니아', emoji: '🇸🇮', region: 'europe', cities: [
        ['블레드', 46.3683, 14.1146],
    ]},
    { country: '이스라엘', emoji: '🇮🇱', region: 'middle-east', cities: [
        ['텔아비브', 32.0853, 34.7818], ['예루살렘', 31.7683, 35.2137],
    ]},
    { country: '요르단', emoji: '🇯🇴', region: 'middle-east', cities: [
        ['암만', 31.9454, 35.9284], ['페트라', 30.3285, 35.4444],
    ]},
    { country: '카타르', emoji: '🇶🇦', region: 'middle-east', cities: [
        ['도하', 25.2854, 51.5310],
    ]},
    { country: '오만', emoji: '🇴🇲', region: 'middle-east', cities: [
        ['무스카트', 23.5880, 58.3829],
    ]},
    { country: '케냐', emoji: '🇰🇪', region: 'africa', cities: [
        ['나이로비', -1.2921, 36.8219], ['마사이마라', -1.5000, 35.0000],
    ]},
    { country: '탄자니아', emoji: '🇹🇿', region: 'africa', cities: [
        ['잔지바르', -6.1659, 39.2026], ['세렝게티', -2.3333, 34.8333],
    ]},
    { country: '나미비아', emoji: '🇳🇦', region: 'africa', cities: [
        ['빈트후크', -22.5609, 17.0658],
    ]},
    { country: '짐바브웨', emoji: '🇿🇼', region: 'africa', cities: [
        ['빅토리아폭포', -17.9243, 25.8567],
    ]},
    { country: '튀니지', emoji: '🇹🇳', region: 'africa', cities: [
        ['튀니스', 36.8065, 10.1815],
    ]},
    { country: '모리셔스', emoji: '🇲🇺', region: 'africa', cities: [
        ['모리셔스', -20.3484, 57.5522],
    ]},
    { country: '세이셸', emoji: '🇸🇨', region: 'africa', cities: [
        ['마헤섬', -4.6796, 55.4920],
    ]},
    { country: '페루', emoji: '🇵🇪', region: 'americas', cities: [
        ['쿠스코', -13.5319, -71.9675], ['리마', -12.0464, -77.0428], ['마추픽추', -13.1547, -72.5254],
    ]},
    { country: '칠레', emoji: '🇨🇱', region: 'americas', cities: [
        ['산티아고', -33.4489, -70.6693], ['이스터섬', -27.1127, -109.3497],
    ]},
    { country: '콜롬비아', emoji: '🇨🇴', region: 'americas', cities: [
        ['보고타', 4.7110, -74.0721], ['카르타헤나', 10.3910, -75.4794],
    ]},
    { country: '볼리비아', emoji: '🇧🇴', region: 'americas', cities: [
        ['우유니', -20.4597, -66.8250], ['라파스', -16.4897, -68.1193],
    ]},
    { country: '에콰도르', emoji: '🇪🇨', region: 'americas', cities: [
        ['갈라파고스', -0.9538, -89.6115], ['키토', -0.1807, -78.4678],
    ]},
    { country: '쿠바', emoji: '🇨🇺', region: 'americas', cities: [
        ['아바나', 23.1136, -82.3666],
    ]},
    { country: '코스타리카', emoji: '🇨🇷', region: 'americas', cities: [
        ['산호세', 9.9281, -84.0907],
    ]},
    { country: '자메이카', emoji: '🇯🇲', region: 'americas', cities: [
        ['몬테고베이', 18.4762, -77.8939],
    ]},
    { country: '도미니카공화국', emoji: '🇩🇴', region: 'americas', cities: [
        ['푼타카나', 18.5601, -68.3725],
    ]},
    { country: '피지', emoji: '🇫🇯', region: 'oceania', cities: [
        ['난디', -17.7765, 177.4356],
    ]},
];

// IATA airport codes keyed by baseCity, for the flight.naver.com deep link
// (script.js's naverFlightDeepLink). Cities without a nearby commercial
// airport (small towns, day-trip spots) are omitted on purpose — the deep
// link falls back to a general Naver search for those instead of guessing.
const AIRPORT_CODES = {
    // 대한민국
    '서울': 'ICN', '부산': 'PUS', '제주도': 'CJU', '강릉': 'YNY', '여수': 'RSU', '속초': 'YNY',
    // 일본
    '도쿄': 'HND', '오사카': 'KIX', '교토': 'ITM', '삿포로': 'CTS', '후쿠오카': 'FUK', '나고야': 'NGO',
    '오키나와': 'OKA', '요코하마': 'HND',
    // 중국
    '베이징': 'PEK', '상하이': 'PVG', '시안': 'XIY', '청두': 'CTU', '구이린': 'KWL', '항저우': 'HGH',
    '광저우': 'CAN', '홍콩': 'HKG',
    // 태국
    '방콕': 'BKK', '치앙마이': 'CNX', '푸켓': 'HKT', '파타야': 'UTP', '끄라비': 'KBV', '코사무이': 'USM',
    // 베트남
    '하노이': 'HAN', '다낭': 'DAD', '호치민': 'SGN', '호이안': 'DAD', '나트랑': 'CXR', '달랏': 'DLI',
    '하롱베이': 'VDO',
    // 싱가포르
    '마리나베이': 'SIN', '센토사': 'SIN', '오차드로드': 'SIN', '차이나타운': 'SIN', '부기스': 'SIN',
    // 말레이시아
    '쿠알라룸푸르': 'KUL', '페낭': 'PEN', '랑카위': 'LGK', '코타키나발루': 'BKI',
    // 인도네시아
    '발리': 'DPS', '자카르타': 'CGK', '족자카르타': 'YIA', '롬복': 'LOP', '코모도': 'LBJ',
    // 필리핀
    '보라카이': 'MPH', '세부': 'CEB', '마닐라': 'MNL', '팔라완': 'PPS', '보홀': 'TAG',
    // 대만
    '타이베이': 'TPE', '가오슝': 'KHH', '타이중': 'RMQ', '화롄': 'HUN',
    // 인도
    '뉴델리': 'DEL', '뭄바이': 'BOM', '자이푸르': 'JAI', '아그라': 'AGR', '고아': 'GOI',
    // 프랑스
    '파리': 'CDG', '니스': 'NCE', '리옹': 'LYS', '마르세유': 'MRS', '보르도': 'BOD', '스트라스부르': 'SXB',
    // 영국
    '런던': 'LHR', '에든버러': 'EDI', '맨체스터': 'MAN',
    // 이탈리아
    '로마': 'FCO', '베니스': 'VCE', '피렌체': 'FLR', '밀라노': 'MXP', '나폴리': 'NAP',
    // 스페인
    '바르셀로나': 'BCN', '마드리드': 'MAD', '세비야': 'SVQ', '그라나다': 'GRX', '발렌시아': 'VLC',
    // 독일
    '베를린': 'BER', '뮌헨': 'MUC', '프랑크푸르트': 'FRA', '함부르크': 'HAM', '드레스덴': 'DRS',
    // 스위스
    '취리히': 'ZRH', '제네바': 'GVA',
    // 네덜란드
    '암스테르담': 'AMS', '로테르담': 'RTM', '헤이그': 'RTM', '위트레흐트': 'AMS',
    // 그리스
    '아테네': 'ATH', '산토리니': 'JTR', '미코노스': 'JMK', '크레타': 'HER',
    // 포르투갈
    '리스본': 'LIS', '포르투': 'OPO', '알가르베': 'FAO',
    // 오스트리아
    '비엔나': 'VIE', '잘츠부르크': 'SZG', '인스브루크': 'INN',
    // 체코
    '프라하': 'PRG',
    // 미국
    '뉴욕': 'JFK', '로스앤젤레스': 'LAX', '라스베가스': 'LAS', '샌프란시스코': 'SFO', '마이애미': 'MIA',
    '하와이': 'HNL', '시카고': 'ORD', '시애틀': 'SEA',
    // 캐나다
    '밴쿠버': 'YVR', '토론토': 'YYZ', '몬트리올': 'YUL', '밴프': 'YYC', '퀘벡시티': 'YQB',
    // 멕시코
    '칸쿤': 'CUN', '멕시코시티': 'MEX', '플라야델카르멘': 'CUN',
    // 브라질
    '리우데자네이루': 'GIG', '상파울루': 'GRU',
    // 아르헨티나
    '부에노스아이레스': 'EZE', '바릴로체': 'BRC',
    // 호주
    '시드니': 'SYD', '멜버른': 'MEL', '골드코스트': 'OOL', '케언즈': 'CNS', '퍼스': 'PER',
    // 뉴질랜드
    '오클랜드': 'AKL', '퀸스타운': 'ZQN', '로토루아': 'ROT',
    // 아랍에미리트
    '두바이': 'DXB', '아부다비': 'AUH',
    // 터키
    '이스탄불': 'IST', '카파도키아': 'NAV', '안탈리아': 'AYT',
    // 이집트
    '카이로': 'CAI', '룩소르': 'LXR', '샤름엘셰이크': 'SSH',
    // 모로코
    '마라케시': 'RAK', '카사블랑카': 'CMN', '페스': 'FEZ',
    // 남아프리카공화국
    '케이프타운': 'CPT', '요하네스버그': 'JNB',
    // 몰디브
    '말레': 'MLE', '아리환초': 'MLE',
    // 네팔
    '카트만두': 'KTM', '포카라': 'PKR',
    // 스리랑카
    '콜롬보': 'CMB',
    // 캄보디아
    '씨엠립': 'SAI', '프놈펜': 'PNH',
    // 라오스
    '루앙프라방': 'LPQ', '비엔티안': 'VTE',
    // 미얀마
    '양곤': 'RGN', '바간': 'NYU',
    // 몽골
    '울란바토르': 'ULN',
    // 부탄
    '파로': 'PBH',
    // 우즈베키스탄
    '타슈켄트': 'TAS', '사마르칸트': 'SKD',
    // 아이슬란드
    '레이캬비크': 'KEF', '블루라군': 'KEF',
    // 노르웨이
    '오슬로': 'OSL', '베르겐': 'BGO', '트롬쇠': 'TOS',
    // 스웨덴
    '스톡홀름': 'ARN', '예테보리': 'GOT',
    // 덴마크
    '코펜하겐': 'CPH',
    // 핀란드
    '헬싱키': 'HEL', '로바니에미': 'RVN',
    // 아일랜드
    '더블린': 'DUB',
    // 폴란드
    '바르샤바': 'WAW', '크라쿠프': 'KRK',
    // 헝가리
    '부다페스트': 'BUD',
    // 크로아티아
    '두브로브니크': 'DBV', '자그레브': 'ZAG', '스플리트': 'SPU',
    // 러시아
    '모스크바': 'SVO', '상트페테르부르크': 'LED',
    // 벨기에
    '브뤼셀': 'BRU',
    // 슬로베니아
    '블레드': 'LJU',
    // 이스라엘
    '텔아비브': 'TLV', '예루살렘': 'TLV',
    // 요르단
    '암만': 'AMM', '페트라': 'AQJ',
    // 카타르
    '도하': 'DOH',
    // 오만
    '무스카트': 'MCT',
    // 케냐
    '나이로비': 'NBO',
    // 탄자니아
    '잔지바르': 'ZNZ',
    // 나미비아
    '빈트후크': 'WDH',
    // 짐바브웨
    '빅토리아폭포': 'VFA',
    // 튀니지
    '튀니스': 'TUN',
    // 모리셔스
    '모리셔스': 'MRU',
    // 세이셸
    '마헤섬': 'SEZ',
    // 페루
    '쿠스코': 'CUZ', '리마': 'LIM', '마추픽추': 'CUZ',
    // 칠레
    '산티아고': 'SCL', '이스터섬': 'IPC',
    // 콜롬비아
    '보고타': 'BOG', '카르타헤나': 'CTG',
    // 볼리비아
    '우유니': 'UYU', '라파스': 'LPB',
    // 에콰도르
    '갈라파고스': 'GPS', '키토': 'UIO',
    // 쿠바
    '아바나': 'HAV',
    // 코스타리카
    '산호세': 'SJO',
    // 자메이카
    '몬테고베이': 'MBJ',
    // 도미니카공화국
    '푼타카나': 'PUJ',
    // 피지
    '난디': 'NAN',
};

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
