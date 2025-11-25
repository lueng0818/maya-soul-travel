import os
import calendar
from PIL import Image

import pandas as pd
import streamlit as st

# ────────────── Path Setup ──────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMG_DIR  = os.path.join(BASE_DIR, "images")

# ────────────── Travel Data Dictionary (內建旅遊資料庫) ──────────────
travel_data = {
    "紅龍": {
        "theme": "尋根溯源，連結古老記憶與大地之母。",
        "trips": [
            {"place": "祕魯馬丘比丘與聖谷", "desc": "深入古印加文明的搖籃，感受大地母親最原始的滋養力量。"},
            {"place": "埃及尼羅河之旅", "desc": "沿著文明的母親河航行，探索金字塔與神廟，喚醒靈魂深處的古老記憶。"},
            {"place": "台灣台東", "desc": "拜訪土地純淨、原住民文化深厚的部落，體驗大地最純粹的生命力。"}
        ]
    },
    "紅蛇": {
        "theme": "喚醒身體的生命能量與熱情。",
        "trips": [
            {"place": "巴西里約熱內盧", "desc": "參加一場熱情的森巴舞課程，感受身體的律動與城市的活力。"},
            {"place": "哥斯大黎加叢林探險", "desc": "在充滿生命力的熱帶雨林中遠足、溯溪，與野生動物連結，點燃你的生存本能。"},
            {"place": "肯亞動物大遷徙", "desc": "親眼見證大自然最壯闊的生命力展演，感受生命的奔騰不息。"}
        ]
    },
    "紅月": {
        "theme": "情緒的流動與療癒，跟隨水的指引。",
        "trips": [
            {"place": "冰島藍湖溫泉與冰川湖", "desc": "讓身體浸泡在富含礦物質的溫泉中，觀賞冰川湖的靜謐，洗滌身心。"},
            {"place": "日本熊野古道", "desc": "沿著古老的朝聖之路，途經瀑布、溪流與神社，進行一場身心靈的淨化之旅。"},
            {"place": "馬爾地夫", "desc": "在清澈見底的海水中浮潛或潛水，感受水的包容與療癒力量。"}
        ]
    },
    "紅天行者": {
        "theme": "打破框架，向未知領域探索。",
        "trips": [
            {"place": "紐西蘭自助公路旅行", "desc": "開著露營車，隨心所欲地探索壯麗的峽灣、冰川與山脈，體驗極致的自由。"},
            {"place": "美國51區周邊與大峽谷", "desc": "駕車穿越廣袤的沙漠公路，抬頭仰望無垠星空，對宇宙和未知保持敞開。"},
            {"place": "西班牙聖雅各之路", "desc": "透過長途步行，一步一腳印地向內在探索，擴展心靈的空間。"}
        ]
    },
    "紅地球": {
        "theme": "跟隨地球的脈動，學習順流與導航。",
        "trips": [
            {"place": "夏威夷火山國家公園", "desc": "親身感受地球創造與毀滅的力量，學習在變動中找到方向。"},
            {"place": "澳洲烏魯魯巨岩", "desc": "在世界的中心感受地球的能量心跳，連結土地的智慧與共時性。"},
            {"place": "參與一場樸門農法工作坊", "desc": "在世界任何一個角落，學習如何與自然和諧共處，順應地球的節律。"}
        ]
    },
    "白風": {
        "theme": "尋找內在的寧靜，與神性連結。",
        "trips": [
            {"place": "尼泊爾安納布爾納山區健行", "desc": "在世界屋脊，透過每一次深長的呼吸，與天地精神交流。"},
            {"place": "愛爾蘭的懸崖與古堡", "desc": "在大西洋的風中，聆聽古老傳說，讓風帶走雜念，帶來清晰的訊息。"},
            {"place": "希臘聖托里尼", "desc": "在藍白相間的純淨小島上，找一個安靜的角落，靜心冥想，寫下內心的話語。"}
        ]
    },
    "白世界橋": {
        "theme": "放下過去，迎接新的開始。",
        "trips": [
            {"place": "墨西哥亡靈節", "desc": "體驗這個紀念與慶祝生命循環的節日，學習優雅地告別與放下。"},
            {"place": "柬埔寨吳哥窟", "desc": "在千年古蹟的寂靜中，思考生與死、繁華與寂滅，找到斷捨離的力量。"},
            {"place": "日本高野山宿坊體驗", "desc": "在寺院中住宿，體驗僧侶的簡樸生活，沉澱心靈，放下執著。"}
        ]
    },
    "白狗": {
        "theme": "回歸無條件的愛與夥伴關係。",
        "trips": [
            {"place": "義大利維諾納或佛羅倫斯", "desc": "在充滿浪漫與藝術氣息的古城中，與伴侶或摯友，重新連結心的關係。"},
            {"place": "擔任國際志工", "desc": "前往需要幫助的地方，為動物或孩童服務，打開你的心，體驗無私的愛。"},
            {"place": "與家人或摯友的深度懷舊之旅", "desc": "回到充滿共同回憶的地方，分享愛與感謝。"}
        ]
    },
    "白鏡": {
        "theme": "看見真相，尋找內在的清明。",
        "trips": [
            {"place": "玻利維亞天空之鏡", "desc": "站在這片世界上最大的鏡子前，看見天與地的完美倒影，也看見最真實的自己。"},
            {"place": "日本京都的枯山水庭園", "desc": "在禪意十足的庭園中，透過簡潔的景觀，映照出內在的秩序與寧靜。"},
            {"place": "瑞士阿爾卑斯山", "desc": "在清澈見底的高山湖泊旁，觀看雪山的倒影，讓心如明鏡。"}
        ]
    },
    "白巫師": {
        "theme": "進入當下，感受生命的魔法與神秘。",
        "trips": [
            {"place": "英國巨石陣與格拉斯頓伯里", "desc": "走進傳說中亞瑟王與魔法的發源地，感受古老神秘的能量。"},
            {"place": "亞馬遜雨林薩滿儀式", "desc": "在叢林深處，參與一場由薩滿帶領的儀式，連結植物的智慧與宇宙的魔法。"},
            {"place": "捷克布拉格", "desc": "漫步在充滿煉金術傳說的古老街道，感受這座「魔法之都」的神秘氛圍。"}
        ]
    },
    "藍夜": {
        "theme": "深入內在世界，探索夢境與潛意識。",
        "trips": [
            {"place": "挪威或芬蘭追尋極光", "desc": "在漫漫長夜中，觀賞夢幻般的北極光，相信內在豐盛的指引。"},
            {"place": "法國巴黎藝術之旅", "desc": "沉浸在羅浮宮、奧賽美術館的藝術品中，讓直覺與靈感自由流淌。"},
            {"place": "參加一場深度靜默禪修", "desc": "遠離塵囂，向內探索，聆聽你內在夢境的聲音。"}
        ]
    },
    "藍手": {
        "theme": "動手創造，體驗療癒與完成的力量。",
        "trips": [
            {"place": "泰國清邁參加手作課程", "desc": "學習烹飪、陶藝或木工，透過雙手，將想法變為現實。"},
            {"place": "義大利托斯卡尼鄉村生活", "desc": "親手採摘橄欖、釀造葡萄酒，體驗從無到有的創造過程。"},
            {"place": "峇里島瑜珈與療癒之旅", "desc": "透過瑜珈、按摩與能量療法，親身體驗療癒的過程。"}
        ]
    },
    "藍猴": {
        "theme": "找回內在小孩，輕鬆幽默地玩樂。",
        "trips": [
            {"place": "美國奧蘭多迪士尼世界", "desc": "盡情享受魔法與幻想，允許自己像孩子一樣大笑與玩耍。"},
            {"place": "西班牙伊比薩島", "desc": "在這個充滿音樂、藝術與自由氣息的島嶼上，隨心所欲地跳舞與生活。"},
            {"place": "印度荷麗節 (Holi Festival)", "desc": "參加色彩的狂歡，打破人與人之間的隔閡，享受純粹的喜悅。"}
        ]
    },
    "藍鷹": {
        "theme": "提升視野，看見生命更大的藍圖。",
        "trips": [
            {"place": "土耳其卡帕多奇亞熱氣球", "desc": "從高空俯瞰奇特的地貌，擴展你的視野與格局。"},
            {"place": "杜拜哈里發塔登頂", "desc": "站上世界最高建築，鳥瞰這座從沙漠中創造出來的奇蹟城市。"},
            {"place": "大峽谷國家公園", "desc": "站在峽谷邊緣，感受時間與空間的宏偉，重新定義自己的問題與挑戰。"}
        ]
    },
    "藍風暴": {
        "theme": "迎接轉變，釋放舊有能量。",
        "trips": [
            {"place": "冰島的瀑布與間歇泉", "desc": "近距離感受大自然強大的能量釋放，讓流動的水與蒸氣帶走不再服務你的一切。"},
            {"place": "尼加拉瀑布", "desc": "感受瀑布雷霆萬鈞的能量，讓它成為你生命中蛻變的催化劑。"},
            {"place": "參與一場大掃除或排毒營", "desc": "透過身體與環境的清理，加速內在的轉化與更新。"}
        ]
    },
    "黃種子": {
        "theme": "播下意圖的種子，專注於目標的實現。",
        "trips": [
            {"place": "日本京都哲學之道", "desc": "在櫻花盛開或楓紅的季節，沿著小徑散步，清晰地設定你未來的目標與意圖。"},
            {"place": "新加坡濱海灣花園", "desc": "觀賞這些充滿未來感的超級樹，啟發你將夢想藍圖實現的潛能。"},
            {"place": "參加目標設定工作坊", "desc": "在一個新的環境中，專注地規劃你的未來。"}
        ]
    },
    "黃星星": {
        "theme": "追尋生活中的美與和諧。",
        "trips": [
            {"place": "法國普羅旺斯", "desc": "在薰衣草花田中漫步，參觀藝術家的小鎮，讓自己沉浸在美麗與優雅之中。"},
            {"place": "奧地利維也納", "desc": "聆聽一場世界級的音樂會，參觀華麗的宮殿，體驗藝術如何融入生活。"},
            {"place": "義大利烏菲茲美術館", "desc": "近距離欣賞文藝復興時期的傑作，感受和諧與神聖之美。"}
        ]
    },
    "黃人": {
        "theme": "探索人類的智慧結晶與自由意志的展現。",
        "trips": [
            {"place": "希臘雅典衛城", "desc": "走在西方哲學與民主的發源地，思考智慧與自由的真諦。"},
            {"place": "參觀世界頂尖大學", "desc": "如英國的牛津、劍橋，或美國的哈佛，感受人類智慧的傳承與力量。"},
            {"place": "德國柏林圍牆遺址", "desc": "見證人類對自由的渴望如何推倒高牆，反思個人選擇的力量。"}
        ]
    },
    "黃戰士": {
        "theme": "挑戰自我，勇敢地探索與提問。",
        "trips": [
            {"place": "以色列耶路撒冷", "desc": "在這個三大宗教的聖城，探索不同的信仰與觀點，勇敢地向自己的信念提問。"},
            {"place": "攀登一座具挑戰性的高山", "desc": "例如馬來西亞神山或台灣玉山，透過身體的挑戰，鍛鍊心智的堅韌與無畏。"},
            {"place": "中美洲馬雅金字塔群", "desc": "親身探索馬雅文明的智慧，解開宇宙的古老提問。"}
        ]
    },
    "黃太陽": {
        "theme": "連結宇宙的源頭之光，慶祝生命。",
        "trips": [
            {"place": "墨西哥圖盧姆海灘日出", "desc": "在馬雅遺址旁，迎接太陽從加勒比海升起，感受宇宙之火的溫暖與力量。"},
            {"place": "印度瓦拉納西恆河晨祭", "desc": "參與古老的儀式，感受生命、死亡與重生的循環，體會合一的意識。"},
            {"place": "陽光普照的島嶼靜修", "desc": "什麼都不做，只是單純地曬太陽，讓陽光充滿你的每一個細胞，感受純粹的生命喜悅。"}
        ]
    }
}


