import streamlit as st

st.set_page_config(
    page_title="土の含水比計算",
    page_icon="icon.png",
    layout="centered"
)

st.title("Hyper 含ちゃん")
st.markdown("含水比 **w (%)** を計算します。")

st.write("### 入力")
ma = st.number_input("ma: 容器 + 湿潤試料 [g]", min_value=0.0, format="%.3f")
mb = st.number_input("mb: 容器 + 乾燥試料 [g]", min_value=0.0, format="%.3f")
mc = st.number_input("mc: 容器 [g]", min_value=0.0, format="%.3f")

def calc_water_content(ma, mb, mc):
    dry_mass = mb - mc
    water_mass = ma - mb

    if dry_mass <= 0:
        raise ValueError("mb - mc は 0 より大きくなる必要があります。")
    if water_mass < 0:
        raise ValueError("ma - mb が負です。入力値を確認してください。")

    return 100 * water_mass / dry_mass, water_mass, dry_mass

if st.button("計算する", use_container_width=True):
    try:
        w, water_mass, dry_mass = calc_water_content(ma, mb, mc)

        st.success(f"含水比 w = {w:.2f} %")

        with st.expander("計算過程を表示"):
            st.write(f"水の質量 = ma - mb = {ma:.3f} - {mb:.3f} = {water_mass:.3f} g")
            st.write(f"乾燥試料の質量 = mb - mc = {mb:.3f} - {mc:.3f} = {dry_mass:.3f} g")
            st.write(f"w = 100 × ({water_mass:.3f}) / ({dry_mass:.3f}) = {w:.2f} %")

    except ValueError as e:
        st.error(str(e))
    except Exception:
        st.error("入力値を確認してください。")

st.markdown("---")
st.caption("式: w = 100 × (ma - mb) / (mb - mc)")
