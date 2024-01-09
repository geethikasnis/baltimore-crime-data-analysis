import pandas as pd
import re
import sqlite3
from sqlite3 import Error
import matplotlib.pyplot as plt

def create_connection(db_file, delete_db=False):
    import os
    if delete_db and os.path.exists(db_file):
        os.remove(db_file)

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = 1")
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql, drop_table_name=None):
    
    if drop_table_name: # You can optionally pass drop_table_name to drop the table. 
        try:
            c = conn.cursor()
            c.execute("""DROP TABLE IF EXISTS %s""" % (drop_table_name))
        except Error as e:
            print(e)
    
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        
def execute_sql_statement(sql_statement, conn):
    cur = conn.cursor()
    cur.execute(sql_statement)

    rows = cur.fetchall()

    return rows

def read_values():

    f = open('Crime_Data.csv', 'r')
    data = f.read()
    lines = data.split("\n")

    #Removing the header values
    del lines[0]

    data_values = []

    for line in lines:
        if not line.strip():
            continue
        values_between_quotes = re.findall(r'"(.*?)"', line)
        for val in values_between_quotes:
            rval = val.replace(',', '~')
            line = line.replace(f'\"{val}\"', rval)
        line = line.split(',')
        data_values.append(line)
        
    return data_values

def create_crime_code_table():

    data_values = read_values()

    conn_normalized = create_connection('normal.db')

    create_crime_code_table = """create table crimecode(CrimeCodeID integer not null primary key autoincrement,
                                                        CrimeCode text not null,
                                                        Description text not null)"""

    insert_crime_code_query = 'insert into crimecode(CrimeCode, Description) values(?, ?)'

    create_table(conn_normalized, create_crime_code_table, drop_table_name= 'crimecode')

    crime_code_dict = {}
    for i in range(len(data_values)):
        crime_code = data_values[i][4]
        description = data_values[i][6]
        crime_code_dict[crime_code] = description

    for key,value in crime_code_dict.items():
        conn_normalized.execute(insert_crime_code_query, (key, value, ))
    
    conn_normalized.commit()
    
#create_crime_code_table()  
    
    

def create_crime_code_dict():

    conn_normalized = create_connection('normal.db')

    select_crime_code_query = 'select CrimeCode, CrimeCodeID from crimecode;'

    crime_code_values = execute_sql_statement(select_crime_code_query, conn_normalized)

    return dict(crime_code_values)

#create_crime_code_dict()

def create_location_table():

    data_values = read_values()

    conn_normalized = create_connection('normal.db')

    create_location_table = """create table location(LocationID integer not null primary key autoincrement,
                                                    Location text not null,
                                                    District text,
                                                    Neighborhood text);"""

    insert_location_query = 'insert into location(Location, District, Neighborhood) values(?, ?, ?)'

    loc_values = {}
    for i in range(len(data_values)):
        location = data_values[i][5]
        district = data_values[i][14]
        neighborhood = data_values[i][15]
        loc_values[location] = ([district, neighborhood])

    create_table(conn_normalized, create_location_table, drop_table_name= 'location')

    for key,value in loc_values.items():
        conn_normalized.execute(insert_location_query, (key, value[0], value[1], ))
    
    conn_normalized.commit()
    
#create_location_table()

def create_location_dict():

    conn_normalized = create_connection('normal.db')

    select_location_query = 'select Location, LocationID from location;'

    location_values = execute_sql_statement(select_location_query, conn_normalized)

    return dict(location_values)

#create_location_dict()

def create_race_table():

    data_values = read_values()

    conn_normalized = create_connection('normal.db')

    create_race_table = """create table race(RaceID integer not null primary key autoincrement,
                                                    Race text not null,
                                                    Ethnicity text);"""

    insert_race_query = 'insert into race(Race, Ethnicity) values(?, ?)'

    eth_race_dict = {}

    for i in range(len(data_values)):
        race = data_values[i][12]
        ethnicity = data_values[i][13]
        if(race == ''):
            eth_race_dict['UNKNOWN_RACE'] = ethnicity
        else:
            eth_race_dict[race] = ethnicity

    create_table(conn_normalized, create_race_table, drop_table_name= 'race')

    for key,value in eth_race_dict.items():
        conn_normalized.execute(insert_race_query, (key, value, ))
    
    conn_normalized.commit()
    
    conn_normalized.commit()

