from tkinter import *
import time
import json
import random
from llmclient import LLMClient

request_data = {"max_tokens": 1000,
                "temperature": 0.8,
                }

llm_client_gpt4 = LLMClient(request_data, "gpt-4-turbo")
debate = "\n".join([l.strip() for l in open("debater_prompt_.txt", "r", encoding="utf-8").readlines()])

global history
global turn

history = ""
turn = 0

UUID = str(hash(time.time()))
model_type = "GPT-4-Turbo"
prompt_ver = "v2"


def append_to_history(history, input_str):
    history += "\n(P): "
    history += input_str
    return history


def call_llm(prompt, history):
    text = None
    eta = None
    while text is None:
        try:
            start = time.time()
            output = llm_client_gpt4.send_request(debate.replace("$HISTORY", history + "\n\nUser: {}".format(prompt)))
            text = output["choices"][0]["text"]
            eta = time.time() - start
        except:
            pass
    return text, eta


def parse_response(response):
    parsed_response = response.split("\nAI:")[-1].strip()
    return parsed_response


def log(prompt, response, history, turn, eta, e2e):
    with open("logs/log_{}_{}_{}.json".format(UUID, model_type, prompt_ver), "a", encoding="utf-8") as f:
        f.write(json.dumps({"Prompt": prompt, "History": history, "Response": response, 
            "ETA": eta, "E2E": e2e, "Turn": turn, "Version": prompt_ver}) + "\n")


def send():
    prompt = e.get("1.0",END).strip()
    send = "You: " + prompt
    txt.insert(END, "\n" + send)
    start = time.time()
 
    global history
    global turn

    if prompt == "debug123":
        if random.choice([0,1,2]) < 1:
            response = "I don't understand your position. Please state a debatable topic."
        elif random.choice([0,1,2]) == 2:
            response = "I don't understand your position. Please state a debatable topic."
            response += "I don't understand your position. Please state a debatable topic."
            response += "I don't understand your position. Please state a debatable topic."
        else:
            response = "this is a gpt4 response"
    else:
        response, eta = call_llm(prompt, history)
    end = time.time() - start

    if not is_base:
        history = append_to_history(history +  "\n\nUser: {}\n".format(prompt), response)
    else:
        history += history +  "\n\nUser: {}\n".format(prompt) + "\n\nAI: {}\n".format(response)
    parsed_response = parse_response(response)

    log(prompt, response, history, turn, eta, end)
    turn += 1

    txt.insert(END, "\nAI: " + parsed_response)
    txt.insert(END, "\n")
    e.delete('1.0', END)
 
 
# GUI
root = Tk()
root.title("LLM Debater: {} Edition".format(model_type))
 
BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
BG_TEXT = "#bdccdb" #"#2C3E50"
TEXT_COLOR = "#EAECEE"
TEXT_COLOR_BLACK = "#000000"

FONT = "Aptos 14"
FONT_BOLD = "Aptos 13 bold"

txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, borderwidth=5, width=85)
txt.grid(row=0, column=0, columnspan=2, pady=10, padx=10, ipady=5, ipadx=5)
 
scrollbar = Scrollbar(txt)
scrollbar.place(relheight=1, relx=1.0)# 0.974)
 
e = Text(root, bg=BG_TEXT, fg=TEXT_COLOR_BLACK, font=FONT, height=2, borderwidth=5, width=70)
#e.pack(ipady=3)
e.grid(row=1, column=0, padx=5, pady=5, ipady=5, ipadx=2)

scrollbar2 = Scrollbar(e)
scrollbar2.place(relheight=1, relx=1.0)# 0.974)

send = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=send).grid(row=1, column=1)
 
root.mainloop()