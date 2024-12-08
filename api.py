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
        st.write("The pie chart illustrates proportion of the nymber of men and women.")
        st.plotly_chart(self.graph_generator.pie_chart_gender(), use_container_width=True)

        st.subheader("Smokers")
        st.write("The pie chart shows the percentage of smokers and non-smokers")
        st.plotly_chart(self.graph_generator.pie_chart_smokers(), use_container_width=True)

        st.subheader("The number of children for men and women")
        st.write(
            "The graph indicates the quantity of men and women without childrenand those, who has one ore more children")
        st.plotly_chart(self.graph_generator.children_histogram(), use_container_width=True)

        st.subheader("BMI's dependence on smoking")
        st.write("The box plot shows relationship between BMI and status of smoking")
        st.plotly_chart(self.graph_generator.plot_bmi_smoker_relationship(), use_container_width=True)

        st.subheader("The sum of charges for men and women with a certain smoking status")
        st.plotly_chart(self.graph_generator.gender_smoker(), use_container_width=True)

        st.subheader("The average charges by regions")
        st.write("The bar chart illustrates the average charges in every region")
        st.plotly_chart(self.graph_generator.bar_charges_age_by_region(), use_container_width=True)

        st.subheader("The numbers of smokers in regions")
        st.plotly_chart(self.graph_generator.smokers_region_histogram(), use_container_width=True)

        st.subheader("Number of people with children in region")
        st.plotly_chart(self.graph_generator.children_region_histogram(), use_container_width=True)

        st.subheader("Correlation")
        st.write("The correlation heatmap visualizes linear relationships between numerical features")
        st.plotly_chart(self.graph_generator.correlation(), use_container_width=True)

        st.subheader("Charges vs Age")
        st.write(
            "The graph shows the relationship between age and medical charges, with points color-coded based on smoking status.")
        st.plotly_chart(self.graph_generator.plot_charges_vs_age(), use_container_width=True)

        st.subheader("Dependence of expenses on BMI by smoking status")
        st.write(
            "The graph illustrates the relationship between BMI and medical expenses, with data divided by smoking status.")
        st.plotly_chart(self.graph_generator.bmi_charges_smoker(), use_container_width=True)

        st.subheader("Medical Charges for Smokers vs Non-Smokers")
        st.write("The boxplot shows the relationship between medical charge and status of smoking")
        st.plotly_chart(self.graph_generator.plot_smoker_vs_charges_boxplot(), use_container_width=True)

        st.subheader("Hypothesis")
        st.write(
            "Let's assume that the average charge for men who smoke over 30 are higher than for non-smoking women over 30 without children. To confirm the hypothesis, let's look at the graphs of each group, and then compare them.")
        fig = self.graph_generator.plot_age_vs_charges_with_conditions()
        st.pyplot(fig)
        df_m = self.df[(self.df['age'] > 30) & (self.df['smoker'] == 'yes') & (self.df['sex'] == 'male')]
        df_w = self.df[(self.df['age'] > 30) & (self.df['smoker'] == 'no') & (self.df['sex'] == 'female') & (
                    self.df['children'] == 0)]
        men_av = df_m["charges"].mean()
        women_av = df_w["charges"].mean()
        st.write(f"The average charge of men over 30:", f"{men_av:.02f}")
        st.write(f"The average charge of women over 30 without children: {women_av:.02f}")
        st.write(
            "We can see, that the average charge of the first group is significantly higher in comparison to the second group. Moreover, we see from our calculation that the average charges of smoking men over 30 is three times hihger than of women over 30 without children. If we recall my hypothesis, we understad that with the help of graphs and calculations, we have proved its truthfulness. It is obviously true that men who smoke have higher charge than non-smoking women without children.")

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
