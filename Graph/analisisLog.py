import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Configurar variables de entorno para el tamaño de la ventana
WINDOW_SIZE = int(os.getenv('WINDOW_SIZE', '1'))  # Tamaño de la ventana en minutos

# Leer el archivo de log
log_file = '../RMI/logCentralizado.log'
data = []

with open(log_file, 'r') as file:
    for line in file:
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
plt.show()

# Gráfico 2: Jugadas realizadas por jugador en un juego
player_actions = df_ini[df_ini['action'].str.contains('lanza-dado')].groupby('arg2').size()
player_actions.plot(kind='bar', title='Jugadas realizadas por jugador')
plt.xlabel('Jugador')
plt.ylabel('Número de jugadas')
plt.show()

"""# Gráfico 3: Curvas de puntuación por equipo a través del tiempo
scores_ini = df[df['event_type'] == 'ini']
scores_fin = df[df['event_type'] == 'fin']

# Asegurarnos de que estamos comparando eventos de inicio y fin correctamente
scores_ini = scores_ini[scores_ini['action'] == 'lanza-dado']
scores_fin = scores_fin[scores_fin['action'] == 'lanza-dado']
scores = pd.merge(scores_ini, scores_fin, on=['timestamp', 'juego', 'action', 'arg1', 'arg2'], suffixes=('_ini', '_fin'))
scores['puntos'] = pd.to_numeric(scores['arg3_fin'], errors='coerce')

teams = scores['arg1'].unique()
for team in teams:
    team_scores = scores[scores['arg1'] == team].set_index('timestamp')['puntos'].resample(f'{WINDOW_SIZE}T').sum()
    team_scores.plot(title=f'Curvas de puntuación del equipo {team} a través del tiempo')

plt.xlabel('Tiempo')
plt.ylabel('Puntuación')
plt.show()

# Gráfico 4: Equipos creados por ventanas de tiempo
teams_created = df_ini[df_ini['action'] == 'crea-jugador'].set_index('timestamp')['arg1'].resample(f'{WINDOW_SIZE}T').nunique()
teams_created.plot(title='Equipos creados por ventanas de tiempo')
plt.xlabel('Tiempo')
plt.ylabel('Número de equipos')
plt.show()

# Gráfico 5: Jugadores creados por ventanas de tiempo
players_created = df_ini[df_ini['action'] == 'crea-jugador'].set_index('timestamp')['arg2'].resample(f'{WINDOW_SIZE}T').nunique()
players_created.plot(title='Jugadores creados por ventanas de tiempo')
plt.xlabel('Tiempo')
plt.ylabel('Número de jugadores')
plt.show()
"""