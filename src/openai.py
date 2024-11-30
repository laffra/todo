"""
Perform an OpenAI completion.
"""

import json
import ltk

OPENAI_KEY_MESSAGE = """
To make todo item suggestions, we need your OpenAI API Key.

Your key will be stored in localStorage for this page only.
It will not be uploaded anywhere, nor shared with anyone else.
You can/should remove your key again in the browser using:
`Developer Tools` > `Application` > `Local storage`.

Please enter your OpenAI Key below:
"""

storage = ltk.window.localStorage

def _load_from_cache(prompt, suggestion_handler, image_handler):
    if not storage.hasOwnProperty(f"openai-suggestion-{prompt}"):
        return False
    suggestion_handler(storage.getItem(f"openai-suggestion-{prompt}"))
    if not storage.hasOwnProperty(f"openai-image-{prompt}"):
        return False
    image_handler(storage.getItem(f"openai-image-{prompt}"))
    return True


def _get_open_ai_key():
    key = storage.getItem("OPENAI_API_KEY")
    if not key or key == "null":
        storage.setItem(
            "OPENAI_API_KEY",
            ltk.window.prompt(OPENAI_KEY_MESSAGE)
        )
    return storage.getItem("OPENAI_API_KEY")


def _suggest_with_openai(prompt, suggestion_handler, image_handler):
    def handle_suggestion(response):
        try:
            suggestion = response["choices"][0]["text"]
        except AttributeError:
            suggestion = json.dumps(response)
        storage.setItem(f"openai-suggestion-{prompt}", suggestion)
        suggestion_handler(suggestion)

    call_openai(
        "v1/completions",
        # https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/chatgpt?tabs=python-new
        {
            "model": "gpt-3.5-turbo-instruct",
            "prompt": prompt,
            "max_tokens": 500,
            "temperature": 0.1
        },
        handle_suggestion,
    )

    def handle_image(response):
        url = response["data"][0]["url"]
        storage.setItem(f"openai-image-{prompt}", url)
        image_handler(url)

    call_openai(
        # https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/dall-e?tabs=dalle3
        "v1/images/generations",
        {
            "model": "dall-e-3",
            "prompt": prompt,
            "size": "1024x1024",
            "quality": "standard",
            "n": 1,
        },
        handle_image
    )


def call_openai(endpoint, request, handler):
    """
    Call an OpenAI endpoint.
    """
    ltk.post(
        f"https://api.openai.com/{endpoint}",
        request,
        ltk.proxy(handler),
        "json",
        {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {_get_open_ai_key()}",
        },
    )


def get_suggestion_and_image(goal, suggestion_handler, image_handler):
    """
    Generate a suggestion on how to achieve a goal. 
    """
    prompt = f"""
        Suggest how to achieve a todo item: {goal}. 
        Write an advice in a few sentences, not a list of steps.
        Indicate whether this goal is achievable and measurable.
        Summarize alternative goals if applicable.
    """
    if not _load_from_cache(prompt, suggestion_handler, image_handler):
        _suggest_with_openai(prompt, suggestion_handler, image_handler)
