# Import required packages
import streamlit as st
import pandas as pd
import numpy as np
import json
import timeit
import plotly.graph_objects as go
import os
from datetime import datetime, timedelta

workout_df = pd.read_csv('workout_database.csv')
st.data_editor(workout_df)