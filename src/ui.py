""" 
The UI for our Todo app
"""

import ltk # see https://github.com/pyscript/ltk

from todo import model
from todo import view

import openai


class TodoApp(ltk.Model):
    """ The state of our app. """
    summary: str = ""


def create_ui(app):
    """ Create the main UI. """

    def update_summary():
        app.summary = f"{ltk.find('.todo').length} Todo Tasks:"

    def create_todo(_):
        view.create(model.TodoModel(), focus=True)
        update_summary()

    def suggest(suggestion):
        ltk.find("#suggest").text(suggestion.strip())

    def image(url):
        ltk.find("#image").attr("src", url).toggle()

    def run_ai(event):
        target = ltk.find(event.target).parent().find(".ltk-input")
        get_suggestion_and_image(target)

    def get_suggestion_and_image(target):
        note = target.val()
        if not isinstance(note, str):
            return
        suggest(f"Loading suggestion for {repr(note)}...")
        image("")
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
            view.create(item)

    get_suggestion_and_image(ltk.find(".ltk-model-todomodel-note"))

    update_summary()


create_ui(TodoApp())
