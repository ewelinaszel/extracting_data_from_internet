import requests
import json
import pandas as pd

def main():
    response = requests.get('https://danepubliczne.imgw.pl/api/data/synop').json()

    capitals = ['Kraków', 'Rzeszów', 'Katowice', 'Opole', 'Kielce', 'Wrocław', 'Warszawa', 'Poznań', 'Gdańsk', 'Toruń', 'Zielona Góra',
                'Olsztyn', 'Łódź', 'Lublin', 'Szczecin', 'Białystok']
    data_for_capitals = [data for data in response if data['stacja'] in capitals]
    df = pd.DataFrame(data_for_capitals)

    with open('meteo_data_for_capitals.json', 'w') as plik:
        json.dump(data_for_capitals, plik, indent=4)

    print(f"Średnia temperatura: {df['temperatura'].astype(float).mean()}")
    print(f"Minimalna temperatura wynosi {df['temperatura'].astype(float).min()} dla miasta {df.loc[df['temperatura'].astype(float).idxmin(), 'stacja']}")
    print(f"Maksymalna temperatura wynosi {df['temperatura'].astype(float).max()} dla miasta {df.loc[df['temperatura'].astype(float).idxmax(), 'stacja']}")
    print(f"Pomiar wykonano: {df['data_pomiaru'].iloc[0]} o godzinie: {df['godzina_pomiaru'].iloc[0]}")

    print(f"Średnia wartość opadów wynosi: {df['suma_opadu'].astype(float).mean()}")
    print(f"Minimalna ilość opadów wynosi {df['suma_opadu'].astype(float).min()} dla miasta {df.loc[df['suma_opadu'].astype(float).idxmin(), 'stacja']}")
    print(f"Maksymalna ilość opadów wynosi {df['suma_opadu'].astype(float).max()} dla miasta {df.loc[df['suma_opadu'].astype(float).idxmax(), 'stacja']}")

    print(f"Średnie ciśnienie wynosi: {df['cisnienie'].astype(float).mean()}")
    print(f"Minimalna wartość ciśnienia wynosi {df['cisnienie'].astype(float).min()} dla miasta {df.loc[df['cisnienie'].astype(float).idxmin(), 'stacja']}")
    print(f"Maksymalna wartość ciśnienia wynosi {df['cisnienie'].astype(float).max()} dla miasta {df.loc[df['cisnienie'].astype(float).idxmax(), 'stacja']}")

if __name__ == "__main__":
    main()