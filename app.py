import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

# =====================
# ページ設定
# =====================
st.set_page_config(
    page_title="含ちゃん",
    page_icon="🧪",
    layout="centered"
)

# =====================
# CSS
# =====================
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    margin-bottom: 18px;
}
.result {
    font-size: 30px;
    font-weight: 700;
    color: #1f77b4;
    text-align: center;
}
.small-note {
    color: #666666;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# =====================
# セッション初期化
# =====================
if "history" not in st.session_state:
    st.session_state.history = []

# =====================
# 関数
# =====================
def get_now_jst():
    return datetime.now(ZoneInfo("Asia/Tokyo"))

def calc_water_content(ma: float, mb: float, mc: float):
    dry_mass = mb - mc
    water_mass = ma - mb

    if mb <= mc:
        raise ValueError("mb は mc より大きくしてください。")
    if ma < mb:
        raise ValueError("ma は mb 以上にしてください。")

    w = 100 * water_mass / dry_mass
    return w, water_mass, dry_mass

# =====================
# タイトル
# =====================
st.markdown("<h1 style='text-align: center;'>🌱 含ちゃん</h1>", unsafe_allow_html=True)

# =====================
# 入力
# =====================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("入力")

sample_name = st.text_input("試料名", placeholder="例: Araki-1")

col1, col2 = st.columns(2)
with col1:
    ma = st.number_input("ma：容器 + 湿潤試料 [g]", min_value=0.0, format="%.3f")
with col2:
    mb = st.number_input("mb：容器 + 乾燥試料 [g]", min_value=0.0, format="%.3f")

mc = st.number_input("mc：容器 [g]", min_value=0.0, format="%.3f")

now_jst = get_now_jst()
st.markdown(
    f"<p class='small-note'>測定日時（自動取得）: {now_jst.strftime('%Y-%m-%d %H:%M:%S')}</p>",
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

# =====================
# ボタン
# =====================
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    calc_clicked = st.button("計算して履歴に追加", use_container_width=True)

with col_btn2:
    clear_clicked = st.button("履歴を削除", use_container_width=True)

# =====================
# 計算処理
# =====================
if calc_clicked:
    try:
        if not sample_name.strip():
            raise ValueError("試料名を入力してください。")

        w, water_mass, dry_mass = calc_water_content(ma, mb, mc)
        timestamp = get_now_jst().strftime("%Y-%m-%d %H:%M:%S")

        record = {
            "測定日時": timestamp,
            "試料名": sample_name.strip(),
            "ma [g]": round(ma, 3),
            "mb [g]": round(mb, 3),
            "mc [g]": round(mc, 3),
            "水の質量 ma-mb [g]": round(water_mass, 3),
            "乾燥試料の質量 mb-mc [g]": round(dry_mass, 3),
            "含水比 w [%]": round(w, 2)
        }

        st.session_state.history.append(record)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"<div class='result'>w = {w:.2f} %</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("今回の計算過程を表示"):
            st.write(f"水の質量 = ma - mb = {ma:.3f} - {mb:.3f} = {water_mass:.3f} g")
            st.write(f"乾燥試料の質量 = mb - mc = {mb:.3f} - {mc:.3f} = {dry_mass:.3f} g")
            st.write(f"w = 100 × ({water_mass:.3f}) / ({dry_mass:.3f}) = {w:.2f} %")

        st.success("履歴に追加しました。")

    except ValueError as e:
        st.error(str(e))
    except Exception:
        st.error("入力値を確認してください。")

# =====================
# 履歴削除
# =====================
if clear_clicked:
    st.session_state.history = []
    st.warning("履歴を削除しました。")

# =====================
# 履歴表示
# =====================
if st.session_state.history:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("計算履歴")

    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True, hide_index=True)

    csv_data = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="履歴をCSVでダウンロード",
        data=csv_data,
        file_name=f"water_content_history_{get_now_jst().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

# =====================
# 式
# =====================
st.markdown("---")
st.caption("式: w = 100 × (ma - mb) / (mb - mc)")
