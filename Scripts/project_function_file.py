import seaborn as sns
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import json
from pandas import Timestamp


def setup_libraries():
    import seaborn as sns
    import pandas as pd
    import plotly.express as px
    import matplotlib.pyplot as plt
    import numpy as np
    import json
    from pandas import Timestamp





def load_data():
    df_c = pd.read_csv('caracteristiques-2019-2021.csv', sep=';', encoding='utf-16', low_memory=False, on_bad_lines='skip')
    df_v = pd.read_csv('vehicules-2019-2021.csv', sep=';', encoding='utf-16', low_memory=False, on_bad_lines='skip')
    df_u = pd.read_csv('usagers-2019-2021.csv', sep=';', encoding='utf-16', low_memory=False, on_bad_lines='skip')
    df_l = pd.read_csv('lieux-2019-2021.csv', sep=';', encoding='utf-16', low_memory=False, on_bad_lines='skip')
    df_an = pd.read_csv('caracteristiques_modified.csv', encoding='ISO-8859-1', low_memory=False)
    df_dep = pd.read_csv('donnees_departements.csv', sep=';', encoding='UTF-8', low_memory=False)

    # Return the loaded dataframes or perform any other operations
    return df_c, df_v, df_u, df_l, df_an, df_dep




def plot_accidents_per_month(df_c):
    # Check if the value is an integer, if not, convert it to an integer
    df_c["mois"] = df_c["mois"].apply(lambda x: int(x) if isinstance(x, str) and x.isnumeric() else x)

    # Filter out non-numeric rows from the "mois" column
    df_c = df_c[df_c["mois"].apply(lambda x: isinstance(x, int))]

    # Count the occurrences of each month
    month_counts = df_c["mois"].value_counts().sort_index()

    # Convert month_counts.index to a list and format the month numbers
    formatted_month_index = [f"{int(month)}" for month in month_counts.index]

    # Create a list with the names of the months in French
    noms_mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

    # Replace the numeric indices with the month names
    formatted_month_index = [noms_mois[int(month) - 1] for month in month_counts.index]

    # Create the bar chart using Plotly Express
    fig = px.bar(
        x=formatted_month_index,
        y=month_counts.values,
        labels={"x": "Month", "y": "Number of accidents"},
        title="Amount of accidents per month"
    )

    # Display the chart
    fig.show()




def plot_yearly_accident_evolution(df_an):
    # Count the occurrences of each year
    year_counts = df_an["annee"].value_counts().sort_index()

    # Create a line chart using Plotly Express
    fig = px.line(x=year_counts.index, y=year_counts.values, labels={"x": "Year", "y": "Amount of accidents"})

    # Add a title to the chart
    fig.update_layout(title_text="The yearly evolution of the amount of accidents")

    # Set the y-axis scale to start from 0
    fig.update_yaxes(range=[0, max(year_counts.values)])

    # Display the chart
    fig.show()




def plot_accidents_by_day_of_week(df_c):
    # Filter out rows with non-numeric values in the 'an' column
    df_c_filtered = df_c[pd.to_numeric(df_c['an'], errors='coerce').notna()]

    # Convert the date to datetime format
    df_c_filtered['date'] = pd.to_datetime(df_c_filtered[['an', 'mois', 'jour']].rename(columns={'an': 'year', 'mois': 'month', 'jour': 'day'}))

    # Define the days of the week
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Count the number of accidents by day of the week
    accidents_by_day_of_week = df_c_filtered['date'].dt.day_name().value_counts().reindex(days_of_week)

    # Create a bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x=accidents_by_day_of_week.index, y=accidents_by_day_of_week.values, color='blue')  # Set bar color to blue
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Accidents')
    plt.title('Number of Accidents by Day of the Week')
    plt.show()




def plot_accidents_by_infrastructure(df_l):
    # Filter out rows with 'infra' value
    df_l_filtered = df_l[df_l['infra'] != 'infra']
    
    # Convert the 'infra' column to integer
    df_l_filtered['infra'] = df_l_filtered['infra'].astype(int)

    # Filter the DataFrame to exclude rows with categories -1 (Not specified), 0 (None), and 9 (Other)
    filtered_df_l = df_l_filtered[~df_l_filtered['infra'].isin([-1, 0, 9])]

    # Count the number of accidents by infrastructure type
    accidents_by_infra = filtered_df_l['infra'].value_counts().reset_index()

    # Rename the columns for easier chart creation
    accidents_by_infra.columns = ['infra', 'count']

    # Create a dictionary to map infrastructure codes to their descriptions
    infra_dict = {
        1: 'Souterrain',
        2: 'Pont',
        3: 'Bretelle',
        4: 'Voie ferrée',
        5: 'Carrefour',
        6: 'Zone piétonne',
        7: 'Zone de péage',
        8: 'Chantier'
    }

    # Replace the infrastructure codes with their descriptions
    accidents_by_infra['infra'] = accidents_by_infra['infra'].replace(infra_dict)

    # Sort the DataFrame by the number of accidents in ascending order
    accidents_by_infra = accidents_by_infra.sort_values('count')

    # Create the bar chart with Plotly Express
    fig = px.bar(accidents_by_infra, x='infra', y='count', title="Amount of accidents on different infrastructure types")

    # Display the chart
    fig.show()





