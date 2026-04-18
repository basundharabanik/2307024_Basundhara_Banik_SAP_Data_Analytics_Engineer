import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html

# ── Load CSV files ─────────────────────────────────────────────────────────────
patients     = pd.read_csv(r"C:\Users\KIIT0001\Desktop\Hospital_Patient_Data_Analysis\Data\Patients.csv")
doctors      = pd.read_csv(r"C:\Users\KIIT0001\Desktop\Hospital_Patient_Data_Analysis\Data\Doctors.csv")
appointments = pd.read_csv(r"C:\Users\KIIT0001\Desktop\Hospital_Patient_Data_Analysis\Data\Appointments.csv")

# ── Calculations ───────────────────────────────────────────────────────────────
merged = appointments.merge(doctors, on="doctor_id").merge(patients, on="patient_id")

patients_per_doctor = merged.groupby("doctor_name")["patient_id"].count().reset_index()
patients_per_doctor.columns = ["Doctor", "Patients"]

common_diseases = merged["diagnosis"].value_counts().reset_index()
common_diseases.columns = ["Disease", "Count"]

gender_split = patients["gender"].value_counts().reset_index()
gender_split.columns = ["Gender", "Count"]

age_groups = pd.cut(patients["age"], bins=[0,20,40,60,100], labels=["0-20","21-40","41-60","60+"])
age_data = age_groups.value_counts().reset_index()
age_data.columns = ["Age Group", "Count"]

# ── Charts ─────────────────────────────────────────────────────────────────────
fig1 = px.bar(patients_per_doctor, x="Doctor", y="Patients",
              title="Number of Patients per Doctor",
              color="Patients", color_continuous_scale="Blues",
              text="Patients")
fig1.update_traces(textposition="outside")

fig2 = px.pie(common_diseases, names="Disease", values="Count",
              title="Most Common Diseases",
              color_discrete_sequence=px.colors.sequential.RdBu)

fig3 = px.bar(common_diseases, x="Disease", y="Count",
              title="Disease Frequency",
              color="Count", color_continuous_scale="Reds",
              text="Count")
fig3.update_traces(textposition="outside")

fig4 = px.pie(gender_split, names="Gender", values="Count",
              title="Patient Gender Distribution",
              color_discrete_sequence=["#3498db","#e91e8c"])

fig5 = px.bar(age_data, x="Age Group", y="Count",
              title="Patients by Age Group",
              color="Count", color_continuous_scale="Greens",
              text="Count")
fig5.update_traces(textposition="outside")

# ── Dashboard ──────────────────────────────────────────────────────────────────
app = dash.Dash(__name__)

app.layout = html.Div(style={"backgroundColor": "#f4f6f9", "fontFamily": "Arial"}, children=[

    # ── Header ────────────────────────────────────────────────────────────────
    html.Div(style={"backgroundColor": "#2c3e50", "padding": "30px", "textAlign": "center"}, children=[
        html.H1("🏥 Hospital Patient Data Analysis Dashboard",
                style={"color": "white", "margin": "0", "fontSize": "28px"}),
        html.P("Analysis of Patients, Doctors and Appointments",
               style={"color": "#bdc3c7", "margin": "5px 0 0 0"}),
    ]),

    # ── Summary Cards ─────────────────────────────────────────────────────────
    html.Div(style={"display": "flex", "justifyContent": "center",
                    "gap": "20px", "padding": "30px"}, children=[

        html.Div(style={"backgroundColor": "white", "padding": "20px 40px",
                        "borderRadius": "10px", "textAlign": "center",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                        "borderTop": "4px solid #3498db"}, children=[
            html.H2(f"{len(patients)}", style={"color": "#3498db", "margin": "0", "fontSize": "36px"}),
            html.P("Total Patients", style={"margin": "5px 0 0 0", "color": "#666"}),
        ]),

        html.Div(style={"backgroundColor": "white", "padding": "20px 40px",
                        "borderRadius": "10px", "textAlign": "center",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                        "borderTop": "4px solid #2ecc71"}, children=[
            html.H2(f"{len(doctors)}", style={"color": "#2ecc71", "margin": "0", "fontSize": "36px"}),
            html.P("Total Doctors", style={"margin": "5px 0 0 0", "color": "#666"}),
        ]),

        html.Div(style={"backgroundColor": "white", "padding": "20px 40px",
                        "borderRadius": "10px", "textAlign": "center",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                        "borderTop": "4px solid #e74c3c"}, children=[
            html.H2(f"{len(appointments)}", style={"color": "#e74c3c", "margin": "0", "fontSize": "36px"}),
            html.P("Total Appointments", style={"margin": "5px 0 0 0", "color": "#666"}),
        ]),

        html.Div(style={"backgroundColor": "white", "padding": "20px 40px",
                        "borderRadius": "10px", "textAlign": "center",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                        "borderTop": "4px solid #f39c12"}, children=[
            html.H2(f"{common_diseases.iloc[0]['Disease']}", style={"color": "#f39c12", "margin": "0", "fontSize": "24px"}),
            html.P("Most Common Disease", style={"margin": "5px 0 0 0", "color": "#666"}),
        ]),
    ]),

    # ── Row 1: Two charts ──────────────────────────────────────────────────────
    html.Div(style={"display": "flex", "gap": "20px", "padding": "0 30px"}, children=[
        html.Div(dcc.Graph(figure=fig1),
                 style={"flex": "1", "backgroundColor": "white",
                        "borderRadius": "10px", "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"}),
        html.Div(dcc.Graph(figure=fig2),
                 style={"flex": "1", "backgroundColor": "white",
                        "borderRadius": "10px", "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"}),
    ]),

    # ── Row 2: Three charts ────────────────────────────────────────────────────
    html.Div(style={"display": "flex", "gap": "20px", "padding": "20px 30px 30px 30px"}, children=[
        html.Div(dcc.Graph(figure=fig3),
                 style={"flex": "1", "backgroundColor": "white",
                        "borderRadius": "10px", "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"}),
        html.Div(dcc.Graph(figure=fig4),
                 style={"flex": "1", "backgroundColor": "white",
                        "borderRadius": "10px", "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"}),
        html.Div(dcc.Graph(figure=fig5),
                 style={"flex": "1", "backgroundColor": "white",
                        "borderRadius": "10px", "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"}),
    ]),

    # ── Footer ─────────────────────────────────────────────────────────────────
    html.Div(style={"textAlign": "center", "padding": "20px",
                    "color": "#888", "fontSize": "13px"}, children=[
        html.P("Hospital Patient Data Analysis | Capstone Project 2026")
    ])
])

if __name__ == "__main__":
    app.run(debug=True)