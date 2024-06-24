import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from dotenv import load_dotenv

# Ejecutar sortLog.py primero
subprocess.run(['python', 'sortLog.py'], check=True)

# Especificar la ruta completa del archivo de log ordenado
log_file = 'logCentralizado_ordenado.log'

with open(log_file, 'r') as file:
    log_contents = file.readlines()

# Inicializar un diccionario para contar jugadores por equipo
teams = {}
teams_4 = {}
teams_5 = {}
data = []

for line in log_contents:
        parts = line.strip().split(', ')
        timestamp = datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S')
        event_type = parts[1]
        juego = parts[2]
        action = parts[3]
        args = parts[4:]
        data.append([timestamp, event_type, juego, action] + args)

columns = ['timestamp', 'event_type', 'juego', 'action', 'arg1', 'arg2', 'arg3']
df = pd.DataFrame(data, columns=columns)

# Filtrar las acciones iniciadas
df_ini = df[df['event_type'] == 'ini']

# Gráfico 1: Jugadores creados por equipo en un juego
created_players = df_ini[df_ini['action'] == 'crea-jugador'].groupby('arg1').size()
created_players.plot(kind='bar', title='Jugadores creados por equipo')
plt.xlabel('Equipo')
plt.ylabel('Número de jugadores')
print("Imprime Grafico 1")
plt.show()

# Gráfico 2: Jugadas realizadas por jugador en un juego
player_actions = df_ini[df_ini['action'].str.contains('lanza-dado')].groupby('arg2').size()
player_actions.plot(kind='bar', title='Jugadas realizadas por jugador')
plt.xlabel('Jugador')
plt.ylabel('Número de jugadas')
print("Imprime Grafico 2")
plt.show()







# Procesar el archivo de registro
for line in log_contents:
    parts = line.strip().split(', ')
    if len(parts) == 6 and parts[3] == 'crea-equipo' and parts[1]=='ini':
        timestamp, status, game, event, team, player = parts
        if team not in teams:
            teams[team] = {"Fecha": [], "valor": []}
            teams_4[team] = {"Fecha": [], "team": []}
            teams_5[team] = {"Fecha": [], "team": []}
        teams_4[team]["Fecha"].append(timestamp)
        teams_4[team]["team"].append(team)
    if len(parts) == 7 and parts[3] == 'lanza-dado':
        timestamp, status, game, event, team, player, number = parts
        numero = int(number)
        teams[team]["Fecha"].append(timestamp)
        teams[team]["valor"].append(numero)
    if len(parts) == 6 and parts[3] == 'crea-jugador' and parts[1]=='fin':
        timestamp, status, game, event, team, player = parts
        teams_5[team]["Fecha"].append(timestamp)
        teams_5[team]["team"].append(team)


print(".---------------------------------.")
print(teams_4)
print(".---------------------------------.")

# Crear DataFrame para todos los equipos
df_list = []
for team, data in teams.items():
    df = pd.DataFrame(data)
    df['Equipo'] = team
    df_list.append(df)

df = pd.concat(df_list)

# Convertir 'Fecha' a datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Calcular puntaje acumulado por equipo
df['Puntaje_Acumulado'] = df.groupby('Equipo')['valor'].cumsum()

# Crear gráfico de dispersión con líneas de tendencia
plt.figure(figsize=(10, 6))

