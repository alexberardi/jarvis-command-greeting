"""Simple greeting command for Jarvis — says hello in different languages."""

import random
from typing import List

from jarvis_command_sdk import (
    IJarvisCommand,
    CommandExample,
    CommandResponse,
    JarvisParameter,
    RequestInformation,
)

GREETINGS = {
    "english": "Hello, {name}!",
    "spanish": "Hola, {name}!",
    "french": "Bonjour, {name}!",
    "japanese": "Konnichiwa, {name}!",
    "italian": "Ciao, {name}!",
    "german": "Hallo, {name}!",
    "portuguese": "Ola, {name}!",
    "korean": "Annyeonghaseyo, {name}!",
    "hindi": "Namaste, {name}!",
    "swahili": "Jambo, {name}!",
}


class GreetingCommand(IJarvisCommand):

    @property
    def command_name(self) -> str:
        return "greeting"

    @property
    def description(self) -> str:
        return "Say hello in different languages. Supports 10 languages."

    @property
    def keywords(self) -> List[str]:
        return ["hello", "hi", "greet", "greeting", "bonjour", "hola", "ciao"]

    @property
    def parameters(self) -> list:
        return [
            JarvisParameter(
                "name", "string", required=False,
                description="Name of the person to greet",
            ),
            JarvisParameter(
                "language", "string", required=False,
                description="Language to greet in",
                enum_values=list(GREETINGS.keys()),
            ),
        ]

    @property
    def required_secrets(self) -> list:
        return []

    def generate_prompt_examples(self) -> List[CommandExample]:
        return [
            CommandExample("say hello to Alex", {"name": "Alex"}, is_primary=True),
            CommandExample("greet me in french", {"language": "french"}),
            CommandExample("say hi in japanese to Yuki", {"name": "Yuki", "language": "japanese"}),
        ]

    def generate_adapter_examples(self) -> List[CommandExample]:
        return self.generate_prompt_examples()

    def run(self, request_info: RequestInformation, **kwargs) -> CommandResponse:
        name = kwargs.get("name", "friend")
        language = kwargs.get("language")

        if language and language.lower() in GREETINGS:
            greeting = GREETINGS[language.lower()].format(name=name)
        else:
            lang = random.choice(list(GREETINGS.keys()))
            greeting = GREETINGS[lang].format(name=name)
            language = lang

        return CommandResponse.success_response({
            "message": greeting,
            "language": language,
            "name": name,
        })
