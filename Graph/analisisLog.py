import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
# Ejecutar sortLog.py primero
subprocess.run(['python', 'sortLog.py'], check=True)

# Configurar variables de entorno para el tamaño de la ventana
WINDOW_SIZE = int(os.getenv('WINDOW_SIZE', '10'))  # Tamaño de la ventana en minutos

# Especificar la ruta completa del archivo de log ordenado
log_file = 'logCentralizado_ordenado.log'

with open(log_file, 'r') as file:
    log_contents = file.readlines()

# Inicializar un diccionario para contar jugadores por equipo
teams = {"Team A": {"Fecha":[],"valor":[]}, "Team B": {"Fecha":[],"valor":[]}}

# Procesar el archivo de registro
for line in log_contents:
    parts = line.strip().split(', ')
    if len(parts) == 7 and parts[3] == 'lanza-dado':
        timestamp, status, game, event, team, player, number = parts
        numero = int(number)
        print(numero)
        print("Numbers Type: ",type(numero))
        teams[team]["Fecha"].append(timestamp)
        teams[team]["valor"].append(numero)
print(teams)
print(teams["Team A"]["Fecha"][0])
print(teams["Team A"]["valor"][0])

# Crear DataFrames para cada equipo
df_a = pd.DataFrame(teams['Team A'])
df_b = pd.DataFrame(teams['Team B'])

# Añadir columna 'Equipo'
df_a['Equipo'] = 'Team A'
df_b['Equipo'] = 'Team B'

# Concatenar DataFrames
df = pd.concat([df_a, df_b])

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
    z = np.polyfit(equipo_data['Fecha'].astype('int64') // 10**9, equipo_data['Puntaje_Acumulado'], 2)
    p = np.poly1d(z)
    plt.plot(equipo_data['Fecha'], p(equipo_data['Fecha'].astype('int64') // 10**9), linestyle='dashed', color='gray')



# Establecer límites del eje X (tiempo)
print(df['Fecha'].min())
print(df['Fecha'].max())
min_time = datetime.strptime('2024-06-23 05:01:07', '%Y-%m-%d %H:%M:%S')  # Tiempo mínimo en los datos
max_time = datetime.strptime('2024-06-23 05:13:07', '%Y-%m-%d %H:%M:%S')  # Tiempo máximo en los datos

# Puedes ajustar estos valores para ampliar o reducir el rango de tiempo mostrado
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
"""  Contar el número de jugadores únicos por equipo
team_a_count = len(teams["Team A"])
team_b_count = len(teams["Team B"])

# Crear el gráfico de barras
plt.bar(['Team A', 'Team B'], [team_a_count, team_b_count], color=['blue', 'red'])
plt.xlabel('Equipos')
plt.ylabel('Número de Jugadores Creados')
plt.title('Número de Jugadores Creados por Equipo')
plt.show() """