def plot_accidents_by_road_type(df_l, df_u):
    # Dictionary of road types
    types_de_route = {
        1: 'Autoroute',
        2: 'Route nationale',
        3: 'Route départementale',
        4: 'Voie communale',
        5: 'Hors réseau public',
        6: 'Parc de stationnement',
        7: 'Route de métropole urbaine',
        9: 'Autre'
    }

    # Convert the "catr" column to integers, ignoring errors
    df_l["catr"] = pd.to_numeric(df_l["catr"], errors='coerce')

    # Remove the first row (header row) if it exists
    if pd.isna(df_l.iloc[0]["catr"]):
        df_l = df_l.iloc[1:]

    # Filter out rows with non-numeric values in the "catr" column
    df_l = df_l[df_l["catr"].notna()]

    # Merge the two dataframes (usagers and lieux) on the "Num_Acc" column
    df_merged = pd.merge(df_u, df_l, on="Num_Acc")

    # Group the data by road type and count the number of accidents
    accidents_par_type_route = df_merged.groupby('catr')['Num_Acc'].count().sort_values(ascending=False)

    # Create a bar chart using Plotly Express
    fig = px.bar(x=accidents_par_type_route.values, y=[types_de_route[int(x)] for x in accidents_par_type_route.index], orientation='h', labels={'x': "Amount of accidents", 'y': 'Road type'}, title="Amount of accidents by road type")

    # Reverse the y-axis to display road types from top to bottom
    fig.update_yaxes(autorange="reversed")

    # Add annotations to display values on the bars
    fig.update_traces(texttemplate='%{x}', textposition='inside')

    # Display the chart
    fig.show()




def plot_accidents_by_area_type(df_c):
    # Count the number of accidents in urban areas (2) and outside urban areas (1)
    agglo_counts = df_c['agg'].value_counts().reset_index()

    # Rename the columns for better readability
    agglo_counts.columns = ['Agglomeration', 'Count']

    # Replace numeric values with descriptive names
    agglo_counts['Agglomeration'] = agglo_counts['Agglomeration'].replace({1: 'Outside urban areas', 2: 'Inside urban areas'})

    # Create a pie chart
    fig = px.pie(agglo_counts, values='Count', names='Agglomeration', title="Accident frequency by Area type")

    # Display the chart
    fig.show()




def plot_accidents_by_department(df_c):
    # Load the GeoJSON file of French departments
    with open('departements.geojson', 'r') as file:
        france_departements = json.load(file)

    # Calculate the number of accidents per department
    df_c['dep'] = df_c['dep'].astype(str).str.zfill(2)
    accidents_by_dep = df_c['dep'].value_counts().reset_index()
    accidents_by_dep.columns = ['dep', 'accidents']

    # Create the choropleth map with Plotly Express
    fig = px.choropleth_mapbox(accidents_by_dep,
                               geojson=france_departements,
                               locations='dep',
                               featureidkey='properties.code',
                               color='accidents',
                               color_continuous_scale="reds",
                               range_color=(0, 15000),
                               mapbox_style="carto-positron",
                               zoom=5,
                               center={"lat": 46.603354, "lon": 1.888334},
                               opacity=0.5,
                               labels={'accidents': "Amount of accidents"},
                               title="Distribution of road accidents in mainland France per department")

    fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
    fig.show()




def plot_speed_distribution(df_l):
    # Convert the 'vma' column to numeric
    df_l['vma'] = pd.to_numeric(df_l['vma'], errors='coerce')

    # Remove rows with 'vma' equal to -1 or greater than 130
    df_l_filtered = df_l[(df_l['vma'] != -1) & (df_l['vma'] <= 130)]

    # Sort the filtered DataFrame by 'vma'
    df_l_sorted = df_l_filtered.sort_values('vma')

    # Create the box plot
    fig = px.box(df_l_sorted, y="vma", 
                 title="Distribution of accidents by maximal speed authorized at the accident location",
                 labels={"vma": "Maximal speed authorized (km/h)"})

    # Show the plot
    fig.show()




