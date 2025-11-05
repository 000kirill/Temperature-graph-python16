import requests
import pandas as pd
from matplotlib import pyplot as plt
import argparse


def get_coordinates(args):
    limit = 20
    url = "https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-postal-code@public/records"
    payload = {
        "limit": limit,
        "where": {
            f'place_name: "{args.city_name}"'
            f'and country_code: "{args.country_code}"'
        }
    }

    response = requests.get(url, params=payload)
    response.raise_for_status()
    total_count = response.json()['total_count']
    if total_count == 0:
        print('Город не найден!')
        exit()
    results = response.json()["results"][0]
    return results['latitude'], results['longitude']


def get_temp_statistics(latitude, longitude, args):
    url = "https://archive-api.open-meteo.com/v1/era5"
    payload = {
        "latitude" : latitude,
        "longitude" : longitude,
        "start_date" : args.start_date,
        "end_date" : args.end_date,
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
    parser = argparse.ArgumentParser()
    parser.add_argument('city_name', help='Название города (например: Minsk)', default='Minsk')
    parser.add_argument('country_code', help='Код страны (например: BY)', default='BY')
    parser.add_argument('start_date', help='Дата начала в формате YYYY-MM-DD', default='2025-10-01')
    parser.add_argument('end_date', help='Дата окончания в формате YYYY-MM-DD', default='2025-10-06')
    args = parser.parse_args()
    
    latitude, longitude = get_coordinates(args)
    df = get_temp_statistics(latitude, longitude, args)
    get_graph(df)


if __name__ == "__main__":
    main()