''' Analyze movies, etc., recorded on DVRs '''

import json
media_file_name = "recordings.json"

def get_media(json_file_name):
    #Open json file
    with open(media_file_name) as media_file:
        #Returns json obj as a dictionary
        return json.load(media_file)

def remove_list (media_dict):
    #TODO flatten each dictionary entry by replacing the list with the value that was in the list
    return (media_dict)

def main():
    """
    DVR media analysis -- or see what Mom is watching to find what streaming services would work best for her
    """

    movie = "2019 Christmas- A First Look Preview Special_HALLHD_2019_07_13_21_00_01.wtv"
    #Show a  movie before being flattened
    print (get_media(media_file_name)[movie])
    #Show the same movie after being flattned by replacing the list
    print (remove_list(get_media(media_file_name))[movie])
    

# This little chunk of code allows this python program to be either used directly or imported into another program
if __name__ == "__main__":
    main()    
