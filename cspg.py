#!/usr/bin/python

__author__ = 'mep'

from Tkinter import *
import sys

def optimize(*args):
    pass

def main(argv):
    root = Tk()

    root.title('CSP')

    input_file = StringVar()
    log_file = StringVar()
    msg_level = StringVar()
    iterations = StringVar()
    strategy = StringVar()

    mainframe = Frame(root) #, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight = 1)
    mainframe.rowconfigure(0, weight = 1)

    in_file = Entry(mainframe, width=10,textvariable=input_file)
    in_file.grid(column=2, row=1, sticky=(W,E))

    log_name = Entry(mainframe, width=10, textvariable=log_file)
    log_name.grid(column=2, row=2, sticky=(W,E))

    msg_lvl = Entry(mainframe, width=7, textvariable=msg_level)
    msg_lvl.grid(column=2, row=3, sticky=(W, E))

    iter_input = Entry(mainframe, width=7, textvariable=iterations)
    iter_input.grid(column=2, row=4, sticky=(W, E))

    strat_name = Entry(mainframe, width=7, textvariable=strategy)
    strat_name.grid(column=2, row=5, sticky=(W, E))

    Label(mainframe, text="Input file").grid(column=1, row=1, sticky=W)
    Label(mainframe, text="Log file").grid(column=1, row=2, sticky=W)
    Label(mainframe, text="Debug level").grid(column=1, row=3, sticky=W)
    Label(mainframe, text="Iterations").grid(column=1, row=4, sticky=W)
    Label(mainframe, text="Strategy").grid(column=1, row=5, sticky=W)

    Button(mainframe, text="Optimize", command=optimize).grid(column=3, row=6, sticky=W)

    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
    in_file.focus()
    root.bind('<Return>', optimize)
    root.mainloop()

if __name__ == '__main__':
    main(sys.argv[1:])

