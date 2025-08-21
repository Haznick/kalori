import streamlit as st
import math

# -----------------------------
# 1. Data & Fungsi BMI
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
# 2. Data & Fungsi Kalori
# -----------------------------
def calorie_calculator(current_weight, target_weight, duration_days):
    # anggaran 7700 kcal per 1kg
    total_loss = current_weight - target_weight
    total_calories = total_loss * 7700
    per_day = total_calories / duration_days if duration_days > 0 else 0
    return total_calories, per_day

activities = {
    "Outdoor": {
        "Jogging (8 km/h)": 480,   # kcal/jam untuk 70kg
        "Brisk Walk (5 km/h)": 280,
        "Cycling (15 km/h)": 400
    },
    "Indoor (no equipment)": {
        "Jumping Jack": 100,
        "Squat": 80,
        "Plank": 60
    },
    "Indoor (with equipment)": {
        "Treadmill (6 km/h)": 300,
        "Elliptical": 350,
        "Rowing Machine": 400
    }
}

def calories_burned(activity_cal_per_hour, duration_min, weight):
    # Anggaran linear ikut berat user
    return activity_cal_per_hour * (duration_min / 60) * (weight / 70)

# -----------------------------
# 3. Streamlit UI
# -----------------------------
st.title("🏃 Health & Fitness App")
st.write("Kira BMI dan sasaran kalori untuk kurangkan berat badan.")

menu = st.sidebar.radio("Pilih modul", ["📊 BMI Calculator", "🔥 Calorie & Exercise Planner"])

# -----------------------------
# Modul 1: BMI
# -----------------------------
if menu == "📊 BMI Calculator":
    st.header("📊 Kalkulator BMI")

    age = st.number_input("Umur", min_value=10, max_value=100, value=25, step=1)
    gender = st.radio("Jantina", ["Lelaki", "Perempuan"])
    height = st.number_input("Tinggi (cm)", min_value=100, max_value=220, value=170, step=1)
    weight = st.number_input("Berat (kg)", min_value=30, max_value=200, value=70, step=1)
    standard = st.selectbox("Pilih standard BMI", list(bmi_standards.keys()))

    if st.button("Kira BMI"):
        bmi = weight / ((height/100) ** 2)
        category = classify_bmi(bmi, standard)

        st.success(f"BMI anda: **{bmi:.1f}**")
        st.info(f"Kategori ({standard}): **{category}**")
        st.write(f"Umur: {age} tahun | Jantina: {gender}")

# -----------------------------
# Modul 2: Calorie & Exercise Planner
# -----------------------------
if menu == "🔥 Calorie & Exercise Planner":
    st.header("🔥 Kalkulator Kalori & Aktiviti Senaman")

    current_weight = st.number_input("Berat sekarang (kg)", 30, 200, 70)
    target_weight = st.number_input("Berat sasaran (kg)", 30, 200, 65)
    duration_days = st.number_input("Tempoh sasaran (hari)", 1, 365, 30)

    if st.button("Kira Kalori Harian"):
        total_cal, per_day = calorie_calculator(current_weight, target_weight, duration_days)

        st.success(f"Jumlah kalori perlu dibakar: {total_cal:,.0f} kcal")
        st.info(f"Purata sehari: {per_day:,.0f} kcal")

        st.subheader("Cadangan Aktiviti Senaman")
        for category, acts in activities.items():
            st.write(f"**{category}**")
            for act, kcal in acts.items():
                cal_burn = calories_burned(kcal, 30, current_weight)
                sessions = math.ceil(per_day / cal_burn) if cal_burn > 0 else 0
                st.write(f"- {act}: ~{cal_burn:.0f} kcal / 30 min → perlu **{sessions} sesi** sehari")