def plot_accident_distribution(df_c, mapbox_access_token):
    # Check if the values are strings, otherwise convert them to strings
    df_c['lat'] = df_c['lat'].astype(str)
    df_c['long'] = df_c['long'].astype(str)

    # Replace commas with dots in the 'lat' and 'long' columns
    df_c['lat'] = df_c['lat'].str.replace(',', '.')
    df_c['long'] = df_c['long'].str.replace(',', '.')

    # Convert the 'lat' and 'long' columns to float and replace non-numeric values with NaN
    df_c['lat'] = pd.to_numeric(df_c['lat'], errors='coerce')
    df_c['long'] = pd.to_numeric(df_c['long'], errors='coerce')

    # Drop rows with NaN values in the 'lat' and 'long' columns
    df_c = df_c.dropna(subset=['lat', 'long'])

    # Set the Mapbox API key for Plotly Express
    px.set_mapbox_access_token(mapbox_access_token)

    # Create a Mapbox map with Plotly Express using the 'lat' and 'long' columns from df_c
    fig = px.scatter_mapbox(df_c, lat='lat', lon='long', zoom=5, height=600,
                            title='Distribution of road accidents in France')

    # Display the map
    fig.show()




def plot_vehicle_comparison(df_v):
    # Remove special characters
    df_v['catv'] = df_v['catv'].str.replace(r'\D', '', regex=True)

    # Replace empty strings with NaN and convert the column to float
    df_v['catv'] = df_v['catv'].replace('', np.nan).astype(float)

    # Filter the data to keep only cars (07, 10) and motorcycles (02, 30, 31, 32, 33, 34)
    filtered_df_v = df_v[df_v['catv'].isin([7, 10, 2, 30, 31, 32, 33, 34])]

    # Create a temporary column for vehicle categories (car or motorcycle) using assign
    filtered_df_v = filtered_df_v.assign(Vehicle_Type=filtered_df_v['catv'].apply(lambda x: 'Car' if x in [7, 10] else '2 wheeled vehicle'))

    # Count the number of accidents per category
    vehicle_counts = filtered_df_v['Vehicle_Type'].value_counts().reset_index()

    # Rename the columns for better readability
    vehicle_counts.columns = ['Vehicle_Type', 'Count']

    # Create the bar chart
    fig = px.bar(vehicle_counts, x='Vehicle_Type', y='Count', title="Comparison of accidents by vehicle type (Cars vs 2 wheeled vehicles)")

    # Display the chart
    fig.show()




def plot_accidents_with_pedestrians(df_u):
    # Filter out non-numeric values in the 'catu' column
    df_u_filtered = df_u[pd.to_numeric(df_u['catu'], errors='coerce').notna()]

    # Convert the 'catu' column to integer
    df_u_filtered['catu'] = df_u_filtered['catu'].astype(int)

    # Filter the DataFrame to keep only rows with user category 3 (pedestrian)
    df_pedestrians = df_u_filtered[df_u_filtered['catu'] == 3]

    # Count the number of unique rows in the 'Num_Acc' column for accidents with pedestrians
    accidents_with_pedestrians = df_pedestrians['Num_Acc'].nunique()

    # Count the total number of unique rows in the 'Num_Acc' column for all accidents
    total_accidents = df_u_filtered['Num_Acc'].nunique()

    # Calculate the number of accidents without pedestrians
    accidents_without_pedestrians = total_accidents - accidents_with_pedestrians

    # Create a DataFrame containing the categories (with pedestrians, without pedestrians) and the corresponding counts
    data = {'Category': ['With pedestrians', 'Without pedestrians'], 'Count': [accidents_with_pedestrians, accidents_without_pedestrians]}
    accidents_df = pd.DataFrame(data)

    # Create the bar chart with Plotly Express
    fig = px.bar(accidents_df, x='Category', y='Count', title="Comparison of amount of accidents with and without a pedestrian involved")

    # Display the chart
    fig.show()






def plot_accidents_by_severity(df):
    # Convert the 'grav' column to string
    df['grav'] = df['grav'].astype(str)

    # Count the number of accidents by severity
    accidents_by_gravity = df['grav'].value_counts().reset_index()

    # Rename the columns for easier chart creation
    accidents_by_gravity.columns = ['grav', 'count']

    # Create a dictionary to map severity codes to their descriptions
    grav_dict = {
        '1': 'Indemne',
        '2': 'Tué',
        '3': 'Blessé hospitalisé',
        '4': 'Blessé léger'
    }

    # Replace the severity codes with their descriptions
    accidents_by_gravity['grav'] = accidents_by_gravity['grav'].replace(grav_dict)

    # Sort the DataFrame by the number of accidents in ascending order
    accidents_by_gravity = accidents_by_gravity.sort_values('count')

    # Create the bar chart with Plotly Express
    fig = px.bar(accidents_by_gravity, x='grav', y='count', title="Comparison of accident amount by their severity")

    # Display the chart
    fig.show()





