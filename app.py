# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# %%
st.title("Covid 19 Dashboard")
st.markdown("Built using python streamlit with data from Malaysia Ministry of Health (MOH)")
st.header("Quote : DG Hisham - Twitter")
st.markdown("> Marie Curie once said, I quote “Nothing in life is to be feared, it is only to be understood. Now is the time to understand more, so that we may fear less”unquote. To manage our fear we need to engage, explain & manage the expectation & understand more to allay the fear")


# %%
@st.cache(persist=True)
def load_data1(DATA_URL):
    data = pd.read_csv(DATA_URL)
    data['date']= pd.to_datetime(data['date'])
    return data

@st.cache(persist=True)
def load_data2(DATA_URL):
    data = pd.read_csv(DATA_URL)
    data['date']= pd.to_datetime(data['date'])
    return data

@st.cache(persist=True)
def load_data3(DATA_URL):
    data = pd.read_csv(DATA_URL)
    data['date']= pd.to_datetime(data['date'])
    return data

@st.cache(persist=True)
def load_data4(DATA_URL):
    data = pd.read_csv(DATA_URL)
    data['date']= pd.to_datetime(data['date'])
    return data
    
@st.cache(persist=True)
def load_data5(DATA_URL):
    data = pd.read_csv(DATA_URL)
    return data


df_vaccmalaysia = load_data1("https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_malaysia.csv")
df_deathmalaysia = load_data2("https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/deaths_malaysia.csv")
df_deathstate = load_data3("https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/deaths_state.csv")
df_vaccstate = load_data4("https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_state.csv")

df_population = load_data5("https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/static/population.csv")


# %%
pop_malaysia = df_population[df_population["state"] == "Malaysia"]["pop"][0]
herd_malaysia = 80/100*pop_malaysia


# %%

st.header("Malaysia Vaccination vs Death")
fig_mas = make_subplots(specs=[[{"secondary_y": True}]])



# Add Dose 1 Vaccice traces
fig_mas.add_trace(
    go.Scatter(x=df_vaccmalaysia["date"], y=df_vaccmalaysia["cumul_partial"], name="Dose1 Vaccince"),
    secondary_y=False,
)

# Add Dose 2 Vaccice traces
fig_mas.add_trace(
    go.Scatter(x=df_vaccmalaysia["date"], y=df_vaccmalaysia["cumul_full"], name="Dose2 Vaccince"),
    secondary_y=False,
)

# Add 100% malaysia trace 
fig_mas.add_shape( # add a horizontal "target" line
    type="line", line_color="olivedrab", line_width=3, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=pop_malaysia, y1=pop_malaysia, yref="y",
    secondary_y=False,
)

fig_mas.add_trace(go.Scatter(
    x=[df_vaccmalaysia["date"].median()],
    y=[0.96*pop_malaysia],
    text=f"100% Population {int(pop_malaysia)}",
    mode="text",
    name= "100% Population",
    showlegend=False,
))

# Add herd malaysia trace 
fig_mas.add_shape( # add a horizontal "target" line
    type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=herd_malaysia, y1=herd_malaysia, yref="y",
    secondary_y=False,
)

fig_mas.add_trace(go.Scatter(
    x=[df_vaccmalaysia["date"].median()],
    y=[0.96*herd_malaysia],
    text=f"Herd Immunity {int(herd_malaysia)}",
    mode="text",
    name= "Herd Immunity",
    showlegend=False,
))

# Add 50% pop Malaysia trace
fig_mas.add_shape( # add a horizontal "target" line
    type="line", line_color="LightSeaGreen", line_width=3, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=pop_malaysia/2, y1=pop_malaysia/2, yref="y",
    secondary_y=False,
)

fig_mas.add_trace(go.Scatter(
    x=[df_vaccmalaysia["date"].median()],
    y=[0.96*pop_malaysia/2],
    text=f"50% population {int(pop_malaysia/2)}",
    mode="text",
    name= "Pop 50%",
    showlegend=False,
))

# Add death Malaysia trace at another y axis, by default is hidden
fig_mas.add_trace(
    go.Scatter(x=df_deathmalaysia["date"], y=df_deathmalaysia["deaths_new"], name="Death (Click to hide/unhide)", line_color="grey", visible = "legendonly"), #mode='markers', marker_color="grey", visible = "legendonly"), #, line_color="grey"), 
    secondary_y=True,
)

