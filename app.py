import streamlit as st

# --- [1. 송곡여고 개설 과목 데이터 세팅] ---
SUBJECTS = {
    "2-1": {
        "국수영": ["국어(융합): 독서 토론과 글쓰기", "수학(진로): 기하", "영어(융합): 세계 문화와 영어"],
        "탐구": ["세계시민과 지리", "세계사", "사회와 문화", "현대사회와 윤리", "물리학", "화학", "생명과학", "지구과학"],
        "기가_외국어": ["정보", "중국어", "한문"],
        "교양_기타": []
    },
    "2-2": {
        "국수영": ["국어(진로): 문학과 영상", "수학(융합): 수학과제 탐구", "영어(진로): 영미 문학 읽기"],
        "탐구": ["한국지리 탐구", "동아시아 역사 기행", "정치", "경제", "윤리와 사상", "역학과 에너지", "물질과 에너지", "생물의 유전", "지구시스템과학"],
        "기가_외국어": ["인공지능 기초", "중국 문화", "언어생활과 한자"],
        "교양_기타": []
    },
    "3-1": {
        "국수영": ["국어(진로): 주제 탐구 독서", "수학(진로): 미적분Ⅱ", "영어(융합): 미디어 영어"],
        "탐구": ["도시의 미래 탐구", "법과 사회", "역사로 탐구하는 현대 세계", "사회문제 탐구", "윤리문제 탐구", "전자기와 양자", "화학 반응의 세계", "세포와 물질대사", "지구시스템과학"],
        "기가_외국어": ["데이터 과학", "중국어 회화", "한문 고전 읽기"],
        "교양_기타": ["교육의 이해*", "보건*", "논술*", "기초 체육 전공 실기", "실용음악실기Ⅰ", "미술실기Ⅰ"]
    },
    "3-2": {
        "국수영": ["국어(융합): 매체 의사소통", "수학(진로): 경제 수학", "영어(진로): 심화 영어"],
        "탐구": ["여행지리", "금융과 경제생활", "인문학과 윤리", "국제 관계의 이해", "기후변화와 지속가능한 세계", "기후변화와 환경생태", "융합과학 탐구"],
        "기가_외국어": ["소프트웨어와 생활", "심화 중국어", "생활과 한문"],
        "교양_기타": ["생태와 환경*", "논리와 사고*", "인간과 심리*", "심화 체육 전공 실기", "실용음악실기Ⅱ", "미술실기Ⅱ"]
    }
}

# --- [2. 세션 상태(State) 초기화] ---
if 'step' not in st.session_state:
    st.session_state.step = "2-1"
if 'choices' not in st.session_state:
    st.session_state.choices = {
        "2-1": {"국수영": [], "탐구": [], "기가_외국어": [], "교양_기타": []},
        "2-2": {"국수영": [], "탐구": [], "기가_외국어": [], "교양_기타": []},
        "3-1": {"국수영": [], "탐구": [], "기가_외국어": [], "교양_기타": []},
        "3-2": {"국수영": [], "탐구": [], "기가_외국어": [], "교양_기타": []},
    }

st.set_page_config(page_title="송곡여고 과목 선택 시스템", page_icon="🎓", layout="wide")
st.title("🎓 송곡여자고등학교 고교학점제 과목 선택")
st.caption("과목 선택 전문 상담 교사 시스템 (단계별 실시간 자동 검증)")

# --- [3. 진행 단계 인디케이터] ---
steps = ["2-1", "2-2", "3-1", "3-2", "최종확인"]
cols = st.columns(len(steps))
for i, s in enumerate(steps):
    with cols[i]:
        if st.session_state.step == s:
            st.markdown(f"**🔵 {s}학기 선택 중**")
        else:
            st.markdown(f"⚪ {s}")
st.write("---")

# --- [4. 학기별 입력 및 단층 검증 함수] ---
def render_semester_ui(sem, next_step):
    st.subheader(f"📅 {sem[0]}학년 {sem[2]}학기 과목 선택")
    
    col1, col2 = st.columns(2)
    with col1:
        kme = st.multiselect("1️⃣ 국어/수학/영어 교과 (학기당 최대 1과목)", SUBJECTS[sem]["국수영"], default=st.session_state.choices[sem]["국수영"])
        tech_lang = st.multiselect("2️⃣ 기술·가정/정보, 제2외국어/한문 교과 (💡 학기별 최대 1과목만 선택 가능)", SUBJECTS[sem]["기가_외국어"], default=st.session_state.choices[sem]["기가_외국어"])
    with col2:
        reseaerch = st.multiselect("3️⃣ 사회 / 과학 탐구 교과", SUBJECTS[sem]["탐구"], default=st.session_state.choices[sem]["탐구"])
        etc = st.multiselect("4️⃣ 교양 및 예체능 교과 (*는 교양 필수)", SUBJECTS[sem]["교양_기타"], default=st.session_state.choices[sem]["교양_기타"]) if SUBJECTS[sem]["교양_기타"] else []

    total_cnt = len(kme) + len(tech_lang) + len(reseaerch) + len(etc)
    st.info(f"💡 현재 {sem}학기 선택한 과목 수: **{total_cnt} / 5 과목**")

    # [학기별 즉시 검증 버튼]
    if st.button(f"➔ {sem}학기 검증 및 다음 단계"):
        errors = []
        if total_cnt != 5:
            errors.append(f"❗ 학기당 정확히 **5과목**을 채워야 합니다. (현재 {total_cnt}과목)")
        if len(kme) > 1:
            errors.append("❗ 국어/수학/영어는 학기당 **최대 1과목**만 선택할 수 있습니다.")
        if len(tech_lang) > 1:
            errors.append("❗ **[신설 제약]** 기술·가정/정보, 제2외국어/한문 교과는 학기별로 **최대 1과목**만 선택 가능합니다.")
        
        # 2학년 필수 조건
        if sem in ["2-1", "2-2"] and len(tech_lang) < 1:
            errors.append(f"❗ 2학년 과정({sem})에서는 기술·가정/정보 또는 제2외국어/한문 중 **필수 1과목**을 지정해야 합니다.")
        
        # 3학년 필수 조건 (교양 뒤에 * 표시 여부로 확인)
        if sem in ["3-1", "3-2"]:
            has_liberal_art = any("*" in sub for sub in etc)
            if not has_liberal_art:
                errors.append(f"❗ 3학년 과정({sem})에서는 **교양 필수 과목(*)**을 최소 1과목 포함해야 합니다.")

        if errors:
            for err in errors:
                st.error(err)
        else:
            # 임시 세션에 저장 후 다음 단계 이동
            st.session_state.choices[sem] = {"국수영": kme, "탐구": reseaerch, "기가_외국어": tech_lang, "교양_기타": etc}
            st.session_state.step = next_step
            st.rerun()