# ────────────── Page Config & CSS ──────────────
st.set_page_config(page_title="Maya 靈魂旅程指南", layout="wide")
st.markdown(
    """<style>
    .hero {padding:4rem 2rem; text-align:center; background:#f0f5f9;}
    .hero h1 {font-size:3rem; font-weight:700; margin-bottom:0.5rem;}
    .hero p  {font-size:1.25rem; margin-bottom:1.5rem;}
    .footer {position:fixed; bottom:0; width:100%; background:#1f2937; color:white; text-align:center; padding:1rem; z-index:999;}
    .footer a {color:#60a5fa; text-decoration:none; margin:0 0.5rem;}
    
    /* 卡片樣式優化 */
    div[data-testid="stContainer"] {
        background-color: #f9fafb;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>""",
    unsafe_allow_html=True,
)

# ────────────── Hero Section ──────────────
st.markdown(
    """
    <section class="hero">
      <h1>Maya 靈魂旅程指南</h1>
      <p>輸入出生日期，解開專屬的印記密碼，探索宇宙為你安排的能量旅行。</p>
      <p><em>請從左側面板輸入你的西元生日，即可立即查看。</em></p>
    </section>
    """,
    unsafe_allow_html=True,
)

# ────────────── Load Data ──────────────
try:
    kin_start   = pd.read_csv(os.path.join(DATA_DIR, "kin_start_year.csv"), index_col="年份")["起始KIN"].to_dict()
    month_accum = pd.read_csv(os.path.join(DATA_DIR, "month_day_accum.csv"),   index_col="月份")["累積天數"].to_dict()
    kin_basic   = pd.read_csv(os.path.join(DATA_DIR, "kin_basic_info.csv"))
    # 已移除自我探索資料讀取
