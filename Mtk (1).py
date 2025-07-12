import streamlit as st
import math
import pandas as pd
import plotly.express as px
# EOQ Optimization App for Toko Buku Cerdas
# ==================================================
# Integrasi kedua versi kode: versi "ringkas dengan opsi pembulatan" 
# dan versi "UI lengkap dengan tab, CSS, dan visualisasi".
# ==================================================

# ---------- Page Configuration ----------
st.set_page_config(
    page_title="EOQ Optimization for Toko Buku Cerdas",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------- Custom CSS ----------
st.markdown(
    """
    <style>
        .main {background-color: #f0f2f6; padding: 20px;}
        .stApp {max-width: 900px; margin: auto;}
        .st-emotion-cache-1pxazr7 {
            background-color: #4CAF50 !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 10px 24px !important;
            font-size: 18px !important;
            font-weight: bold !important;
            border: none !important;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        }
        .st-emotion-cache-1pxazr7:hover {background-color: #45a049 !important;}
        h1 {color: #2e86de; text-align: center; font-size: 2.5em; margin-bottom: 20px;}
        h2 {color: #34495e; font-size: 1.8em; border-bottom: 2px solid #aec6cf; padding-bottom: 5px; margin-top: 30px;}
        .metric-box {background-color: #ffffff; border-radius: 10px; padding: 15px; margin-bottom: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center;}
        .metric-value {font-size: 2.2em; font-weight: bold; color: #28a745;}
        .metric-label {font-size: 1em; color: #555;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Title & Intro ----------
st.title("📚 EOQ Optimization for Toko Buku Cerdas")
st.markdown("### *Meningkatkan Efisiensi Persediaan Toko Buku*")
st.write(
    """
    Selamat datang di aplikasi simulasi **Economic Order Quantity (EOQ)**!
    Aplikasi ini membantu Anda menentukan jumlah pemesanan optimal untuk
    meminimalkan *total biaya persediaan*. Silakan jelajahi tab untuk memahami
    konsep, memasukkan data, melihat hasil perhitungan, serta FAQ.
    """
)

# ---------- Tabs ----------
tab1, tab2, tab3, tab4 = st.tabs(["💡 Tentang EOQ", "📊 Input Data", "📈 Hasil & Analisis", "❓ FAQ"])

# ---------- Tab 1: About EOQ ----------
with tab1:
    st.header("💡 Apa Itu EOQ?")
    st.write(
        """
        **EOQ (Economic Order Quantity)** adalah model persediaan klasik yang
        digunakan untuk menentukan **jumlah pemesanan optimal** yang
        meminimalkan total biaya persediaan. Dua komponen biaya utama:

        * **Biaya Pemesanan (Ordering Cost)** – biaya setiap kali melakukan
          pemesanan (administrasi, pengiriman, dsb).
        * **Biaya Penyimpanan (Holding Cost)** – biaya menahan stok di gudang
          (sewa ruang, asuransi, opportunity cost, dsb).
        """
    )
    st.write("#### Asumsi Model EOQ:")
    st.markdown(
        """
        * Permintaan konstan & diketahui.
        * Biaya pemesanan & penyimpanan per unit konstan.
        * Tidak ada kekurangan stok (stock‑out).
        * Lead time (waktu antara pesan & terima) konstan.
        """
    )

# ---------- Tab 2: Input Data ----------
with tab2:
    st.header("📊 Masukkan Data Anda")
    st.write("Isi parameter berikut untuk menghitung EOQ.")

    col1, col2 = st.columns(2)
    with col1:
        D = st.number_input(
            "Permintaan Tahunan (D) - unit/tahun",
            min_value=0,
            value=0,
            step=1,
            format="%d",
            help="Jumlah unit yang dibutuhkan dalam setahun."
        )
        S = st.number_input(
            "Biaya Pemesanan (S) - Rp/pesanan",
            min_value=0,
            value=0,
            step=1000,
            format="%d",
            help="Biaya sekali memesan (tidak termasuk biaya unit)."
        )
    with col2:
        H = st.number_input(
            "Biaya Penyimpanan (H) - Rp/unit/tahun",
            min_value=0,
            value=0,
            step=100,
            format="%d",
            help="Biaya menyimpan satu unit selama setahun."
        )
        bulat = st.checkbox("Tampilkan hasil bulat", value=True, key="round_pref")


# ---------- Tab 3: Results & Analysis ----------
with tab3:
    st.header("📈 Hasil Perhitungan & Analisis")

    if st.session_state.get("calculate", False):
        p = st.session_state.params
        D, S, H, bulat = p["D"], p["S"], p["H"], p["bulat"]

        try:
            eoq = math.sqrt((2 * D * S) / H)
            orders_per_year = D / eoq if eoq else 0

            if bulat:
                eoq_disp = f"{round(eoq):,}"
                orders_disp = f"{math.ceil(orders_per_year):,}"
            else:
                eoq_disp = f"{eoq:,.2f}"
                orders_disp = f"{orders_per_year:,.2f}"

            total_ordering_cost = math.ceil(orders_per_year) * S
            total_holding_cost = (eoq / 2) * H
            total_inventory_cost = total_ordering_cost + total_holding_cost

            total_inventory_disp = f"Rp {total_inventory_cost:,.0f}" if bulat else f"Rp {total_inventory_cost:,.2f}"

            # ----- Display Metrics -----
            st.success("Perhitungan berhasil!")
            st.markdown("### Ringkasan Hasil")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    f"""
                    <div class='metric-box'>
                        <div class='metric-value'>{eoq_disp} unit</div>
                        <div class='metric-label'>EOQ (Unit Optimal per Pesanan)</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            with col2:
                st.markdown(
                    f"""
                    <div class='metric-box'>
                        <div class='metric-value'>{orders_disp} kali</div>
                        <div class='metric-label'>Jumlah Pesanan per Tahun</div>
                    </div>""",
                    unsafe_allow_html=True,
                )

            st.markdown(
                f"""
                <div class='metric-box'>
                    <div class='metric-value'>{total_inventory_disp}</div>
                    <div class='metric-label'>Total Biaya Persediaan Tahunan</div>
                </div>""",
                unsafe_allow_html=True,
            )

            # ----- Cost Details -----
            st.markdown("### Detail Biaya")
            st.info(
                f"**Total Biaya Pemesanan:** Rp {total_ordering_cost:,.0f} "
                f"(dari {math.ceil(orders_per_year)} pesanan × Rp {S:,.0f}/pesanan)"
            )
            st.info(
                f"**Total Biaya Penyimpanan:** Rp {total_holding_cost:,.0f} "
                f"(dari ({eoq_disp} unit / 2) × Rp {H:,.0f}/unit/tahun)"
            )

            # ----- Recommendation -----
            st.markdown("### Rekomendasi")
            st.write(
                f"Dengan memesan sekitar **{eoq_disp} unit** tiap kali (\~**{orders_disp}** pesanan/tahun), "
                "Anda dapat meminimalkan total biaya persediaan menjadi "
                f"{total_inventory_disp}.")

            # ----- Visualization -----
            st.markdown("### Visualisasi Biaya EOQ")
            st.write(
                "Kurva di bawah menunjukkan perubahan biaya pemesanan, penyimpanan, dan total "
                "terhadap variasi jumlah pesanan.")

            # Generate range around EOQ for plotting
            min_q = max(1, int(eoq * 0.1))
            max_q = int(eoq * 2)
            step_q = max(1, int(eoq / 50))

            quantities, cost_order, cost_hold, cost_total = [], [], [], []
            for q in range(min_q, max_q + step_q, step_q):
                co = (D / q) * S
                ch = (q / 2) * H
                ct = co + ch
                quantities.extend([q])
                cost_order.extend([co])
                cost_hold.extend([ch])
                cost_total.extend([ct])

            df = pd.DataFrame({
                "Jumlah Pesanan (Unit)": quantities,
                "Biaya Pemesanan": cost_order,
                "Biaya Penyimpanan": cost_hold,
                "Total Biaya": cost_total,
            })
            df_melt = df.melt(
                id_vars="Jumlah Pesanan (Unit)",
                var_name="Jenis Biaya",
                value_name="Biaya (Rp)",
            )

            fig = px.line(
                df_melt,
                x="Jumlah Pesanan (Unit)",
                y="Biaya (Rp)",
                color="Jenis Biaya",
                title="Kurva Biaya EOQ",
                hover_data={"Biaya (Rp)":":,.0f"},
            )
            fig.add_vline(
                x=eoq,
                line_dash="dash",
                line_color="red",
                annotation_text=f"EOQ ≈ {round(eoq):,}",
                annotation_position="top right",
            )
            fig.update_layout(hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

        except ZeroDivisionError:
            st.error("Biaya penyimpanan (H) tidak boleh nol.")
        except Exception as ex:
            st.error(f"Terjadi kesalahan: {ex}")
    else:
        st.info("Masukkan data di tab 'Input Data' lalu klik 'Hitung EOQ'.")

# ---------- Tab 4: FAQ ----------
with tab4:
    st.header("❓ Pertanyaan Umum (FAQ)")
    st.subheader("Mengapa EOQ penting?")
    st.write(
        "EOQ membantu menyeimbangkan biaya pemesanan & penyimpanan, sehingga total "
        "biaya persediaan minimal & arus kas lebih efisien.")
    st.subheader("Apakah asumsi EOQ selalu berlaku?")
    st.write(
        "Model EOQ mengasumsikan permintaan & lead time konstan. Bila tidak terpenuhi, "
        "perusahaan dapat menyesuaikan model (mis. safety stock, diskon kuantitas, "
        "atau sistem perencanaan persediaan lainnya).")
    st.subheader("Bagaimana jika permintaan tidak konstan?")
    st.write(
        "Gunakan metode peramalan permintaan & model lain (ROP, (Q,r) policy, dll.) "
        "untuk menyesuaikan fluktuasi permintaan.")

# ---------- Footer ----------
st.markdown(
    "---\n<p style='text-align:center; color:gray;'>\nAplikasi ini dibuat untuk tujuan edukasi — Studi Kasus EOQ Toko Buku Cerdas.\n</p>",
    unsafe_allow_html=True,
)
