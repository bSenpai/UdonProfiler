from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk


# Overwrite navigation toolbar.
# See: https://stackoverflow.com/a/59658768
class NavigationToolbar2CTk(NavigationToolbar2Tk):
    def __init__(self, canvas, window, *, pack_toolbar=True) -> None:
        super().__init__(canvas=canvas, window=window, pack_toolbar=pack_toolbar)

    def mouse_move(self, event) -> None:
        pass
