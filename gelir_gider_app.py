import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Gelir Gider Takip", page_icon="💰", layout="centered")

st.title("💰 Gelir Gider Takip Uygulaması")

# Kullanıcı seçimi
kisi = st.text_input("Kullanıcı adı girin:")
dosya_adi = f"{kisi}.csv" if kisi else None

def dosya_kontrol_et(dosya_adi):
    if not os.path.exists(dosya_adi):
        df = pd.DataFrame(columns=["Tarih", "Tür", "Kategori", "Tutar", "Not"])
        df.to_csv(dosya_adi, index=False)

if kisi:
    dosya_kontrol_et(dosya_adi)

    menu = st.sidebar.radio("Menü", ["Yeni Kayıt", "Kayıtları Listele", "Aylık Özet"])

    if menu == "Yeni Kayıt":
        with st.form("yeni_kayit_formu"):
            tarih = st.date_input("Tarih", datetime.today())
            tur = st.radio("Tür", ["gelir", "gider"])
            kategori = st.text_input("Kategori")
            tutar = st.number_input("Tutar", min_value=0.0, format="%.2f")
            notlar = st.text_area("Not (opsiyonel)")
            kaydet = st.form_submit_button("Kaydet")

            if kaydet:
                yeni = pd.DataFrame([[tarih, tur, kategori, tutar, notlar]],
                                    columns=["Tarih", "Tür", "Kategori", "Tutar", "Not"])
                df = pd.read_csv(dosya_adi)
                df = pd.concat([df, yeni], ignore_index=True)
                df.to_csv(dosya_adi, index=False)
                st.success("✅ Kayıt eklendi.")

    elif menu == "Kayıtları Listele":
        if os.path.exists(dosya_adi):
            df = pd.read_csv(dosya_adi)
            st.subheader("📋 Mevcut Kayıtlar")
            st.dataframe(df)
        else:
            st.info("Henüz kayıt yok.")

    elif menu == "Aylık Özet":
        if os.path.exists(dosya_adi):
            df = pd.read_csv(dosya_adi)
            df["Tarih"] = pd.to_datetime(df["Tarih"], errors="coerce")

            yil = st.number_input("Yıl", min_value=2000, max_value=2100, value=datetime.today().year)
            ay = st.number_input("Ay", min_value=1, max_value=12, value=datetime.today().month)

            ay_df = df[(df["Tarih"].dt.year == yil) & (df["Tarih"].dt.month == ay)]

            if not ay_df.empty:
                toplam_gelir = ay_df[ay_df["Tür"] == "gelir"]["Tutar"].sum()
                toplam_gider = ay_df[ay_df["Tür"] == "gider"]["Tutar"].sum()
                bakiye = toplam_gelir - toplam_gider

                st.subheader("📊 Aylık Özet")
                st.write(f"**Toplam Gelir:** {toplam_gelir:.2f} TL")
                st.write(f"**Toplam Gider:** {toplam_gider:.2f} TL")
                st.write(f"**Bakiye:** {bakiye:.2f} TL")
            else:
                st.info("Bu ay için kayıt bulunamadı.")
        else:
            st.info("Henüz kayıt yok.")
else:
    st.info("👆 Önce kullanıcı adı girin.")
