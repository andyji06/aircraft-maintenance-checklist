
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="항공기 정비 체크리스트",
    page_icon="✈️",
    layout="wide"
)

# 디자인 설정
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #edf4fc, #ffffff);
}
[data-testid="stSidebar"] {
    background-color: #10243e;
}
[data-testid="stSidebar"] * {
    color: white;
}
.hero {
    background: linear-gradient(120deg, #10243e, #2366a5);
    padding: 30px;
    border-radius: 18px;
    color: white;
    margin-bottom: 22px;
}
.hero h1 {
    font-size: 30px;
    margin-bottom: 10px;
}
.hero p {
    color: #e0efff;
}
div[data-testid="stMetric"] {
    background: white;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid #dce7f4;
}
.stButton button {
    border-radius: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>✈️ 항공기 정비 점검 체크리스트</h1>
    <p>항공기 점검 항목과 진행 상황을 관리하는 교육용 프로그램입니다.</p>
</div>
""", unsafe_allow_html=True)

# 점검 항목
CHECKLIST = {
    "🔧 엔진 점검": [
        "엔진 외관 손상 여부 확인",
        "누유 및 누출 흔적 확인",
        "주변 부품 고정 상태 확인"
    ],
    "🛞 타이어 및 착륙장치": [
        "타이어 외관 및 마모 상태 확인",
        "착륙장치 주변 손상 여부 확인",
        "주변 이물질 여부 확인"
    ],
    "🛩️ 날개 및 기체": [
        "날개 표면 손상 여부 확인",
        "기체 외부 패널 상태 확인",
        "기체 외부 이물질 여부 확인"
    ],
    "💡 조명 및 표시 장치": [
        "외부 조명 상태 확인",
        "표시 장치 이상 여부 확인",
        "점검 기록 누락 여부 확인"
    ]
}

all_items = [
    item
    for items in CHECKLIST.values()
    for item in items
]

if "checked" not in st.session_state:
    st.session_state.checked = {
        item: False for item in all_items
    }

if "memo" not in st.session_state:
    st.session_state.memo = ""

# 메뉴
page = st.sidebar.radio(
    "✈️ 메뉴",
    ["점검하기", "점검 결과", "프로그램 안내"]
)

st.sidebar.markdown("---")
st.sidebar.caption("항공정비 진로 탐색 프로젝트")
st.sidebar.caption("교육용 시뮬레이션")

# 점검하기
if page == "점검하기":

    st.subheader("🧰 정비 점검 항목")
    st.write("각 항목을 확인하고 체크해 주세요.")

    done = sum(st.session_state.checked.values())
    total = len(all_items)
    progress = done / total

    col1, col2, col3 = st.columns(3)

    col1.metric("전체 항목", f"{total}개")
    col2.metric("체크 완료", f"{done}개")
    col3.metric("진행률", f"{progress:.0%}")

    st.progress(progress)

    for category, items in CHECKLIST.items():

        with st.expander(category, expanded=True):

            for item in items:
                st.session_state.checked[item] = st.checkbox(
                    item,
                    value=st.session_state.checked[item],
                    key="check_" + item
                )

    st.subheader("📝 점검 메모")

    st.session_state.memo = st.text_area(
        "기록할 내용을 입력하세요.",
        value=st.session_state.memo,
        placeholder="추가 확인 사항을 입력하세요."
    )

    if st.button("🔄 체크리스트 초기화"):
        for item in all_items:
            st.session_state.checked[item] = False
            st.session_state["check_" + item] = False

        st.session_state.memo = ""
        st.rerun()

    st.info("점검 결과는 왼쪽 메뉴의 '점검 결과'에서 확인할 수 있습니다.")

# 점검 결과
elif page == "점검 결과":

    st.subheader("📊 점검 결과 요약")

    rows = []

    for category, items in CHECKLIST.items():

        for item in items:

            status = (
                "체크 완료"
                if st.session_state.checked[item]
                else "미체크"
            )

            rows.append({
                "점검 분류": category,
                "점검 항목": item,
                "상태": status
            })

    df = pd.DataFrame(rows)

    done = sum(st.session_state.checked.values())
    total = len(all_items)
    missing = total - done
    progress = done / total

    col1, col2, col3 = st.columns(3)

    col1.metric("완료 항목", f"{done}개")
    col2.metric("미체크 항목", f"{missing}개")
    col3.metric("진행률", f"{progress:.0%}")

    st.progress(progress)

    if missing > 0:
        st.warning(f"아직 확인하지 않은 항목이 {missing}개 있습니다.")
        st.dataframe(
            df[df["상태"] == "미체크"],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("모든 교육용 체크 항목을 선택했습니다.")

    st.subheader("📋 전체 점검 목록")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("📝 점검 메모")
    st.write(st.session_state.memo or "작성된 메모가 없습니다.")

    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "📥 점검 결과 CSV 다운로드",
        data=csv,
        file_name=f"점검결과_{date.today()}.csv",
        mime="text/csv",
        use_container_width=True
    )

# 프로그램 안내
else:

    st.subheader("ℹ️ 프로그램 소개")

    st.write("""
    이 프로그램은 항공정비학과 진로 탐색을 위해 만든
    교육용 항공기 정비 점검 체크리스트입니다.

    ### 주요 기능

    - 엔진, 타이어, 날개 등 점검 항목 확인
    - 체크박스를 이용한 점검 기록
    - 점검 완료 개수 자동 계산
    - 전체 점검 진행률 표시
    - 미체크 항목 확인
    - 점검 결과 표와 CSV 파일 다운로드

    ### 기대 효과

    항공기 정비에서 점검 기록과 안전 확인이
    중요한 이유를 이해할 수 있습니다.
    """)

    st.warning("""
    주의: 이 프로그램은 학습용 예시입니다.
    실제 항공기 정비 절차나 안전 판정을 대신하지 않습니다.
    """)

st.markdown("---")
st.caption("항공정비 진로 탐색 프로젝트 | Python + Streamlit")
