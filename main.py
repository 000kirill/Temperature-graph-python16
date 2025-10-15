import requests
import pandas as pd
from matplotlib import pyplot as plt


def get_coordinates(city_name, country_code):
    limit = 20
    url = "https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-postal-code@public/records"
    payload = {
    "limit": limit,
    "where": {f'place_name: "{city_name}" and country_code: "{country_code}"'},
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    total_count = response.json()['total_count']
    if total_count == 0:
        print('Город не найден!')
        exit()
    results = response.json()["results"][0]
    return results['latitude'], results['longitude']


def get_temp_statistics(latitude, longitude, start_date, end_date):
    url = "https://archive-api.open-meteo.com/v1/era5"
    payload = {
        "latitude" : latitude,
        "longitude" : longitude,
        "start_date" : start_date,
        "end_date" : end_date,
        "hourly": "temperature_2m"
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    temperature_value = response.json()['hourly']['temperature_2m']
    tempеrature_date = response.json()['hourly']['time']
    df = pd.DataFrame(list(zip(tempеrature_date, temperature_value)), columns=['date', 'temp'])
    return df


def get_graph(df):
    df.plot(x='date', y='temp', kind='line')
    plt.xlabel('Дата')
    plt.ylabel('Температура (°C)')
    plt.show()


def main():
    city_name = "Minsk"
    country_code = "BY"
    start_date = '2025-10-01'
    end_date = '2025-10-06'
    latitude, longitude = get_coordinates(city_name, country_code)
    df = get_temp_statistics(latitude, longitude, start_date, end_date)
    get_graph(df)


if __name__ == "__main__":
    main()