# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 01:01:04 2021

@author: Teletrabajo
"""

import time
import pandas as pd
import numpy as np

name = input("¿Cuál es tu nombre?: ")
print('''
¡Hola {}!

Bienvenido al sistema de información sobre el alquiler de bicicletas.
   
     _\/         _\/         _\/      
  (o) (o)     (o) (o)     (o) (o)    
------------------------------------
'''.format(name.title()))

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    cities=['chicago','new york city','washington']
    months=['january','february','march', 'april','may','june']
    days=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
        
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
            city = input("\n Sobre qué ciudad quieres obtener información. \n Por favor elige sólo una y escríbela de alguna de las siguientes formas: Chicago, New York city, Washington. \n").lower()
            if city not in cities:
                print("¡Ups! Parece que escribiste mal la ciudad. Por favor inténtalo nuevamente.")
                continue
            else:
                break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
            month = input("\n Por favor elige uno de los siguientes meses: january, february, march, april, may, june. \n").lower()
            if month !='all' and month not in months:
                print("¡Ups! Parece que escribiste mal el mes. Por favor inténtalo nuevamente.")
                continue
            else:
                break  

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
            day = input("\n Por favor elige uno de los siguientes días: monday, tuesday, wednesday, thursday, friday, saturday, sunday.\n").lower()
            if day !='all' and day not in days:
                print("¡Ups! Parece que escribiste mal el día. Por favor inténtalo nuevamente.")
                continue
            else:
                break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
#Carga archivo en dataframe
    df = pd.read_csv(CITY_DATA[city])

#Convierte hora inicial a formato datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
#Extrae mes y día de la semana de hora inicial para crear nueva columna
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

#Crea variable "hour" hora
    df['hour'] = df['Start Time'].dt.hour

#Crea el viaje más popular
    df['recorrido'] = df['Start Station'] + ' y '+ df['End Station']
    

#Filtra mes si aplica
    if month != 'all':
        months=['january','february','march', 'april','may','june']
        # use the index of the months list to get the corresponding int
        month = months.index(month)+1 

#Filtra día de la semana si aplica
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculando los momentos de viaje más frecuentes...\n')
    start_time = time.time()

    # TO DO: display the most common month
    mes_popular = df['month'].mode()[0]
    print('\nEl mes número {} del año fue el más popular para realizar recorridos.'.format(mes_popular))

    # TO DO: display the most common day of week
    dia_popular = df['day_of_week'].mode()[0]
    print('\nEl día más popular de la semana para viajar fue: ', dia_popular)

    # TO DO: display the most common start hour
    hora_popular = df['hour'].mode()[0]
    print('\nLas {} horas es el momento más frecuente para viajar.\n'.format(hora_popular))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculando la estación y los recorridos más populares...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    estacion_partida =df['Start Station'].value_counts().sort_values(ascending=False).head(1)
    print('\nLa estación más popular para iniciar los recorridos es ', estacion_partida)
    
    # TO DO: display most commonly used end station
    estacion_final =df['End Station'].value_counts().sort_values(ascending=False).head(1)
    print('\nLa estación más popular para finalizar los recorridos es ', estacion_final)

    # TO DO: display most frequent combination of start station and end station trip
    #viaje=df.groupby(["Start Station", "End Station"]).size().sort_values(ascending=False).head(1)
    viaje = df['recorrido'].mode()[0]
    print('\nEl trayecto más frecuente para los recorriedo comprende las estaciones ', viaje)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculando la duración de viaje...\n')
    start_time = time.time()

    # TO DO: display total travel time
    tiempo_viaje=df['Trip Duration'].sum()
    print('\nEl tiempo total de recorridos es de {} horas que equivalen a {} días.\n'.format(round((tiempo_viaje/3600), 1), round((tiempo_viaje/86400), 1)))

    # TO DO: display mean travel time
    prom_tiempo_viaje=df['Trip Duration'].mean()
    print('\nEl tiempo promedio de recorrido por viaje es de {} minutos.\n'.format(round((prom_tiempo_viaje/60), 1)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculando estadísticas...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    tipo_usuario=df['User Type'].value_counts()
    print('Los tipos de usuarios que utilizan las bicicletas son:\n', tipo_usuario)

    # TO DO: Display counts of gender
    try:
          genero=df['Gender'].value_counts()
          print('\nLos siguientes son los géneros que utilizan las bicicletas:\n', genero)
    except KeyError:
          print('\n¡Ups! No tenemos información relacionada para tu consulta.')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        anio_antiguo=df['Birth Year'].min()
        print('\nLa persona más longeva en utilizar las bicicletas nació en el año ', round(anio_antiguo, 0))
    except KeyError:
        print('\n¡Ups! No tenemos información relacionada para tu consulta.')
    
    try:
        anio_reciente=df['Birth Year'].max()
        print('\nLa persona más joven en utilizar las bicicletas nació en el año ', round(anio_reciente, 0))
    except KeyError:
        print('\n¡Ups! No tenemos información relacionada para tu consulta.')

    try:
        anio_moda=df['Birth Year'].value_counts().sort_values(ascending=False).head(1)
        print('\nEl año más común de nacimiento de las personas que utilizan las bicicletas es ', round(anio_moda, 0))
    except KeyError:
        print('\n¡Ups! No tenemos información relacionada para tu consulta.')
      
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        adicional=input('\n¿Te gustaría ver las primeras cinco filas de la base de datos? Por favor responde sí o no a continuación: ').lower()
        cinco=0
        respuesta=True
        
        while (respuesta):
            print(df.iloc[cinco:cinco+5])
            cinco+=5
            adicional = input("\n¿Te gustaría ver las siguientes cinco líneas de la base de datos? Por favor responde sí o no a continuación: ").lower()
            if adicional == "no":
                respuesta=False
        
            
        reinicio = input('\n¿Deseas reiniciar el programa y realizar otra consulta? Por favor responde sí o no. Si eliges otra opción no se reiniciará el programa.\n').lower()
        if reinicio.lower() != 'sí':
            break


if __name__ == "__main__":
	main()
