''' Analyze movies, etc., recorded on DVRs '''

import json
media_file_name = "recordings.json"

def get_media(json_file_name):
    #Open json file
    with open(media_file_name) as media_file:
        #Returns json obj as a dictionary
        return json.load(media_file)



def main():
    """
    DVR media analysis -- or see what Mom is watching to find what streaming services would work best for her
    """

    print (get_media(media_file_name))

# This little chunk of code allows this python program to be either used directly or imported into another program
if __name__ == "__main__":
    main()    
