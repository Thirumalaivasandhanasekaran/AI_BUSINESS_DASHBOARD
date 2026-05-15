import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==============================
# AI API IMPORT
# ==============================

# FREE OPTION (Groq)
# from groq import Groq

# PAID OPTION (OpenAI)
from openai import OpenAI


# ==============================
# PAGE CONFIGURATION
# ==============================

st.set_page_config(
    page_title="AI Dashboard",
    page_icon="📊",
    layout="wide"
)


# ==============================
# CONNECT TO AI API
# ==============================

# OpenAI Client
client = OpenAI(api_key=st.secrets["openai_API_KEY"])


def ask_ai(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# ==============================
# CREATE SAMPLE SALES DATA
# ==============================

@st.cache_data
def load_data():

    months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]

    data = pd.DataFrame({
        'Month': months,
        'Sales': np.random.randint(50000, 200000, 12),
        'Profit': np.random.randint(10000, 80000, 12),
        'Leads': np.random.randint(100, 500, 12)
    })

    return data


df = load_data()


# ==============================
# PAGE TITLE
# ==============================

st.title("📈 AI-Powered Business Dashboard")
st.caption("Ask questions about your business data in plain English")


# ==============================
# KPI CARDS
# ==============================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Sales",
    "Rs. " + str(df['Sales'].sum()),
    "+12%"
)

c2.metric(
    "Total Profit",
    "Rs. " + str(df['Profit'].sum()),
    "+8%"
)

c3.metric(
    "Best Month",
    df.loc[df['Sales'].idxmax(), 'Month']
)

c4.metric(
    "Avg Leads",
    str(int(df['Leads'].mean())) + " / mo"
)


# ==============================
# CHARTS SECTION
# ==============================

col_a, col_b = st.columns(2)

# -------- LEFT CHART --------
with col_a:

    st.subheader("Sales Trend")

    fig1 = px.line(
        df,
        x='Month',
        y='Sales',
        markers=True,
        color_discrete_sequence=['#00d4ff']
    )

    st.plotly_chart(
        fig1,
        width='stretch'
    )


# -------- RIGHT CHART --------
with col_b:

    st.subheader("Profit vs Sales")

    fig2 = px.bar(
        df,
        x='Month',
        y=['Sales', 'Profit'],
        barmode='group'
    )

    st.plotly_chart(
        fig2,
        width='stretch'
    )


# ==============================
# SHOW DATA TABLE
# ==============================

st.subheader("Business Data")
st.dataframe(df, width='stretch')


# ==============================
# AI QUESTION & ANSWER SECTION
# ==============================

st.divider()

st.subheader("🤖 Ask AI About Your Data")

question = st.text_input(
    "Your Question:",
    placeholder="Which month had highest profit?"
)


if st.button("Ask AI") and question:

    with st.spinner("Thinking..."):

        # Create AI Prompt
        prompt = f"""
        You are a business analyst.

        Here is the business data:

        {df.to_string(index=False)}

        User Question:
        {question}

        Give a short and clear answer.
        """

        # Get AI Response
        answer = ask_ai(prompt)

        # Display Answer
        st.success(answer)