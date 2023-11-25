import streamlit as st
import numpy as np

st.title('Nutrition')
st.subheader('Info')
# Create 3 columns
col1, col2, col3 = st.columns(3)
# Widget for introducing weight
weight =  col1.number_input(label='Weight (kg)', min_value=30.0, max_value=250.0, value=65.0, step=0.1)
# Widget for protein ratio
protein_ratio = col2.slider(label='Grams of protein per kg of bodyweight:', min_value=0.0, max_value=4.0, value=2.0, step=0.1)
# Widget for protein goal
protein_goal = col3.number_input(label='Protein (g)', min_value=50.0, max_value=1000.0, value=weight*protein_ratio, step=1.0, disabled=True)
# Create 3 columns
col4, col5, col6 = st.columns(3)
# Widget for calories goal
calories_goal = col4.number_input(label='Calories', min_value=1000.0, max_value=10000.0, value=2000.0, step=10.0)
# Compute calories from protein
protein_calories = protein_goal * 4
# Compute % of calories from protein
ratio_protein = protein_calories * 100 / calories_goal
# Widget for calories from fat goal. Defaults to 50% of remaining calories after protein
fat_ratio = col5.number_input(label='Calories from fat (%):', min_value=0.0, max_value=100-ratio_protein, value=(100-ratio_protein)/2)
# Compute calories from fats
fat_calories = fat_ratio * calories_goal/100
# Widget for calories from carbs. Defaults to remaining calories after protein and fats
carbs_ratio = col6.number_input(label='Calories from carbs (%):', min_value=0.0, max_value=100-ratio_protein - fat_ratio, value=100-ratio_protein-fat_ratio, disabled=True)
# Compute calories from carbs
carbs_calories = carbs_ratio * calories_goal/100
# Compute fat goal
fat_goal = fat_calories / 9
# Compute carbs goal
carbs_goal = carbs_calories / 4
st.divider()
# Display summary results
st.subheader('Summary')
st.markdown('**Weight:** ' + str(np.round(weight,2)))
st.markdown('**Calories:** ' + str(np.round(calories_goal, 2)))
st.markdown('**Protein (g):** ' + str(np.round(protein_goal, 2)) + ' (' + str(np.round(ratio_protein,2)) + '%)')
st.markdown('**Fat (g):** ' + str(np.round(fat_goal, 2)) + ' (' + str(np.round(fat_ratio,2)) + '%)')
st.markdown('**Carbs (g):** ' + str(np.round(carbs_goal, 2)) + ' (' + str(np.round(carbs_ratio,2)) + '%)')