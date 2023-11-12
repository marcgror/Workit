import streamlit as st
import pandas as pd

exercises = pd.read_csv('muscles_targeted.csv', delimiter=',')
st.markdown('**Current added exercises**')
st.dataframe(exercises)
st.divider()
col1, col2, col3 = st.columns(3)
name = col1.text_input(label='Exercise name:')
primary = col2.text_input('Primary muscle:')
secondary = col3.text_input('Secondary muscle (if required):')
temporal_exercise = pd.Series([name, primary, secondary], index=['Exercise', 'Primary', 'Secondary'])
add_button = st.button('Add exercise')
st.divider()
if add_button:
    if name not in exercises['Exercise'].unique():
        exercises = pd.concat([exercises, temporal_exercise.to_frame().T])
    else:
        st.error('Exercise already added!')
exercises.reset_index(inplace=True, drop=True)
st.dataframe(exercises)
save_button = st.button(label='Save')
if save_button:
    temporal_exercise.to_frame().T.to_csv('muscles_targeted.csv', index=None, mode='a', header=None)
