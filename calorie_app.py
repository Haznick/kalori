import streamlit as st
import math
import matplotlib.pyplot as plt

# -----------------------------
# BMI Standard
# -----------------------------
bmi_standards = {
    "WHO / Europe": [
        (18.5, "Underweight"),
        (24.9, "Normal"),
        (29.9, "Overweight"),
        (100, "Obese")
    ],
    "Asia / SEA": [
        (18.5, "Underweight"),
        (22.9, "Normal"),
        (24.9, "Overweight (At risk)"),
        (29.9, "Obese I"),
        (100, "Obese II")
    ],
    "China": [
        (18.5, "Underweight"),
        (23.9, "Normal"),
        (27.9, "Overweight"),
        (100, "Obese")
    ]
}

def classify_bmi(bmi, standard):
    for threshold, category in bmi_standards[standard]:
        if bmi <= threshold:
            return category
    return "Undefined"

# -----------------------------
# Kalori & Aktiviti
# -----------------------------
def calorie_calculator(current_weight, target_weight, duration_days):
    total_loss = current_weight - target_weight
    total_calories = total_loss * 7700  # 1kg ≈ 7700 kcal
    per_day = total_calories / duration_days if duration_days > 0 else 0
    return total_calories, per_day

activities = {
    "Outdoor": {
        "Jogging (8 km/h)": {"kcal_per_hour": 480, "per_km": 60},
        "Brisk Walk (5 km/h)": {"kcal_per_hour": 280, "per_km": 50},
        "Cycling (15 km/h)": {"kcal_per_hour": 400, "per_km": 30}
    },
    "Indoor (no equipment)": {
        "Jumping Jack": {"kcal_per_hour": 600},
        "Squat": {"kcal_per_hour": 480},
        "Plank": {"kcal_per_hour": 240}
    },
    "Indoor (with equipment)": {
        "Treadmill (6 km/h)": {"kcal_per_hour": 300},
        "Elliptical": {"kcal_per_hour": 350},
        "Rowing Machine": {"kcal_per_hour": 400}
    }
}

def calories_burned(kcal_per_hour, duration_min, weight):
    return kcal_per_hour * (duration_min / 60) * (weight / 70)

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🏃 Health & Fitness App")
st.write("Gabungan Kalkulator BMI + Kalori + Multi-Aktiviti Senaman")

# Input Asas
age = st.number_input("Umur", min_value=10, max_value=100, value=25, step=1)
gender = st.radio("Jantina", ["Lelaki", "Perempuan"])
height = st.number_input("Tinggi (cm)", min_value=100, max_value=220, value=170, step=1)
weight = st.number_input("Berat sekarang (kg)", 30, 200, 70)
target_weight = st.number_input("Berat sasaran (kg)", 30, 200, 65)
duration_days = st.number_input("Tempoh sasaran (hari)", 1, 365, 30)
standard = st.selectbox("Pilih standard BMI", list(bmi_standards.keys()))

if st.button("Kira BMI & Kalori"):
    # Kiraan BMI
    bmi = weight / ((height/100) ** 2)
    category = classify_bmi(bmi, standard)
    st.subheader("📊 Hasil BMI")
    st.success(f"BMI anda: **{bmi:.1f}**")
    st.info(f"Kategori ({standard}): **{category}**")
    st.write(f"Umur: {age} tahun | Jantina: {gender}")

    # Kiraan Kalori
    total_cal, per_day = calorie_calculator(weight, target_weight, duration_days)
    st.subheader("🔥 Kiraan Kalori")
    st.success(f"Jumlah kalori perlu dibakar: {total_cal:,.0f} kcal")
    st.info(f"Purata sehari: {per_day:,.0f} kcal")

    # Multi Aktiviti
    st.subheader("🏋️ Pilih Sehingga 5 Aktiviti Senaman")

    total_burned = 0
    activity_results = []

    for i in range(1, 6):
        with st.expander(f"Aktiviti {i}"):
            category_choice = st.selectbox(f"Kategori Aktiviti {i}", list(activities.keys()), key=f"cat{i}")
            activity_choice = st.selectbox(f"Aktiviti {i}", list(activities[category_choice].keys()), key=f"act{i}")
            duration_min = st.slider(f"Tempoh (minit) {i}", 10, 120, 30, key=f"dur{i}")

            distance_km = None
            if category_choice == "Outdoor" and "per_km" in activities[category_choice][activity_choice]:
                distance_km = st.slider(f"Jarak (km) {i}", 1, 20, 5, key=f"dist{i}")

            kcal_info = activities[category_choice][activity_choice]
            kcal_hour = kcal_info["kcal_per_hour"]

            if distance_km:
                cal_burn = kcal_info["per_km"] * distance_km * (weight / 70)
            else:
                cal_burn = calories_burned(kcal_hour, duration_min, weight)

            total_burned += cal_burn
            activity_results.append((activity_choice, cal_burn))

    # Hasil Multi Aktiviti
    st.subheader("📋 Ringkasan Aktiviti")
    st.write(f"Jumlah kalori terbakar: **{total_burned:.0f} kcal**")
    remaining = per_day - total_burned

    # Progress bar
    progress = min(total_burned / per_day, 1.0) if per_day > 0 else 0
    st.progress(progress)
    st.write(f"✅ Pencapaian: {progress*100:.1f}% daripada target harian")

    if remaining > 0:
        st.warning(f"Masih perlu bakar: **{remaining:.0f} kcal**")
    else:
        st.success("🎉 Target kalori harian sudah dicapai dengan aktiviti terpilih!")

    # Berapa sesi diperlukan untuk cover baki
    if remaining > 0:
        st.subheader("🔄 Sesi Tambahan Diperlukan")
        for act, cal in activity_results:
            if cal > 0:
                sessions = math.ceil(remaining / cal)
                st.info(f"Jika guna {act} sahaja → perlu **{sessions} sesi tambahan**")

    # Pie chart visual
    if activity_results:
        st.subheader("📊 Pecahan Aktiviti (Pie Chart)")
        labels = [a for a, _ in activity_results]
        values = [c for _, c in activity_results]

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%")
        ax.set_title("Sumbangan Kalori Terbakar Mengikut Aktiviti")
        st.pyplot(fig)