# --- [5. 화면 라우팅 흐름] ---
if st.session_state.step == "2-1":
    render_semester_ui("2-1", "2-2")
elif st.session_state.step == "2-2":
    render_semester_ui("2-2", "3-1")
elif st.session_state.step == "3-1":
    render_semester_ui("3-1", "3-2")
elif st.session_state.step == "3-2":
    render_semester_ui("3-2", "최종확인")

# --- [6. 최종 전역 검증 및 리포트 출력] ---
elif st.session_state.step == "최종확인":
    st.subheader("🏁 전 학기 누적 제약 요건 최종 검증 리포트")
    
    # 데이터 취합
    all_kme = []
    all_tech_lang_sem_count = 0  # 기가/외국어가 선택된 학기 수 카운트
    social_cnt = 0
    science_cnt = 0
    total_credits = 0

    # 사회/과학 과목 마스터 리스트 (구분을 위함)
    social_subs = ["세계시민과 지리", "세계사", "사회와 문화", "현대사회와 윤리", "한국지리 탐구", "동아시아 역사 기행", "정치", "경제", "윤리와 사상", "도시의 미래 탐구", "법과 사회", "역사로 탐구하는 현대 세계", "사회문제 탐구", "윤리문제 탐구", "여행지리", "금융과 경제생활", "인문학과 윤리", "국제 관계의 이해", "기후변화와 지속가능한 세계"]
    science_subs = ["물리학", "화학", "생명과학", "지구과학", "역학과 에너지", "물질과 에너지", "생물의 유전", "지구시스템과학", "전자기와 양자", "화학 반응의 세계", "세포와 물질대사", "기후변화와 환경생태", "융합과학 탐구"]

    for sem in ["2-1", "2-2", "3-1", "3-2"]:
        c = st.session_state.choices[sem]
        all_kme.extend(c["국수영"])
        
        # 학기별 기가/외국어 선택 여부 카운트
        if len(c["기가_외국어"]) == 1:
            all_tech_lang_sem_count += 1
            total_credits += 3  # 과목당 3학점
            
        # 사회 과학 카운트
        for sub in c["탐구"]:
            if sub in social_subs: social_cnt += 1
            if sub in science_subs: science_cnt += 1
            
        # 교양 학점 카운트
        for sub in c["교양_기타"]:
            if "*" in sub: total_credits += 2 # 교양 과목당 2학점

    # 검증 플래그
    kme_ok = len(all_kme) <= 3
    tech_lang_sem_ok = all_tech_lang_sem_count >= 3
    social_ok = social_cnt >= 1
    science_ok = science_cnt >= 1
    credit_ok = total_credits >= 12

    # UI 출력
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 📊 검증 통과 항목")
        st.write(f"{'✅' if kme_ok else '❌'} 국·수·영 총 3과목 이하 (현재: {len(all_kme)}과목)")
        st.write(f"{'✅' if tech_lang_sem_ok else '❌'} **[신설]** 기가/정보/외국어 최소 3개 학기 이수 (현재: {all_tech_lang_sem_count}개 학기)")
        st.write(f"{'✅' if social_ok else '❌'} 사회 필수 1과목 이수 여부 (현재: {social_cnt}과목)")
        st.write(f"{'✅' if science_ok else '❌'} 과학 필수 1과목 이수 여부 (현재: {science_cnt}과목)")
        st.write(f"{'✅' if credit_ok else '❌'} 지정교과 최소 12학점 충족 여부 (현재: {total_credits}학점)")

    with col_b:
        st.markdown("### 📝 선택 과목 요약 표")
        summary_data = []
        for sem in ["2-1", "2-2", "3-1", "3-2"]:
            c = st.session_state.choices[sem]
            summary_data.append({
                "학기": sem,
                "선택 과목 목록": ", ".join(c["국수영"] + c["기가_외국어"] + c["탐구"] + c["교양_기타"])
            })
        st.table(summary_data)

    # 최종 승인 결과
    if kme_ok and tech_lang_sem_ok and social_ok and science_ok and credit_ok:
        st.balloons()
        st.success("🎉 축하합니다! 모든 고교학점제 선택 요건 및 누적 제약 조건을 완벽하게 충족했습니다. 제출이 가능합니다.")
    else:
        st.error("⚠️ 누적 제약 요건 중 미충족된 항목이 있습니다. 아래 버튼을 눌러 처음부터 다시 설계해 주세요.")

    if st.button("🔄 처음부터 다시 선택하기"):
        st.session_state.step = "2-1"
        st.session_state.choices = {sem: {"국수영": [], "탐구": [], "기가_외국어": [], "교양_기타": []} for sem in ["2-1", "2-2", "3-1", "3-2"]}
        st.rerun()
