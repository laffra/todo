"""
The model for todo items.
"""

import ltk

class TodoModel(ltk.LocalStorageModel):
    """ A reactive todo item model. """

    note: str = ""
    completed: bool = False
    suggestion: str = ""
