#!/usr/bin/env python3
import os
import sys

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject

import about


class WindowMain(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        # Get GUI from Glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.dirname(__file__) + "/unar.glade")
        self.builder.connect_signals(self)

        # Display main window
        self.windowMain = self.builder.get_object("window_main")
        self.windowMain.show()

        #
        files_info = [[0, '']]
        self.filesTreeView = self.builder.get_object("files_list")  # TreeView object
        self.files_store = Gtk.ListStore(int, str)
        for info in files_info:
            self.files_store.append(info)
        self.filesTreeView.set_model(self.files_store)

        for i, col in enumerate(['序号', '文件名']):
            renderer = Gtk.CellRendererText()  # means how to draw the data
            column = Gtk.TreeViewColumn(col, renderer, text=i)  # text is column number
            column.set_sort_column_id(i)  # Make columns sortable
            self.filesTreeView.append_column(column)

    #     selected_file = self.filesTreeView.get_selection()
    #     selected_file.connect('changed', self.print_selected_file_info)
    #
    # @staticmethod
    # def print_selected_file_info(selection):
    #     model, row = selection.get_selected()
    #     if row:
    #         print(model[row][0])
    #         print(model[row][1])
    #         print()

    def on_file_open_activate(self, widget, data=None):
        dialog = Gtk.FileChooserDialog('Select an archive', self, Gtk.FileChooserAction.OPEN,
                                       ('OK', Gtk.ResponseType.OK,
                                        'Cancel', Gtk.ResponseType.CANCEL))
        filename = ''
        if dialog.run() == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            print('File selected: ' + filename)
        else:
            print('User did not choose any file')
        dialog.destroy()
        self.list_files(filename)

    def list_files(self, archive):
        if not archive:
            return
        p = os.popen('lsar %s' % archive)
        result = p.read()
        self.files_store.clear()
        for i, line in enumerate(result.splitlines()):
            if i:
                self.files_store.append([i, line])

    def on_about_activate(self, widget, data=None):
        self.aboutDialog = about.AboutDialog(self)

    @staticmethod
    def on_window_main_destroy(widget, data=None):
        print("on_window_main_destory")
        Gtk.main_quit()

    def on_file_quit_activate(self, widget, data=None):
        print("on_file_quit")
        self.windowMain.destroy()

    def main(self, file):
        self.list_files(file)
        Gtk.main()


if __name__ == "__main__":
    archive = sys.argv[1]
    application = WindowMain()
    application.main(archive)
