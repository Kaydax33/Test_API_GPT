from flask import Flask, render_template, request, jsonify, redirect
from openai import OpenAI
import time
import re

client = OpenAI(
    # This is the default and can be omitted
    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",
)

app = Flask(__name__)
assistant_id = "asst_FYyFzZYc2EoRYvR0Pr1U7TWa"
history = []
history_esme = []


@app.route("/")
def index():
    return redirect("/chatbot")


@app.route("/chatbot")
def chatbot():
    return render_template('chat.html')


@app.route("/chatbot/get", methods=['GET', 'POST'])
def chatbotmsg():
    msg = request.form['msg']
    return get_chat_response(msg)


def get_chat_response(prompt):
    history.append({"role": "user", "content": prompt})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=history
    )
    response_content = completion.choices[0].message.content
    history.append({"role": "assistant", "content": response_content})
    return response_content


@app.route("/chatesme")
def chatesme():
    return render_template('chatesme.html')


@app.route("/chatesme/get", methods=['GET', 'POST'])
def chatesmemsg():
    msg = request.form['msg']
    return get_chat_response_esme(msg)


def get_chat_response_esme(prompt):
    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    while run.status != 'completed':
        time.sleep(0.1)

    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    returned_value = messages.model_dump()['data'][0]['content'][0]['text']['value']
    return re.sub('【.*】', '', returned_value)


if __name__ == "__main__":
    app.run()
