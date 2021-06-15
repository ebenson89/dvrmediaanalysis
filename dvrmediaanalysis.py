''' Analyze movies, etc., recorded on DVRs '''

import json
import sys

from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

from PyQt5 import QtCore, QtGui, QtWidgets, uic  # C library, ignore F401
from PyQt5.QtGui import QIcon  # C library, ignore F401
from PyQt5.QtWidgets import QLabel, QListWidget, QPushButton, QMessageBox  # C library, ignore F401

graph_file_name = "graph_skeletons.json"
speed_file_name = "speedtest.log"
media_file_name = "recordings.json"
qtCreatorFile = "mainwindow.ui"  # GUI Design file
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """Takes data from json media file, cleans it up and puts it in a dataframe. Build graphs from the data in the media dataframe."""

    def __init__(self):
        """Create the a window that displays all graphs that can be built or updated."""
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # Movies
        self.clean_moviedict = self.cleanup_time(self.remove_list(self.get_data_json(media_file_name)))
        self.main_movies_dataframe = self.dict_to_dataframe(self.clean_moviedict)
        # Upload times
        self.speed_time_dict = self.get_data_log(speed_file_name)
        self.speed_time_dataframe = self.set_types(self.dict_to_dataframe(self.cleanup_speed_times(self.speed_time_dict)))
        # Graph variables
        self.main_graph_dict = self.get_data_json(graph_file_name)
        self.single_graph_labels_dict = {}  # All of the variables from the graph skeleton is in here.
        # Functions
        self.graph_options()
        self.build_graph_button.clicked.connect(self.build_graph)
        self.build_all_graphs_button.clicked.connect(self.build_all_graphs)
        self.graph_list.clicked.connect(self.choose_graph)

    def graph_options(self):
        """Display what graphs the user can choose from."""
        i = 0

        for graph_name in self.main_graph_dict:
            self.graph_list.insertItem(i, graph_name)
            i += 1

    def choose_graph(self, qmodelindex):
        """Select what graph to build on the GUI."""
        graph_name = self.graph_list.currentItem()
        self.single_graph_labels_dict.update(self.main_graph_dict[graph_name.text()])

    def get_data_json(self, json_file_name):
        """Put the data from the json file into a dict."""
        # Open json file
        with open(json_file_name) as media_file:
            # Returns json obj as a dictionary
            return json.load(media_file)

    def get_data_log(self, log_file_name):
        """Put the data from the log file into something that can be turned into a dataframe."""
        data_dict = {}

        log_file = open(log_file_name, 'r')
        lines = log_file.read().splitlines()
        log_file.close()

        for line in lines:
            json_to_dict = json.loads(line)
            data_dict.update({json_to_dict["timestamp"]: json_to_dict})

        return data_dict

    def remove_list(self, media_dict):
        """Flatten each dictionary entry by replacing the list with the value that was in the list."""
        simple_dict = {}
        # Run though raw dict
        for movie in media_dict:
            # Add new dict entry to simple_dict
            simple_dict.update({movie: media_dict[movie][0]})
        return (simple_dict)

    def show_length(self, time_string):
        """Round the times in the runtime to the nearest half hour."""
        minutes = int(time_string[2:4])
        hours = int(time_string[:1])

        # Round to .5 if under 30
        if minutes < 30:
            rounded_time = time_string[:1] + ".5"
        # Round to .5 if 15 to 44, yes this is redundent, might be changed later
        elif minutes < 45:
            rounded_time = time_string[:1] + ".5"
        # Round up to the next hour if 45 or greater
        else:
            rounded_time = str(hours + 1) + ".0"

        return (float(rounded_time))

    def month_int_to_str(self, month_int):
        """Month number to string name."""
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        return months[month_int - 1]

    def cleanup_speed_times(self, speed_time_dict):
        """Change download and upload from bytes to mega bits. 1 byte / 1,000,000 = 1 MB."""
        speed_time_updated_dict = {}

        for entry in speed_time_dict:
            # Copy the entry data dict
            entry_data_dict = speed_time_dict[entry]

            # Change timestamp string to datetime obj: '2018-06-15T19:25:07.621089Z'
            fixed_timestamp = entry_data_dict["timestamp"][:10] + ' ' + entry_data_dict["timestamp"][11:]
            datetime_timestamp = datetime.strptime(fixed_timestamp, "%Y-%m-%d %H:%M:%S.%f%z").astimezone()
            # Find the date
            date_timestamp_string = entry_data_dict["timestamp"][:10]
            # Find the month that the entry was logged
            log_month = datetime_timestamp.month
            # Find the year that the entry was logged
            log_year = datetime_timestamp.year
            # Update "download" to MB
            download_MB = float(entry_data_dict["download"]) / 1000000
            # Update "upload" to MB
            upload_MB = float(entry_data_dict["upload"]) / 1000000

            # Check data type
            if isinstance(download_MB, float) is False:
                print("Error in this dict: ", entry_data_dict)
                quit()
            if isinstance(upload_MB, float) is False:
                print("Error in this dict: ", entry_data_dict)
                quit()

            # Put the updated time back in the dict
            entry_data_dict.update({"timestamp": date_timestamp_string})
            # Put the date in a new column
            entry_data_dict.update({"date": date_timestamp_string})
            # Add year that entry was logged to the dict
            entry_data_dict.update({"year": log_year})
            # Add month that entry was logged to the dict
            entry_data_dict.update({"month": log_month})
            # Put the updated download speed back in the dict
            entry_data_dict.update({"download": download_MB})
            # Put the updated upload speed back in the dict
            entry_data_dict.update({"upload": upload_MB})

            # Put the entry into the new datetime dict
            speed_time_updated_dict.update({entry: entry_data_dict})

        return speed_time_updated_dict

    def cleanup_time(self, media_dict):
        """Convert all EncodeTime to a valid datetime object and round the runtimes to nearest half hour."""
        datetime_updated_dict = {}
        # Run through dict
        for movie in media_dict:
            if "EncodeTime" in media_dict[movie]:  # Also removes invalid entries
                # Copy the movie data dict
                movie_data_dict = media_dict[movie]

                # Copy encode time string and update it to datetime obj with timezone
                datetime_encodetime = datetime.strptime(movie_data_dict["EncodeTime"], "%Y:%m:%d %H:%M:%S%z").astimezone()
                # Call show_length to round the runtimes
                simple_runtime = self.show_length(movie_data_dict["MediaOriginalRunTime"])
                # Find the hour that the show was recorded
                recorded_hour = datetime_encodetime.hour
                # Find the month that the show was recorded
                recorded_month = datetime_encodetime.month
                # Find the year that the show was recorded
                recorded_year = datetime_encodetime.year

                # Put the updated time back into the copy of the movie data
                movie_data_dict.update({"EncodeTime": datetime_encodetime})
                # Put the rounded runtime back into the copy of the movie data
                movie_data_dict.update({"MediaOriginalRunTime": simple_runtime})
                # Add hour that show was recorded to the dict
                movie_data_dict.update({"RecordedHour": recorded_hour})
                # Add year that show was recorded to the dict
                movie_data_dict.update({"RecordedYear": recorded_year})
                # Add month that show was recorded to the dict
                movie_data_dict.update({"RecordedMonth": recorded_month})

                # Put the movie and the movie data dict into the new datetime dict
                datetime_updated_dict.update({movie: movie_data_dict})

        return datetime_updated_dict

    def dict_to_dataframe(self, media_dict):
        """Put a dict into a dataframe and transpose it."""
        new_dataframe = pd.DataFrame(data=media_dict).T
        # print("Type: ", type(new_dataframe))
        # print("New dataframe: ", "\n", new_dataframe)
        return new_dataframe

    def set_types(self, speed_dataframe):
        '''Change the column types from object to numeric'''
        if "download" in speed_dataframe:
            speed_dataframe = speed_dataframe.astype(dtype={"download": "float64"})
        if "upload" in speed_dataframe:
            speed_dataframe = speed_dataframe.astype(dtype={"upload": "float64"})

        return speed_dataframe

    def find_all_unique_movies(self, media_dataframe):
        """Return all unique movie titles in dataframe."""
        return media_dataframe.drop_duplicates(subset=['Title'])

    def save_graph(self, Title):
        """Save created graph."""
        graph_file_name = "Saved Graphs\\" + Title + ".jpg"
        plt.savefig(graph_file_name, format="jpg")

    def bar_graph(self, new_dataframe):
        """Build a bar graph."""
        # Plot and label bar graph
        new_dataframe.fillna(0).plot(
            kind='bar', figsize=(7, 9),
            title=self.single_graph_labels_dict["Title"],
            xlabel=self.single_graph_labels_dict["X-Label"],
            ylabel=self.single_graph_labels_dict["Y-Label"])

        # Show graph
        plt.show()
        # Save graph
        self.save_graph(self.single_graph_labels_dict["Title"])

    def pie_graph(self, new_dataframe):
        """Build a pie graph."""
        # Plot and label pie graph
        new_dataframe.fillna(0).plot(
            kind='pie', figsize=(9, 7),
            title=self.single_graph_labels_dict["Title"])

        plt.legend(bbox_to_anchor=(1, 1), loc="upper left")
        # Show graph
        plt.show()
        # Save graph
        self.save_graph(self.single_graph_labels_dict["Title"])

    def stacked_bar_graph(self, new_dataframe):
        """Build a stacked bar graph."""
        # Plot and label stacked bar graph
        new_dataframe.unstack().fillna(0).plot(
            kind='bar', stacked=True, figsize=(13, 9),
            title=self.single_graph_labels_dict["Title"],
            xlabel=self.single_graph_labels_dict["X-Label"],
            ylabel=self.single_graph_labels_dict["Y-Label"])

        plt.legend(bbox_to_anchor=(1, 1), loc="upper left")

        # Show graph
        plt.show()
        # Save graph
        self.save_graph(self.single_graph_labels_dict["Title"])

    def scatter_graph(self, new_dataframe, keys):
        """Build a scatter plot graph."""
        ax = new_dataframe.plot(x=self.single_graph_labels_dict["X-Axis"], y=self.single_graph_labels_dict["Y-Axis"], style='o', figsize=(13, 7))
        ax.set_xlabel(self.single_graph_labels_dict["X-Label"])
        ax.set_ylabel(self.single_graph_labels_dict["Y-Label"])
        ax.set_title(self.single_graph_labels_dict["Title"])

        # Show graph
        plt.show()
        # Save graph
        self.save_graph(self.single_graph_labels_dict["Title"])

    def build_graph(self):
        """Build the graph selected on the GUI."""

        # If no graph has been selected throw an error box
        if self.single_graph_labels_dict == {}:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Error")
            msgBox.setText("Please choose a graph.")
            msgBox.exec()

        else:
            # Find the dataframe view string
            dataframe_view_string = self.single_graph_labels_dict["DataFrameCall"]
            # Evaluate the dataframe view
            new_dataframe = eval(dataframe_view_string)
            # Debug
            # print("Type: ", type(new_dataframe))
            # print("Object in use: ", "\n", new_dataframe)

            # Get all the keys in the dataframe
            keys = new_dataframe.keys()

            if self.single_graph_labels_dict["Chart"] == "Bar":
                # Build bar graph
                self.bar_graph(new_dataframe)
            elif self.single_graph_labels_dict["Chart"] == "Pie":
                # Build pie graph
                self.pie_graph(new_dataframe)
            elif self.single_graph_labels_dict["Chart"] == "SBar":
                # Build stacked bar graph
                self.stacked_bar_graph(new_dataframe)
            elif self.single_graph_labels_dict["Chart"] == "Scatter":
                # Build line graph
                self.scatter_graph(new_dataframe, keys)
            else:
                # Should never reach here
                pass

    def build_all_graphs(self):
        """Build all graphs"""
        # print("Graph skeletons: ", self.main_graph_dict)
        #for graph_name in self.main_graph_dict:
            #print("Current graph: ", graph_name)
            #self.single_graph_labels_dict.update(self.main_graph_dict[graph_name])
            #print("Data for the current graph: ", self.single_graph_labels_dict)
            #self.build_graph()
            #self.single_graph_labels_dict = {}


# This little chunk of code allows this python program to be either used directly or imported into another program
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
