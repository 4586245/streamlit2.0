import uuid
import seaborn as sns
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# raise HTTPException(status_code=404, detail="No matching data found.")
class Medical_cost:
    def __init__(self, df):
        self.df = df

    def pie_chart_gender(self):
        value_gender = self.df["sex"].value_counts()
        fig_sex = go.Figure(data=[
            go.Pie(
                labels=value_gender.index,
                values=value_gender.values,
                marker=dict(colors=['#F1A7A7', '#A7DDF1']),
                textinfo="label+percent",
                textfont=dict(color="white")
            )
        ])

        fig_sex.update_layout(
            title_text="Genders",
            title_x=0.5,
            template="plotly_white",
            showlegend=False,
            width=600,
            height=400
        )
        return fig_sex

    def pie_chart_smokers(self):
        value_gender = self.df["smoker"].value_counts()
        fig_sex = go.Figure(data=[
            go.Pie(
                labels=value_gender.index,
                values=value_gender.values,
                marker=dict(colors=['#F1A7A7', '#A7DDF1']),
                textinfo="label+percent",
                textfont=dict(color="white")
            )
        ])

        fig_sex.update_layout(
            title_text="Smokers",
            title_x=0.5,
            template="plotly_white",
            showlegend=False,
            width=600,
            height=400
        )
        return fig_sex

    def children_histogram(self):
        data = self.df[['sex', 'children']]

        fig = px.histogram(
            data,
            x='children',
            color='sex',
            barmode='group',
            category_orders={"children": [0, 1, 2, 3, 4, 5]},
            title="Number of Children by Gender",
            labels={"children": "Number of Children", "count": "Count", "sex": "Gender"},
            color_discrete_map={'female': '#D487EC', 'male': '#22A7D7'}
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title="Number of Children",
            yaxis_title="Count",
            bargap=0.2,
            width=800,
            height=600
        )

        return fig

    def plot_bmi_smoker_relationship(self):
        fig = px.box(
            self.df,
            x='smoker',
            y='bmi',
            color='smoker',
            title="BMI Distribution by Smoking Status",
            labels={"bmi": "BMI", "smoker": "Smoking Status"},
            color_discrete_map={'yes': '#50E39B', 'no': '#9284DA'}
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title="Smoking Status",
            yaxis_title="BMI",
            width=800,
            height=600
        )

        return fig

    def gender_smoker(self):
        fig = px.histogram(self.df, x="smoker", y="charges", color="smoker", pattern_shape="sex")
        return fig

    def bar_charges_age_by_region(self):
        avg_age_by_region = self.df.groupby('region')['charges'].mean().reset_index()

        fig = px.bar(
            avg_age_by_region,
            x='region',
            y='charges',
            color='region',
            title="Average charges by Region",
            labels={"region": "Region", "charges": "cahrges"},
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title="Region",
            yaxis_title="Average charges",
            width=800,
            height=600
        )

        return fig

    def smokers_region_histogram(self):
        data = self.df[['smoker', 'region']]

        fig = px.histogram(
            data,
            x='region',
            color='smoker',
            barmode='group',
            title="Number of smokers in region",
            labels={"children": "Number of Children", "count": "Count", "sex": "Gender"},
            color_discrete_map={'female': '#D487EC', 'male': '#22A7D7'}
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title="Region",
            yaxis_title="Count",
            bargap=0.2,
            width=800,
            height=600
        )

        return fig

    def children_region_histogram(self):
        data = self.df[self.df["children"].isin([1, 2, 3, 4, 5])]

        fig = px.histogram(
            data,
            x='region',
            color='sex',
            barmode='group',
            title="Number of people with children in region",
            labels={"children": "Number of Children", "count": "Count", "sex": "Gender"},
            color_discrete_map={'female': '#D487EC', 'male': '#22A7D7'}
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title="Region",
            yaxis_title="Count",
            bargap=0.2,
            width=800,
            height=600
        )

        return fig

    def correlation(self):
        numeric_data = self.df.select_dtypes(include=['float64', 'int64'])

        correlation_matrix = numeric_data.corr()

        z_values = correlation_matrix.values
        annotations = [
            dict(
                x=x,
                y=y,
                text=f"{z:.2f}",
                showarrow=False,
                font=dict(color="white" if abs(z) > 0.5 else "black")
            )
            for x_idx, x in enumerate(correlation_matrix.columns)
            for y_idx, y in enumerate(correlation_matrix.index)
            for z in [z_values[y_idx][x_idx]]
        ]

        fig = go.Figure(data=go.Heatmap(
            z=z_values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='Viridis',
            colorbar_title="Correlation"
        ))

        fig.update_layout(
            title="Correlation",
            xaxis_title="Features",
            yaxis_title="Features",
            annotations=annotations,
            width=800,
            height=600
        )

        return fig

    def plot_charges_vs_age(self):
        fig = px.scatter(
            self.df,
            x='age',
            y='charges',
            color='smoker',
            title="Charges vs Age",
            labels={"age": "Age", "charges": "Medical Charges", "smoker": "Smoker Status"},
            color_discrete_map={'yes': '#F1A7A7', 'no': '#A7DDF1'}
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title="Age",
            yaxis_title="Medical Charges",
            width=900,
            height=600
        )

        return fig

    def bmi_charges_smoker(self):
        fig = px.scatter(
            self.df,
            x="bmi",
            y="charges",
            color="smoker",
            title="Dependence of expenses on body mass index, taking into account the smoking factor",
            labels={"bmi": "BMI", "charges": "Charges"}
        )
        return fig

    def plot_smoker_vs_charges_boxplot(self):
        fig = px.box(
            self.df,
            x='smoker',
            y='charges',
            color='smoker',
            title="Medical Charges for Smokers vs Non-Smokers",
            labels={"smoker": "Smoking Status", "charges": "Medical Charges"},
            color_discrete_map={'yes': '#F1A7A7', 'no': '#A7DDF1'},
        )

        # Настройки графика
        fig.update_layout(
            template="plotly_white",
            xaxis_title="Smoking Status",
            yaxis_title="Medical Charges",
            width=900,
            height=600
        )

        return fig

    def charges_region_children(self):
        average_charges = self.df.groupby(['region', 'children']).charges.mean().reset_index()
        fig = px.bar(
            average_charges,
            x="region",
            y="charges",
            color="children",
            barmode="group",
            title="Average expenses depending on the region and the number of children",
            labels={"region": "Region", "charges": "Charges", "children": "Number of children"}
        )
        return fig

    def plot_age_vs_charges_with_conditions(self):
        df_m = self.df[(self.df['age'] > 30) & (self.df['smoker'] == 'yes') & (self.df['sex'] == 'male')]
        df_w = self.df[(self.df['age'] > 30) & (self.df['smoker'] == 'no') & (self.df['sex'] == 'female') & (self.df['children'] == 0)]
        df_n = pd.concat([df_m, df_w])
        sns.lmplot(data=df_n, x="age", y="charges", hue="sex")

    def generate_key(self, prefix="chart"):
        return f"{prefix}_{uuid.uuid4().hex}"

