''' Analyze movies, etc., recorded on DVRs '''

import json
from datetime import datetime
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QIcon, QPixmap

graph_file_name = "graph_skeletons.json"
media_file_name = "recordings.json"
qtCreatorFile = "mainwindow.ui" # GUI Design file
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        #Variables
        self.clean_moviedict = self.cleanup_time(self.remove_list(self.get_data(media_file_name)))
        self.main_movies_dataframe = self.dict_to_dataframe(self.clean_moviedict)
        self.main_graph_dict = self.get_data(graph_file_name)
        self.single_graph_labels_dict = {}
        #Functions
        self.graph_options()
        self.build_graph_button.clicked.connect(self.build_graph)
        self.graph_list.clicked.connect(self.choose_graph)

    #What graphs the user can choose from
    def graph_options(self):
        i = 0

        for graph_name in self.main_graph_dict:
            self.graph_list.insertItem(i, graph_name)
            i += 1

    #Choose what graph to build
    def choose_graph(self, qmodelindex):
        graph_name = self.graph_list.currentItem()
        self.single_graph_labels_dict.update(self.main_graph_dict[graph_name.text()])

    #Get the data from the json file
    def get_data(self, json_file_name):
        #Open json file
        with open(json_file_name) as media_file:
            #Returns json obj as a dictionary
            return json.load(media_file)

    #Flatten each dictionary entry by replacing the list with the value that was in the list
    def remove_list (self, media_dict):
        simple_dict = {}
        #Run though raw dict
        for movie in media_dict:
            #Add new dict entry to simple_dict
            simple_dict.update({movie:media_dict[movie][0]})
        return (simple_dict)

    #Round the times in the runtime to the nearest half hour
    def show_length (self, time_string):
        minutes = int(time_string[2:4])
        hours = int(time_string[:1])
        
        #round to .5 if under 30
        if minutes < 30:
            rounded_time = time_string[:1] + ".5"
        #round to .5 if 15 to 44, yes this is redundent, might be changed later
        elif minutes < 45:
            rounded_time = time_string[:1] + ".5"
        #round up to the next hour if 45 or greater
        else:
            rounded_time = str(hours + 1) + ".0"

        return (float(rounded_time))

    #Month number to string name
    def month_int_to_str(self, month_int):
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        return months[month_int - 1]
    
    #Convert all EncodeTime to a valid datetime object and round the runtimes to nearest half hour
    def cleanup_time(self, media_dict):
        datetime_updated_dict = {}
        #Run through dict
        for movie in media_dict:
            if "EncodeTime" in media_dict[movie]: #Also removes invalid entries
                #copy the movie data dict
                movie_data_dict = media_dict[movie]

                #copy encode time string and update it to datetime obj with timezone
                datetime_encodetime = datetime.strptime(movie_data_dict["EncodeTime"],"%Y:%m:%d %H:%M:%S%z").astimezone()
                #Call show_length to round the runtimes
                simple_runtime = self.show_length(movie_data_dict["MediaOriginalRunTime"])
                #Find the hour that the show was recorded
                recorded_hour = datetime_encodetime.hour
                #Find the month that the show was recorded
                recorded_month = datetime_encodetime.month
                #Find the year that the show was recorded
                recorded_year = datetime_encodetime.year

                #Put the year and month together
                recorded_year_month = str(recorded_year) + ", " + self.month_int_to_str(recorded_month)

                #put the updated time back into the copy of the movie data
                movie_data_dict.update({"EncodeTime":datetime_encodetime})
                #put the rounded runtime back into the copy of the movie data
                movie_data_dict.update({"MediaOriginalRunTime":simple_runtime})
                #Add hour that show was recorded to the dict
                movie_data_dict.update({"RecordedHour":recorded_hour})
                #Add year and month that show was recorded to the dict
                movie_data_dict.update({"RecordedYearMonth":recorded_year_month})

                #put the movie and the movie data dict into the new datetime dict
                datetime_updated_dict.update({movie:movie_data_dict})

        return datetime_updated_dict

    #Put a dict into a dataframe and transpose it
    def dict_to_dataframe(self, media_dict):
        return pd.DataFrame(data=media_dict).T

    #Return all unique movie titles in dataframe
    def find_all_unique_movies(self, media_dataframe):
        return media_dataframe.drop_duplicates(subset=['Title'])

    #Return the data for the graph
    def get_graph_data(self, dataframe, keys_dataframe):
        data = []

        #Pull the data out of the dataframe
        for key in keys_dataframe:
            data.append(dataframe[key])

        return data

    #Save created graph
    def save_graph(self, Title):
        graph_file_name = "Saved Graphs\\" + Title + ".jpg"
        plt.savefig(graph_file_name, format ="jpg")    
    
    #Build a bar graph
    def bar_graph(self, new_dataframe, keys):
        #Find the height of the bar graph data
        height = self.get_graph_data(new_dataframe, keys)
        #Print Bar chart, bar(x-axis, height)
        plt.xlabel(self.single_graph_labels_dict["X-Label"])
        plt.ylabel(self.single_graph_labels_dict["Y-Label"])
        plt.title(self.single_graph_labels_dict["Title"])
        plt.xticks(range(len(height)), keys)
        plt.bar(range(len(height)), height)
        #Save graph
        self.save_graph(self.single_graph_labels_dict["Title"])
        #self.graph_output_label.setQpixmap(graph_file_name)
        plt.show()

    #Build a pie graph
    def pie_graph(self, new_dataframe, keys):
        #Find the size of the bar graph data
        size = self.get_graph_data(new_dataframe, keys)
        #Print Pie chart, pie(size, lables)
        plt.title(self.single_graph_labels_dict["Title"])
        patches, texts = plt.pie(size)
        plt.legend(patches, keys, loc="best")
        #Save graph
        self.save_graph(self.single_graph_labels_dict["Title"])
        plt.show()
    
    #Build the selected graph
    def build_graph(self):

        #If no graph has been selected throw an error box
        if self.single_graph_labels_dict == {}:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Error")
            msgBox.setText("Please choose a graph.")
            msgBox.exec()

        else:
            #Find the dataframe view string
            dataframe_view_string = self.single_graph_labels_dict["DataFrameCall"]
            #Evaluate the dataframe view
            new_dataframe = eval(dataframe_view_string)

            #Get all the keys in the dataframe
            keys = new_dataframe.keys()
            
            if self.single_graph_labels_dict["Chart"] == "Bar":
                #Build bar graph
                self.bar_graph(new_dataframe, keys)
            elif self.single_graph_labels_dict["Chart"] == "Pie":
                #Build pie graph
                self.pie_graph(new_dataframe, keys)
            else:
                #Should never reach here
                pass

# This little chunk of code allows this python program to be either used directly or imported into another program
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