def plot_pedestrian_accidents_by_severity(df):
    # Filter the data to keep only accidents involving pedestrians (catu = 3)
    df_u_pedestrians = df[df['catu'] == 3]

    # Count the number of accidents involving pedestrians by severity
    accidents_by_gravity_pedestrians = df_u_pedestrians['grav'].value_counts().reset_index()

    # Rename the columns for easier chart creation
    accidents_by_gravity_pedestrians.columns = ['grav', 'count']

    # Replace the severity codes with their descriptions
    grav_dict = {
        '1': 'Indemne',
        '2': 'Tué',
        '3': 'Blessé hospitalisé',
        '4': 'Blessé léger'
    }
    accidents_by_gravity_pedestrians['grav'] = accidents_by_gravity_pedestrians['grav'].replace(grav_dict)

    # Sort the DataFrame by the number of accidents in ascending order
    accidents_by_gravity_pedestrians = accidents_by_gravity_pedestrians.sort_values('count')

    # Create the bar chart with Plotly Express
    fig = px.bar(accidents_by_gravity_pedestrians, x='grav', y='count', title="Accidents amount by severity where a pedestrian was involved")

    # Display the chart
    fig.show()





def plot_accidents_by_user_category_and_severity(df_u):
    # Create a dictionary for user categories
    catu_dict = {
        1: 'Conducteur',
        2: 'Passager',
        3: 'Piéton'
    }

    # Create a dictionary for severity categories
    grav_dict = {
        1: 'Indemne',
        2: 'Tué',
        3: 'Blessé hospitalisé',
        4: 'Blessé léger'
    }

    # Count the number of accidents by user category and severity
    accidents_by_catu_gravity = df_u.groupby(['catu', 'grav']).size().reset_index()

    # Rename the columns for easier chart creation
    accidents_by_catu_gravity.columns = ['catu', 'grav', 'count']

    # Replace the user category and severity codes with their descriptions
    accidents_by_catu_gravity['catu'] = accidents_by_catu_gravity['catu'].replace(catu_dict)
    accidents_by_catu_gravity['grav'] = accidents_by_catu_gravity['grav'].replace(grav_dict)

    # Create the grouped bar chart with Plotly Express
    fig4 = px.bar(accidents_by_catu_gravity, x='catu', y='count', color='grav', barmode='group',
                  title="Gravité des blessures par catégorie d'usager", text='count')
    
    # Display the chart
    fig4.show()





def plot_maximal_speed_distribution(df):
    # Convert the 'vma' column to numeric
    df['vma'] = pd.to_numeric(df['vma'], errors='coerce')

    # Remove rows with 'vma' equal to -1 or greater than 130
    df_filtered = df[(df['vma'] != -1) & (df['vma'] <= 130)]

    # Sort the filtered DataFrame by 'vma'
    df_sorted = df_filtered.sort_values('vma')

    # Create the box plot
    fig = px.box(df_sorted, y="vma", 
                 title="Distribution of the maximal speed authorized at the accident locations",
                 labels={"MSA": "Maximal speed authorized (in km/h)"})

    # Show the plot
    fig.show()





def plot_accidents_by_age(df, title):
    # Convert the "an_nais" column to integers, ignoring errors
    df["an_nais"] = pd.to_numeric(df["an_nais"], errors='coerce')

    # Remove rows with missing values in the "an_nais" column
    df = df.dropna(subset=['an_nais'])

    # Add a calculated "age" column based on the birth year
    df['age'] = Timestamp.now().year - df['an_nais']

    # Remove rows with non-numeric values in the "an_nais" column
    df = df[df["an_nais"].notna()]

    # Define the age bins
    age_bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]

    # Group ages into bins and count the number of accidents for each bin
    age_groups = pd.cut(df['age'], bins=age_bins)
    accidents_by_age = df.groupby(age_groups)['Num_Acc'].count()

    # Create a bar chart using Plotly Express
    fig = px.bar(x=accidents_by_age.index.astype(str), y=accidents_by_age.values, labels={"x": "Age slice", "y": "Amount of accidents"}, title=title)

    # Add annotations to display values on the bars
    fig.update_traces(texttemplate='%{y}', textposition='outside')

    # Display the chart
    fig.show()





