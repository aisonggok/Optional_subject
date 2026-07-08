import streamlit as st

# --- [1. 송곡여고 개설 과목 데이터 세팅] ---
SUBJECTS = {
    "2-1": {
        "국수영": ["국어(융합): 독서 토론과 글쓰기", "수학(진로): 기하", "영어(융합): 세계 문화와 영어"],
        "탐구": ["세계시민과 지리", "세계사", "사회와 문화", "현대사회와 윤리", "물리학", "화학", "생명과학", "지구과학"],
        "기가_외국어": ["정보", "중국어", "한문"],
        "교양": [],
        "예체능": []
    },
    "2-2": {
        "국수영": ["국어(진로): 문학과 영상", "수학(융합): 수학과제 탐구", "영어(진로): 영미 문학 읽기"],
        "탐구": ["한국지리 탐구", "동아시아 역사 기행", "정치", "경제", "윤리와 사상", "역학과 에너지", "물질과 에너지", "생물의 유전", "지구시스템과학"],
        "기가_외국어": ["인공지능 기초", "중국 문화", "언어생활과 한자"],
        "교양": [],
        "예체능": []
    },
    "3-1": {
        "국수영": ["국어(진로): 주제 탐구 독서", "수학(진로): 미적분Ⅱ", "영어(융합): 미디어 영어"],
        "탐구": ["도시의 미래 탐구", "법과 사회", "역사로 탐구하는 현대 세계", "사회문제 탐구", "윤리문제 탐구", "전자기와 양자", "화학 반응의 세계", "세포와 물질대사", "지구시스템과학"],
        "기가_외국어": ["데이터 과학", "중국어 회화", "한문 고전 읽기"],
        "교양": ["교육의 이해", "보건", "논술"],
        "예체능": ["기초 체육 전공 실기", "실용음악실기Ⅰ", "미술실기Ⅰ"]
    },
    "3-2": {
        "국수영": ["국어(융합): 매체 의사소통", "수학(진로): 경제 수학", "영어(진로): 심화 영어"],
        "탐구": ["여행지리", "금융과 경제생활", "인문학과 윤리", "국제 관계의 이해", "기후변화와 지속가능한 세계", "기후변화와 환경생태", "융합과학 탐구"],
        "기가_외국어": ["소프트웨어와 생활", "심화 중국어", "생활과 한문"],
        "교양": ["생태와 환경", "논리와 사고", "인간과 심리"],
        "예체능": ["심화 체육 전공 실기", "실용음악실기Ⅱ", "미술실기Ⅱ"]
    }
}

# 마스터 탐구 과목 분류 리스트
SOCIAL_SUBS = [
    "세계시민과 지리", "세계사", "사회와 문화", "현대사회와 윤리", 
    "한국지리 탐구", "동아시아 역사 기행", "정치", "경제", "윤리와 사상", 
    "도시의 미래 탐구", "법과 사회", "역사로 탐구하는 현대 세계", "사회문제 탐구", "윤리문제 탐구", 
    "여행지리", "금융과 경제생활", "인문학과 윤리", "국제 관계의 이해", "기후변화와 지속가능한 세계"
]
SCIENCE_SUBS = [
    "물리학", "화학", "생명과학", "지구과학", 
    "역학과 에너지", "물질과 에너지", "생물의 유전", "지구시스템과학", 
    "전자기와 양자", "화학 반응의 세계", "세포와 물질대사", 
    "기후변화와 환경생태", "융합과학 탐구"
]

# --- [2. 세션 상태(State) 초기화] ---
if 'step' not in st.session_state:
    st.session_state.step = "2-1"
if 'choices' not in st.session_state:
    st.session_state.choices = {
        "2-1": {"국수영": [], "탐구": [], "기가_외국어": [], "교양": [], "예체능": []},
        "2-2": {"국수영": [], "탐구": [], "기가_외국어": [], "교양": [], "예체능": []},
        "3-1": {"국수영": [], "탐구": [], "기가_외국어": [], "교양": [], "예체능": []},
        "3-2": {"국수영": [], "탐구": [], "기가_외국어": [], "교양": [], "예체능": []},
    }

# --- [3. 페이지 설정 및 디자인] ---
st.set_page_config(page_title="송곡여고 과목 선택 시스템 v3", page_icon="🎓", layout="wide")

