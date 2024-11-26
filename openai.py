"""
Perform an OpenAI completion.
"""

import json
import ltk

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
    if not storage.hasOwnProperty("OPENAI_API_KEY"):
        storage.setItem(
            "OPENAI_API_KEY",
            ltk.window.prompt("Please enter your OPENAI Key")
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
        {
            "model": "gpt-3.5-turbo-instruct",
            "prompt": prompt,
            "max_tokens": 500,
            "temperature": 0.5
        },
        handle_suggestion,
    )

    def handle_image(response):
        url = response["data"][0]["url"]
        storage.setItem(f"openai-image-{prompt}", url)
        image_handler(url)

    call_openai(
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
        Indicate whether this goal achievable and measurable.
        Summarize alternative goals if applicable.
    """
    if not _load_from_cache(prompt, suggestion_handler, image_handler):
        _suggest_with_openai(prompt, suggestion_handler, image_handler)
