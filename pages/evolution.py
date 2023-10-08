import streamlit as st
import pandas as pd
import numpy as np
import json
import timeit
import plotly.graph_objects as go
import os
from plotly.subplots import make_subplots
import datetime
st.set_page_config(layout='wide')
st.header(':red[Evolution]')
# Display graphical tools
st.sidebar.markdown('### Graphical and display options')
st.sidebar.markdown('**Text size**')
title_text_size = st.sidebar.slider(label='Please, select the text size:', min_value=10, max_value=100, value=16)
figure_marker_size = st.sidebar.slider(label='Please, select the marker size:', min_value=10, max_value=100, value=16)
# Databases paths
workout_database = 'workout_database.csv'
volume_database = 'volume_database.csv'
if os.path.exists(workout_database) & os.path.exists(volume_database):
    # Read volume csv
    volume_df = pd.read_csv(volume_database, parse_dates=['Day'])
    # Get the week
    volume_df['Week'] = volume_df['Day'].dt.isocalendar().week
    # Get only the date
    volume_df['Day'] = volume_df['Day'].dt.date
    # Read the workout csv
    workout_df = pd.read_csv(workout_database, parse_dates=['Day'])
    # Get the week
    workout_df['Week'] = workout_df['Day'].dt.isocalendar().week
    # Get only the date
    workout_df['Day'] = workout_df['Day'].dt.date
    # List the exercises
    exercises_list = sorted(workout_df['Exercise'].unique())
    st.subheader(':rainbow[Weight evolution]', divider='rainbow')
    # Display a widget to select an exercise
    selected_exercise = st.selectbox(label='Select an exercise:', options=exercises_list)
    # Create a Figure
    fig_weight = go.Figure()
    # Add trace
    fig_weight.add_trace(go.Scatter(x=workout_df.loc[workout_df['Exercise']==selected_exercise]['Day'], y=workout_df.loc[workout_df['Exercise']==selected_exercise]['Weight (kg)'], mode='markers+lines', line_dash='dash', marker_size=figure_marker_size))
    # Update x-y axes
    fig_weight.update_xaxes(title='Date', tickfont_size=title_text_size, title_font=dict(size=title_text_size), type='category')
    fig_weight.update_yaxes(title='Weight (kg)', tickfont_size=title_text_size, title_font=dict(size=title_text_size))
    # Update Figure layout
    fig_weight.update_layout(title='Weight lifted evolution for ' + selected_exercise, width=1000, height=700)
    # Display Figure
    st.plotly_chart(fig_weight)
    st.divider()
    st.subheader(':rainbow[Volume distribution per week and session]', divider='rainbow')
    # List all muscles
    muscles = volume_df['Muscle'].unique()
    # Create a 2x1 Figuere
    fig_volume = make_subplots(rows=2, cols=1, subplot_titles=['Session', 'Week'])
    # Create 3 columns
    col1, col2, col3 = st.columns(3)
    # Display a widget to select a muscle to filter
    muscle_selected = col1.selectbox(label='Select a muscle', options=muscles)
    # Display widgets to filter by date
    date_min = col2.date_input(label='Select a minimum date:', value=datetime.date(2023, 6, 1))
    date_max = col3.date_input(label='Select a maximum date:')
    # Filter by muscle
    volume_df_muscle = volume_df.loc[volume_df['Muscle']==muscle_selected]
    # Filter by date
    volume_df_muscle_date = volume_df_muscle.loc[(volume_df_muscle['Day']>=pd.to_datetime(date_min, format='%Y-%m-%d').date()) & (volume_df_muscle['Day']<=pd.to_datetime(date_max, format="%Y-%m-%d").date())]
    # Add traces
    fig_volume.add_trace(go.Bar(x=volume_df_muscle_date.groupby('Day').sum().index, y=volume_df_muscle_date.groupby('Day').sum()['Total Sets'], name=muscle_selected),row=1, col=1)
    fig_volume.add_trace(go.Bar(x=volume_df_muscle_date.groupby('Week').sum().index, y=volume_df_muscle_date.groupby('Week').sum()['Total Sets']), row=2, col=1)
    # Update x-y axes
    fig_volume.update_xaxes(tickfont_size=title_text_size, title_font=dict(size=title_text_size), type='category', categoryorder='category ascending', row=1, col=1)
    fig_volume.update_xaxes(title='Week of year', tickfont_size=title_text_size, title_font=dict(size=title_text_size), row=2, col=1)
    fig_volume.update_yaxes(title='Sets', tickfont_size=title_text_size, title_font=dict(size=title_text_size))
    # Update Figure layout
    fig_volume.update_layout(title='Sets per session per muscle', width=1000, height=700, showlegend=False)
    # Display Figure
    st.plotly_chart(fig_volume)
    st.divider()
    st.subheader(body=':rainbow[Volume per week]', divider='rainbow')
    # Get the list of weeks
    weeks = volume_df['Week'].unique()
    # Display a widget to select a week
    week_selected = st.selectbox(label='Select the week:', options=weeks, index=len(weeks)-1)
    # Filter data by selected week, group it by Muscle and sum Total sets
    volume_df_week_grouped = volume_df.loc[volume_df['Week']==week_selected].groupby('Muscle').sum()
    # Create a Figure
    fig_pie_week_volume = go.Figure()
    # Add trace
    fig_pie_week_volume.add_trace(go.Pie(labels=volume_df_week_grouped.index, values=volume_df_week_grouped['Total Sets'], textinfo='label+value'))
    # Update Figure layout
    fig_pie_week_volume.update_layout(width=400, height=400)
    # Display Figure
    st.plotly_chart(fig_pie_week_volume)