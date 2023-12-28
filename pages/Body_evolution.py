import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

st.header(':red[Body Evolution]')
# Display graphical tools
st.sidebar.markdown('### Graphical and display options')
st.sidebar.markdown('**Text size**')
title_text_size = st.sidebar.slider(label='Please, select the text size:', min_value=10, max_value=100, value=16)
figure_marker_size = st.sidebar.slider(label='Please, select the marker size:', min_value=10, max_value=100, value=16)
# Create file if missing
if not os.path.exists('bodyweight.csv'):
    with st.status('Bodyweigfht file not detected...'):
        weight = pd.DataFrame(columns=['Date', 'Weight (kg)'])
        weight.to_csv('bodyweight.csv', index=False)
        st.success('File created!')
    st.markdown('Hola')
else:
    # Load file
    weight_df = pd.read_csv('bodyweight.csv', parse_dates=['Date'])
    with st.expander(label='Add entry:'):
        # Create 2 columns
        col1, col2 = st.columns(2)
        # Display a widget to select date
        date = col1.date_input(label='Select date:')
        # Display a widget to add weight
        weight = col2.number_input(label='Introduce weight (in kg)', value=65.0, step=0.1)
    # Display a Save button
    save_button = st.button('Add entry')
    if save_button:
        # Concat data
        weight_df = pd.concat([weight_df, pd.Series([date, weight],index=['Date', 'Weight (kg)']).to_frame().T])
        # Export to file
        weight_df.to_csv('bodyweight.csv', index=False)
    st.divider()
    # Load file
    weight_df = pd.read_csv('bodyweight.csv', parse_dates=['Date'])
    # Create a Figure
    fig_weight = go.Figure()
    # Add trace
    fig_weight.add_trace(go.Scatter(x=weight_df['Date'], y=weight_df['Weight (kg)'], marker_size=figure_marker_size))
    # Update x-y axes
    fig_weight.update_xaxes(title='Day', tickfont_size=title_text_size, title_font=dict(size=title_text_size))
    fig_weight.update_yaxes(title='Weight (kg)', tickfont_size=title_text_size, title_font=dict(size=title_text_size))
    # Update Figure layout
    fig_weight.update_layout(title='Weight evolution with time', hoverlabel=dict(font_size=title_text_size))
    # Display Figure
    st.plotly_chart(fig_weight)

