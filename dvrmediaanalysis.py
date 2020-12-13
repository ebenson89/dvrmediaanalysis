''' Analyze movies, etc., recorded on DVRs '''

import json

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
    assert False, "Remove this statement and update this def to convert the media_dict encode_time strings to a datetime objects" 

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
