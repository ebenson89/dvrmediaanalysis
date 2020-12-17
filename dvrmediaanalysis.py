''' Analyze movies, etc., recorded on DVRs '''

import json
from datetime import datetime

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

def convert_encode_time(media_dict):
    ''' Convert all EncodeTime to a valid datetime object '''
    #Current london time - 6 to get chicago time
    datetime_updated_dict = {}
    #Run through dict
    for movie in media_dict:
        if "EncodeTime" in media_dict[movie]: #Also removes invalid entries
            #copy the movie data dict
            movie_data_dict = media_dict[movie]
            #copy encode time string and update it to datetime obj and get rid of the Z
            datetime_encodetime = datetime.strptime(movie_data_dict["EncodeTime"],"%Y:%m:%d %H:%M:%S%z").astimezone()
            #put the updated time back into the copy of the movie data
            movie_data_dict.update({"EncodeTime":datetime_encodetime})
            #put the movie and the movie data dict into the new datetime dict
            datetime_updated_dict.update({movie:movie_data_dict})

    return datetime_updated_dict


def main():
    """
    DVR media analysis -- or see what Mom is watching to find what streaming services would work best for her
    """

    movie = "2019 Christmas- A First Look Preview Special_HALLHD_2019_07_13_21_00_01.wtv"
    #Show a  movie with the original EncodeTime
    print (remove_list(get_media(media_file_name))[movie])
    #Show the same movie with the updated EncodeTime
    print (convert_encode_time(remove_list(get_media(media_file_name)))[movie])


# This little chunk of code allows this python program to be either used directly or imported into another program
if __name__ == "__main__":
    main()    
