import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_map(data):

    fig = go.Figure()

    for _, row in data.iterrows():

        fig.add_trace(
            go.Scattermap(
                lat=[
                    row["Lat_Origin"],
                    row["Lat_Destination"]
                ],
                lon=[
                    row["Lon_Origin"],
                    row["Lon_Destination"]
                ],
                mode="lines+markers",
                line=dict(
                    width=2
                ),
                marker=dict(
                    size=6
                ),
                name=f"{row["Type_Origin"]} to {row["Type_Destination"]}",
                hoverinfo="text",
                text=(
                    f"Stage: {row['Route_Stage']}<br>"
                    f"Type: {row['Type_Origin']} to {row['Type_Destination']}<br>"
                    f"From: {row['Location_Origin']} {row['City_Origin']}<br>"
                    f"To: {row['Location_Destination']} {row['City_Destination']}<br>"
                    f"Distance: {row['Distance_km']:.1f} km"
                )
            )
        )

    fig.update_layout(
        map=dict(
            style="carto-darkmatter",
            center={
                "lat": 51.0,
                "lon": 10.5
            },
            zoom=5
        ),
        height=700,
        showlegend=True
    )

    return fig





st.set_page_config(
    page_title="OEM1 Supply Chain Analysis",
    layout="wide"
)



col1, col2 = st.columns([1, 5])

with col1:
    st.image("www/Case_Study_Logo.png", width=180)

with col2:
    st.markdown(
        """
        <h1 style="
            font-size: 42px;
            margin-top: 25px;
            margin-bottom: 0px;
            color: #71bef1";
        ">
            OEM1 Sustainability Analysis
        </h1>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
    """
    <p style="
        color:#7FA8C9;
        font-size:16px;
        margin-top:-10px;
    ">
    Logistics route analysis of vehicles produced in 2015
    </p>
    """,
    unsafe_allow_html=True
)


@st.cache_data
def load_data():
    return pd.read_csv("SoSe26_Case_Study_finalData_Group_11.csv")

df = load_data()


tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview","Route Explorer", "Distance Analysis", "Dataset Overview"]
)

with tab1:
    st.markdown(
    """
    <div style="
        max-width: 900px;
        margin: auto;
        text-align: center;
    ">

    <h1>Application Overview</h1>

    <p style="font-size:18px;">
    This application visualizes the logistics routes of vehicles produced by OEM1 in 2015.
    The objective is to analyze transportation distances across the supply chain and
    explore the logistics structure of vehicles, components, and individual parts.
    </p>

    <p style="font-size:16px;">
    The analysis includes the following supply chain stages:
    <br>
    Single Parts → Components<br>
    Components → Vehicle Production Plant<br>
    Vehicle Production Plant → Distribution Center
    </p>

    <p style="font-size:16px;">
    An analysis of the final customer delivery stage is excluded, as the customer location cannot be reliably determined and is outside the manufacturer's control. 
    Therefore, this stage is not considered relevant for assessing the sustainability of the controllable supply chain.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


    st.write("")


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Vehicles Analyzed",
            f"{df['ID_Vehicle'].nunique():,}"
        )

    with col2:
        st.metric(
            "Supply Chain Routes",
            f"{len(df):,}"
        )

    with col3:
        st.metric(
            "Total Distance",
            f"{df['Distance_km'].sum():,.0f} km"
        )


    st.write("")

    st.info(
        """
        Use the interactive views to explore individual supply chains,
        compare logistics distances, and inspect the processed dataset.
        """
    )


with tab2: 
    st.header("Interactive Supply Chain Map")

    st.markdown(
        """
        Explore the logistics routes of individual vehicles produced in 2015.
        
        Use the search field to find a specific vehicle and visualize its complete
        supply chain from component suppliers to the distribution center.
        """
    )
    vehicle_search = st.text_input(
    "Search Vehicle ID"
    )

    if vehicle_search:
        vehicle_options = df[
            df["ID_Vehicle"].str.contains(
                vehicle_search,
                case=False,
                na=False
            )
        ]["ID_Vehicle"].unique()
    else:
        vehicle_options = df["ID_Vehicle"].unique()


    selected_vehicle = st.selectbox(
        "Select Vehicle",
        vehicle_options
    )
    map_df = df[
        df["ID_Vehicle"] == selected_vehicle
    ]
    
    st.subheader(f"Supply Chain Map - Vehicle {selected_vehicle}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Logistics Distance",
            f"{map_df['Total_Distance_km'].iloc[0]:,.1f} km"
        )

    with col2:
        st.metric(
            "Number of Route Stages",
            len(map_df)
        )

    with col3:
        st.metric(
            "Average Route Distance",
            f"{map_df['Distance_km'].mean():,.1f} km"
        )
        
    fig = create_map(map_df)

    st.plotly_chart(
        fig,
        use_container_width=True
    )
 
with tab4:

    st.write(
        "Analysis of logistics routes for vehicles produced in 2015."
    )

    st.dataframe(df)