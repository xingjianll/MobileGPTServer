import openai


class ResponseGetter:
    org_id: str
    api_key: str
    conversations: dict[str, list]

    def initialize(self):
        self.conversations = {}

    def request_response(self, prompt: str, model: str, conversation_name: str,
                         temperature: float) -> str:
        curr_chat = self.conversations.get(conversation_name)

        if curr_chat is None:
            self.conversations[conversation_name] = []
            curr_chat = self.conversations.get(conversation_name)

        curr_chat.append({"role": "user", "content": prompt})

        openai.api_key = self.api_key
        completion = openai.ChatCompletion.create(
            model=model,
            messages=curr_chat
        )

        curr_chat.append({"role": "assistant",
                          "content": completion.choices[0].message.content})
        return completion.choices[0].message.content

    def set_organization_id(self, org_id: str) -> None:
        self.org_id = org_id

    def set_apikey(self, api_key: str) -> None:
        self.api_key = api_key

    def get_conversations(self) -> dict[str: list]:
        return self.conversations

    def set_conversations(self, conversations: dict[str: list]) -> None:
        self.conversations = conversations

    def delete_conversation(self, conversation_name: str) -> None:
        self.conversations.__delitem__(conversation_name)
