import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration with a cute title
st.set_page_config(
    page_title="냉장고 파먹기 🥦",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injected CSS for cute pastel styling and custom animations
st.markdown("""
<style>
/* Import Gowun Dodum & Outfit fonts */
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Outfit:wght@300;400;600&display=swap');

/* Base Styles */
html, body, [class*="css"] {
    font-family: 'Gowun Dodum', 'Outfit', sans-serif !important;
    background-color: #FFFDF9; /* Warm warm cream background */
}

/* App Header styling */
.header-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    background: linear-gradient(135deg, #FFE5D9 0%, #FFCAD4 100%);
    border-radius: 24px;
    margin-bottom: 25px;
    border: 3px dashed #FFB4A2;
}

.main-title {
    color: #F07167;
    font-size: 2.8rem;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 0px;
    text-shadow: 2px 2px 0px #FFFFFF;
}

.main-subtitle {
    color: #6D4C41;
    font-size: 1.15rem;
    margin-top: 5px;
    font-weight: 500;
}

/* Category header badge */
.category-badge {
    background-color: #F07167;
    color: white;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: bold;
    display: inline-block;
    margin-bottom: 10px;
    box-shadow: 0 4px 6px rgba(240, 113, 103, 0.2);
}

/* Card Container Styles */
.recipe-card {
    background-color: #FFFFFF;
    border: 2px solid #FFE5D9;
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 20px;
    box-shadow: 0 8px 16px rgba(255, 180, 162, 0.12);
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out, border-color 0.2s;
}

.recipe-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(255, 180, 162, 0.22);
    border-color: #F07167;
}

.recipe-card-title {
    color: #D94E43;
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.recipe-card-description {
    color: #5C5C5C;
    font-size: 0.95rem;
    line-height: 1.5;
    margin-bottom: 12px;
}

/* Custom Badges */
.badge-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 12px;
}

.badge-tag {
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: bold;
}

.badge-time {
    background-color: #FFF0EC;
    color: #F07167;
    border: 1px solid #FFCAD4;
}

.badge-author {
    background-color: #E8F0FE;
    color: #1A73E8;
    border: 1px solid #D2E3FC;
}

.badge-microwave {
    background-color: #FFF9C4;
    color: #F57F17;
    border: 1px solid #FFF59D;
}

.badge-general {
    background-color: #E8F5E9;
    color: #2E7D32;
    border: 1px solid #C8E6C9;
}

.badge-match-high {
    background-color: #E8F5E9;
    color: #2E7D32;
    border: 2px solid #81C784;
}

.badge-match-medium {
    background-color: #FFF3E0;
    color: #E65100;
    border: 2px solid #FFB74D;
}

.badge-match-none {
    background-color: #FFEBEE;
    color: #C62828;
    border: 2px solid #EF9A9A;
}

/* Ingredients list format */
.ingredients-text {
    font-size: 0.85rem;
    color: #7A7A7A;
    background-color: #FAFAFA;
    padding: 8px 12px;
    border-radius: 12px;
    border: 1px solid #EEEEEE;
    margin-bottom: 12px;
}

/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background-color: #FFF5F3 !important;
    border-right: 2px solid #FFE5D9;
}

.sidebar-title {
    color: #F07167;
    font-weight: bold;
    font-size: 1.25rem;
    margin-bottom: 15px;
    text-align: center;
}

/* Custom separator line */
.cute-hr {
    border: 0;
    height: 3px;
    background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(255, 180, 162, 0.75), rgba(0, 0, 0, 0));
    margin: 20px 0;
}

/* Form Styles */
.form-container {
    background-color: #FFFDF9;
    border: 2px solid #FFCAD4;
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 25px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.02);
}

</style>
""", unsafe_allow_html=True)

# ----------------- DATA PREPARATION -----------------

# Set initial default recipes if not in session state
if "recipes" not in st.session_state:
    st.session_state.recipes = [
        {
            "id": 1,
            "title": "초간단 김치볶음밥 🍳",
            "description": "반찬 없을 때 최고! 매콤새콤하고 고소한 자취생 필수 김치볶음밥",
            "type": "일반",
            "ingredients": ["김치", "즉석밥(햇반)", "계란", "간장", "참기름"],
            "steps": [
                "김치를 가위로 잘게 썰어줍니다.",
                "팬에 식용유를 두르고 김치를 충분히 볶아줍니다.",
                "김치가 나른해지면 간장 1스푼을 팬 가장자리에 부어 백종원식 불맛을 냅니다.",
                "즉석밥(데우지 않은 찬밥 상태)을 넣고 국자로 꾹꾹 누르며 잘 섞어 볶아줍니다.",
                "마지막에 불을 끄고 참기름을 한 바퀴 두른 뒤, 계란후라이를 반숙으로 올려 마무리합니다."
            ],
            "author": "자취대장",
            "likes": 42,
            "is_custom": False,
            "prep_time": 10
        },
        {
            "id": 2,
            "title": "5분 완성 계란간장밥 🧈",
            "description": "요리하기 귀찮은 날, 버터 한 조각으로 극상의 고소함을 느끼는 꿀맛 한 그릇",
            "type": "일반",
            "ingredients": ["즉석밥(햇반)", "계란", "간장", "참기름", "버터"],
            "steps": [
                "즉석밥을 전자레인지에 뜨겁게 데워 그릇에 담습니다 (약 2분).",
                "따뜻한 밥 위에 버터 반 조각을 얹어 자연스럽게 녹입니다.",
                "계란후라이를 반숙으로 구워 밥 위에 얹습니다.",
                "간장 1.5스푼, 참기름 1스푼을 넣고 슥슥 비벼 노른자와 섞어 먹습니다."
            ],
            "author": "레시피봇",
            "likes": 28,
            "is_custom": False,
            "prep_time": 5
        },
        {
            "id": 3,
            "title": "해장 직빵 부대라면 🍜",
            "description": "스팸과 소시지, 치즈가 어우러져 깊고 진한 국물 맛을 내는 부대찌개풍 라면",
            "type": "일반",
            "ingredients": ["라면사리", "스팸", "소시지", "김치", "대파", "모짜렐라 치즈"],
            "steps": [
                "냄비에 물을 550ml 넣고 김치 약간과 송송 썬 대파를 넣어 먼저 끓입니다.",
                "스팸은 얇게 썰고 소시지는 어긋썰어 준비합니다.",
                "물이 끓으면 라면 스프와 면, 썰어둔 스팸, 소시지를 함께 넣습니다.",
                "면이 거의 익어가면 불을 끄고 위에 슬라이스 치즈나 모짜렐라 치즈를 얹은 뒤 뚜껑을 덮어 1분간 녹여 완성합니다."
            ],
            "author": "라면고수",
            "likes": 56,
            "is_custom": False,
            "prep_time": 15
        },
        {
            "id": 4,
            "title": "토마토 달걀볶음 (토달볶) 🍅",
            "description": "다이어트에도 좋고 건강에도 좋은 부드럽고 상큼한 중국식 가정식 요리",
            "type": "일반",
            "ingredients": ["토마토", "계란", "대파", "간장", "설탕"],
            "steps": [
                "토마토는 먹기 좋은 크기로 썰고, 대파는 송송 썰어줍니다.",
                "계란을 풀어 소금 한 꼬집을 넣고 팬에서 스크램블 에그를 만들어 따로 그릇에 덜어둡니다.",
                "팬에 다시 기름을 두르고 대파를 볶아 파기름을 낸 뒤 토마토를 넣어 즙이 촉촉하게 나올 때까지 볶습니다.",
                "간장 1스푼, 설탕 0.5스푼을 넣어 간을 한 뒤 덜어둔 계란을 합쳐 가볍게 볶아냅니다."
            ],
            "author": "다이어터",
            "likes": 19,
            "is_custom": False,
            "prep_time": 8
        },
        {
            "id": 5,
            "title": "푸딩처럼 촉촉한 전자레인지 계란찜 💛",
            "description": "설거지 걱정 끝! 머그컵이나 내열용기로 뚝딱 만드는 초스피드 반찬",
            "type": "전자레인지",
            "ingredients": ["계란", "대파", "참기름", "설탕"],
            "steps": [
                "내열 용기나 머그컵에 계란 2개를 깨뜨려 넣고 젓가락으로 알끈을 풀며 잘 저어줍니다.",
                "물 100ml(계란 양과 1:1 비율)와 소금 반 티스푼, 설탕 한 꼬집을 넣고 섞어줍니다.",
                "송송 썬 대파를 올리고 고소함을 위해 참기름 한두 방울을 위에 떨어뜨립니다.",
                "용기에 랩을 씌우고 포크로 숨구멍을 3-4개 뚫어줍니다.",
                "전자레인지에 넣고 3분간 조리합니다 (익지 않았다면 30초 추가)."
            ],
            "author": "기숙사요정",
            "likes": 65,
            "is_custom": False,
            "prep_time": 5
        },
        {
            "id": 6,
            "title": "전자레인지 3분 마요콘치즈 🌽",
            "description": "단짠단짠의 정석! 맥주 안주로도, 밥반찬으로도 환상적인 마법의 치즈 조합",
            "type": "전자레인지",
            "ingredients": ["모짜렐라 치즈", "마요네즈", "설탕", "버터"],
            "steps": [
                "내열용기에 물기를 뺀 스위트콘(혹은 참치캔 내용물과 함께) 1컵을 담습니다.",
                "마요네즈 2스푼, 설탕 0.5스푼을 넣고 골고루 섞어 평평하게 펴줍니다.",
                "버터 한 조각을 작게 잘라 군데군데 얹어줍니다.",
                "위에 모짜렐라 치즈를 빈틈없이 듬뿍 얹어줍니다.",
                "전자레인지에서 치즈가 완전히 녹아 지글거릴 때까지 약 2분~2분 30초간 돌려줍니다."
            ],
            "author": "치즈러버",
            "likes": 48,
            "is_custom": False,
            "prep_time": 4
        },
        {
            "id": 7,
            "title": "전자레인지 참치마요 덮밥 🐟",
            "description": "불 없이 만드는 초스피드 꿀맛 한 그릇! 캔참치와 마요네즈의 사기 조합",
            "type": "전자레인지",
            "ingredients": ["참치캔", "즉석밥(햇반)", "마요네즈", "계란", "간장", "참기름"],
            "steps": [
                "즉석밥을 전자레인지에 데워 동그란 대접에 예쁘게 담습니다.",
                "참치캔의 기름을 적당히 뺀 후 밥 위에 도톰하게 올려줍니다.",
                "그릇 한쪽 구석에 계란 1개를 깨 넣고 노른자를 터뜨린 뒤 전자레인지에 1분간 돌려 살짝 익힙니다.",
                "마요네즈를 지그재그로 예쁘게 뿌리고, 참기름 0.5스푼과 간장 0.5스푼을 더해 비벼 먹습니다."
            ],
            "author": "참치대장",
            "likes": 39,
            "is_custom": False,
            "prep_time": 5
        },
        {
            "id": 8,
            "title": "컵 하나로 끝내는 치즈 떡볶이 🌶️",
            "description": "기숙사에서 떡볶이가 당길 때 번거로운 냄비 조리 없이 컵 하나로 매콤달콤",
            "type": "전자레인지",
            "ingredients": ["떡볶이떡", "고추장", "설탕", "간장", "대파", "모짜렐라 치즈"],
            "steps": [
                "머그컵이나 깊은 내열용기에 떡볶이 떡 한 줌을 물에 가볍게 헹궈 넣습니다.",
                "물 50ml, 고추장 1스푼, 설탕 1스푼, 간장 0.5스푼을 넣고 떡과 양념을 잘 풀어 섞어줍니다.",
                "송송 썬 대파를 약간 올린 뒤 랩을 느슨하게 씌워 전자레인지에 2분간 돌립니다.",
                "꺼내서 한번 섞어준 뒤 모짜렐라 치즈를 솔솔 뿌려 다시 1분간 돌려 치즈를 녹입니다."
            ],
            "author": "떡볶이매니아",
            "likes": 72,
            "is_custom": False,
            "prep_time": 7
        }
    ]

# Ingredients categories for selection
INGREDIENT_CATEGORIES = {
    "🥬 채소류": ["김치", "대파", "양파", "마늘", "토마토", "감자", "당근", "버섯"],
    "🍖 단백질류": ["계란", "참치캔", "스팸", "소시지", "베이컨", "돼지고기", "닭고기", "두부"],
    "🍚 탄수화물": ["즉석밥(햇반)", "라면사리", "떡볶이떡", "파스타면"],
    "🍯 소스 & 치즈": ["간장", "참기름", "고추장", "설탕", "마요네즈", "굴소스", "모짜렐라 치즈", "버터"]
}

# Flatten list of all default ingredients
ALL_INGREDIENTS = []
for k, v in INGREDIENT_CATEGORIES.items():
    ALL_INGREDIENTS.extend(v)

# ----------------- APP LAYOUT & SIDEBAR -----------------

# Cute Top Header Banner
col_logo_left, col_logo_center, col_logo_right = st.columns([1, 2, 1])
with col_logo_center:
    try:
        st.image("cute_fridge.png", width=220)
    except Exception:
        # Fallback if image not found
        st.write("🥦🍳🌶️🍔🧀")

st.markdown("""
<div class="header-container">
    <div class="main-title">말랑말랑 냉장고 파먹기 🥦</div>
    <div class="main-subtitle">내 냉장고 속 남은 식재료로 쉽고 맛있고 귀여운 요리를 시작해봐요!</div>
</div>
""", unsafe_allow_html=True)

# Cute Sidebar for Ingredient Input
with st.sidebar:
    st.markdown('<div class="sidebar-title">내 냉장고 채우기 🧺</div>', unsafe_allow_html=True)
    st.write("보유하고 있는 재료들을 선택해 주세요! 매칭률이 계산됩니다.")
    
    selected_ingredients = []
    
    # Render multi-select grouped by categories
    for category, items in INGREDIENT_CATEGORIES.items():
        with st.expander(category, expanded=True):
            for item in items:
                # Use unique key for checkbox
                if st.checkbox(item, key=f"sb_{item}"):
                    selected_ingredients.append(item)
                    
    # Custom ingredient text input
    custom_in = st.text_input("목록에 없는 재료 추가 (쉼표로 구분)", placeholder="치즈, 양배추...")
    if custom_in:
        custom_items = [x.strip() for x in custom_in.split(",") if x.strip()]
        selected_ingredients.extend(custom_items)
        
    st.markdown('<hr class="cute-hr">', unsafe_allow_html=True)
    st.write(f"현재 보유 재료: **{len(selected_ingredients)}**개")
    if selected_ingredients:
        st.caption(", ".join(selected_ingredients))
    else:
        st.caption("재료를 선택하면 레시피 매칭이 시작돼요!")

# ----------------- TABS SETUP -----------------

tab1, tab2, tab3, tab4 = st.tabs([
    "🥦 냉장고 털기 (맞춤 레시피)", 
    "⚡ 초간단 전자레인지 탭", 
    "✍️ 나만의 레시피 (자유게시판)", 
    "🏆 명예의 전당 (인기 랭킹)"
])

# Helper function to compute ingredient match percentage
def calculate_match(recipe_ingredients, selected_list):
    if not selected_list:
        return 0, recipe_ingredients, []
    
    matched = list(set(recipe_ingredients) & set(selected_list))
    missing = list(set(recipe_ingredients) - set(selected_list))
    
    percentage = int((len(matched) / len(recipe_ingredients)) * 100)
    return percentage, matched, missing

# Helper function to display recipe detail modal-like window inside Streamlit using st.dialog
@st.dialog("레시피 상세 보기 📖", width="large")
def show_recipe_detail(recipe, matched, missing, match_pct):
    # Cute title
    st.subheader(recipe["title"])
    st.caption(f"작성자: {recipe['author']} | 조리시간: 약 {recipe['prep_time']}분")
    st.write(f"*{recipe['description']}*")
    
    st.markdown('<hr class="cute-hr">', unsafe_allow_html=True)
    
    # Ingredient status
    col_ing1, col_ing2 = st.columns(2)
    with col_ing1:
        st.write("🟢 **나한테 있는 재료**:")
        if matched:
            st.write(", ".join([f"`{m}`" for m in matched]))
        else:
            st.write("없음")
            
    with col_ing2:
        st.write("🔴 **부족한 재료**:")
        if missing:
            st.write(", ".join([f"`{m}`" for m in missing]))
        else:
            st.write("🎉 **모든 재료 보유 중!**")
            
    st.markdown('<hr class="cute-hr">', unsafe_allow_html=True)
    
    # Cooking Steps
    st.write("### 👩‍🍳 조리 순서")
    for idx, step in enumerate(recipe["steps"], 1):
        st.markdown(f"**{idx}.** {step}")
        
    st.write("")
    
    # Bottom actions in dialog
    col_like, col_close = st.columns([1, 4])
    with col_like:
        # We need to find the recipe index and add likes inside session state
        if st.button("❤️ 추천!", key=f"detail_like_{recipe['id']}"):
            for r in st.session_state.recipes:
                if r["id"] == recipe["id"]:
                    r["likes"] += 1
                    break
            st.success("추천 완료! (창을 닫으면 갱신됩니다)")
            st.rerun()

# ----------------- TAB 1: FRIDGE MATCHING -----------------
with tab1:
    st.markdown('<div class="category-badge">보유 식재료 매칭 레시피</div>', unsafe_allow_html=True)
    st.write("내가 가진 식재료와 매칭률이 높은 레시피들을 추천해 줍니다. 원하는 정렬 방식을 선택해 보세요.")
    
    # Sort and Filter Controls
    col_sort1, col_sort2, col_sort3 = st.columns([2, 1, 1])
    with col_sort1:
        search_query = st.text_input("🔍 레시피 제목 또는 식재료 검색", placeholder="예: 김치, 계란...")
    with col_sort2:
        sort_by = st.selectbox(
            "정렬 방식", 
            ["매칭률 높은 순 🌟", "인기순 (추천수) ❤️", "최신 등록순 🕒"]
        )
    with col_sort3:
        filter_type = st.selectbox(
            "요리 분류",
            ["전체보기", "일반 요리", "전자레인지 요리"]
        )
        
    # Process recipes data
    processed_recipes = []
    for r in st.session_state.recipes:
        # Search filter
        if search_query:
            query = search_query.strip().lower()
            ingredients_str = " ".join(r["ingredients"]).lower()
            if query not in r["title"].lower() and query not in r["description"].lower() and query not in ingredients_str:
                continue
                
        # Type filter
        if filter_type == "일반 요리" and r["type"] != "일반":
            continue
        elif filter_type == "전자레인지 요리" and r["type"] != "전자레인지":
            continue
            
        # Calculate matching rate
        pct, matched, missing = calculate_match(r["ingredients"], selected_ingredients)
        
        processed_recipes.append({
            "recipe": r,
            "match_pct": pct,
            "matched": matched,
            "missing": missing
        })
        
    # Sort logic
    if sort_by == "매칭률 높은 순 🌟":
        processed_recipes.sort(key=lambda x: (-x["match_pct"], -x["recipe"]["likes"]))
    elif sort_by == "인기순 (추천수) ❤️":
        processed_recipes.sort(key=lambda x: -x["recipe"]["likes"])
    else: # 최신 등록순
        processed_recipes.sort(key=lambda x: -x["recipe"]["id"])
        
    # Render recipes grid
    if not processed_recipes:
        st.warning("조건에 맞는 레시피가 없어요 😢 다른 재료를 선택하거나 레시피를 직접 등록해 보세요!")
    else:
        # Display in columns (2 cards per row)
        cols = st.columns(2)
        for idx, item in enumerate(processed_recipes):
            r = item["recipe"]
            col_target = cols[idx % 2]
            
            with col_target:
                # Custom badge class for match rate
                match_class = "badge-match-none"
                if item["match_pct"] >= 80:
                    match_class = "badge-match-high"
                elif item["match_pct"] > 0:
                    match_class = "badge-match-medium"
                    
                match_text = f"매칭률 {item['match_pct']}%"
                if item['match_pct'] == 100:
                    match_text += " (재료 완료! 🌟)"
                
                # Setup HTML layout inside markdown
                badge_type_html = f'<span class="badge-tag badge-microwave">⚡ 전자레인지</span>' if r["type"] == "전자레인지" else f'<span class="badge-tag badge-general">🍳 일반요리</span>'
                
                st.markdown(f"""
                <div class="recipe-card">
                    <div class="recipe-card-title">{r['title']}</div>
                    <div class="badge-container">
                        {badge_type_html}
                        <span class="badge-tag badge-time">⏱️ {r['prep_time']}분</span>
                        <span class="badge-tag badge-author">👤 {r['author']}</span>
                        <span class="badge-tag {match_class}">💡 {match_text}</span>
                    </div>
                    <div class="recipe-card-description">{r['description']}</div>
                    <div class="ingredients-text">🥕 필요 재료: {", ".join(r['ingredients'])}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Interaction buttons below markdown card
                col_btn1, col_btn2 = st.columns([1, 1])
                with col_btn1:
                    if st.button("상세 레시피 보기 🔍", key=f"view_{r['id']}_{idx}"):
                        show_recipe_detail(r, item["matched"], item["missing"], item["match_pct"])
                with col_btn2:
                    if st.button(f"❤️ 추천하기 ({r['likes']})", key=f"like_{r['id']}_{idx}"):
                        for original_r in st.session_state.recipes:
                            if original_r["id"] == r["id"]:
                                original_r["likes"] += 1
                                break
                        st.success("레시피를 추천했습니다! 👍")
                        st.rerun()
                st.write("") # Spacer

# ----------------- TAB 2: MICROWAVE ONLY -----------------
with tab2:
    st.markdown('<div class="category-badge" style="background-color:#F57F17;">기숙사생을 위한 초간단 전자레인지 탭</div>', unsafe_allow_html=True)
    st.write("가스레인지나 에어프라이어가 없어도 걱정 마세요! 오직 전자레인지만으로 만들 수 있는 기숙사 맞춤형 황금 레시피입니다. ⚡")
    
    # Mini banner tip
    st.info("💡 **기숙사 꿀팁:** 전자레인지 조리 시에는 수분이 날아가지 않도록 랩을 씌우고 포크로 숨구멍을 뚫어주는 것이 촉촉함의 핵심입니다! 또한 쇠그릇이나 은박지 그릇은 화재 위험이 있으니 꼭 내열유리/내열플라스틱/머그컵을 사용해 주세요.")
    
    # Filter only microwave
    mw_recipes = [r for r in st.session_state.recipes if r["type"] == "전자레인지"]
    
    # Sort selector for microwave recipes
    mw_sort = st.radio("정렬 기준", ["인기순", "이름순", "최신순"], horizontal=True, key="mw_sort")
    if mw_sort == "인기순":
        mw_recipes.sort(key=lambda x: -x["likes"])
    elif mw_sort == "이름순":
        mw_recipes.sort(key=lambda x: x["title"])
    else:
        mw_recipes.sort(key=lambda x: -x["id"])
        
    cols = st.columns(2)
    for idx, r in enumerate(mw_recipes):
        col_target = cols[idx % 2]
        with col_target:
            # Check match status for current selected ingredients
            pct, matched, missing = calculate_match(r["ingredients"], selected_ingredients)
            match_class = "badge-match-none"
            if pct >= 80:
                match_class = "badge-match-high"
            elif pct > 0:
                match_class = "badge-match-medium"
                
            st.markdown(f"""
            <div class="recipe-card" style="border-left: 5px solid #F57F17;">
                <div class="recipe-card-title">{r['title']}</div>
                <div class="badge-container">
                    <span class="badge-tag badge-microwave">⚡ 전자레인지 전용</span>
                    <span class="badge-tag badge-time">⏱️ {r['prep_time']}분</span>
                    <span class="badge-tag badge-author">👤 {r['author']}</span>
                    <span class="badge-tag {match_class}">💡 매칭률 {pct}%</span>
                </div>
                <div class="recipe-card-description">{r['description']}</div>
                <div class="ingredients-text">🧀 재료 목록: {", ".join(r['ingredients'])}</div>
            </div>
            """, unsafe_allow_html=True)
            
            col_btn1, col_btn2 = st.columns([1, 1])
            with col_btn1:
                if st.button("상세 조리방법 보기 🔍", key=f"mw_view_{r['id']}"):
                    show_recipe_detail(r, matched, missing, pct)
            with col_btn2:
                if st.button(f"❤️ 추천 ({r['likes']})", key=f"mw_like_{r['id']}"):
                    for original_r in st.session_state.recipes:
                        if original_r["id"] == r["id"]:
                            original_r["likes"] += 1
                            break
                    st.success("레시피를 추천했습니다! 👍")
                    st.rerun()
            st.write("") # Spacer

# ----------------- TAB 3: CUSTOM BOARD (CRUD) -----------------
with tab3:
    st.markdown('<div class="category-badge" style="background-color:#1A73E8;">자취생 요리 뽐내기 게시판</div>', unsafe_allow_html=True)
    st.write("나만 알기 아까운 꿀맛 보장 커스텀 레시피를 공유해 주세요! 언제든지 수정 및 삭제가 가능합니다.")
    
    # Initialize add/edit status in session_state
    if "board_action" not in st.session_state:
        st.session_state.board_action = "view"  # "view", "create", "edit"
    if "edit_target_id" not in st.session_state:
        st.session_state.edit_target_id = None
        
    # --- RENDER FORM FOR CREATION OR EDIT ---
    if st.session_state.board_action == "create":
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.subheader("🍳 나만의 황금 레시피 등록")
        
        with st.form("recipe_create_form"):
            c_title = st.text_input("레시피 이름 (귀여운 이모티콘을 붙여주면 더 좋아요!)", placeholder="예: 불닭 치즈 삼각김밥 덮밥 🍙")
            c_desc = st.text_input("간단한 한 줄 설명", placeholder="예: 불닭의 매콤함과 고소한 치즈가 어우러진 스트레스 해소 요리")
            
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                c_type = st.selectbox("조리 방식 선택", ["일반", "전자레인지"])
            with col_c2:
                c_time = st.number_input("조리 시간 (분)", min_value=1, max_value=120, value=10)
                
            c_ingredients = st.text_area("필요 식재료 (쉼표로 구분해서 입력해 주세요)", placeholder="예: 즉석밥(햇반), 참치캔, 마요네즈, 김치")
            c_steps = st.text_area("조리 순서 (한 줄에 한 단계를 입력하고 엔터(줄바꿈)를 쳐주세요)", placeholder="1. 밥을 그릇에 담습니다.\n2. 참치를 얹고 마요네즈를 뿌립니다.")
            c_author = st.text_input("닉네임", placeholder="예: 신촌자취러")
            
            col_form_btns = st.columns([1, 1, 4])
            with col_form_btns[0]:
                submit_create = st.form_submit_button("등록 완료 ✨")
            with col_form_btns[1]:
                cancel_create = st.form_submit_button("취소 ❌")
                
            if submit_create:
                if not c_title or not c_ingredients or not c_steps or not c_author:
                    st.error("앗! 레시피 이름, 재료, 조리 순서, 닉네임은 필수 항목입니다 🥺")
                else:
                    new_id = max([x["id"] for x in st.session_state.recipes]) + 1 if st.session_state.recipes else 1
                    # Parse ingredients and steps
                    ing_list = [x.strip() for x in c_ingredients.split(",") if x.strip()]
                    step_list = [x.strip() for x in c_steps.split("\n") if x.strip()]
                    
                    st.session_state.recipes.append({
                        "id": new_id,
                        "title": c_title,
                        "description": c_desc,
                        "type": c_type,
                        "ingredients": ing_list,
                        "steps": step_list,
                        "author": c_author,
                        "likes": 0,
                        "is_custom": True,
                        "prep_time": int(c_time)
                    })
                    st.success("축하합니다! 새로운 레시피가 등록되었습니다! 🎉")
                    st.session_state.board_action = "view"
                    st.rerun()
                    
            if cancel_create:
                st.session_state.board_action = "view"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif st.session_state.board_action == "edit" and st.session_state.edit_target_id is not None:
        # Find target recipe
        recipe_to_edit = None
        for r in st.session_state.recipes:
            if r["id"] == st.session_state.edit_target_id:
                recipe_to_edit = r
                break
                
        if recipe_to_edit:
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            st.subheader(f"✍️ {recipe_to_edit['title']} 레시피 수정하기")
            
            with st.form("recipe_edit_form"):
                e_title = st.text_input("레시피 이름", value=recipe_to_edit["title"])
                e_desc = st.text_input("간단한 한 줄 설명", value=recipe_to_edit["description"])
                
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    # Resolve initial index
                    type_idx = 0 if recipe_to_edit["type"] == "일반" else 1
                    e_type = st.selectbox("조리 방식 선택", ["일반", "전자레인지"], index=type_idx)
                with col_e2:
                    e_time = st.number_input("조리 시간 (분)", min_value=1, max_value=120, value=recipe_to_edit["prep_time"])
                    
                e_ingredients = st.text_area("필요 식재료 (쉼표로 구분)", value=", ".join(recipe_to_edit["ingredients"]))
                e_steps = st.text_area("조리 순서 (한 줄에 한 단계)", value="\n".join(recipe_to_edit["steps"]))
                e_author = st.text_input("닉네임", value=recipe_to_edit["author"])
                
                col_form_btns = st.columns([1, 1, 4])
                with col_form_btns[0]:
                    submit_edit = st.form_submit_button("수정 완료 💾")
                with col_form_btns[1]:
                    cancel_edit = st.form_submit_button("취소 ❌")
                    
                if submit_edit:
                    if not e_title or not e_ingredients or not e_steps or not e_author:
                        st.error("필수 입력란을 모두 채워주세요!")
                    else:
                        # Update inside session state
                        for r in st.session_state.recipes:
                            if r["id"] == recipe_to_edit["id"]:
                                r["title"] = e_title
                                r["description"] = e_desc
                                r["type"] = e_type
                                r["ingredients"] = [x.strip() for x in e_ingredients.split(",") if x.strip()]
                                r["steps"] = [x.strip() for x in e_steps.split("\n") if x.strip()]
                                r["author"] = e_author
                                r["prep_time"] = int(e_time)
                                break
                        st.success("레시피가 성공적으로 수정되었습니다! 🌈")
                        st.session_state.board_action = "view"
                        st.session_state.edit_target_id = None
                        st.rerun()
                        
                if cancel_edit:
                    st.session_state.board_action = "view"
                    st.session_state.edit_target_id = None
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
    # --- RENDER BOARD LIST ---
    if st.session_state.board_action == "view":
        col_board_top1, col_board_top2 = st.columns([4, 1])
        with col_board_top1:
            st.write("자취생 및 기숙사생 요리연구가들의 보물 같은 요리 기록들입니다. 나만의 맛있는 레시피가 있다면 자랑해 주세요!")
        with col_board_top2:
            if st.button("🍳 내 레시피 자랑하기", use_container_width=True):
                st.session_state.board_action = "create"
                st.rerun()
                
        st.markdown('<hr class="cute-hr">', unsafe_allow_html=True)
        
        # Split community into Custom Recipes vs Default Recipes
        # Users can view all, but edit/delete only custom ones.
        board_recipes = sorted(st.session_state.recipes, key=lambda x: -x["id"])
        
        for idx, r in enumerate(board_recipes):
            badge_custom = "💡 사용자 레시피" if r["is_custom"] else "⭐ 공식 레시피"
            badge_custom_style = "background-color: #E2F0CB; color: #556B2F; border: 1px solid #C8E6C9;" if r["is_custom"] else "background-color: #FFF0F5; color: #C71585; border: 1px solid #FFB6C1;"
            
            badge_type_html = f'<span class="badge-tag badge-microwave">⚡ 전자레인지</span>' if r["type"] == "전자레인지" else f'<span class="badge-tag badge-general">🍳 일반요리</span>'
            
            st.markdown(f"""
            <div class="recipe-card" style="margin-bottom:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:1.35rem; font-weight:700; color:#D94E43;">{r['title']}</span>
                    <span class="badge-tag" style="{badge_custom_style}">{badge_custom}</span>
                </div>
                <div class="badge-container" style="margin-top:8px;">
                    {badge_type_html}
                    <span class="badge-tag badge-time">⏱️ {r['prep_time']}분</span>
                    <span class="badge-tag badge-author">👤 작성자: {r['author']}</span>
                    <span class="badge-tag" style="background-color:#E8F0FE; color:#1A73E8; border: 1px solid #C8E6C9;">❤️ 추천 {r['likes']}개</span>
                </div>
                <p style="color:#5C5C5C; font-size:0.95rem; margin-top:8px;">{r['description']}</p>
                <div class="ingredients-text">🛒 재료: {", ".join(r['ingredients'])}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons for card
            col_b1, col_b2, col_b3, col_b4 = st.columns([2, 1, 1, 4])
            with col_b1:
                pct, matched, missing = calculate_match(r["ingredients"], selected_ingredients)
                if st.button("상세 레시피 보기 🔍", key=f"board_view_{r['id']}"):
                    show_recipe_detail(r, matched, missing, pct)
            
            with col_b2:
                # Edit button - only enabled for custom, or we can allow edit for demo
                # Let's restrict it to custom but show a friendly tooltip
                if r["is_custom"]:
                    if st.button("수정 ✍️", key=f"board_edit_{r['id']}"):
                        st.session_state.board_action = "edit"
                        st.session_state.edit_target_id = r["id"]
                        st.rerun()
                else:
                    st.button("수정 ✍️", key=f"board_edit_disabled_{r['id']}", disabled=True, help="공식 레시피는 수정할 수 없습니다.")
                    
            with col_b3:
                # Delete button
                if r["is_custom"]:
                    if st.button("삭제 🗑️", key=f"board_del_{r['id']}"):
                        st.session_state.recipes = [x for x in st.session_state.recipes if x["id"] != r["id"]]
                        st.success("레시피가 삭제되었습니다.")
                        st.rerun()
                else:
                    st.button("삭제 🗑️", key=f"board_del_disabled_{r['id']}", disabled=True, help="공식 레시피는 삭제할 수 없습니다.")
            st.write("") # Spacer
            st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

# ----------------- TAB 4: HALL OF FAME -----------------
with tab4:
    st.markdown('<div class="category-badge" style="background-color:#E65100;">🏆 명예의 전당 (인기 랭킹)</div>', unsafe_allow_html=True)
    st.write("유저들에게 가장 많은 좋아요/추천을 받은 인기 레시피 TOP 3 및 인기 요리 순위입니다.")
    
    # Sort all by likes desc
    popular_recipes = sorted(st.session_state.recipes, key=lambda x: -x["likes"])
    
    if len(popular_recipes) >= 1:
        # Show top 3 in special layout
        st.subheader("🌟 실시간 인기 랭킹 TOP 3")
        
        cols_podium = st.columns(3)
        
        # Podium indices: 2nd place, 1st place, 3rd place
        podium_indices = [1, 0, 2]
        podium_styles = {
            0: {"title": "🥇 1등 요리", "border_color": "#FFD700", "bg": "#FFFDF0"},
            1: {"title": "🥈 2등 요리", "border_color": "#C0C0C0", "bg": "#F5F5F5"},
            2: {"title": "🥉 3등 요리", "border_color": "#CD7F32", "bg": "#FAF0E6"}
        }
        
        for p_pos, p_idx in enumerate(podium_indices):
            if p_idx < len(popular_recipes):
                recipe = popular_recipes[p_idx]
                style = podium_styles[p_pos] # match visual columns to position 0=Silver, 1=Gold, 2=Bronze
                
                with cols_podium[p_pos]:
                    st.markdown(f"""
                    <div style="background-color:{style['bg']}; border: 3px solid {style['border_color']}; border-radius: 20px; padding: 20px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.05);">
                        <h3 style="color:{style['border_color']}; margin-top:0;">{style['title']}</h3>
                        <h4 style="color:#D94E43; margin-bottom:5px;">{recipe['title']}</h4>
                        <p style="font-size:0.85rem; color:#777; margin-bottom:10px;">작성자: {recipe['author']}</p>
                        <div style="font-size:1.5rem; font-weight:bold; color:#F07167; margin-bottom:10px;">❤️ {recipe['likes']} 추천</div>
                        <p style="font-size:0.9rem; min-height: 50px;">"{recipe['description']}"</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    pct, matched, missing = calculate_match(recipe["ingredients"], selected_ingredients)
                    if st.button("레시피로 바로가기 🔍", key=f"podium_{recipe['id']}"):
                        show_recipe_detail(recipe, matched, missing, pct)
                        
        st.markdown('<hr class="cute-hr">', unsafe_allow_html=True)
        
        # Render the rest of the rankings as a neat table
        st.subheader("📈 전체 순위판")
        rank_data = []
        for rank, r in enumerate(popular_recipes, 1):
            rank_data.append({
                "순위": f"{rank}위",
                "레시피명": r["title"],
                "조리 방식": r["type"],
                "조리 시간": f"{r['prep_time']}분",
                "작성자": r["author"],
                "추천 수": f"❤️ {r['likes']}"
            })
            
        df = pd.DataFrame(rank_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("아직 등록된 레시피가 없습니다.")