# 대시보드 스타일 헤더
st.markdown("""
    <div style="background-color:#1E3A8A; padding:20px; border-radius:10px; margin-bottom:25px;">
        <h1 style="color:white; margin:0; font-size:28px; text-align:center;">🎓 송곡여자고등학교 고교학점제 모의 상담 시스템</h1>
        <p style="color:#D1D5DB; margin:5px 0 0 0; text-align:center; font-size:14px;">(기능 업데이트) 지정 교과목 1과목 초과 선택 방지 시스템 적용 완료</p>
    </div>
""", unsafe_allow_html=True)

# --- [4. 사이드바: 실시간 누적 규칙 체크 대시보드] ---
st.sidebar.markdown("## 📊 실시간 누적 이수 진단")
st.sidebar.caption("과목을 선택할 때마다 실시간으로 반영됩니다.")

# 누적 데이터 계산
all_kme = []
tech_lang_sems = 0
social_cnt = 0
science_cnt = 0
tech_lang_credits = 0
liberal_credits = 0

for sem in ["2-1", "2-2", "3-1", "3-2"]:
    c = st.session_state.choices[sem]
    all_kme.extend(c["국수영"])
    if len(c["기가_외국어"]) > 0:
        tech_lang_sems += 1
        tech_lang_credits += 3 * len(c["기가_외국어"])
    for sub in c["탐구"]:
        if sub in SOCIAL_SUBS: social_cnt += 1
        if sub in SCIENCE_SUBS: science_cnt += 1
    liberal_credits += 2 * len(c["교양"])

total_credits = tech_lang_credits + liberal_credits

# 사이드바 시각적 지표 배치
st.sidebar.markdown("---")
st.sidebar.markdown("### 1. 교과별 과목 수 제한")

kme_ok = len(all_kme) <= 3
st.sidebar.metric(label="국·수·영 총합 (최대 3과목)", value=f"{len(all_kme)} / 3 개", delta="정상" if kme_ok else "초과!", delta_color="normal" if kme_ok else "inverse")

tl_sem_ok = tech_lang_sems >= 3
st.sidebar.metric(label="기가/정보/외국어 이수 학기 (최소 3학기)", value=f"{tech_lang_sems} / 4 학기", delta="만족" if tl_sem_ok else "부족", delta_color="normal" if tl_sem_ok else "inverse")

st.sidebar.markdown("### 2. 필수 이수 영역")
st.sidebar.markdown(f"{'✅' if social_cnt >= 1 else '❌'} 사회 탐구 필수 이수 (현재: {social_cnt}개)")
st.sidebar.markdown(f"{'✅' if science_cnt >= 1 else '❌'} 과학 탐구 필수 이수 (현재: {science_cnt}개)")

st.sidebar.markdown("### 3. 지정 교과 최소 학점")
credit_ok = total_credits >= 12
st.sidebar.metric(label="기가/외국어/교양 총 학점 (최소 12학점)", value=f"{total_credits} / 12 학점", delta=f"+{total_credits-12}" if credit_ok else f"-{12-total_credits}", delta_color="normal" if credit_ok else "inverse")

st.sidebar.markdown("---")
if st.sidebar.button("🔄 전체 초기화 및 처음으로"):
    st.session_state.step = "2-1"
    st.session_state.choices = {sem: {"국수영": [], "탐구": [], "기가_외국어": [], "교양": [], "예체능": []} for sem in ["2-1", "2-2", "3-1", "3-2"]}
    st.rerun()

# --- [5. 메인 화면: 단계별 진행 인디케이터] ---
steps = ["2-1", "2-2", "3-1", "3-2", "최종확인"]
cols = st.columns(len(steps))
for i, s in enumerate(steps):
    with cols[i]:
        if st.session_state.step == s:
            st.markdown(f"<div style='text-align:center; padding:10px; background-color:#3B82F6; color:white; border-radius:5px; font-weight:bold;'>🔵 {s}학기 선택</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:center; padding:10px; background-color:#F3F4F6; color:#6B7280; border-radius:5px;'>⚪ {s}</div>", unsafe_allow_html=True)
st.write("")

