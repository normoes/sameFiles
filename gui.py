#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

try:
    from Tkinter import Listbox
    from Tkinter import Scrollbar
    from Tkinter import Button
    from Tkinter import Canvas
    from Tkinter import Frame
    from Tkinter import END
    from Tkinter import ANCHOR
    from Tkinter import SINGLE
    from Tkinter import EXTENDED
    from Tkinter import BOTH
    from Tkinter import RIGHT
    from Tkinter import LEFT
    from Tkinter import TOP
    from Tkinter import BOTTOM
    from Tkinter import VERTICAL
    from Tkinter import HORIZONTAL
    from Tkinter import Y
    from Tkinter import X
    import Tkinter as tk
    ## treeview
    import ttk
except ImportError:
    raise ImportError, "The Tkinter module is required to run his program."

import os

class simpleapp_tk(tk.Tk):
    def __init__(self, parent):
        ## class derives from Tkinter --> call its constructor
        tk.Tk.__init__(self, parent)
        ## keep track of the parent
        self.parent = parent
        self.initialize()

    def initialize(self):
        listFrame= Frame(self)
        listFrame.pack(side=TOP,fill=BOTH,expand=True)

        scrollbary = Scrollbar(listFrame , orient=VERTICAL)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx = Scrollbar(listFrame , orient=HORIZONTAL)
        scrollbarx.pack(side=BOTTOM, fill=X)
        ##bd --> border
        self.listbox = Listbox(listFrame,bd=0, selectmode=SINGLE, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        #self.listbox.bind('<<ListboxSelect>>',self.OnSelectClick)

        scrollbary.config(command=self.listbox.yview)
        scrollbarx.config(command=self.listbox.xview)

        # initialize with data from file
        self.populateFrom()

        self.listbox.config(width=self.listbox.winfo_reqwidth())          #width=self.listbox.winfo_reqwidth()
        self.listbox.pack(side=LEFT,fill=BOTH,expand=True)           #fill=Y, expand=False

        #self.listbox.focus_set()
        buttonFrame = Frame(self)
        buttonFrame.pack(fill=X)

        self.Path = tk.StringVar()
        self.Path.set('')
        self.SourcePath = tk.Entry(buttonFrame, textvariable=self.Path)


        b = Button(buttonFrame, text="TODO")
        b.bind('<Button-1>',self.OnDeleteSingleClick)

        b.pack(side=RIGHT)

        debugFrame = Frame(self)
        debugFrame.pack(side=BOTTOM,fill=X)
        self.selectedPath = tk.StringVar()
        self.pathLabel = tk.Label(debugFrame, textvariable=self.selectedPath, bg="white", anchor=tk.W)

        self.pathLabel.pack(side=LEFT,fill=X, expand=True)

        self.update()
        ## fix the size of the window by setting the window size to its own size
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry('{0}x{1}+{2}+{3}'.format(self.winfo_reqwidth(), self.winfo_reqheight(), w-self.winfo_reqwidth()-20, 0)) #self.geometry()
        ## update(): Tkinter has finished rendering all widgets and evaluating their size
        self.update()

        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())

    def populateFrom(self):
        pass

    def OnDeleteSingleClick(self, event):
        print '====DELETESINGLE===='
        #print self.listbox.get(tk.ANCHOR)
        #print list(self.listbox.get(0, END))
        #self.listbox.delete(tk.ANCHOR)
    def OnDeleteAllClick(self, event):
        print '====DELETEALL===='
        #self.clearListbox()
        #self.saveToCSV(self.filePath)

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('same files')
    #app.wm_attributes('-topmost', 1) # always on top
    app.mainloop()
