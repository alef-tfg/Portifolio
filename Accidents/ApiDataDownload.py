import requests
import geopandas as gpd



def fetch_all_data(base_url, chunk_size=2000):
    all_features = []
    offset = 0

    while True:
        params = {
            'where': '1=1',
            'outFields': '*',
            'f': 'geojson',
            'resultOffset': offset,
            'resultRecordCount': chunk_size
        }

        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'features' not in data or not data['features']:
            break

        all_features.extend(data['features'])
        offset += chunk_size

    return {
        "type": "FeatureCollection",
        "features": all_features
    }

# Base URL for the FeatureServer
base_url = "https://pamgia.ibama.gov.br/server/rest/services/01_Publicacoes_Bases/tra_trecho_rodoviario_principal_l/FeatureServer/23/query"

# Fetch all data
geojson_data = fetch_all_data(base_url)

cols_to_keep = ['codigo_br', 'unidade_fe', 'quilometra', 
                'quilometr0', 'extensao', 'superficie', 'obra', 
                'unidade_lo','Shape__Length', 'geometry']

gdf = gpd.GeoDataFrame.from_features(geojson_data['features'])[cols_to_keep]
gdf.to_parquet('data/roads.parquet')
