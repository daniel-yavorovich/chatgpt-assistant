import openai
import settings

openai.api_key = settings.OPENAI_API_KEY


class OpenAIChat:
    def __init__(self):
        self.prompt = "The following is a conversation with an AI assistant." \
                      "The assistant is helpful, creative, clever, and very friendly.\n\n" \
                      "Human: Hello, who are you?\n" \
                      "AI: I am an AI created by OpenAI. How can I help you today?\n" \
                      "Human: I'd like to cancel my subscription.\n" \
                      "AI:"
        self.temperature = 0.9
        self.max_tokens = 150
        self.top_p = 1
        self.frequency_penalty = 0.0
        self.presence_penalty = 0.6
        self.stop = [" Human:", " AI:"]
        self.response = None

    def chat(self):
        self.response = openai.Completion.create(
            model="text-davinci-003",
            prompt=self.prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            stop=self.stop
        )
        return self.response.choices[0].text

    def add_human_message(self, message):
        self.prompt += "Human: " + message + "\n"
        self.prompt += "AI: "

    def add_ai_message(self, message):
        self.prompt += "AI: " + message + "\n"
        self.prompt += "Human: "

    def get_response(self):
        return self.response.choices[0].text

    def get_prompt(self):
        return self.prompt

    def set_prompt(self, prompt):
        self.prompt = prompt
        self.prompt += "Human: "