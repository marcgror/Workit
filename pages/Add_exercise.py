import streamlit as st
import pandas as pd

exercises = pd.read_csv('muscles_targeted.csv', delimiter=',')
st.markdown('**Current added exercises**')
st.dataframe(exercises)
# Get the list of Primary muscles
primary_muscles = sorted(exercises['Primary'].unique())
# Get the list of Secondary muscles
secondary_muscles = exercises['Secondary'].unique()
st.divider()
col1, col2, col3 = st.columns(3)
name = col1.text_input(label='Exercise name:')
# Display a widget to select the Primary muscle
primary = col2.selectbox('Primary muscle:', options=primary_muscles)
# Display a widget to select the Secondary muscle
secondary = col3.selectbox('Secondary muscle (if required):', options=secondary_muscles)
# Create a Serie to store data
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
