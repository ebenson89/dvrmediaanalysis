''' Analyze movies, etc., recorded on DVRs '''
# TODO: Update the function get_media to read a json file and return the data in python dictionary format
# Hint: https://stackoverflow.com/questions/41476636/how-to-read-a-json-file-and-return-as-dictionary-in-python
import json
media_file_name = "recordings.json"

def get_media(json_file_name):
    #Open json file
    f = open(media_file_name,)
    #Returns json obj as a dictionary
    data = json.load(f)
    #Close json file
    f.close

    return data



def main():
    """
    DVR media analysis -- or see what Mom is watching to find what streaming services would work best for her
    """

    print (get_media(media_file_name))

# This little chunk of code allows this python program to be either used directly or imported into another program
if __name__ == "__main__":
    main()    
