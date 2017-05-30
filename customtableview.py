from PyQt5.QtWidgets import QTableView

class CustomTableView(QTableView):
    """
    This is a table view that deselects everything when the mouse 
    is clicked outside of a cell.
    """
    def mousePressEvent(self, event):
        self.clearSelection()
        super(CustomTableView, self).mousePressEvent(event)

