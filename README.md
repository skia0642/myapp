# 🛒 쇼핑 리스트

장보기 항목을 추가·수정·삭제·체크할 수 있는 가벼운 Streamlit 웹 앱입니다.

- **배포 URL**: _(배포 후 여기에 입력)_

## 기능
- 항목 추가 (Enter 지원, 빈 값 차단)
- 항목 수정 (저장 / 취소, Enter 지원)
- 항목 삭제, 체크된 항목 일괄 삭제
- 체크 시 취소선 처리, 미완료 항목은 위 / 완료 항목은 아래로 정렬
- 진행 현황(완료 n / 전체 m) 표시
- 모바일·PC, 라이트·다크 모드 지원

> 데이터는 브라우저 세션(`st.session_state`)에만 저장되므로 새로고침하면 초기화됩니다.

## 로컬 실행
```
pip install -r requirements.txt
streamlit run app.py
```
http://localhost:8501 에서 확인합니다.

## 프로젝트 구조
```
app.py                  # Streamlit 앱 (단일 파일)
requirements.txt
.streamlit/config.toml  # 테마(라이트/다크 포인트 컬러)
PRD.md                  # 요구사항 문서
```

## 배포 (Streamlit Community Cloud)
1. 이 저장소를 GitHub에 올린다.
2. https://share.streamlit.io 에 GitHub 계정으로 로그인한다.
3. **Create app** → 저장소, 브랜치(`main`), Main file path(`app.py`)를 지정하고 **Deploy**.
4. 발급된 URL을 위 **배포 URL**에 적는다.

무료 호스팅은 일정 시간 접속이 없으면 앱이 잠들 수 있어, 첫 접속 시 로딩이 걸릴 수 있습니다.
