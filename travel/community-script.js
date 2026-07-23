// ==================== TRAVEL Community Page ====================

const QNA_SEED = [
    { title: '부산 3박4일 예산 얼마나 잡아야 할까요?', author: '여행초보', answers: 5, tags: ['부산', '예산'] },
    { title: '제주도 렌트카 필수인가요?', author: '길치탈출', answers: 8, tags: ['제주도', '교통'] },
    { title: '도쿄 혼행 안전한가요?', author: '나홀로여행', answers: 3, tags: ['도쿄', '혼행'] },
];

const STORIES_SEED = [
    { title: '파리 신혼여행 완벽 후기', author: '민지커플', emoji: '🗼', likes: 128 },
    { title: '태국 배낭여행 2주 기록', author: '방랑자', emoji: '🛕', likes: 94 },
    { title: '아이와 함께한 제주 힐링 여행', author: '엄마의여행', emoji: '🍊', likes: 76 },
];

const BUDDY_SEED = [
    { name: '김하늘', destination: '방콕', dates: '2026.09.10 - 09.15', bio: '맛집 탐방 좋아하는 30대입니다.' },
    { name: '이서준', destination: '교토', dates: '2026.10.02 - 10.06', bio: '사진 찍는 걸 좋아해요. 같이 다니실 분!' },
    { name: '박지우', destination: '싱가포르', dates: '2026.11.20 - 11.24', bio: '가족 여행인데 다른 가족과 정보 공유하고 싶어요.' },
];

function renderQnaList() {
    const posts = getLS('communityPosts', []);
    const all = [...posts, ...QNA_SEED];
    document.getElementById('qnaList').innerHTML = all.map(q => `
        <div class="card qna-item">
            <div class="qna-question">${escapeHtml(q.title)}</div>
            ${q.body ? `<p class="text-muted" style="font-size:14px;">${escapeHtml(q.body)}</p>` : ''}
            <div class="qna-meta">
                <span>${escapeHtml(q.author)}</span>
                <span>답변 ${q.answers || 0}개</span>
            </div>
            ${q.tags ? `<div class="qna-tags">${q.tags.map(t => `<span class="badge badge-primary">${t}</span>`).join('')}</div>` : ''}
        </div>
    `).join('');
}

function renderStories() {
    document.getElementById('storiesGrid').innerHTML = STORIES_SEED.map(s => `
        <div class="card story-card">
            <div class="ph photo-tile" style="background-image:url('${photoUrl('story-' + s.title)}');"><span class="tile-emoji-badge">${s.emoji}</span></div>
            <div class="story-body">
                <strong>${s.title}</strong>
                <div class="story-meta">
                    <span>${s.author}</span>
                    <span>❤️ ${s.likes}</span>
                </div>
            </div>
        </div>
    `).join('');
}

function renderBuddyList() {
    document.getElementById('buddyList').innerHTML = BUDDY_SEED.map((b, i) => `
        <div class="card buddy-card">
            <div class="buddy-header">
                <div class="buddy-avatar">${b.name[0]}</div>
                <div>
                    <strong>${b.name}</strong>
                    <div class="text-muted" style="font-size:12px;">${b.destination} · ${b.dates}</div>
                </div>
            </div>
            <p class="text-muted" style="font-size:13px;">${b.bio}</p>
            <button class="btn btn-secondary btn-buddy-contact" data-buddy="${i}">💬 연락하기</button>
        </div>
    `).join('');

    document.querySelectorAll('.btn-buddy-contact').forEach(btn => {
        btn.addEventListener('click', () => {
            showToast('여행 버디 연락 기능은 아직 준비 중이에요');
        });
    });
}

function switchTab(tabName) {
    document.querySelectorAll('.community-tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tabName));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.toggle('active', c.dataset.tab === tabName));
}

function openWriteModal() { document.getElementById('writeModal').classList.remove('hidden'); }
function closeWriteModal() { document.getElementById('writeModal').classList.add('hidden'); }

function submitWrite() {
    const title = document.getElementById('writeTitleInput').value.trim();
    const body = document.getElementById('writeBodyInput').value.trim();
    if (!title || !body) { showToast('제목과 내용을 모두 입력해주세요', 'error'); return; }

    const posts = getLS('communityPosts', []);
    posts.unshift({ title, body, author: '나', answers: 0, tags: [] });
    setLS('communityPosts', posts);

    document.getElementById('writeTitleInput').value = '';
    document.getElementById('writeBodyInput').value = '';
    closeWriteModal();
    switchTab('qna');
    renderQnaList();
    showToast('글이 등록되었습니다', 'success');
    earnPoints('커뮤니티 글 작성', 100);
}

document.addEventListener('DOMContentLoaded', () => {
    renderQnaList();
    renderStories();
    renderBuddyList();

    document.querySelectorAll('.community-tab').forEach(tab => {
        tab.addEventListener('click', () => switchTab(tab.dataset.tab));
    });

    document.getElementById('writeBtn').addEventListener('click', openWriteModal);
    document.getElementById('closeWriteModalBtn').addEventListener('click', closeWriteModal);
    document.getElementById('submitWriteBtn').addEventListener('click', submitWrite);
    document.getElementById('writeModal').addEventListener('click', e => { if (e.target.id === 'writeModal') closeWriteModal(); });
});
