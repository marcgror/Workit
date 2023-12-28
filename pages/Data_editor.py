# Import required packages
import streamlit as st
import pandas as pd
from datetime import datetime

st.header(':red[Data Editor]')
# Load the database
workout_df = pd.read_csv('workout_database.csv')
# Display a toggle to edit the database
edit_toggle = st.toggle('Edit mode')
if edit_toggle:
    st.success('Edit mode enabled.')
    # Get the unique dates
    available_dates = workout_df['Day'].unique()
    # Display a widget to select the date to edit
    date = st.selectbox(label='Select date to filter data:', options=available_dates)
    # Display the data editor
    data_edited = st.data_editor(workout_df.loc[workout_df['Day']==date])
    # Display a Save button
    save_button = st.button('Save')
    if save_button:
        with st.status('Saving...', expanded=True):
            # Get today date and time
            today = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            st.success('Backing-up database...')
            # Backup original database
            workout_df.to_csv('Backup/workout_database_' + today + '.csv', index=False)
            # Replace edited data
            workout_df.loc[data_edited.index] = data_edited
            # Save the database
            workout_df.to_csv('workout_database.csv', index=False)
            st.success('Saved!', icon='✅')
else:
    st.info('Edit mode is disabled. Toogle it to edit the database.')
    # Display the database
    st.dataframe(workout_df)