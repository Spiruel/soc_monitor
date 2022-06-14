import streamlit as st
import extra_streamlit_components as stx

import geemap
import ee
ee.Initialize()

import pandas as pd
import geopandas as gpd

st.set_page_config(page_title="test",layout="wide")

st.title('SOC monitoring of agricultural lands')

a, b = st.columns([5,8])

with a:
    st.header('Welcome to the SOC monitoring tool')
    #st.write('----------')
    st.write('''
    **Description**
    
    This platform serves as a tool for estimating soil organic carbon (SOC) stocks in agricultural systems. After estimating a baseline SOC stock mp, it is posible to estimate changes in SOC stock over a defined period (for example, every two years).
    
    Inside the platform you can find options for SOC mapping. You can choose between ML models and there is available a set of environmental covariates to use as predictors.
    
    -------------------
    
    **Instructions**
    
    1. Upload data
    2. Choose environmental covariates
    3. Run the model - measure accuracy and uncertainty
    4. Build a baseline SOC stock map
    5. Prediction every two years, until the 8th year
    6. Compare the differences in SOC during the period
    7. Measure additionality/leakage
    8. Make recommendations
    
    ''')
    
with b:
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id=1, title="Map", description=""),
        stx.TabBarItemData(id=2, title="Summary", description=""),
        stx.TabBarItemData(id=3, title="Modelling", description=""),
        stx.TabBarItemData(id=4, title="SOC changes", description=""),
        stx.TabBarItemData(id=5, title="Recommendations", description=""),
    ], default=1, key='orig')
    

    if chosen_id == '1':
        Map = geemap.Map(center=(50,0), zoom=5)
    
        dataset = ee.Image("OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02")
        visualization = {
          'bands': ['b0'],
          'min': 0.0,
          'max': 120.0,
          'palette': [
            "ffffa0","f7fcb9","d9f0a3","addd8e","78c679","41ab5d",
            "238443","005b29","004b29","012b13","00120b",
          ]
        }

        Map.addLayer(dataset, visualization, "Soil organic carbon content in x 5 g / kg")
    
        empty_map = st.empty()
        st.write('---------')
        
        with st.spinner(text="Loading map..."):
                #c,d = st.columns(2)
                #with c:
                data_up = st.file_uploader('Upload data. Choose csv file', type='csv')
                if data_up is not None:
                    bytes_data = data_up.getvalue()
                    bytes_data_save = f'/tmp/{data_up.name}'
                    with open(bytes_data_save, 'wb') as f:
                        f.write(bytes_data)
                    
                    df = pd.read_csv(bytes_data_save)
                    with st.expander('Csv preview'):
                        st.write(df.head())
                    
                    if 'longitude' not in df.columns or 'latitude' not in df.columns:
                        st.error('Cannot find coordinates from csv')
                    else:
                        vector = geemap.csv_to_ee(bytes_data_save)
                        Map.addLayer(vector, {}, 'csv layer')
                #with d:
                shape_up = st.file_uploader('Upload map. Choose geojson', type='geojson')
                if shape_up is not None:
                    bytes_data = shape_up.getvalue()
                    bytes_shape_save = f'/tmp/{shape_up.name}'
                    with open(bytes_shape_save, 'wb') as f:
                        f.write(bytes_data)
                    vector = geemap.geojson_to_ee(bytes_shape_save)
                    if vector is not None:
                        gdf = gpd.read_file(bytes_shape_save)
                        with st.expander('Geojson preview'):
                            st.write(gdf.head())
                        
                        Map.addLayer(vector, {}, 'map layer')
                    else:
                        st.error('Couldn\'t read geojson correctly')
                        
                with empty_map:
                    Map.to_streamlit()
            
    elif chosen_id == '2':
        st.warning('A summary is written here')
    elif chosen_id == '3':
        st.error('Modelling info is written here')
    else:
        st.write('Information goes here')
