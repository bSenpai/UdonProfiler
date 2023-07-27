# See: https://stackoverflow.com/a/29158947
# See: https://stackoverflow.com/a/59625277
# See: https://stackoverflow.com/a/3794505
# See: https://tkdocs.com/tutorial/tree.html
# See: https://www.pythontutorial.net/tkinter/tkinter-object-oriented-window/
# See: https://www.digitalocean.com/community/tutorials/tkinter-working-with-classes
# See: https://www.tutorialspoint.com/how-to-clear-items-from-a-ttk-treeview-widget
# See: https://www.tutorialspoint.com/python/tk_frame.htm
# See: https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
# See: https://stackoverflow.com/a/21198403
# See: https://stackoverflow.com/a/61020195
# See: https://coderslegacy.com/python/tkinter-pack-two-frames-side-by-side/
# See: https://stackoverflow.com/a/62338378
# See: https://stackoverflow.com/a/13308493
# See: https://stackoverflow.com/a/73069099

from os import path

from UdonProfiler import UdonProfiler


if __name__ == "__main__":
    # See: https://stackoverflow.com/a/52534405
    #      https://docs.unity3d.com/Manual/LogFiles.html
    log_file: str = path.expandvars(r"%LOCALAPPDATA%\Unity\Editor\Editor.log")

    app: UdonProfiler = UdonProfiler(log_file)
    app.run()
