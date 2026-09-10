<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>단일 페이지 웹사이트</title>
    <style>
        /* CSS 초기화 및 기본 스타일 */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Pretendard', 'Segoe UI', sans-serif; line-height: 1.6; color: #333; }
        html { scroll-behavior: smooth; } /* 부드러운 스크롤 */

        /* 네비게이션 바 */
        nav { background: #1a1a1a; color: #fff; padding: 1rem 5%; display: flex; justify-content: space-between; align-items: center; position: fixed; width: 100%; top: 0; z-index: 1000; }
        nav .logo { font-size: 1.5rem; font-weight: bold; }
        nav ul { list-style: none; display: flex; gap: 2rem; }
        nav a { color: #fff; text-decoration: none; transition: color 0.3s; }
        nav a:hover { color: #3498db; }

        /* 공통 섹션 스타일 */
        section { padding: 100px 5%; min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }
        h1 { font-size: 3rem; margin-bottom: 1rem; }
        h2 { font-size: 2.5rem; margin-bottom: 2rem; color: #1a1a1a; }
        p { font-size: 1.1rem; max-width: 600px; margin-bottom: 2rem; color: #666; word-break: keep-all; }

        /* 홈 섹션 */
        #home { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
        .btn { display: inline-block; padding: 12px 30px; background: #3498db; color: #fff; text-decoration: none; border-radius: 25px; font-weight: bold; transition: transform 0.3s, background 0.3s; }
        .btn:hover { background: #2980b9; transform: translateY(-3px); }

        /* 서비스 섹션 (그리드 레이아웃) */
        #services { background: #f9f9f9; }
        .grid { display: flex; gap: 2rem; flex-wrap: wrap; justify-content: center; max-width: 1000px; width: 100%; }
        .card { background: #fff; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); flex: 1; min-width: 250px; transition: transform 0.3s; }
        .card:hover { transform: translateY(-10px); }
        .card h3 { margin-bottom: 1rem; color: #3498db; }

        /* 문의 폼 섹션 */
        form { display: flex; flex-direction: column; gap: 1rem; width: 100%; max-width: 400px; }
        input, textarea { padding: 15px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem; outline: none; }
        input:focus, textarea:focus { border-color: #3498db; }
        button { padding: 15px; background: #1a1a1a; color: #fff; border: none; border-radius: 8px; cursor: pointer; font-size: 1rem; font-weight: bold; transition: background 0.3s; }
        button:hover { background: #333; }

        /* 푸터 */
        footer { background: #1a1a1a; color: #fff; text-align: center; padding: 2rem; }

        /* 모바일 반응형 */
        @media (max-width: 768px) {
            nav ul { display: none; } /* 모바일에서는 메뉴 숨김 (필요시 햄버거 메뉴 추가) */
            h1 { font-size: 2.2rem; }
            h2 { font-size: 2rem; }
        }
    </style>
</head>
<body>

    <!-- 상단 네비게이션 -->
    <nav>
        <div class="logo">MyBrand</div>
        <ul>
            <li><a href="#home">홈</a></li>
            <li><a href="#about">소개</a></li>
            <li><a href="#services">서비스</a></li>
            <li><a href="#contact">문의하기</a></li>
        </ul>
    </nav>

    <!-- 홈 섹션 -->
    <section id="home">
        <h1>하나의 파일로 완성하는 웹사이트</h1>
        <p>HTML, CSS, JavaScript가 모두 한 파일에 포함된 깔끔한 원페이지(One-Page) 템플릿입니다. 스크롤을 내려 확인해 보세요.</p>
        <a href="#services" class="btn">기능 둘러보기</a>
    </section>

    <!-- 소개 섹션 -->
    <section id="about">
        <h2>우리에 대해</h2>
        <p>이 코드는 메모장이나 VS Code에 복사한 뒤 <strong>index.html</strong>로 저장하고 웹 브라우저에서 열면 바로 작동합니다. 서버 없이도 디자인과 애니메이션을 확인할 수 있습니다.</p>
    </section>

    <!-- 서비스 섹션 -->
    <section id="services">
        <h2>제공하는 기능</h2>
        <div class="grid">
            <div class="card">
                <h3>반응형 디자인</h3>
                <p>스마트폰, 태블릿, 데스크톱 등 화면 크기에 맞춰 레이아웃이 자동으로 최적화됩니다.</p>
            </div>
            <div class="card">
                <h3>부드러운 스크롤</h3>
                <p>상단 메뉴를 클릭하면 해당 섹션으로 딱딱하게 끊기지 않고 부드럽게 이동합니다.</p>
            </div>
            <div class="card">
                <h3>인터랙티브 폼</h3>
                <p>자바스크립트가 내장되어 있어 하단 폼 작성 후 제출 시 알림창이 작동합니다.</p>
            </div>
        </div>
    </section>

    <!-- 문의 섹션 -->
    <section id="contact">
        <h2>문의하기</h2>
        <form id="contactForm" onsubmit="submitForm(event)">
            <input type="text" placeholder="이름" required>
            <input type="email" placeholder="이메일 주소" required>
            <textarea rows="5" placeholder="메시지를 입력해주세요..." required></textarea>
            <button type="submit">메시지 보내기</button>
        </form>
    </section>

    <!-- 푸터 -->
    <footer>
        <p>&copy; 2026 MyBrand. All rights reserved.</p>
    </footer>

    <!-- 자바스크립트 (기능 구현) -->
    <script>
        // 폼 제출 이벤트 처리
        function submitForm(event) {
            event.preventDefault(); // 페이지 새로고침 방지
            alert('메시지가 성공적으로 전송되었습니다! (데모 버전)');
            document.getElementById('contactForm').reset(); // 폼 초기화
        }
    </script>
</body>
</html>
