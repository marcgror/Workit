# Import required packages
import streamlit as st
import pandas as pd
import numpy as np
import json
import timeit
import plotly.graph_objects as go
import os
from datetime import datetime, timedelta

# Display graphical tools
st.sidebar.markdown('### Graphical and display options')
st.sidebar.markdown('**Text size**')
title_text_size = st.sidebar.slider(label='Please, select the text size:', min_value=10, max_value=100, value=16)
# Load csv file
muscles_targeted = pd.read_csv('muscles_targeted.csv')
# Databases paths
workout_database = 'workout_database.csv'
volume_database = 'volume_database.csv'
tab1, tab2, tab3 = st.tabs(['Today', 'Last workout', 'Past workout'])
with tab1:
    # Create a DataFrame for the exercise
    exercise_df = pd.DataFrame()
    # Display a widget to select the exercise to add
    selected_exercise = st.selectbox(label='Please, select an exercise:', options=sorted(muscles_targeted['Exercise']))
    # Display a widget to introduce the secondary muscles factor
    secondary_factor = st.number_input(label='How much secondary muscles will be involved, from 0 to 1:', min_value=0.0, max_value=1.0, value=0.0)
    if selected_exercise:
        # Create lists for exercise, sets, reps, weights and notes
        exercises_list = []
        sets_list = []
        reps_list = []
        weights_list = []
        notes_list = []
        # Display an expander for options
        with st.expander(label='Exercise selection', expanded=True):
            st.markdown(selected_exercise)
            col_sets, col_date = st.columns(2)
            # Display a widget to select the number of sets performed
            sets = col_sets.number_input('Sets:', min_value=0, max_value=10, key=selected_exercise + '_sets', value=3)
            # Display a widget to select the data
            date = col_date.date_input(label='Please, introduce the date for the exercise:')
            # Create 3 columns
            col1, col2, col3 = st.columns([1,1,3])
            # Define last_weight based on last workout
            workout_df = pd.read_csv(workout_database, parse_dates=['Day'])
            last_weight = workout_df.loc[workout_df['Exercise']==selected_exercise].tail(1)['Weight (kg)'].values[0]
            last_reps = 8
            # Display options
            for i in np.linspace(1, sets, sets):
                # Append set
                sets_list.append(1)
                # Display a widget to select the number of repetitions performed in the set
                reps = col1.number_input('Repetitions:', min_value=1, max_value=50, key=selected_exercise + '_reps_' + str(i), value=last_reps)
                # Display a widget to select the weight used    
                weights = col2.number_input('Weight:', step=0.5, key=selected_exercise + '_weight_' + str(i), value=last_weight)
                # Update last weight
                last_weight = weights
                # Update last reps
                last_reps = reps
                # Append exercise
                exercises_list.append(selected_exercise)
                # Append repetitions
                reps_list.append(reps)
                # Append weights
                weights_list.append(weights)
                # Display a widget to add a note for the set
                notes = col3.text_input(label='Notes', key=selected_exercise +'_notes_' + str(i))
                # Append note
                notes_list.append(notes)
            st.divider()
            intensity_methods_check = st.toggle(label='Intensity methods')
            if intensity_methods_check:
                col1, col2, col3 = st.columns(3)
                drop_sets = col1.number_input(label='Drop Sets', min_value=0, max_value=50, key=selected_exercise + '_drop_sets_' + str(i))
                myo_reps = col2.number_input(label='Myo reps (sets)', min_value=0, max_value=50, key=selected_exercise + '_myo_sets_' + str(i))
                iso_hold = col3.number_input(label='Isometric hold (s)', min_value=0, max_value=200, key=selected_exercise + '_iso_hold_' + str(i))
            else:
                drop_sets = 0
                myo_reps = 0
                iso_hold = 0
        # Display a button to save the introduced data
        apply_button = st.button(label="Add exercise to today's workout")
        st.divider()
        if apply_button:
            # Set Excercise column as index
            muscles_targeted.set_index('Exercise', inplace=True)
            # Add columns
            exercise_df['Exercise'] = exercises_list
            exercise_df['Sets'] = sets_list
            exercise_df['Reps'] = reps_list
            exercise_df['Weight (kg)'] = weights_list
            exercise_df['Weight per set (kg)'] = exercise_df['Reps'] * exercise_df['Weight (kg)']
            exercise_df['Notes'] = notes_list
            exercise_df['Day'] = date
            exercise_df['Drop Sets'] = np.append(np.zeros(sets-1), drop_sets)
            exercise_df['Myo reps'] = np.append(np.zeros(sets-1), myo_reps)
            exercise_df['Isometric hold (s)'] = np.append(np.zeros(sets-1), iso_hold)
            exercise_df['Primary'] = muscles_targeted.loc[selected_exercise, 'Primary']
            exercise_df['Secondary'] = muscles_targeted.loc[selected_exercise, 'Secondary']
            # Group by Exercise and sum sets and reps
            exercise_grouped = exercise_df.groupby('Exercise').sum(numeric_only=True)
            # Set Exercise column as index
            exercise_df.set_index('Exercise', inplace=True)
            st.dataframe(exercise_df, width=2000)
            st.divider()
            # Update databases, and create them if necessary
            if os.path.exists(workout_database):
                exercise_df.to_csv(workout_database, mode='a', header=False)
            else:
                exercise_df.to_csv(workout_database)
            st.success('Exercise succesfully added!')
            st.divider()
        if os.path.exists(workout_database) & os.path.exists(volume_database):
            # Load databases
            workout_df = pd.read_csv(workout_database, parse_dates=['Day'])
            # Get today date
            today = pd.Timestamp.today().date()
            # Select today workout
            workout_df = workout_df.loc[workout_df['Day']==pd.to_datetime(today)]
            # Select today volume
            if not workout_df.empty:
                # Display today's workout, set by set
                st.markdown("This is your today's workout:")
                st.dataframe(workout_df.drop(['Sets', 'Day'], axis=1))
                st.divider()
                # Group by Exercise and sum Sets and Reps
                workout_df_grouped = workout_df.groupby('Exercise').sum(numeric_only=True)
                # Display today's workout, exercise by exercise
                st.markdown('**Volume per exercise**')
                st.dataframe(workout_df_grouped)
                st.divider()
                # Display the total volume per muscle
                st.markdown('**Volume per muscle**')
                volume_df_grouped = workout_df.groupby('Primary').sum(numeric_only=True)
                st.dataframe(volume_df_grouped)
                st.divider()
                # Create and display a Pie Chart for exercises
                fig_exercises = go.Figure()
                fig_exercises.add_trace(go.Pie(labels=workout_df_grouped.index, values=workout_df_grouped['Sets'], textinfo='label+value'))
                fig_exercises.update_layout(title='Distribution of exercises for the session', width=1000, height=600, legend=dict(font_size=title_text_size),
                    hoverlabel=dict(font_size=title_text_size))
                st.plotly_chart(fig_exercises)
                st.divider()
                # Create and display a Pie Chart for volume
                fig_volume = go.Figure()
                fig_volume.add_trace(go.Pie(labels=volume_df_grouped.index, values=volume_df_grouped['Sets'], textinfo='label+value'))
                fig_volume.update_layout(title='Volume distribution for the session', width=1000, height=600, legend=dict(font_size=title_text_size),
                    hoverlabel=dict(font_size=title_text_size))
                st.plotly_chart(fig_volume)
            else:
                st.markdown('You did not workout today!')
            st.divider()
    workout_df = pd.read_csv('workout_database.csv', parse_dates=['Day'])       
    with tab2:
        # Convert Day column in a pandas datetime date object
        workout_df['Day'] = workout_df['Day'].dt.date
        # Get last week workout date
        last_day = date.today() - timedelta(weeks=1)
        # Display a widget to select a day and initialize it to one week before
        date_selected = st.date_input(label='Select the date:', value=last_day)
        st.divider()
        # Display last week workout
        #st.dataframe(workout_df.loc[workout_df['Day']==date_selected].drop(['Sets', 'Day', 'Weight per set (kg)'], axis=1), width=1000, height=1200)
        # Turn columns to int dtype
        workout_df_today = workout_df.loc[workout_df['Day']==date_selected]
        workout_df_today['Drop Sets'] = workout_df_today['Drop Sets'].astype(int)
        workout_df_today['Myo reps'] = workout_df_today['Myo reps'].astype(int)
        workout_df_today['Isometric hold (s)'] = workout_df_today['Isometric hold (s)'].astype(int)
        # Iterate over exercises
        for exercise in workout_df_today['Exercise'].unique():
            # Create 3 columns
            st.markdown('**' + exercise + '**')
            col1, col2, col3 = st.columns(3)
            # Iterate over rows for each exercise
            for index, row in workout_df_today.loc[workout_df_today['Exercise']==exercise].iterrows():
                # Display reps x weight
                col1.markdown(str(row['Reps']) + 'x' + str(row['Weight (kg)']))
                # Display Drop Sets, Myo reps and Isometric holds
                col2.markdown(str(row['Drop Sets']) + ' Drop Sets, ' + str(row['Myo reps']) + ' Myo Reps, ' + str(row['Isometric hold (s)']) + ' s')
                # Display Notes if exist
                if type(row['Notes'])==str:
                    col3.markdown('Note: ' + str(row['Notes']))
                else:
                    col3.markdown(' ')
            st.divider()
    with tab3:
        dates = workout_df['Day'].unique()
        dates_reversed = sorted(dates, reverse=True)
        for date in dates_reversed:
            date_to_datetime = pd.to_datetime(date)
            week_day = date_to_datetime.day_name()
            number_day = date_to_datetime.day
            month = date_to_datetime.month_name()
            st.markdown('**' + str(week_day) + ', ' + str(number_day) + ' ' + month + '**')
            st.dataframe(workout_df.loc[workout_df['Day']==date].drop(['Day', 'Sets', 'Weight per set (kg)'], axis=1), use_container_width=True)
            st.divider()
