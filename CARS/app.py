import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="MediCare Clinic System", page_icon="🏥", layout="wide")

# --- MOCK DATABASE ---
if 'patients' not in st.session_state:
    st.session_state.patients = {
        "P001": {"name": "Ali bin Ahmad", "phone": "012-3456789", "is_emergency": False},
        "P002": {"name": "Siti Aminah", "phone": "019-8765432", "is_emergency": False}
    }

if 'appointments' not in st.session_state:
    st.session_state.appointments = {
        ("Dr. Tan", "2026-10-25", "09:00 AM"): "P001"
    }

# --- UI HEADER ---
st.title("🏥 MediCare Clinic Appointment & Record System (CARS)")
st.markdown("---")

# --- NAVIGATION SIDEBAR ---
menu = st.sidebar.selectbox("Select Role / Menu", 
    ["Patient Portal (Book Appointment)", "Receptionist Dashboard", "Doctor View", "Manager Reports"]
)

# ==========================================
# 1. PATIENT PORTAL & DECISION LOGIC
# ==========================================
if menu == "Patient Portal (Book Appointment)":
    st.header("Book an Appointment")
    
    with st.form("booking_form"):
        col1, col2 = st.columns(2)
        with col1:
            patient_id = st.text_input("Enter Patient ID (e.g., P001, or type 'NEW' if unregistered)")
            doctor = st.selectbox("Select Doctor", ["Dr. Tan", "Dr. Lim", "Dr. Wong"])
            date = st.date_input("Select Date", datetime.now())
        
        with col2:
            time = st.selectbox("Select Time", ["09:00 AM", "10:00 AM", "11:00 AM", "02:00 PM", "03:00 PM"])
            is_emergency = st.checkbox("Check if this is an EMERGENCY")
            submit = st.form_submit_button("Request Appointment")

    if submit:
        date_str = date.strftime("%Y-%m-%d")
        slot_key = (doctor, date_str, time)
        
        st.subheader("System Processing:")
        
        if patient_id not in st.session_state.patients and patient_id != "NEW":
            st.error("❌ Rule 6: Patient not registered. Please register at the front desk first.")
        else:
            slot_taken = slot_key in st.session_state.appointments
            doctor_on_duty = not (doctor == "Dr. Lim" and date.weekday() == 6) 

            if not slot_taken and doctor_on_duty:
                st.session_state.appointments[slot_key] = patient_id
                st.success(f"✅ Rule 1 (Confirm): Booking confirmed for {patient_id} with {doctor} on {date_str} at {time}.")
            elif slot_taken:
                if is_emergency:
                    st.warning(f"🚨 Rule 4 (Emergency): Slot is taken, but patient is flagged as EMERGENCY. Escalated to emergency queue. Doctor alerted!")
                else:
                    st.info(f"ℹ️ Rule 3 (Alternative): The slot {time} with {doctor} is already taken. Please select another time or doctor.")
            elif not doctor_on_duty:
                st.warning(f"ℹ️ Rule 2 (Alternative): {doctor} is not on duty on this date (Sundays). Please choose another day or doctor.")

# ==========================================
# 2. RECEPTIONIST DASHBOARD
# ==========================================
elif menu == "Receptionist Dashboard":
    st.header("📋 Daily Schedule")
    if len(st.session_state.appointments) == 0:
        st.info("No appointments booked yet.")
    else:
        data = []
        for (doc, date, time), p_id in st.session_state.appointments.items():
            p_name = st.session_state.patients.get(p_id, {}).get("name", "Unknown")
            data.append({"Date": date, "Time": time, "Doctor": doc, "Patient ID": p_id, "Patient Name": p_name})
        
        df = pd.DataFrame(data)
        st.dataframe(df.sort_values(by=["Date", "Time"]), use_container_width=True)
        
    st.markdown("---")
    st.subheader("Register New Patient")
    with st.form("register_form"):
        new_id = st.text_input("New Patient ID (e.g., P003)")
        new_name = st.text_input("Full Name")
        new_phone = st.text_input("Phone Number")
        reg_submit = st.form_submit_button("Register Patient")
        
        if reg_submit and new_id and new_name:
            st.session_state.patients[new_id] = {"name": new_name, "phone": new_phone, "is_emergency": False}
            st.success(f"Patient {new_name} registered successfully as {new_id}!")

# ==========================================
# 3. DOCTOR VIEW
# ==========================================
elif menu == "Doctor View":
    st.header("👨‍⚕️ Doctor Consultation")
    doctor_select = st.selectbox("Login as Doctor", ["Dr. Tan", "Dr. Lim", "Dr. Wong"])
    
    doc_appts = {k: v for k, v in st.session_state.appointments.items() if k[0] == doctor_select}
    
    if not doc_appts:
        st.info("No appointments scheduled for you today.")
    else:
        st.write("### Your Today's Patients")
        for (doc, date, time), p_id in doc_appts.items():
            p_name = st.session_state.patients.get(p_id, {}).get("name", "Unknown")
            with st.expander(f"{time} - {p_name} ({p_id})"):
                st.write(f"**Date:** {date}")
                st.write(f"**Phone:** {st.session_state.patients[p_id]['phone']}")
                st.text_area("Consultation Notes", placeholder="Enter diagnosis and prescription here...", key=f"note_{p_id}_{time}")
                st.button("Save Record", key=f"save_{p_id}_{time}")

# ==========================================
# 4. MANAGER REPORTS
# ==========================================
elif menu == "Manager Reports":
    st.header("📊 Clinic Performance Dashboard")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Registered Patients", len(st.session_state.patients))
    col2.metric("Total Booked Appointments", len(st.session_state.appointments))
    col3.metric("System Status", "Online", "99.9% Uptime")
    
    st.markdown("---")
    st.subheader("Appointments by Doctor")
    if len(st.session_state.appointments) > 0:
        data = [{"Doctor": k[0]} for k in st.session_state.appointments.keys()]
        df = pd.DataFrame(data)
        st.bar_chart(df["Doctor"].value_counts())
    else:
        st.info("Not enough data to generate charts.")