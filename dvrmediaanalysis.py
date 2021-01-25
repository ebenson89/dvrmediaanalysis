''' Analyze movies, etc., recorded on DVRs '''

import json
from datetime import datetime
import pandas as pd
from pandas import DataFrame, Series

media_file_name = "recordings.json"

def get_media(json_file_name):
    #Open json file
    with open(media_file_name) as media_file:
        #Returns json obj as a dictionary
        return json.load(media_file)

def remove_list (media_dict):
    #Flatten each dictionary entry by replacing the list with the value that was in the list
    simple_dict = {}
    #Run though raw dict
    for movie in media_dict:
        #Add new dict entry to simple_dict
        simple_dict.update({movie:media_dict[movie][0]})
    return (simple_dict)

def show_length (time_string):
    #Round the times in the runtime to the nearest half hour
    minutes = int(time_string[2:4])
    hours = int(time_string[:1])
    
    #round to .0 if under 15
    if minutes < 15:
        rounded_time = time_string[:1] + ".0"
    #round to .5 if 15 to 44
    elif minutes < 45:
        rounded_time = time_string[:1] + ".5"
    #round up to the next hour if 45 or greater
    else:
        rounded_time = str(hours + 1) + ".0"

    return (float(rounded_time))

def cleanup_time(media_dict):
    ''' Convert all EncodeTime to a valid datetime object and round the runtimes to nearest half hour'''
    datetime_updated_dict = {}
    #Run through dict
    for movie in media_dict:
        if "EncodeTime" in media_dict[movie]: #Also removes invalid entries
            #copy the movie data dict
            movie_data_dict = media_dict[movie]

            #copy encode time string and update it to datetime obj with timezone
            datetime_encodetime = datetime.strptime(movie_data_dict["EncodeTime"],"%Y:%m:%d %H:%M:%S%z").astimezone()
            #Call show_length to round the runtimes
            simple_runtime = show_length(movie_data_dict["MediaOriginalRunTime"])

            #put the updated time back into the copy of the movie data
            movie_data_dict.update({"EncodeTime":datetime_encodetime})
            #put the rounded runtime back into the copy of the movie data
            movie_data_dict.update({"MediaOriginalRunTime":simple_runtime})

            #put the movie and the movie data dict into the new datetime dict
            datetime_updated_dict.update({movie:movie_data_dict})

    return datetime_updated_dict

def dict_to_dataframe(media_dict):
    #Put a dict into a dataframe and transpose it
    return pd.DataFrame(data=media_dict).T

def find_all_unique_movies(media_dataframe):
    #Return all unique movie titles in dataframe
    return media_dataframe.drop_duplicates(subset=['Title'])

def main():
    """
    DVR media analysis -- or see what Mom is watching to find what streaming services would work best for her
    """

    #movie = "2019 Christmas- A First Look Preview Special_HALLHD_2019_07_13_21_00_01.wtv"
    #Show a  movie with the original EncodeTime
    #print (remove_list(get_media(media_file_name))[movie])
    #Show the same movie with the updated EncodeTime
    #print (cleanup_time(remove_list(get_media(media_file_name)))[movie])

    #Check show length function
    #print ("1:00:00 to ", show_length("1:00:00"))
    #print ("1:14:00 to ", show_length("1:14:00"))
    #print ("1:15:00 to ", show_length("1:15:00"))
    #print ("1:44:00 to ", show_length("1:44:00"))
    #print ("1:45:00 to ", show_length("1:45:00"))

    #Pull and clean up the raw file data into a dict
    clean_moviedict = cleanup_time(remove_list(get_media(media_file_name)))
    #Put the movie dict into the pandas dataframe
    main_movies_dataframe = dict_to_dataframe(clean_moviedict)
    #Show the main movie dataframe
    #print ("Main movie dataframe: ", main_movies_dataframe)

    #Find all unique movie titles
    unique_movies_dataframe = find_all_unique_movies(main_movies_dataframe)
    #Show the unique movies dataframe
    #print ("Unique movies dataframe: ", unique_movies_dataframe)

    #Show the total watch time for each show in descending order
    #print (main_movies_dataframe.groupby('Title')['MediaOriginalRunTime'].sum().sort_values(ascending = False))

    #Show how many shows are watched with a given duration
    print (main_movies_dataframe['MediaOriginalRunTime'].value_counts())



# This little chunk of code allows this python program to be either used directly or imported into another program
if __name__ == "__main__":
    main()    