except Exception as e:
    st.error(f"❌ 資料載入失敗：{e}")
    st.stop()

# ────────────── Sidebar Input ──────────────
st.sidebar.header("📅 查詢你的 Maya 印記")
year = st.sidebar.selectbox("西元年", sorted(kin_start.keys()), index=sorted(kin_start.keys()).index(1990))
month = st.sidebar.selectbox("月份", list(range(1,13)), index=0)
max_day = calendar.monthrange(year, month)[1]
day = st.sidebar.slider("日期", 1, max_day, 1)

# ────────────── KIN 計算 ──────────────
start_kin = kin_start.get(year)
if start_kin is None:
    st.sidebar.error("⚠️ 此年份無起始 KIN")
    st.stop()
raw = start_kin + month_accum.get(month,0) + day
mod = raw % 260
kin = 260 if mod==0 else mod

# ────────────── 顯示基本 KIN 與圖騰 ──────────────
subset = kin_basic[kin_basic["KIN"]==kin]
if subset.empty:
    st.error(f"❓ 找不到 KIN {kin} 資料")
    st.stop()
info = subset.iloc[0]
totem = info["圖騰"]  # 取得圖騰名稱 (例如: "紅龍")

# 這裡移除「主印記」文字，讓畫面更聚焦
st.markdown(f"## 🔢 你的 KIN：{kin} ｜ {totem}", unsafe_allow_html=True)

