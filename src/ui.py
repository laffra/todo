""" 
The UI for our Todo app
"""

import ltk # see https://github.com/pyscript/ltk

from lib import openai
from todo import model
from todo import view


class TodoApp(ltk.Model):
    """ The state of our app. """
    summary: str = ""


def create_ui(app):
    """ Create the main UI. """

    def update_summary():
        app.summary = f"{ltk.find('.todo').length} Todo Items:"

    def create_todo(_):
        view.create(model.TodoModel(), focus=True)
        update_summary()

    def suggest(suggestion):
        ltk.find("#suggest").text(suggestion.strip())

    def image(url):
        ltk.find("#image").attr("src", url)

    def run_ai(event):
        target = ltk.find(event.target).parent().find(".ltk-input")
        get_suggestion_and_image(target)

    def get_suggestion_and_image(target):
        note = repr(target.val())
        if not note:
            return
        suggest(f"Loading suggestion for {note}...")
        openai.get_suggestion_and_image(note, suggest, image)

    ltk.find("body").append(
        ltk.VBox(
            ltk.HBox(
                ltk.Button("New 󠁜 ✔", create_todo),
                ltk.Text(app.summary)
            ),
            ltk.HorizontalSplitPane(
                ltk.VerticalSplitPane(
                    ltk.VBox()
                        .addClass("todos"),
                    ltk.Preformatted("")
                        .attr("id", "suggest"),
                    "todos"
                ),
                ltk.Div(
                    ltk.Image("")
                        .attr("id", "image"),
                ),
                "todos and images"
            )
            .addClass("main-splitter")
        )
        .addClass("main")
        .on("change", run_ai)
        .on("focusin", run_ai)
    )

    for item in model.TodoModel.load():
        if item.note:
            get_suggestion_and_image(view.create(item))

    update_summary()


create_ui(TodoApp())