#create_race_table()

def create_race_dict():

    conn_normalized = create_connection('normal.db')

    select_race_query = 'select Race, RaceID from race;'

    race_values = execute_sql_statement(select_race_query, conn_normalized)

    return dict(race_values)

#create_race_dict()


def create_criminal_table():

    data_values = read_values()

    conn_normalized = create_connection('normal.db')

    race_values = create_race_dict()

    create_criminal_table = """create table criminal(CriminalID integer not null primary key autoincrement,
                                                Gender text,
                                                Age text,
                                                RaceID text,
                                                foreign key(RaceID) references race(RaceID));"""

    insert_criminal_query = 'insert into criminal(Gender, Age, RaceID) values(?, ?, ?)'

    create_table(conn_normalized, create_criminal_table, drop_table_name= 'criminal')

    criminal_data = []
    for i in range(len(data_values)):
        gender = data_values[i][10]
        age = data_values[i][11]
        race = data_values[i][12]
        if(race == ''):
            race = 'UNKNOWN_RACE'
        race_id = race_values[race]
        criminal_data.append([gender, age, race_id])

    criminal_data = [tuple(criminal) for criminal in criminal_data]

    with conn_normalized:
        cur = conn_normalized.cursor()
        cur.executemany(insert_criminal_query, criminal_data)
        
#create_criminal_table()
    

def create_criminal_dict():

    conn_normalized = create_connection('normal.db')

    select_criminal_query = 'select Gender, CriminalID from criminal;'

    criminal_values = execute_sql_statement(select_criminal_query, conn_normalized)

    return dict(criminal_values)

#create_criminal_dict()

def create_crime_table():

    data_values = read_values()

    crime_code_values = create_crime_code_dict()

    location_values = create_location_dict()

    criminal_values = create_criminal_dict()

    conn_normalized = create_connection('normal.db')

    create_crime_table = """create table crime(CrimeID integer not null primary key autoincrement, 
                                                CrimeDateTime text not null, 
                                                Inside_Outside text, 
                                                Weapon text,
                                                CrimeCodeID integer not null,
                                                LocationID integer not null,
                                                CriminalID integer not null,
                                                foreign key(CrimeCodeID) references crimecode(CrimeCodeID),
                                                foreign key(LocationID) references location(LocationID),
                                                foreign key(CriminalID) references criminal(CriminalID));"""

    insert_crime_query = 'insert into crime values(null, ?, ?, ?, ?, ?, ?)'

    create_table(conn_normalized, create_crime_table, drop_table_name= 'crime')

    crime_data = []
    for i in range(len(data_values)):
        crime_date_time = data_values[i][3]
        crime_code = data_values[i][4]
        inside_outside = data_values[i][7]
        weapon = data_values[i][8]
        location = data_values[i][5]
        gender = data_values[i][10]
        crime_code_id = crime_code_values[crime_code]
        location_id = location_values[location]
        criminal_id = criminal_values[gender]
        crime_data.append([crime_date_time, inside_outside, weapon, crime_code_id, location_id, criminal_id])

    crime_data = [tuple(crime) for crime in crime_data]

    crime_data = sorted(crime_data, key = lambda c:c[0])

    with conn_normalized:
        cur = conn_normalized.cursor()
        cur.executemany(insert_crime_query, crime_data)


#create_crime_table()

def get_all_crimecode_data():
    conn = sqlite3.connect('normal.db')
    sql = 'select Description, group_concat(CrimeCode) AS codes from crimecode group by Description ORDER BY codes'
    query = pd.read_sql_query(sql, conn)
    df = pd.DataFrame(query)
    return df
    

def get_least_crime_committing_race():
    conn = sqlite3.connect('normal.db')
    sql = """select t.Race, count(*) As number_of_crimes From Race as t
             JOIN criminal as ti
             ON t.RaceID = ti.RaceID
             GROUP BY ti.RaceID
             ORDER BY number_of_crimes limit 3"""
    query = pd.read_sql_query(sql, conn)
    df = pd.DataFrame(query)
    return df

#get_least_crime_committing_race()

def get_crimetype_count():
    conn = sqlite3.connect('normal.db')
    sql =  """SELECT crimecode.Description, count(crimecode.Description) as 'CountOfCrimes'
             FROM crimecode
             INNER JOIN crime
             ON crimecode.CrimeCodeID = crime.CrimeCodeID
             GROUP BY crimecode.Description"""
    query = pd.read_sql_query(sql, conn)
    df =  pd.DataFrame(query)
    #print (df)
    return df

