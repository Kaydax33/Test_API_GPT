from openai import OpenAI

api_key = "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"
assistant_id = "asst_FYyFzZYc2EoRYvR0Pr1U7TWa"
prompt = "Quel coût pour lees différentes années ?"

client = OpenAI(
    api_key=api_key
)

history = []

def get_chat_response(prompt):
    history.append({"role": "user", "content": prompt})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=history
    )
    response_content = completion.choices[0].message.content
    print(completion.choices[0])
    history.append({"role": "assistant", "content": response_content})
    return response_content

print(get_chat_response("ca va ?"))
