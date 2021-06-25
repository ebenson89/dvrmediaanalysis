"""Launch a local web server to display the plotted graphs"""
from bottle import route, run, static_file, template
import os

graphs_folder = r"./Saved Graphs/"
media_folder = r"./Saved Graphs/Media/"
speed_folder = r"./Saved Graphs/Speed/"
webpagefile = "index.html"


def get_graphs(graph_folder, parent_folder):
    """Returns a list of graph plots filenames"""
    graph_name_list = []
    file_names_list = []

    _, _, file_names_list = next(os.walk(graph_folder))

    for file_name in file_names_list:
        if file_name[-4:] == ".jpg":
            graph_name_list.append("/" + parent_folder + "/" + file_name)

    return graph_name_list


@route("/speed/<filename>")
def server_static_speed(filename):
    """ Get any needed static files -- the speed graph files """
    return static_file(filename, root='./Saved Graphs/Speed')


@route("/media/<filename>")
def server_static_media(filename):
    """ Get any needed static files -- the media graph files """
    return static_file(filename, root='./Saved Graphs/Media')


@route("/")
def webserve():
    """ Display links to other pages """
    return template(webpagefile)


@route("/media")
def media():
    """ Display the graphs being plotted on the media web page """
    media = get_graphs(media_folder, "media")
    return template("media.html", {"media": media})


@route("/speed")
def speed():
    """ Display the graphs being plotted on the speed web page """
    speed = get_graphs(speed_folder, "speed")
    return template("speed.html", {"speed": speed})


def main():
    """ Launch a local web server to display the plotted graphs"""
    run(host="127.0.0.1")


if __name__ == "__main__":
    # execute only if run as a script
    main()
