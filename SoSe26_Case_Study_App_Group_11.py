import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings

warnings.filterwarnings("ignore")


st.set_page_config(
    page_title="OEM1 Sustainability Analysis",
    layout="wide"
)



@st.cache_data
def load_data():
    return pd.read_csv("data/SoSe26_Case_Study_finalData_Group_11.csv")

@st.cache_data
def convert_df_to_csv(data):
    return data.to_csv(index=False).encode("utf-8")

@st.cache_data
def prepare_boxplot_data(data):

    base = data[
        [
            "ID_Vehicle",
            "Vehicle_Type",
            "Type_Origin",
            "Route_Stage",
            "Distance_km",
            "Total_Distance_km"
        ]
    ]

    return {
        "Vehicle Type": (
            base[
                [
                    "ID_Vehicle",
                    "Vehicle_Type",
                    "Total_Distance_km"
                ]
            ]
            .drop_duplicates()
        ),

        "Engine Type": (
            base[
                base["Type_Origin"].str.startswith(
                    "Engine",
                    na=False
                )
            ][
                [
                    "Type_Origin",
                    "Total_Distance_km"
                ]
            ]
            .drop_duplicates()
        ),

        "Gearshift Type": (
            base[
                base["Type_Origin"].str.startswith(
                    "Gearshift",
                    na=False
                )
            ][
                [
                    "Type_Origin",
                    "Total_Distance_km"
                ]
            ]
            .drop_duplicates()
        ),

        "Single Part Type": (
            base[
                base["Type_Origin"].str.startswith(
                    "T",
                    na=False
                )
            ][
                [
                    "Type_Origin",
                    "Total_Distance_km"
                ]
            ]
            .drop_duplicates()
        ),

        "Route Stage": (
            base[
                [
                    "Route_Stage",
                    "Distance_km"
                ]
            ]
        )
    }




def create_boxplot(plot_df, category):

    if category == "Route Stage":
        x_column = "Route_Stage"
        y_column = "Distance_km"
        y_title = "Stage Distance (km)"

    elif category == "Vehicle Type":
        x_column = "Vehicle_Type"
        y_column = "Total_Distance_km"
        y_title = "Total Logistics Distance (km)"

    else:
        x_column = "Type_Origin"
        y_column = "Total_Distance_km"
        y_title = "Total Logistics Distance (km)"


    fig = px.box(
        plot_df,
        x=x_column,
        y=y_column,
        points=False,
        title=f"Distance Distribution by {category}"
    )

    fig.update_layout(
        xaxis_title=category,
        yaxis_title=y_title,
        height=600
    )

    return fig


def prepare_boxplot_figures(boxplot_data):

    figures = {}

    for category, data in boxplot_data.items():
        figures[category] = create_boxplot(
            data,
            category
        )

    return figures




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
                    size= [7, 12]
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



df = load_data()
boxplot_data = prepare_boxplot_data(df)
boxplot_figures = prepare_boxplot_figures(boxplot_data)



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

    st.caption(
        "Explore the logistics routes of individual vehicles produced in 2015.\n\n" +
        
        "Use the search field to find a specific vehicle and visualize its complete\
        supply chain from component suppliers to the distribution center."
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

    vehicle_total_distance = map_df["Total_Distance_km"].iloc[0]

    average_vehicle_distance = (
        df.groupby("ID_Vehicle")["Total_Distance_km"]
        .first()
        .mean()
    )

    with col1:
        st.metric(
            "Vehicle Total Distance",
            f"{vehicle_total_distance:,.1f} km"
        )

    with col2:
        st.metric(
            "Average Vehicle Distance",
            f"{average_vehicle_distance:,.1f} km"
        )

    with col3:
        difference = (
            vehicle_total_distance - average_vehicle_distance
        )

        st.metric(
            "Difference from Average",
            f"{difference:+,.1f} km"
        )
        
    fig = create_map(map_df)

    st.plotly_chart(
        fig,
        width = "stretch"
    )
    st.info(
    """
    **Map Interpretation**

    - Small markers represent the **origin** of a logistics route.
    - Large markers represent the **destination** of a logistics route.
    - Lines indicate the transportation path between locations.
    - Hover over a route to view detailed information about the logistics stage,
      locations, and travelled distance.

    The displayed routes represent the supply chain stages of the selected vehicle,
    from component suppliers to the distribution center.
    """
)

with tab3:

    st.header("Interactive Logistics Distance Analysis")

    st.caption(
        "Compare logistics distances across different supply chain categories."
    )

    category = st.selectbox(
    "Compare by",
    list(boxplot_figures.keys())
    )

    fig = boxplot_figures[category]

    st.plotly_chart(
        fig,
        width="stretch"
    )

with tab4:

    st.header("Dataset Overview")

    st.caption(
        "Explore the final dataset used for the supply chain analysis."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Rows",
            f"{len(df):,}"
        )

    with col2:
        st.metric(
            "Total Columns",
            len(df.columns)
        )


    selected_columns = st.multiselect(
        "Select columns to display",
        df.columns,
        default=list(df.columns)
    )


    number_rows = st.slider(
        "Number of rows to display",
        min_value=10,
        max_value=1000,
        value=100,
        step=10
    )


    display_df = df.loc[:, selected_columns].head(number_rows)

    st.dataframe(
        display_df,
        width = "stretch",
        height=400
    )

    csv = convert_df_to_csv(df)


    st.download_button(
        label="Download Complete Dataset",
        data=csv,
        file_name="OEM1_supply_chain_dataset.csv",
        mime="text/csv"
    )