# --- [6. 학기별 선택 UI 구성 함수] ---
def render_semester_ui(sem, next_step):
    st.markdown(f"### 📅 {sem[0]}학년 {sem[2]}학기 과목 선택 룸")
    st.markdown("학생의 진로와 이수 규칙을 고려하여 아래 과목들을 분류별로 선택해 주세요.")
    
    with st.container():
        st.markdown("<div style='background-color:#F9FAFB; padding:20px; border-radius:8px; border:1px solid #E5E7EB;'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📕 기초 교과 및 지정 교과")
            # [핵심 수정] max_selections=1 속성을 부여하여 한 과목 선택 시 잠금 처리
            kme = st.multiselect("1. 국어 / 수학 / 영어 교과 (💡 최대 1과목)", SUBJECTS[sem]["국수영"], default=st.session_state.choices[sem]["국수영"], max_selections=1)
            tech_lang = st.multiselect("2. 기술·가정/정보, 제2외국어/한문 (💡 최대 1과목)", SUBJECTS[sem]["기가_외국어"], default=st.session_state.choices[sem]["기가_외국어"], max_selections=1)
            
            st.markdown("#### 📙 교양 교과 (*3학년 필수 영역)")
            if SUBJECTS[sem]["교양"]:
                # [핵심 수정] 교양 과목 역시 1과목만 선택 가능하도록 제한
                liberal = st.multiselect("3. 교양 과목 선택 (💡 최대 1과목)", SUBJECTS[sem]["교양"], default=st.session_state.choices[sem]["교양"], max_selections=1)
            else:
                st.caption("ℹ️ 본 학기에는 개설된 교양 과목이 없습니다.")
                liberal = []
                
        with col2:
            st.markdown("#### 📘 탐구 교과 (사회 / 과학)")
            # 탐구 영역은 남은 과목 수를 채워야 하므로 선택 개수 제한(max_selections)을 두지 않습니다.
            research = st.multiselect("4. 사회 · 과학 탐구 과목 (자유 선택)", SUBJECTS[sem]["탐구"], default=st.session_state.choices[sem]["탐구"])
            
            st.markdown("#### 🎨 예체능 및 기타 교과")
            if SUBJECTS[sem]["예체능"]:
                # [핵심 수정] 예체능 영역 1과목 초과 방지
                arts_sports = st.multiselect("5. 체육 / 예술 실기 (💡 최대 1과목)", SUBJECTS[sem]["예체능"], default=st.session_state.choices[sem]["예체능"], max_selections=1)
            else:
                st.caption("ℹ️ 본 학기에는 개설된 예체능 과목이 없습니다.")
                arts_sports = []
                
        st.markdown("</div>", unsafe_allow_html=True)

    # 실시간 선택 수치 브리핑
    total_cnt = len(kme) + len(tech_lang) + len(research) + len(liberal) + len(arts_sports)
    
    if total_cnt == 5:
        st.success(f"✅ 현재 정확히 {total_cnt}과목을 선택하셨습니다. (기준 충족)")
    else:
        st.warning(f"⚠️ 현재 {total_cnt}과목 선택됨. 학기당 반드시 **정확히 5과목**을 채워야 합니다.")

    # [검증 및 다음 단계 이동 로직]
    if st.button(f"➔ {sem}학기 선택 완료 및 규칙 검증"):
        errors = []
        if total_cnt != 5:
            errors.append(f"❌ 학기당 과목 수는 정확히 **5과목**이어야 합니다. (현재 {total_cnt}과목)")
        
        # 2학년 학기별 지정 교과 필수 요건
        if sem in ["2-1", "2-2"] and len(tech_lang) < 1:
            errors.append(f"❌ 2학년 과정({sem})에서는 기술·가정/정보 또는 제2외국어/한문 중 **학기별 필수 1과목**을 지정해야 합니다.")
        
        # 3학년 학기별 교양 필수 요건
        if sem in ["3-1", "3-2"] and len(liberal) < 1:
            errors.append(f"❌ 3학년 과정({sem})에서는 **교양 과목을 한 학기에 최소 1과목** 필수 이수해야 합니다.")

        if errors:
            for err in errors:
                st.error(err)
        else:
            # 이상 없을 시 세션 상태에 저장 후 새로고침 이동
            st.session_state.choices[sem] = {
                "국수영": kme, "탐구": research, "기가_외국어": tech_lang, "교양": liberal, "예체능": arts_sports
            }
            st.session_state.step = next_step
            st.rerun()

