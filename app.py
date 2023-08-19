from xml.sax.handler import feature_external_ges
import streamlit as st
import pandas as pd
#import plotly.express as px
from herows import *
import re
from collections import defaultdict
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import numpy as np


# Initialize Streamlit app
run_herows()

st.set_page_config(page_title="HEAowS", 
                   page_icon=":bar_chart:",
                   layout="wide")

# Load your DataFrame (cached using st.cache)
@st.cache_data
def load_data_HEA_calculated():
    return pd.read_excel(io="hhh2.xlsx", engine='openpyxl', sheet_name='Sheet1')

df = load_data_HEA_calculated()

@st.cache_data
def load_data_Decile():
    return pd.read_excel(io="Decile.xlsx", engine='openpyxl', sheet_name='Sheet1')

Decile = load_data_Decile()
sorted_decile = Decile.sort_values(by="HERowS_Score")



# X and Y selection using containers and caching
container1 = st.container()


col11, col12 = container1.columns(2)
col121 , col122 = col12.columns(2)

alloy_input = col11.text_input('Calculer les proprietés 👇' , 'AuAlOs')


v_fco2_avg = (fCO2_max(alloy_input) + fCO2_min(alloy_input))/2
v_fe_avg = (fE_max(alloy_input) + fE_min(alloy_input))/2
v_hhi = hhi(alloy_input)
v_esg = esg(alloy_input)
v_sr = Supply_risk(alloy_input)
v_p_avg = p_avg(alloy_input,100)
v_r_avg = r_avg(alloy_input,100)
v_c_avg = c_avg(alloy_input)
v_p_max = p_max(alloy_input)
v_r_max = r_max(alloy_input)
v_c_max = c_max(alloy_input)
herows_score = 100

@st.cache_resource
def h():
    v_fco2_avg = (fCO2_max(alloy_input) + fCO2_min(alloy_input))/2
    v_fe_avg = (fE_max(alloy_input) + fE_min(alloy_input))/2
    v_hhi = hhi(alloy_input)
    v_esg = esg(alloy_input)
    v_sr = Supply_risk(alloy_input)
    v_p_avg = p_avg(alloy_input,100)
    v_r_avg = r_avg(alloy_input,100)
    v_c_avg = c_avg(alloy_input)
    v_p_max = p_max(alloy_input)
    v_r_max = r_max(alloy_input)
    v_c_max = c_max(alloy_input)
    herows_score = 100    

    

if col11.button('Say hello'):
    h()


col121.write(f"fco2_avg: {round(v_fco2_avg,3)}")
col121.write(f"fe_avg: {round(v_fe_avg,3)}")
col121.write(f"hhi: {round(v_hhi,3)}")
col121.write(f"esg: {round(v_esg,3)}")
col121.write(f"sr: {round(v_sr,3)}")
col121.write(f"p_avg: {round(v_p_avg,3)}")

col122.write(f"r_avg: {round(v_r_avg,3)}")
col122.write(f"c_avg: {round(v_c_avg,3)}")
col122.write(f"p_max: {round(v_p_max,3)}")
col122.write(f"r_max: {round(v_r_max,3)}")
col122.write(f"c_max: {round(v_c_max,3)}")
col122.write(f"herows_score: {round(herows_score,3)}")

st.markdown('----')


#################-----> CONTAINER 2 <-----#################


container2 = st.container()
col21,col22 = container2.columns([0.7, 0.3] , gap = "large")


col211,col212 = col21.columns(2)

X_scatter_plot = col211.selectbox(
    "Select the X axis",
    options=list(df.columns[1:]),
    key="selectbox_X"  # Key helps Streamlit identify the widget
)

Y_scatter_plot = col212.selectbox(
    "Select the Y axis",
    options=list(df.columns[1:]),
    key="selectbox_Y"  # Key helps Streamlit identify the widget
)


@st.cache_resource
def create_scatter_plot(X_scatter_plot, Y_scatter_plot):
    scatter_plot = px.scatter(df, x=X_scatter_plot, y=Y_scatter_plot, hover_name='index')
    scatter_plot.update_layout(title=f"<b>Scatter Plot: {X_scatter_plot} vs {Y_scatter_plot}</b>",
                               xaxis_title=X_scatter_plot,
                               yaxis_title=Y_scatter_plot,
                               title_font_color="#103778",
                               title_x=0.1,
                               width=800,
                               height=600)
    scatter_plot.update_traces(marker=dict(
        color='#0593A2'))
    return scatter_plot

scatter_plot = create_scatter_plot(X_scatter_plot, Y_scatter_plot)
col21.plotly_chart(scatter_plot,use_container_width=True)


col221 , col222 = col22.columns(2)

var_circular_barplot_var_decile = col221.selectbox(
    "Select the variable",
    options=list(Decile.columns[1:-1]),
    key="selectbox_var_circular_barplot_var_decile"  # Key helps Streamlit identify the widget
)

decile_circular_barplot_var_decile = col222.selectbox(
    "Select the decile",
    options= [1,2,3,4,5,6,7,8,9,10],
    key="selectbox_decile_circular_barplot_var_decile"  # Key helps Streamlit identify the widget
)

