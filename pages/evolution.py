import streamlit as st
import pandas as pd
import numpy as np
import json
import timeit
import plotly.graph_objects as go
import os
from plotly.subplots import make_subplots
st.title('Workout log')
# Display graphical tools
st.sidebar.markdown('### Graphical and display options')
st.sidebar.markdown('**Text size**')
title_text_size = st.sidebar.slider(label='Please, select the text size:', min_value=10, max_value=100, value=16)
figure_marker_size = st.sidebar.slider(label='Please, select the marker size:', min_value=10, max_value=100, value=16)
# Databases paths
workout_database = 'workout_database.csv'
volume_database = 'volume_database.csv'
if os.path.exists(workout_database) & os.path.exists(volume_database):
    volume_df = pd.read_csv(volume_database, parse_dates=['Day'])
    volume_df['Week'] = volume_df['Day'].dt.isocalendar().week
    volume_df['Day'] = volume_df['Day'].dt.date
    workout_df = pd.read_csv(workout_database, parse_dates=['Day'])
    workout_df['Week'] = workout_df['Day'].dt.isocalendar().week
    workout_df['Day'] = workout_df['Day'].dt.date
    exercises_list = sorted(workout_df['Exercise'].unique())
    selected_exercise = st.selectbox(label='Select an exercise:', options=exercises_list)
    fig_weight = go.Figure()
    fig_weight.add_trace(go.Scatter(x=workout_df.loc[workout_df['Exercise']==selected_exercise]['Day'], y=workout_df.loc[workout_df['Exercise']==selected_exercise]['Weight (kg)'], mode='markers+lines', line_dash='dash', marker_size=figure_marker_size))
    fig_weight.update_xaxes(title='Date', tickfont_size=title_text_size, title_font=dict(size=title_text_size), type='category')
    fig_weight.update_yaxes(title='Weight (kg)', tickfont_size=title_text_size, title_font=dict(size=title_text_size))
    fig_weight.update_layout(title='Weight lifted evolution for ' + selected_exercise, width=1000, height=700)
    st.plotly_chart(fig_weight)
    st.divider()
    number_muscles = len(volume_df['Muscle'].unique())
    fig_volume = make_subplots(rows=number_muscles, cols=1, subplot_titles=volume_df['Muscle'].unique())
    i = 1
    for m in volume_df['Muscle'].unique():
        df = volume_df.loc[volume_df['Muscle']==m]
        fig_volume.add_trace(go.Bar(x=df['Day'], y=df['Total Sets'], name=m), row=i, col=1)
        i += 1
    fig_volume.update_xaxes(tickfont_size=title_text_size, title_font=dict(size=title_text_size), type='category', categoryorder='category ascending')
    fig_volume.update_yaxes(title='Sets', tickfont_size=title_text_size, title_font=dict(size=title_text_size))
    fig_volume.update_layout(title='Sets per session per muscle', width=1000, height=2500, showlegend=False)
    st.plotly_chart(fig_volume)
    st.divider()
    fig_volume_week = go.Figure()
    fig_volume_week.add_trace(go.Bar(x=volume_df.groupby('Week').sum().index, y=volume_df.groupby('Week').sum()['Total Sets']))
    fig_volume_week.update_xaxes(title='Week of year', tickfont_size=title_text_size, title_font=dict(size=title_text_size))
    fig_volume_week.update_yaxes(title='Total Sets', tickfont_size=title_text_size, title_font=dict(size=title_text_size))
    fig_volume_week.update_layout(title='Total Sets per week', width=1000, height=600)
    st.plotly_chart(fig_volume_week)