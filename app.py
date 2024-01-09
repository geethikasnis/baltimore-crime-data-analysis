import matplotlib.pyplot as plt
import seaborn as sns

import database
import pandas as pd
import charts


MENU_PROMPT = """ -- BALTIMORE CITY CRIME ANALYSIS --

Please choose one one of these options

1) See all crimeID
2) Total number of crimes by each type
3) Number of crimes by location 
4) More details of crimes in the highest reported place 
5) Crimes by Year at 1500 RUSSELL ST 
6) Crimes by Race 
7) Crimes by Age and Location
8) Exit

Your selection : """



def menu():
    print(MENU_PROMPT)
    conn =  database.create_connection("normalized.db")

    while (user_input := input(MENU_PROMPT)) != "8":
        if user_input == "1":
            crimecode_data = database.get_all_crimecode_data()
            charts.crimecode_data_bar(crimecode_data)
            plt.show()

        elif user_input == "2":
            count_of_crimes_by_type = database.get_crimetype_count()
            charts.types_of_crimes_count(count_of_crimes_by_type)
            plt.show()
        
        elif user_input == "3":
            charts.crimes_by_location_graph()
            plt.show()

        elif user_input == "4":
            more_details_crime_loc = database.get_more_details_crime()
            charts.more_details_by_loc_graph(more_details_crime_loc)
            plt.show()

        elif user_input == "5":
            inside_outside = database.find_crime_by_location()
            charts.inside_outside_scatterplot(inside_outside)
            plt.show()

        elif user_input == "6":
            least_crime_race_data = database.get_least_crime_committing_race()
            charts.least_crime_committing_bar(least_crime_race_data)
            plt.show()
        
        elif user_input == "7":
            male_female_age = database.group_criminals_by_their_age()
            charts.male_female_heatmap(male_female_age)
            plt.show()
            
        else :
            print("Invalid input, please try again")

menu()




