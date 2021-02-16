"""Launch a local web server to display the plotted graphs"""
from bottle import route, run, static_file, template
import os
import sys

graphs_folder = r"./Saved Graphs/"
webpagefile = "index.html"

def get_graphs():
    """Returns a list of graph plots filenames"""
    file_name_list = []

    for _ , _ , file_name in os.walk("Saved Graphs"):
        if file_name[0][-4] == ".jpg":
            file_name_list.append(file_name)

    return file_name_list

@route(graphs_folder+"/<filename>")
def server_static(filename):
    """ Get any needed static files -- the graph files """
    return static_file(filename, root=graphs_folder)

@route("/")
def webserve():
    """ Display the graphs being plotted on a web page """
    graphs = get_graphs()
    return template(webpagefile,{"graphs": graphs})

def main():
    """ Launch a local web server to display the plotted graphs"""
    run(host="127.0.0.1")

if __name__ == "__main__":
    # execute only if run as a script
    main()    