for equipo in df['Equipo'].unique():
    equipo_data = df[df['Equipo'] == equipo]
    plt.scatter(equipo_data['Fecha'], equipo_data['Puntaje_Acumulado'], label=equipo, marker='o' if equipo == 'Team A' else 'x')

    # Calcular y graficar línea de tendencia cuadrática
    # Centrar y escalar valores de fecha para mejorar la condición de la regresión polinómica
    x = (equipo_data['Fecha'].astype('int64') // 10**9).values
    x_scaled = x - x.mean()  # Centramos los valores de fecha
    y = equipo_data['Puntaje_Acumulado'].values
    z = np.polyfit(x_scaled, y, 2)
    p = np.poly1d(z)
    # Generar valores de fecha para la curva
    x_vals = np.linspace(x_scaled.min(), x_scaled.max(), 500)
    plt.plot(pd.to_datetime((x_vals + x.mean()) * 10**9), p(x_vals), linestyle='dashed', color='gray')

# Establecer límites del eje X (tiempo)
load_dotenv()
min_env = os.getenv('3_TIME_START')
max_env = os.getenv('3_TIME_END')
print(min_env)
print(max_env)
min_time = datetime.strptime(min_env, '%Y-%m-%d %H:%M:%S')  # Tiempo mínimo en los datos
max_time = datetime.strptime(max_env, '%Y-%m-%d %H:%M:%S')  # Tiempo máximo en los datos

plt.xlim(min_time, max_time)  # Establecer los límites del eje X

# Ajustar los límites del eje Y (opcional)
plt.ylim(0, df['Puntaje_Acumulado'].max() * 1.1)  # Ampliar un poco el rango del eje Y

# Personalizar el gráfico
plt.xlabel('Fecha y Hora')
plt.ylabel('Puntaje Acumulado')
plt.title('Puntajes Acumulados y Tendencias por Equipo')
plt.legend()
plt.grid(axis='y')
plt.xticks(rotation=45)

# Mostrar el gráfico
plt.show()



def plot_team_creation_over_time(teams_4):
    # Crear una lista para almacenar los datos
    data = []

    for team, team_data in teams_4.items():
        for i in range(len(team_data['Fecha'])):
            data.append((team_data['Fecha'][i], team))

    # Convertir la lista en un DataFrame
    df_creation = pd.DataFrame(data, columns=['Fecha', 'Equipo'])
    
    # Convertir 'Fecha' a datetime
    df_creation['Fecha'] = pd.to_datetime(df_creation['Fecha'])

    # Crear gráfico
    plt.figure(figsize=(10, 6))

    # Iterar sobre cada equipo para graficar la cantidad de equipos creados en relación con las fechas
    for equipo in df_creation['Equipo'].unique():
        equipo_data = df_creation[df_creation['Equipo'] == equipo]
        equipo_data = equipo_data.sort_values('Fecha')
        equipo_data['Cantidad_Equipos'] = range(1, len(equipo_data) + 1)
        
        plt.plot(equipo_data['Fecha'], equipo_data['Cantidad_Equipos'], marker='o', linestyle='-', label=equipo)
    
    min_env = os.getenv('4_TIME_START')
    max_env = os.getenv('4_TIME_END')
    print(min_env)
    print(max_env)
    min_time = datetime.strptime(min_env, '%Y-%m-%d %H:%M:%S')  # Tiempo mínimo en los datos
    max_time = datetime.strptime(max_env, '%Y-%m-%d %H:%M:%S')  # Tiempo máximo en los datos
    plt.xlim(min_time, max_time)  # Establecer los límites del eje X
    # Personalizar el gráfico
    plt.xlabel('Fecha y Hora')
    plt.ylabel('Cantidad de Equipos')
    plt.title('Cantidad de Equipos Creados en Relación a la Fecha por Equipo')
    plt.legend()
    plt.grid(axis='y')
    plt.xticks(rotation=45)
    
    # Mostrar el gráfico
    plt.show()


def plot_player_creation_over_time(teams_4):
    # Crear una lista para almacenar los datos
    data = []

    for team, team_data in teams_4.items():
        for i in range(len(team_data['Fecha'])):
            data.append((team_data['Fecha'][i], team))

    # Convertir la lista en un DataFrame
    df_creation = pd.DataFrame(data, columns=['Fecha', 'Equipo'])
    
    # Convertir 'Fecha' a datetime
    df_creation['Fecha'] = pd.to_datetime(df_creation['Fecha'])

    # Crear gráfico
    plt.figure(figsize=(10, 6))

    # Iterar sobre cada equipo para graficar la cantidad de equipos creados en relación con las fechas
    for equipo in df_creation['Equipo'].unique():
        equipo_data = df_creation[df_creation['Equipo'] == equipo]
        equipo_data = equipo_data.sort_values('Fecha')
        equipo_data['Cantidad_Equipos'] = range(1, len(equipo_data) + 1)
        
        plt.plot(equipo_data['Fecha'], equipo_data['Cantidad_Equipos'], marker='o', linestyle='-', label=equipo)

    min_env = os.getenv('5_TIME_START')
    max_env = os.getenv('5_TIME_END')
    print(min_env)
    print(max_env)
    min_time = datetime.strptime(min_env, '%Y-%m-%d %H:%M:%S')  # Tiempo mínimo en los datos
    max_time = datetime.strptime(max_env, '%Y-%m-%d %H:%M:%S')  # Tiempo máximo en los datos

    plt.xlim(min_time, max_time)  # Establecer los límites del eje X
    
    # Personalizar el gráfico
    plt.xlabel('Fecha y Hora')
    plt.ylabel('Cantidad de Equipos')
    plt.title('Cantidad de Jugadores Creados en Relación a la Fecha por Equipo')
    plt.legend()
    plt.grid(axis='y')
    plt.xticks(rotation=45)
    
    # Mostrar el gráfico
    plt.show()

# Llamar a la función para graficar
plot_team_creation_over_time(teams_4)
plot_player_creation_over_time(teams_5)