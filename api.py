import streamlit as st
import pandas as pd
import requests
from preprocessing import get_min_max
import grahps


class InsuranceFrontendApp:
    def __init__(self, backend_url):
        self.backend_url = backend_url
        self.df = self.load_data()
        self.graph_generator = grahps.Medical_cost(self.df)

    @staticmethod
    def load_data():
        try:
            df = pd.read_csv("insurance.csv")
            return df
        except Exception as e:
            st.error(f"Error loading dataset: {e}")
            return pd.DataFrame()

    def display_form(self):
        st.title("Insurance Data Matching")

        min_ma_a = get_min_max(self.df, "age")
        min_ma_b = get_min_max(self.df, "bmi")
        min_ma_c = get_min_max(self.df, "children")

        # Create form for input
        with st.form("Match Data"):
            a = st.slider("Age", min_value=min_ma_a[0], max_value=min_ma_a[1])
            b = st.slider("BMI", min_value=min_ma_b[0], max_value=min_ma_b[1])
            c = st.slider("Children", min_value=min_ma_c[0], max_value=min_ma_c[1])

            g = st.radio("Gender", options=["Male", "Female"])
            s = st.radio("Smoking status", options=["Yes", "No"])
            r = st.radio("Region", options=["Southwest", "Southeast", "Northwest", "Northeast"])

            sb = st.form_submit_button(label="Match")

        if sb:
            self.submit_form(a, b, c, g, s, r)

    def submit_form(self, age, bmi, children, gender, smoker, region):
        data = {
            "age": age,
            "bmi": bmi,
            "gender": gender.lower(),
            "children": children,
            "smoke": smoker.lower(),
            "region": region.lower(),
        }
        try:
            response = requests.post(f"{self.backend_url}/submit_form", json=data)
            if response.status_code == 200:
                st.subheader("Your average charge")
                charges = response.json()
                if charges and "average_charges" in charges:
                    st.write(charges['average_charges'])
                elif charges and "random_charge" in charges:
                    st.write(charges['random_charge'])
                else:
                    st.error("Failed to retrieve data.")


            else:
                st.error(f"Failed to match data. Error: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the backend: {e}")

    def display_add_data_form(self):
        st.header("Add New Insurance Record")
        min_ma_a = get_min_max(self.df, "age")
        min_ma_b = get_min_max(self.df, "bmi")
        min_ma_c = get_min_max(self.df, "children")

        with st.form("Add Data"):
            age = st.number_input("Age", min_value=min_ma_a[0], max_value=min_ma_a[1], step=1)
            sex = st.selectbox("Sex", options=["male", "female"])
            bmi = st.number_input("BMI", min_value=min_ma_b[0], max_value=min_ma_b[1], step=0.1)
            children = st.number_input("Children", min_value=min_ma_c[0], max_value=min_ma_c[1], step=1)
            smoker = st.selectbox("Smoker Status", options=["yes", "no"])
            region = st.selectbox("Region", options=["southwest", "southeast", "northwest", "northeast"])
            charges = st.number_input("Charges", min_value=800, max_value=100000)

            submitted = st.form_submit_button("Add Record")
            if submitted:
                self.add_data(age, sex, bmi, children, smoker, region, charges)

    def add_data(self, age, sex, bmi, children, smoker, region, charges):
        data = {
            "age": age,
            "sex": sex,
            "bmi": bmi,
            "children": children,
            "smoker": smoker,
            "region": region,
            "charges": charges,
        }

        try:
            response = requests.post(f"{self.backend_url}/add_data", json=data)
            if response.status_code == 200:
                st.success("Data added successfully!")
                self.df = self.load_data()
                self.display_graphs()
            else:
                st.error(f"Failed to add data. Error: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the backend: {e}")

    def display_graphs(self):
        st.header("Insurance Data Visualizations")

        st.subheader("Genders")
        st.plotly_chart(self.graph_generator.pie_chart_gender(), use_container_width=True)

        st.subheader("Smokers")
        st.plotly_chart(self.graph_generator.pie_chart_smokers(), use_container_width=True)

        st.subheader("The number of children for men and women")
        st.plotly_chart(self.graph_generator.children_histogram(), use_container_width=True)

        st.subheader("BMI's dependence on smoking")
        st.plotly_chart(self.graph_generator.plot_bmi_smoker_relationship(), use_container_width=True)

        st.subheader("The sum of charges for men and women with a certain smoking status")
        st.plotly_chart(self.graph_generator.gender_smoker(), use_container_width=True)

        st.subheader("The average charges by regions")
        st.plotly_chart(self.graph_generator.bar_charges_age_by_region(), use_container_width=True)

        st.subheader("The numbers of smokers in regions")
        st.plotly_chart(self.graph_generator.smokers_region_histogram(), use_container_width=True)

        st.subheader("Number of people with children in region")
        st.plotly_chart(self.graph_generator.children_region_histogram(), use_container_width=True)

        st.subheader("Correlation")
        st.plotly_chart(self.graph_generator.correlation(), use_container_width=True)

        st.subheader("Charges vs Age")
        st.plotly_chart(self.graph_generator.plot_charges_vs_age(), use_container_width=True)

        st.subheader("Dependence of expenses on BMI by smoking status")
        st.plotly_chart(self.graph_generator.bmi_charges_smoker(), use_container_width=True)

        st.subheader("Medical Charges for Smokers vs Non-Smokers")
        st.plotly_chart(self.graph_generator.plot_smoker_vs_charges_boxplot(), use_container_width=True)

        st.subheader("Average expenses by region and number of children")
        st.plotly_chart(self.graph_generator.charges_region_children(), use_container_width=True)

    def run(self):
        st.title("Insurance Analysis Dashboard")

        tab1, tab2, tab3 = st.tabs(["Match Data", "Add Data", "View Graphs"])
        with tab1:
            self.display_form()

        with tab2:
            self.display_add_data_form()

        with tab3:
            if not self.df.empty:
                self.display_graphs()
            else:
                st.warning("No data available for visualizations.")


if __name__ == "__main__":
    BACKEND_URL = "http://127.0.0.1:8000"
    app = InsuranceFrontendApp(BACKEND_URL)
    app.run()