# Add figure title
fig_mas.update_layout(
    title_text="Malaysia Vaccination vs Daily Death"
)

# Set x-axis title
fig_mas.update_xaxes(title_text="Date", 

)

# Set y-axes titles
fig_mas.update_yaxes(title_text="<b>Vaccination</b> 1 & 2", secondary_y=False)
fig_mas.update_yaxes(title_text="<b>Death</b>", secondary_y=True)

# Visualize and export to HTML (if required)
# fig_mas.show()
# fig_mas.write_html("VaccinationvsDeath.html")
st.plotly_chart(fig_mas)

# %%
statelist = df_vaccstate["state"].unique().tolist()
default_ix = statelist.index("Selangor")
x = st.selectbox('Select State', statelist, index=default_ix)
# x = "Selangor"
st.header(f"{x} Vaccination vs Death")

df_deathstatex = df_deathstate[df_deathstate["state"] == x]
df_vaccstatex = df_vaccstate[df_vaccstate["state"] == x]
popstatex = df_population[df_population["state"] == x]["pop"].values[0]
herd_statex = 80/100*popstatex

# %%
fig_statex = make_subplots(specs=[[{"secondary_y": True}]])

# Add Dose 1 Vaccice traces for stateX
fig_statex.add_trace(
    go.Scatter(x=df_vaccstatex["date"], y=df_vaccstatex["cumul_partial"], name="Dose1 Vaccince"),
    secondary_y=False,
)


# Add Dose 2 Vaccice traces for stateX
fig_statex.add_trace(
    go.Scatter(x=df_vaccstatex["date"], y=df_vaccstatex["cumul_full"], name="Dose2 Vaccince"),
    secondary_y=False,
)

# Add 100% stateX trace 
fig_statex.add_shape(
    type="line", line_color="olivedrab", line_width=3, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=popstatex, y1=popstatex, yref="y",
    secondary_y=False,
)

fig_statex.add_trace(go.Scatter(
    x=[df_vaccstatex["date"].median()],
    y=[0.96*popstatex],
    text=f"100% Population {popstatex}",
    mode="text",
    name= "100% Population",
    showlegend=False,
))

# Add herd stateX trace 
fig_statex.add_shape(
    type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=herd_statex, y1=herd_statex, yref="y",
    secondary_y=False,
)

fig_statex.add_trace(go.Scatter(
    x=[df_vaccstatex["date"].median()],
    y=[0.96*herd_statex],
    text=f"Herd Immunity {herd_statex}",
    mode="text",
    name= "Herd Immunity",
    showlegend=False,
))

# Add 50% pop stateX trace
fig_statex.add_shape( # add a horizontal "target" line
    type="line", line_color="LightSeaGreen", line_width=3, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=popstatex/2, y1=popstatex/2, yref="y",
    secondary_y=False,
)

fig_statex.add_trace(go.Scatter(
    x=[df_vaccstatex["date"].median()],
    y=[0.96*popstatex/2],
    text=f"50% Population {popstatex/2}",
    mode="text",
    name= "50% Population",
    showlegend=False,
))

# Add death stateX trace at another y axis, by default is hidden
fig_statex.add_trace(
    go.Scatter(x=df_deathstatex["date"], y=df_deathstatex["deaths_new"], name="Death (Click to hide/unhide)", line_color="grey", visible = "legendonly"), #mode='markers', marker_color="grey", visible = "legendonly"), #, line_color="grey"), 
    secondary_y=True,
)

# Add figure title
fig_statex.update_layout(
    title_text=f"{x} State Vaccination vs Daily Death"
)

# Set x-axis title
fig_statex.update_xaxes(title_text="Date", 

)

# Set y-axes titles
fig_statex.update_yaxes(title_text="<b>Vaccination</b> 1 & 2", secondary_y=False)
fig_statex.update_yaxes(title_text="<b>Death</b>", secondary_y=True)

# Visualize and export to HTML (if required)
# fig_statex.show()
# fig_statex.write_html(f"State {x} VaccinationvsDeath.html")
st.plotly_chart(fig_statex)

# %%
st.markdown('<small>© Copyright 2021, Masri Mustaman</small>', unsafe_allow_html=True)
st.markdown('<small>https://github.com/masrimustaman/data-analysis-moh-vaccination-death</small>', unsafe_allow_html=True)
st.markdown('<small>https://www.linkedin.com/in/md-masri-md-mustaman</small>', unsafe_allow_html=True)
