#Import Library
import streamlit as st
import pandas as pd
import pickle as pkl

#Load model
@st.cache_data
def load_model():
    with open("xgboost_model.pkl", "rb") as file:
        model = pkl.load(file)
    return model

model = load_model()

#Title
st.title("Prediksi Pembatalan Booking Hotel")

#Test Case
st.sidebar.title("Test Case")
if st.sidebar.button("Test Case 1 - Tidak Dibatalkan"):
    st.session_state.update({
        'Jumlah Orang Dewasa': 2,
        'Jumlah Anak Kecil': 0,
        'Jumlah malam akhir pekan tamu menginap atau memesan untuk menginap di hotel': 1,
        'Jumlah malam dalam seminggu tamu menginap atau memesan untuk menginap di hotel': 2,
        'Meal Plan': 1,
        'Apakah pelanggan membutuhkan tempat parkir mobil?': 0,
        'Tipe Kamar': 1,
        'Lead Time (hari)': 20,
        'Tahun Kedatangan': 2018,
        'Bulan Kedatangan': 7,
        'Tanggal Kedatangan': 15,
        'Penunjukan segmen pasar': 3,
        'Tamu Langganan?': 0,
        'Jumlah Pembatalan Sebelumnya': 0,
        'Booking Sebelumnya Tidak Dibatalkan': 0,
        'Harga Rata-Rata per Kamar': 80.0,
        'Jumlah Permintaan Khusus': 0
    })
    st.rerun()

if st.sidebar.button("Test Case 2 - Dibatalkan"):
    st.session_state.update({
        'Jumlah Orang Dewasa': 1,
        'Jumlah Anak Kecil': 1,
        'Jumlah malam akhir pekan tamu menginap atau memesan untuk menginap di hotel': 0,
        'Jumlah malam dalam seminggu tamu menginap atau memesan untuk menginap di hotel': 0,
        'Meal Plan': 2,
        'Apakah pelanggan membutuhkan tempat parkir mobil?': 0,
        'Tipe Kamar': 3,
        'Lead Time (hari)': 100,
        'Tahun Kedatangan': 2018,
        'Bulan Kedatangan': 12,
        'Tanggal Kedatangan': 20,
        'Penunjukan segmen pasar': 4,
        'Tamu Langganan?': 0,
        'Jumlah Pembatalan Sebelumnya': 1,
        'Booking Sebelumnya Tidak Dibatalkan': 0,
        'Harga Rata-Rata per Kamar': 200.0,
        'Jumlah Permintaan Khusus': 2
    })
    st.rerun()

#Input
with st.form("booking_form"):
    st.subheader("Masukkan data booking")

    no_of_adults = st.number_input("Jumlah Orang Dewasa", min_value=1, max_value=10, key="Jumlah Orang Dewasa")
    no_of_children = st.number_input("Jumlah Anak Kecil", min_value=0, max_value=10, key="Jumlah Anak Kecil")
    no_of_weekend_nights = st.number_input("Jumlah malam akhir pekan tamu menginap atau memesan untuk menginap di hotel", min_value=0, max_value=10, key="Jumlah malam akhir pekan tamu menginap atau memesan untuk menginap di hotel")
    no_of_week_nights = st.number_input("Jumlah malam dalam seminggu tamu menginap atau memesan untuk menginap di hotel", min_value=0, max_value=10, key="Jumlah malam dalam seminggu tamu menginap atau memesan untuk menginap di hotel")
    type_of_meal_plan = st.selectbox("Meal Plan", [1, 2, 3], index=[1, 2, 3].index(st.session_state.get("Meal Plan", 1)), key="Meal Plan")
    required_car_parking_space = st.selectbox("Apakah pelanggan membutuhkan tempat parkir mobil?", [0, 1], index=[0, 1].index(st.session_state.get("Butuh Parkir?", 0)), key="Apakah pelanggan membutuhkan tempat parkir mobil?")
    room_type_reserved = st.selectbox("Tipe Kamar", [1, 2, 3, 4, 5, 6, 7], index=[1, 2, 3, 4, 5, 6, 7].index(st.session_state.get("Tipe Kamar", 1)), key="Tipe Kamar")
    lead_time = st.number_input("Lead Time (hari)", min_value=0, key="Lead Time (hari)")
    arrival_year = st.selectbox("Tahun Kedatangan", [2017, 2018], index=[2017, 2018].index(st.session_state.get("Tahun Kedatangan", 2018)), key="Tahun Kedatangan")
    arrival_month = st.selectbox("Bulan Kedatangan", list(range(1, 13)), index=list(range(1, 13)).index(st.session_state.get("Bulan Kedatangan", 1)), key="Bulan Kedatangan")
    arrival_date = st.selectbox("Tanggal Kedatangan", list(range(1, 32)), index=list(range(1, 32)).index(st.session_state.get("Tanggal Kedatangan", 1)), key="Tanggal Kedatangan")
    market_segment_type = st.selectbox("Penunjukan segmen pasar", [1, 2, 3, 4, 5, 6, 7], index=[1, 2, 3, 4, 5, 6, 7].index(st.session_state.get("Penunjukan segmen pasar", 1)), key="Penunjukan segmen pasar")
    repeated_guest = st.selectbox("Tamu Langganan?", [0, 1], index=[0, 1].index(st.session_state.get("Tamu Langganan?", 0)), key="Tamu Langganan?")
    no_of_previous_cancellations = st.number_input("Jumlah Pembatalan Sebelumnya", min_value=0, key="Jumlah Pembatalan Sebelumnya")
    no_of_previous_bookings_not_canceled = st.number_input("Booking Sebelumnya Tidak Dibatalkan", min_value=0, key="Booking Sebelumnya Tidak Dibatalkan")
    avg_price_per_room = st.number_input("Harga Rata-Rata per Kamar", min_value=0.0, key="Harga Rata-Rata per Kamar")
    no_of_special_requests = st.number_input("Jumlah Permintaan Khusus", min_value=0, key="Jumlah Permintaan Khusus")

    submit = st.form_submit_button("Prediksi")

#Prediksi
if submit:
    input_data = pd.DataFrame({
        'no_of_adults': [no_of_adults],
        'no_of_children': [no_of_children],
        'no_of_weekend_nights': [no_of_weekend_nights],
        'no_of_week_nights': [no_of_week_nights],
        'type_of_meal_plan': [type_of_meal_plan],
        'required_car_parking_space': [required_car_parking_space],
        'room_type_reserved': [room_type_reserved],
        'lead_time': [lead_time],
        'arrival_year': [arrival_year],
        'arrival_month': [arrival_month],
        'arrival_date': [arrival_date],
        'market_segment_type': [market_segment_type],
        'repeated_guest': [repeated_guest],
        'no_of_previous_cancellations': [no_of_previous_cancellations],
        'no_of_previous_bookings_not_canceled': [no_of_previous_bookings_not_canceled],
        'avg_price_per_room': [avg_price_per_room],
        'no_of_special_requests': [no_of_special_requests]
    })

    prediction = model.predict(input_data)[0]
    label = "❌ Dibatalkan (Canceled)" if prediction == 1 else "✅ Tidak Dibatalkan (Not Canceled)"

    st.success(f"Hasil Prediksi: {label}")
