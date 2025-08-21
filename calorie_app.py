import streamlit as st
import matplotlib.pyplot as plt

# MET values
activities = {
    "Outdoor": {
        "Brisk Walk": 4.3,
        "Jogging": 7.0,
        "Cycling": 6.8
    },
    "Indoor (No Equipment)": {
        "Jump Rope": 12.0,
        "Jumping Jack": 8.0,
        "Squat (Bodyweight)": 5.0,
        "Plank": 3.0,
        "HIIT Bodyweight": 8.5,
        "Zumba/Aerobic": 7.0
    },
    "Indoor (With Equipment)": {
        "Treadmill Walk": 4.3,
        "Rowing Machine": 6.0,
        "Stationary Bike": 5.5
    }
}

def calories_burned(met, weight, minutes):
    return (met * 3.5 * weight / 200) * minutes

def calorie_calculator(current_weight, target_loss, days):
    total_cal_deficit = target_loss * 7700
    daily_cal_deficit = total_cal_deficit / days
    return daily_cal_deficit


# ----------------- Streamlit UI -----------------
st.title("🔥 Advanced Calorie Burn Calculator")
st.write("Kira kalori defisit harian + pilih aktiviti & lihat ranking senaman indoor.")

# Session state untuk simpan pilihan user
if "calorie_deficit" not in st.session_state:
    st.session_state.calorie_deficit = None

# Input asas
current_weight = st.number_input("Berat sekarang (kg)", min_value=30, max_value=200, value=70, step=1)
target_loss = st.number_input("Berapa kg nak turun", min_value=1, max_value=50, value=5, step=1)
days = st.number_input("Target dalam berapa hari", min_value=7, max_value=365, value=60, step=1)

if st.button("Kira Defisit"):
    st.session_state.calorie_deficit = calorie_calculator(current_weight, target_loss, days)

# Hanya teruskan kalau dah kira defisit
if st.session_state.calorie_deficit:
    daily_cal_deficit = st.session_state.calorie_deficit
    st.subheader("🎯 Hasil Pengiraan")
    st.write(f"👉 Perlu defisit: **{daily_cal_deficit:.0f} kcal sehari**")

    # Pilih aktiviti
    st.subheader("📌 Pilih Aktiviti")
    category = st.selectbox("Kategori aktiviti:", list(activities.keys()))
    act_choice = st.selectbox("Aktiviti:", list(activities[category].keys()))

    # Input masa
    minutes = st.number_input("Masa aktiviti (minit)", min_value=10, max_value=180, value=30, step=5)

    # Outdoor: boleh pilih jarak
    if category == "Outdoor":
        km = st.number_input("Anggaran jarak (km)", min_value=0.0, max_value=50.0, value=0.0, step=0.1)
        if km > 0:
            # kira masa semula ikut pace
            if act_choice == "Brisk Walk":
                pace = 5.5
            elif act_choice == "Jogging":
                pace = 8.5
            else:
                pace = 15.0
            minutes = (km / pace) * 60

    # Kiraan kalori
    kcal_burn = calories_burned(activities[category][act_choice], current_weight, minutes)
    sesi = daily_cal_deficit / kcal_burn

    st.success(f"{act_choice} selama {minutes:.0f} min → terbakar **{kcal_burn:.0f} kcal**")
    st.info(f"👉 Untuk capai defisit {daily_cal_deficit:.0f} kcal, perlu ~ **{sesi:.1f} sesi** sehari")

    # Ranking senaman indoor
    if category == "Indoor (No Equipment)":
        st.subheader("💪 Ranking Senaman Indoor (30 min)")
        ranking = []
        for ex, met in activities["Indoor (No Equipment)"].items():
            kcal = calories_burned(met, current_weight, 30)
            ranking.append((ex, kcal))
        ranking.sort(key=lambda x: x[1], reverse=True)

        # Senarai teks
        for ex, kcal in ranking:
            st.write(f"- {ex}: **{kcal:.0f} kcal/30 min**")

        # Graf bar
        st.subheader("📊 Visual Ranking")
        ex_names = [x[0] for x in ranking]
        kcal_vals = [x[1] for x in ranking]

        fig, ax = plt.subplots()
        ax.barh(ex_names, kcal_vals)
        ax.invert_yaxis()
        ax.set_xlabel("Kalori (kcal)")
        ax.set_title("Kalori terbakar (30 min)")
        st.pyplot(fig)
