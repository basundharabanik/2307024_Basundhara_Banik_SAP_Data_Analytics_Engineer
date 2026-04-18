import pandas as pd
import os

# ── STEP 1: Load the CSV files ────────────────────────────────────────────────
patients     = pd.read_csv(r"C:\Users\KIIT0001\Desktop\Hospital_Patient_Data_Analysis\Data\Patients.csv")
doctors      = pd.read_csv(r"C:\Users\KIIT0001\Desktop\Hospital_Patient_Data_Analysis\Data\Doctors.csv")
appointments = pd.read_csv(r"C:\Users\KIIT0001\Desktop\Hospital_Patient_Data_Analysis\Data\Appointments.csv")

print(" Files loaded successfully")
print(f"   Patients: {len(patients)} rows")
print(f"   Doctors: {len(doctors)} rows")
print(f"   Appointments: {len(appointments)} rows\n")

print("📋 Patients columns:", list(patients.columns))
print("📋 Doctors columns:", list(doctors.columns))
print("📋 Appointments columns:", list(appointments.columns))
print()

# ── STEP 2: Merge all three files ─────────────────────────────────────────────
merged = appointments.merge(doctors, on="doctor_id")
merged = merged.merge(patients, on="patient_id")

# ── STEP 3: Patients per doctor ───────────────────────────────────────────────
patients_per_doctor = merged.groupby("doctor_name")["patient_id"].count().reset_index()
patients_per_doctor.columns = ["Doctor Name", "Number of Patients"]
patients_per_doctor = patients_per_doctor.sort_values("Number of Patients", ascending=False)

print("📊 Number of Patients Per Doctor:")
print(patients_per_doctor.to_string(index=False))
print()


# ── STEP 4: Most common diseases ──────────────────────────────────────────────
common_diseases = merged["diagnosis"].value_counts().reset_index()
common_diseases.columns = ["Disease", "Count"]

print("🦠 Most Common Diseases:")
print(common_diseases.to_string(index=False))
print()

# ── STEP 5: Save results ──────────────────────────────────────────────────────
os.makedirs(r"C:\Users\KIIT0001\Desktop\Hospital_Patient_Data_Analysis\Data\Output", exist_ok=True)

patients_per_doctor.to_csv(r"C:\Users\KIIT0001\Desktop\Hospital_Patient_Data_Analysis\Data\Output\patients_per_doctor.csv", index=False)
common_diseases.to_csv(r"C:\Users\KIIT0001\Desktop\Hospital_Patient_Data_Analysis\Data\Output\common_diseases.csv", index=False)

print("Results saved to Output folder")