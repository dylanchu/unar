#!/usr/bin/env python3

from gi.repository import Gtk
import os


class AboutDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, 'About Dialog', parent, Gtk.DialogFlags.MODAL)
        # Get GUI from Glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.dirname(__file__) + "/unar.glade")

        # Display main window
        self.aboutDialog = self.builder.get_object("about_dialog")
        self.aboutDialog.connect('destroy', self.on_about_dialog_destroy)
        self.aboutDialog.show()

    def on_about_dialog_destroy(self, widget, data=None):
        self.aboutDialog.destroy()
