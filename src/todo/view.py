"""
The view for todo items.
"""

import ltk
from todo import model

class TodoView(ltk.HBox):
    """ A reactive todo item view. """

    classes = ["ltk-hbox", "todo"]

    def __init__(self, item: model.TodoModel):
        @ltk.callback
        def remove(_event):
            self.remove()
            item.remove()

        super().__init__(
            ltk.Checkbox(item.completed),
            ltk.Input(item.note),
            ltk.Label("🗑️")
                .addClass("delete")
                .on("click", remove)
        )


def create(item: model.TodoModel, focus=False):
    """ Create a new todo item. """
    view = TodoView(item).appendTo(ltk.find(".todos"))
    if focus:
        view.find(".ltk-input").focus()
    return view
