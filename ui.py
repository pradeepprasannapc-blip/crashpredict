import streamlit as st
import pandas as pd
import fetch
import hash_multiplier
import train
import train_rnn


def get_model_prediction_crashCNN():
    with st.spinner():
        hash_multiplier.main()
        prediction = train.predict_next_event()
        st.title(prediction)


def get_model_prediction_crashRNN():
    with st.spinner():
        prediction = train_rnn.predict_rnn()
        st.title(prediction)
        

def laod_game_data():
    with st.spinner():
        x = fetch.main()

        payout = x.get("payout", " ")
        target = x.get("ticket", " ")
        startedAt = x.get("startedAt", " ")
        numberOfBets = x.get("numberOfBets", " ")
        serverSeed = x.get("serverSeed", " ")
        game_id = x.get("id", " ")
        endTime = x.get("endTime", " ")

        # සාමාන්‍ය Streamlit metrics මගින් ලස්සන කාඩ් පත් සෑදීම
        cols = st.columns(3)
        with cols[0]:
            st.metric(label="Total Payout", value=f"{payout}")
        with cols[1]:
            st.metric(label="Game Multiplier", value=target/100 if isinstance(target, (int, float)) else f"{target}")
        with cols[2]:
            st.metric(label="No. of Bets", value=numberOfBets)

        st.info(f"**Game Hash:** {serverSeed}")
        

st.sidebar.title("Select Model")
selected_model = st.sidebar.selectbox("Choose a model", ["Crash CNN", "Crash RNN"])

st.title("Crash Predictor")

# තෝරාගත් මොඩලය පෙන්වීම
st.warning(f"Selected Model: {selected_model}")

# සාමාන්‍ය Streamlit Button එකක් භාවිතය
if st.button("Predict Next Event", key="clk_btn", type="primary"):
    st.subheader("Last Game Data")
    laod_game_data()

    st.subheader("Predicted Multiplier of Next Game")
    if selected_model == "Crash CNN":
        get_model_prediction_crashCNN()
    if selected_model == "Crash RNN":
        get_model_prediction_crashRNN()
else:
    st.subheader("Last Game Data")
    laod_game_data()

    st.subheader("Predicted Multiplier of Next Game")
    if selected_model == "Crash CNN":
        get_model_prediction_crashCNN()
    if selected_model == "Crash RNN":
        get_model_prediction_crashRNN()
