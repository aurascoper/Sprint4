import scipy.stats
import streamlit as st
import time

st.header('Tossing a Coin')

# Initialize the chart with 0.5 to set a centered starting point
chart = st.line_chart([0.5])

def toss_coin(n):
    # Generating bernoulli trials (0 or 1)
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        
        current_mean = outcome_1_count / outcome_no
        chart.add_rows([current_mean])
        time.sleep(0.05)

    return current_mean

number_of_trials = st.slider('Number of trials?', 1, 1000, 10)
start_button = st.button('Run')

if start_button:
    st.write(f'Running the experiment of {number_of_trials} trials.')
    mean = toss_coin(number_of_trials)
    st.write(f'The final mean is: {mean}')
