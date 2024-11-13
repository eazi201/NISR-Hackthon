import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# Load the model and datasets
model = joblib.load("model_pipeline.pkl")
skills_data = pd.read_csv("highSkills.csv")

# Title and Description
st.title("Growth Rate and Skill Demand Dashboard")
st.write("""
This dashboard predicts growth rates for industries and recommends skills in high demand for the selected industry.
""")


st.header("Industry Selection")
industry = st.selectbox("Select Industry", skills_data['industry'].unique())
field = st.text_input("Enter Specific Field (Optional)")


st.header("Growth Rate Prediction")
year = st.selectbox("Select Year", [2025, 2026, 2027])
gdp_growth = st.slider("GDP Growth (%)", -10.0, 10.0, 2.5)
inflation_rate = st.slider("Inflation Rate (%)", 0.0, 20.0, 3.0)
unemployment_rate = st.slider("Unemployment Rate (%)", 0.0, 25.0, 5.0)


default_values = {
    'industry': industry,
    'field': field,
    'year': year,
    'gdp_growth': gdp_growth,
    'inflation_rate': inflation_rate,
    'unemployment_rate': unemployment_rate,
    'supply_chain_index': 50.0,
    'regulatory_score': 3.0,
    'adoption_rate': 0.5,
    'market_size_bn': 10.0,
    'quarter': 1,
    'competition_index': 0.6,
    'workforce_demand': 1000,
    'energy_costs': 100.0,
    'export_growth': 5.0,
    'interest_rate': 2.0,
    'consumer_sentiment': 0.7,
    'venture_funding_bn': 1.0,
    'r_and_d_spending_mn': 500.0,
    'r_and_d_spending_mn_rwf': 500.0,
    'investment_bn_rwf': 10.0,
    'market_size_bn_rwf': 10.0
}

user_input = pd.DataFrame([default_values])

if st.button("Predict Growth Rate"):
    prediction = model.predict(user_input)
    st.write(f"Predicted Growth Rate for {year}: {prediction[0]:.2f}%")

    st.subheader("Growth Rate Prediction Across Quarters")
    quarters = [1, 2, 3, 4]
    predictions = []
    for q in quarters:
        user_input['quarter'] = q
        pred = model.predict(user_input)[0]
        predictions.append(pred)

    predictions_df = pd.DataFrame({"Quarter": quarters, "Predicted Growth Rate": predictions})

    fig = px.line(predictions_df, x="Quarter", y="Predicted Growth Rate",
                  title=f"Predicted Growth Rate for {field} in {industry} ({year})",
                  labels={"Quarter": "Quarter", "Predicted Growth Rate": "Growth Rate (%)"},
                  markers=True)
    st.plotly_chart(fig)

    if prediction[0] > 4.0:
        st.success(f"Recommendation: {field} in {industry} shows promising growth for {year}. Investing here could yield positive results.")
    else:
        st.info(f"Recommendation: Growth for {field} in {industry} is moderate. Explore strategies to improve growth.")


st.header("Skill Demand Recommendations")
st.write("""
Based on the selected industry, here are skills currently in high demand, along with their peak periods and details.
""")


filtered_data = skills_data[skills_data['industry'] == industry]

if field:
    filtered_data = filtered_data[filtered_data['Skill'].str.contains(field, case=False, na=False)]

if not filtered_data.empty:
    st.subheader(f"Recommended Skills in {industry}")
    st.write(filtered_data[['Skill', 'Demand_Level', 'Peak_Period', 'Details']])

  
    st.subheader("Skill Demand Leaderboard")
    demand_levels = {"Very High": 3, "High": 2, "Medium": 1}
    filtered_data['Demand_Score'] = filtered_data['Demand_Level'].map(demand_levels)
    leaderboard = filtered_data.sort_values(by='Demand_Score', ascending=False)

    fig = px.bar(leaderboard, x='Skill', y='Demand_Score',
                 color='Demand_Level', text='Demand_Level',
                 title=f"Skill Demand Leaderboard for {industry}",
                 labels={"Demand_Score": "Demand Level", "Skill": "Skill"})
    st.plotly_chart(fig)
else:
    st.warning(f"No skills found for the selected industry{' and field' if field else ''}.")