#get_crimetype_count()

def get_crimes_by_location():
    conn = sqlite3.connect('normal.db')
    #top 20 most locations with highest crime rate
    sql_statement = """select location.Location, count(crimecode.Description) as crimes
    from crimecode Join crime on crimecode.CrimeCodeID = crime.CrimeCodeID
    JOIN location ON location.LocationID = crime.LocationID
    where location.Location != ''
    group by location.Location HAVING count(crimecode.Description) >= 512
    ORDER BY crimes DESC"""
    df = pd.read_sql_query(sql_statement, conn)
    #print(df)
    return df

def get_crimes_by_districts():
    conn = sqlite3.connect('normal.db')
    sql = """ select location.District, count(crimecode.Description) as crimes_by_district
              from crimecode Join crime on crimecode.CrimeCodeID = crime.CrimeCodeID
              JOIN location ON location.LocationID = crime.LocationID
              group by location.District HAVING count(crimecode.Description) >= 0
              ORDER BY crimes_by_district DESC """

    query = pd.read_sql_query(sql, conn)
    df = pd.DataFrame(query)
   # print(df)
    return df


def get_more_details_crime():
    conn = sqlite3.connect('normal.db')
    sql = """ select location.Location, crimecode.Description, sum(case when crimecode.Description > 0 Then 1 else 0 end ) as times
              from crimecode Join crime on crimecode.CrimeCodeID = crime.CrimeCodeID
              JOIN location ON location.LocationID = crime.LocationID
              where location.Location = '1500 RUSSELL ST'
              group by crimecode.Description, location.Location
              ORDER BY times DESC """
    query = pd.read_sql_query(sql, conn)
    df = pd.DataFrame(query)
   # print(df)
    return df

def group_criminals_by_their_age():

    conn_norm = sqlite3.connect('normal.db')
    sql_statement = """select criminal.gender, 
                            crimecode.description, location.location,
                            criminal.age,
                            count(criminal.age) as "Criminals_Age"
                            from criminal
                            inner join crime
                            on criminal.criminalid = crime.CriminalID
                            inner join crimecode
                            on crimecode.crimecodeid = crime.CrimeCodeID
                            inner join location
                            on location.locationid = crime.locationid
                            group by crimecode.description
                            order by Criminals_Age desc
                    """

    df_criminals_by_age = pd.read_sql_query(sql_statement, conn_norm)
    df_criminals_by_age['Age'] = df_criminals_by_age['Age'].replace('', 0)
    df_criminals_by_age['Age'] = df_criminals_by_age['Age'].astype(int)
    df_criminals_by_age['Gender'] = df_criminals_by_age['Gender'].replace('M', 'Male')
    df_criminals_by_age['Gender'] = df_criminals_by_age['Gender'].replace('F', 'Female')
    df_criminals_by_age['Gender'] = df_criminals_by_age['Gender'].replace('', None)
    
    return df_criminals_by_age

def find_crime_by_location():
    
    conn_norm = sqlite3.connect('normal.db')

    sql_statement = """select crimecode.description, criminal.age,
                            substr(crime.crimedatetime,0, 5) as 'YearOfCrime', 
                            crime.inside_outside, crime.weapon
                            from crime 
                            inner join location
                            on location.LocationID = crime.LocationID
                            inner join crimecode
                            on crimecode.CrimeCodeID = crime.CrimeCodeID
                            inner join criminal
                            on criminal.CriminalID = crime.CriminalID
                            where location = '2900 E MADISON ST'
                            order by crimecode.description"""

    df_crime_by_loc = pd.read_sql_query(sql_statement, conn_norm)

    df_crime_by_loc = df_crime_by_loc.replace('I', 'Inside')
    df_crime_by_loc = df_crime_by_loc.replace('O', 'Outside')
    df_crime_by_loc['Inside_Outside'] = df_crime_by_loc['Inside_Outside'].replace('', None)
    df_crime_by_loc['Age'] = df_crime_by_loc['Age'].replace('', 0)
    df_crime_by_loc['Age'] = df_crime_by_loc['Age'].astype(int)
    df_crime_by_loc['YearOfCrime'] = df_crime_by_loc['YearOfCrime'].astype(int)

    return df_crime_by_loc