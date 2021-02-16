"""Launch a local web server to display the plotted graphs"""
from bottle import route, run, static_file, template
import os
import sys

graphs_folder = r"./Saved Graphs/"
webpagefile = "index.html"

def get_graphs():
    """Returns a list of graph plots filenames"""
    graph_name_list = []
    file_names_list = []

    #for _ , _ , file_names in os.walk(graphs_folder):
        #file_names_list = file_names.copy()

    dirpath, _, file_names_list = next(os.walk(graphs_folder))
    
    #print (file_names_list)

    for file_name in file_names_list:
        #print (file_name)
        if file_name[-4:] == ".jpg":
            #print (file_name)
            graph_name_list.append(file_name)

    print (graph_name_list)
    return graph_name_list

@route("/<filename>")
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