# --- [7. 라우팅 실행] ---
if st.session_state.step == "2-1":
    render_semester_ui("2-1", "2-2")
elif st.session_state.step == "2-2":
    render_semester_ui("2-2", "3-1")
elif st.session_state.step == "3-1":
    render_semester_ui("3-1", "3-2")
elif st.session_state.step == "3-2":
    render_semester_ui("3-2", "최종확인")

# --- [8. 최종 누적 검증 스크린] ---
elif st.session_state.step == "최종확인":
    st.markdown("### 🏁 전 학기 누적 조건 최종 스크린 검증")
    
    # 최종 결과 판단 플래그
    final_errors = []
    if len(all_kme) > 3:
        final_errors.append(f"❌ 국·수·영 교과 총합 제한 초과 (최대 3과목 이하 규칙 / 현재 {len(all_kme)}과목)")
    if tech_lang_sems < 3:
        final_errors.append(f"❌ 기술·가정/정보, 제2외국어/한문 교과 최소 이수 학기 부족 (최소 3개 학기 필수 / 현재 {tech_lang_sems}개 학기)")
    if social_cnt < 1:
        final_errors.append("❌ 사회 탐구 과목 미이수 (최소 1과목 필수)")
    if science_cnt < 1:
        final_errors.append("❌ 과학 탐구 과목 미이수 (최소 1과목 필수)")
    if total_credits < 12:
        final_errors.append(f"❌ 지정교과(기가/외국어/교양) 최소 이수 학점 미달 (최소 12학점 필수 / 현재 {total_credits}학점)")

    # 시각적 가독성을 높인 최종 리포트 배치
    col_res1, col_res2 = st.columns([2, 3])
    
    with col_res1:
        st.markdown("#### 📋 조건 합격 여부 요약")
        st.markdown(f"{'✅' if len(all_kme)<=3 else '❌'} **국·수·영 총 3과목 이하:** {len(all_kme)}과목")
        st.markdown(f"{'✅' if tech_lang_sems>=3 else '❌'} **기가/외국어 최소 3개 학기:** {tech_lang_sems}개 학기")
        st.markdown(f"{'✅' if social_cnt>=1 else '❌'} **사회 교과 1과목 이상 이수:** {social_cnt}과목")
        st.markdown(f"{'✅' if science_cnt>=1 else '❌'} **과학 교과 1과목 이상 이수:** {science_cnt}과목")
        st.markdown(f"{'✅' if total_credits>=12 else '❌'} **지정교과 최소 12학점 충족:** {total_credits}학점")
        
        st.write("")
        if not final_errors:
            st.balloons()
            st.success("🎉 모든 졸업 및 선택 교육과정 제약 규칙을 완벽하게 충족했습니다! 최종 제출이 가능합니다.")
        else:
            st.error("⚠️ 누적 규칙 미충족 사항이 발견되었습니다. 왼쪽의 사이드바 지표를 참고하여 재설정해 주세요.")
            
    with col_res2:
        st.markdown("#### 📋 학생 선택 과목 타임라인 요약")
        
        # 가독성 높은 표 형태로 재가공
        summary_list = []
        for sem in ["2-1", "2-2", "3-1", "3-2"]:
            c = st.session_state.choices[sem]
            summary_list.append({
                "학기": f"{sem[0]}학년 {sem[2]}학기",
                "기초(국수영)": ", ".join(c["국수영"]) if c["국수영"] else "-",
                "지정(기가/외국어)": ", ".join(c["기가_외국어"]) if c["기가_외국어"] else "-",
                "탐구(사/과)": ", ".join(c["탐구"]) if c["탐구"] else "-",
                "교양": ", ".join(c["교양"]) if c["교양"] else "-",
                "예체능": ", ".join(c["예체능"]) if c["예체능"] else "-"
            })
        st.table(summary_list)
        
    if st.button("🔄 전체 초기화 후 다시 설계하기"):
        st.session_state.step = "2-1"
        st.session_state.choices = {sem: {"국수영": [], "탐구": [], "기가_외국어": [], "교양": [], "예체능": []} for sem in ["2-1", "2-2", "3-1", "3-2"]}
        st.rerun()