@st.cache_resource
def circular_barplot_var_decile(var, decile):
    element_counts_regular = {}
    a = []
    b = []
    element_counts = {}

    selected_data = Decile[["index", var]][Decile[var] == decile]

    element_counts = defaultdict(int)

    for index_value in selected_data["index"]:
        elements = index_value.split("-")
        for element in elements:
            element_counts[element] += 1
    element_counts_regular = dict(element_counts)

    a = list(element_counts_regular.keys())
    b = list(element_counts_regular.values())
    fig = go.Figure()
    fig.add_trace(go.Barpolar(r=b, theta=a, text=a, hoverinfo='text+r'))
    fig.update_layout(
        title="Circular Barplot",
        polar=dict(radialaxis=dict(showticklabels=False, ticks=''), angularaxis=dict(direction="clockwise"))
    )
    
    return fig  # Return the figure object

cirular_bar1 = circular_barplot_var_decile(var_circular_barplot_var_decile, decile_circular_barplot_var_decile)
col22.plotly_chart(cirular_bar1 ,use_container_width=True)

st.markdown('----')



#################-----> CONTAINER 3 <-----#################


container3 = st.container()
col31,col32 = container3.columns([0.3, 0.7], gap = "large" )


col311,col312 = col31.columns(2 , gap = "large")

best_worst = col311.selectbox(
    "Select best or worst",
    options=["best",'worst'],
    key="selectbox_best_worst"  # Key helps Streamlit identify the widget
)

n_best_worst = col312.number_input("Pick a number",1,30000)



@st.cache_resource
def circular_barplot_best_600(etat , n):
    element_counts_regular = {}
    a = []
    b = []
    element_counts = {}
    sorted_decile = Decile.sort_values(by="HERowS_Score")
    if etat == 'best' : 
        selected_rows_10 = sorted_decile.head(n)
    else :
        selected_rows_10 = sorted_decile.tail(n)
    
    element_counts = defaultdict(int)
    for index_value in selected_rows_10["index"]:
        elements = index_value.split("-")  # Diviser la valeur en éléments chimiques
        for element in elements:
            element_counts[element] += 1  # Incrémenter le compteur d'occurrences

    # Convertir le dictionnaire en un dictionnaire régulier (si nécessaire)
    element_counts_regular = dict(element_counts)
    
    a = list(element_counts_regular.keys())
    b = list(element_counts_regular.values())
    fig = go.Figure()
    fig.add_trace(go.Barpolar(r=b,theta=a,text=a,hoverinfo='text+r',))
    fig.update_layout(
    title="Circular Barplot for the best/wordt n alloys",
    polar=dict(radialaxis=dict(showticklabels=False, ticks=''),angularaxis=dict(direction="clockwise"),))
    return fig

cirular_bar2 = circular_barplot_best_600(best_worst , n_best_worst)
col31.plotly_chart(cirular_bar2 ,use_container_width=True)

@st.cache_resource
def plot_density():
    hist_data = [list(Decile["HERowS_Score"])]
    group_labels = ['Group 1']
    color = ["#103778"]
    fig = ff.create_distplot(hist_data, group_labels, colors=color, show_rug=False)

    return fig
density_plot = plot_density()
col32.plotly_chart(density_plot ,use_container_width=True  ,use_container_height=True)


st.markdown('----')


#######

########## CNTAINER 4 3#######

container4 = st.container()
col41,col42 = container4.columns([0.7, 0.3], gap = "large" )

@st.cache_resource
def cumulative_graph():
    density = np.histogram(Decile["HERowS_Score"], bins=30, density=True)
    cumulative_density = np.cumsum(density[0]) * np.diff(density[1])[0]

    # Create cumulative KDE plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=density[1][1:], y=cumulative_density, mode='lines'))

    # Update layout
    fig.update_layout(
        title="Cumulative KDE of HERowS_Score",
        xaxis_title="HERowS_Score",
        yaxis_title="Cumulative Density",
    )
    return fig

cum_plot = cumulative_graph()
col41.plotly_chart(cum_plot ,use_container_width=True  ,use_container_height=True)


@st.cache_resource
def circular_barplot_all():
    element_counts_regular = {}
    a = []
    b = []
    element_counts = {}
    element_counts = defaultdict(int)
    for index_value in Decile["index"]:
        elements = index_value.split("-")  # Diviser la valeur en éléments chimiques
        for element in elements:
            element_counts[element] += 1  # Incrémenter le compteur d'occurrences

    # Convertir le dictionnaire en un dictionnaire régulier (si nécessaire)
    element_counts_regular = dict(element_counts)
    
    a = list(element_counts_regular.keys())
    b = list(element_counts_regular.values())
    fig = go.Figure()
    fig.add_trace(go.Barpolar(r=b,theta=a,text=a,hoverinfo='text+r',))
    fig.update_layout(
    title="Circular Barplot for all the 30000 alloys",
    polar=dict(radialaxis=dict(showticklabels=False, ticks=''),angularaxis=dict(direction="clockwise"),))
    return fig


all_plot_circular_bar = circular_barplot_all()
col42.plotly_chart(all_plot_circular_bar ,use_container_width=True  ,use_container_height=True)