col_img, col_desc = st.columns([1, 5])
with col_img:
    img_file = os.path.join(IMG_DIR, f"{totem}.png")
    if os.path.exists(img_file):
        st.image(Image.open(img_file), width=120)

# ────────────── 靈魂旅程建議 ──────────────
st.markdown("---")
st.markdown(f"## ✈️ {totem} 的靈魂旅程建議")

if totem in travel_data:
    travel_info = travel_data[totem]
    
    # 顯示旅行主題，使用 info 樣式更吸睛
    st.info(f"**🗺️ 旅行主題：** {travel_info['theme']}")
    
    # 顯示三個推薦行程
    t_col1, t_col2, t_col3 = st.columns(3)
    cols = [t_col1, t_col2, t_col3]
    
    for idx, trip in enumerate(travel_info['trips']):
        with cols[idx]:
            with st.container(border=True):
                st.markdown(f"#### 📍 {trip['place']}")
                st.write(trip['desc'])
else:
    st.warning("目前尚無此圖騰的專屬旅遊建議。")

# ────────────── 固定 Footer ──────────────
st.markdown(
    """
    <div style="margin-bottom: 80px;"></div>
    <footer class="footer">
      <a href="https://www.facebook.com/soulclean1413/" target="_blank">👉 加入粉專</a> 
      <a href="https://www.instagram.com/tilandky/" target="_blank">👉 追蹤IG</a>
      <a href="https://line.me/R/ti/p/%40690ZLAGN" target="_blank">👉 加入社群</a>
    </footer>
    """,
    unsafe_allow_html=True
)