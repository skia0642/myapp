import re

import streamlit as st

st.set_page_config(page_title="쇼핑 리스트", page_icon="🛒", layout="centered")


def escape_markdown(text):
    """체크박스 라벨은 마크다운으로 렌더링되므로, 입력한 이름은 ASCII 특수문자를 이스케이프한다"""
    return re.sub(r"([!-/:-@\[-`{-~])", r"\\\1", text)


# ---------- 상태 변경 로직 (콜백) ----------
def init_state():
    """세션 상태 초기화 (샘플 데이터 포함)"""
    if "shopping_items" not in st.session_state:
        st.session_state.shopping_items = [
            {"id": 1, "name": "우유", "checked": False},
            {"id": 2, "name": "계란", "checked": False},
            {"id": 3, "name": "빵", "checked": True},
        ]
        st.session_state.next_id = 4
        st.session_state.editing_id = None  # 현재 수정 중인 항목 id
        st.session_state.flash = None  # 다음 렌더링에 보여줄 경고 문구


def find_item(item_id):
    return next((i for i in st.session_state.shopping_items if i["id"] == item_id), None)


def add_item():
    name = st.session_state.get("new_item", "").strip()
    if not name:
        st.session_state.flash = "항목 이름을 입력해 주세요."
        return
    st.session_state.shopping_items.append(
        {"id": st.session_state.next_id, "name": name, "checked": False}
    )
    st.session_state.next_id += 1


def toggle_item(item_id):
    item = find_item(item_id)
    if item:
        item["checked"] = st.session_state[f"chk_{item_id}"]


def start_edit(item_id):
    item = find_item(item_id)
    if item:
        st.session_state.editing_id = item_id  # 한 번에 한 항목만 수정
        st.session_state[f"edit_{item_id}"] = item["name"]


def save_edit(item_id):
    name = st.session_state.get(f"edit_{item_id}", "").strip()
    if not name:
        st.session_state.flash = "빈 이름으로는 저장할 수 없어요."
        return
    item = find_item(item_id)
    if item:
        item["name"] = name
    st.session_state.editing_id = None


def cancel_edit():
    st.session_state.editing_id = None


def delete_item(item_id):
    st.session_state.shopping_items = [
        i for i in st.session_state.shopping_items if i["id"] != item_id
    ]
    if st.session_state.editing_id == item_id:
        st.session_state.editing_id = None


def clear_checked():
    st.session_state.shopping_items = [
        i for i in st.session_state.shopping_items if not i["checked"]
    ]
    editing = st.session_state.editing_id
    if editing is not None and find_item(editing) is None:
        st.session_state.editing_id = None


# ---------- 화면 렌더링 ----------
CSS = """
<style>
footer, #MainMenu { visibility: hidden; }
.block-container { padding-top: 2.5rem; max-width: 640px; }
h1 { font-size: 1.9rem !important; padding-bottom: .25rem; }

/* 모바일에서도 항목 행을 한 줄로 유지 */
[data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: .5rem !important; align-items: center; }
[data-testid="stColumn"] { min-width: 0 !important; }

/* 터치하기 편한 버튼 크기 */
.stButton button, .stFormSubmitButton button { min-height: 40px; padding: 0 .6rem; white-space: nowrap; }

/* 항목 행 */
[data-testid="stCheckbox"] label { min-height: 40px; align-items: center; }
[data-testid="stCheckbox"] label p { font-size: 1.05rem; overflow-wrap: anywhere; }
[data-testid="stCheckbox"]:has(input:checked) label p { opacity: .5; }

/* 빈 목록 안내 */
.empty-state { text-align: center; padding: 2.5rem 0; opacity: .6; }
.empty-state .emoji { font-size: 2.5rem; }
</style>
"""


def render_header():
    st.markdown(CSS, unsafe_allow_html=True)
    st.title("🛒 쇼핑 리스트")


def render_input():
    """항목 입력창 + 추가 버튼 (Enter 제출 지원)"""
    with st.form("add_form", clear_on_submit=True):
        col_input, col_btn = st.columns([4, 1])
        col_input.text_input(
            "항목",
            key="new_item",
            placeholder="사야 할 물건을 입력하세요",
            label_visibility="collapsed",
        )
        col_btn.form_submit_button(
            "추가", type="primary", use_container_width=True, on_click=add_item
        )
    if st.session_state.flash:
        st.warning(st.session_state.flash)
        st.session_state.flash = None


def render_status():
    """진행 현황: 완료 n / 전체 m"""
    items = st.session_state.shopping_items
    done = sum(1 for i in items if i["checked"])
    st.progress(done / len(items) if items else 0.0, text=f"완료 {done} / 전체 {len(items)}")


def render_row(item):
    item_id = item["id"]
    if st.session_state.editing_id == item_id:
        # form으로 감싸 Enter 키로도 저장되게 한다 (첫 번째 submit 버튼이 저장)
        with st.form(f"edit_form_{item_id}", border=False):
            col_text, col_save, col_cancel = st.columns([6, 2, 2], vertical_alignment="center")
            col_text.text_input(
                "이름 수정", key=f"edit_{item_id}", label_visibility="collapsed"
            )
            col_save.form_submit_button("저장", on_click=save_edit, args=(item_id,))
            col_cancel.form_submit_button("취소", on_click=cancel_edit)
        return

    col_chk, col_edit, col_del = st.columns([8, 1.3, 1.3], vertical_alignment="center")
    name = escape_markdown(item["name"])
    label = f"~~{name}~~" if item["checked"] else name
    col_chk.checkbox(
        label,
        value=item["checked"],
        key=f"chk_{item_id}",
        on_change=toggle_item,
        args=(item_id,),
    )
    col_edit.button("✏️", key=f"edit_btn_{item_id}", on_click=start_edit, args=(item_id,))
    col_del.button("🗑️", key=f"del_{item_id}", on_click=delete_item, args=(item_id,))


def render_list():
    """미완료 항목을 위, 완료 항목을 아래로 (같은 그룹은 추가 순서 유지)"""
    items = st.session_state.shopping_items
    if not items:
        st.markdown(
            '<div class="empty-state"><div class="emoji">🛍️</div>'
            "목록이 비어 있어요.<br>사야 할 물건을 추가해 보세요!</div>",
            unsafe_allow_html=True,
        )
        return
    for item in sorted(items, key=lambda i: (i["checked"], i["id"])):
        render_row(item)


def render_footer():
    has_checked = any(i["checked"] for i in st.session_state.shopping_items)
    st.button("체크된 항목 모두 삭제", on_click=clear_checked, disabled=not has_checked)


init_state()
render_header()
render_input()
render_status()
render_list()
render_footer()
