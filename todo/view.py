"""
The view for todo items.
"""

import ltk

class TodoView(ltk.HBox):
    """ A reactive todo item view. """

    def __init__(self, item):
        super().__init__(
            ltk.Checkbox(item.completed),
            ltk.Input(item.note),
        )
        self.addClass("todo").appendTo(ltk.find(".todos"))


def create(item, focus=False):
    """ Create a new todo item. """
    view = TodoView(item)
    if focus:
        view.find(".ltk-input").focus()
        