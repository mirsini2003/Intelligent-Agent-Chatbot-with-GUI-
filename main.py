import tkinter as tk  
from tkinter import scrolledtext, messagebox  
from dotenv import load_dotenv  
import os 
from datetime import datetime  
from pydantic import BaseModel  
from langchain_openai import ChatOpenAI  
from langchain_core.prompts import ChatPromptTemplate  
from langchain_core.output_parsers import PydanticOutputParser  
from langchain.agents import create_tool_calling_agent, AgentExecutor  
from tools import search_tool, wiki_tool, save_tool  
from langchain_core.runnables import RunnableLambda
import pyttsx3  
import threading  


# text-to-Speech
tts_engine = pyttsx3.init()  # initialize TTS
tts_engine.setProperty('rate', 160)  # speech speed 
voices = tts_engine.getProperty('voices')  # list of voices
tts_engine.setProperty('voice', voices[0].id)  # voice selection

# makes text to speech
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

load_dotenv() # loading environmental variables from .env file

# data model for research
class ResearchResponse(BaseModel):
    topic: str  # research topic
    summary: str  # summary of results
    sources: list[str]  # list of sources
    tools_used: list[str]  # tools used

#  save questions-answers to the research_output.txt
def save_to_file(question: str, answer: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
    formatted_text = (
        f"--- Research Entry ---\n"
        f"Timestamp: {timestamp}\n" # date and time
        f"Question: {question}\n" # question
        f"Answer: {answer}\n\n" # chatbot's answer
    )
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text) 

# Language model
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",  # use of mistral model
    base_url="https://openrouter.ai/api/v1",  # OpenRouter API
    api_key=os.getenv("OPENAI_API_KEY")  # API Key 
)

# agent
parser = PydanticOutputParser(pydantic_object=ResearchResponse)  # Export data in structured format

# Research Agent
research_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a research assistant. Answer the query and use tools if necessary. "
               "Wrap the output in the format given in {format_instructions} and do not add extra text."),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}")
])

research_tools = [search_tool, wiki_tool, save_tool]  # Available research tools
research_agent = create_tool_calling_agent(llm=llm, prompt=research_prompt, tools=research_tools)  # create agent
research_executor = AgentExecutor(agent=research_agent, tools=research_tools, verbose=False)  # Executive agent

# Chat Agent
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly and funny assistant. You can answer casually, tell jokes, and chat informally."),
    ("human", "{input}")
])

def chat_logic(inputs):
    
    message = chat_prompt.format_messages(input=inputs["input"])
    return llm.invoke(message)

chat_agent = RunnableLambda(chat_logic)  # Agent for simple discussion

# Math Agent
math_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a math assistant. You can perform calculations and solve mathematical problems accurately."),
    ("human", "{input}")
])

def math_logic(inputs):
    message = math_prompt.format_messages(input=inputs["input"])
    return llm.invoke(message)

math_agent = RunnableLambda(math_logic)  # math agent

# Placeholder Entry
class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder  # placeholder text
        self.placeholder_color = color  # placeholder color
        self.default_fg_color = self['fg']  

        # Connection events
        self.bind("<FocusIn>", self._clear_placeholder)  # Cleaning when pressed
        self.bind("<FocusOut>", self._add_placeholder)  # Return placeholder if empty

        self._add_placeholder()  # Display placeholder initially

    #Removes the placeholder when the field gets focus
    def _clear_placeholder(self, event=None):
        if self['fg'] == self.placeholder_color:
            self.delete(0, tk.END)
            self['fg'] = self.default_fg_color

    # Adds a placeholder if the field is empty
    def _add_placeholder(self, event=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

# gui class
class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        root.title("Your personal assistant")  
        root.geometry("700x520") 
        root.configure(bg="#E6E0F8") 

        self.agent_choice = tk.StringVar(value="1") # Research Agent default selection

        # select agent
        frame_agent = tk.Frame(root, bg="#E6E0F8")
        frame_agent.pack(pady=10)
        tk.Label(frame_agent, text="Choose an agent: ", bg="#E6E0F8", fg="#4B0082", font=("Arial", 11, "bold")).pack(side=tk.LEFT)

        # select buttons for agent
        tk.Radiobutton(frame_agent, text="Research Agent", variable=self.agent_choice, value="1",
                       bg="#E6E0F8", fg="#4B0082", selectcolor="#D1C4E9", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(frame_agent, text="Chat Agent", variable=self.agent_choice, value="2",
                       bg="#E6E0F8", fg="#4B0082", selectcolor="#D1C4E9", font=("Arial", 10)).pack(side=tk.LEFT)
        tk.Radiobutton(frame_agent, text="Math Agent", variable=self.agent_choice, value="3",
                       bg="#E6E0F8", fg="#4B0082", selectcolor="#D1C4E9", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        # Field for entering a query
        tk.Label(root, text="Question:", bg="#E6E0F8", fg="#4B0082", font=("Arial", 11, "bold")).pack(anchor="w", padx=10)
        self.entry = PlaceholderEntry(root, placeholder="Type your question here...", width=80)
        self.entry.pack(padx=10, pady=5)

        # Send query button
        self.send_button = tk.Button(root, text="Send", command=self.on_send,
                                     bg="#673AB7", fg="white", font=("Arial", 11, "bold"),
                                     activebackground="#5E35B1", activeforeground="white", relief="raised", bd=3,
                                     cursor="hand2")
        self.send_button.pack(pady=10)

        # Hover over the Send button
        self.send_button.bind("<Enter>", lambda e: self.send_button.config(bg="#7E57C2"))  
        self.send_button.bind("<Leave>", lambda e: self.send_button.config(bg="#673AB7")) 

        # view answers
        tk.Label(root, text="Answer:", bg="#E6E0F8", fg="#4B0082", font=("Arial", 11, "bold")).pack(anchor="w", padx=10)
        self.response_box = scrolledtext.ScrolledText(root, height=15, width=80, state='disabled', wrap='word',
                                                      bg="#F3E5F5", fg="#311B92", font=("Arial", 10))
        self.response_box.pack(padx=10, pady=5)
        frame_buttons = tk.Frame(root, bg="#E6E0F8")
        frame_buttons.pack(pady=10)

        # Exit button
        self.exit_button = tk.Button(frame_buttons, text="EXIT", command=self.on_exit,
                                     bg="#4B0082", fg="white", font=("Arial", 11, "bold"),
                                     activebackground="#3A0068", activeforeground="white", relief="raised", bd=3,
                                     cursor="hand2")
        self.exit_button.pack(side=tk.LEFT, padx=10)

        # Hover for Exit button
        self.exit_button.bind("<Enter>", lambda e: self.exit_button.config(bg="#5E35B1"))
        self.exit_button.bind("<Leave>", lambda e: self.exit_button.config(bg="#4B0082"))

        self.saved_any = False  # checks if something has been saved in the window

        # welcome message
        welcome_text = "Welcome! I am your assistant. Feel free to ask me anything."
        self.update_response(welcome_text)
        threading.Thread(target=speak, args=(welcome_text,), daemon=True).start()  # welcome speech

    # send question
    def on_send(self):
        query = self.entry.get().strip()
        # if question== empty
        if not query or query == self.entry.placeholder:  
            messagebox.showwarning("Warning", "Please write a question.")
            return

        # view question
        self.response_box.config(state='normal')
        self.response_box.insert(tk.END, f"You: {query}\n")
        self.response_box.config(state='disabled')
        self.entry.delete(0, tk.END)  # clean

        # Execute query in thread to prevent GUI from freezing
        threading.Thread(target=self.handle_query, args=(query,), daemon=True).start()

     # Manage query with selected agent
    def handle_query(self, query):
        try:
             # Research Agent
            if self.agent_choice.get() == "1": 
                raw_info = research_executor.invoke({
                    "query": query,
                    "format_instructions": parser.get_format_instructions(),
                    "agent_scratchpad": ""
                })
                research_text = raw_info.get("output")
                structured = parser.parse(research_text)  # structured response
                answer = structured.summary  # export summary
                save_to_file(query, answer)  # save
                self.saved_any = True
            # Chat Agent
            elif self.agent_choice.get() == "2":  
                chat_response = chat_agent.invoke({"input": query})
                answer = chat_response.content
                save_to_file(query, answer)
                self.saved_any = True
            # Math Agent
            elif self.agent_choice.get() == "3":  
                math_response = math_agent.invoke({"input": query})
                answer = math_response.content
                save_to_file(query, answer)
                self.saved_any = True
            else:
                answer = "Unknown agent selected."
        except Exception as e:
            answer = f"Error occurred: {e}"  # error message

        self.update_response(answer)
        threading.Thread(target=speak, args=(answer,), daemon=True).start()  

     # Update the frame with a new response
    def update_response(self, text):
        self.response_box.config(state='normal')
        self.response_box.insert(tk.END, f"Assistant: {text}\n\n")
        self.response_box.see(tk.END)  
        self.response_box.config(state='disabled')

     # Application shutdown
    def on_exit(self):
        if self.saved_any:
            goodbye_text = "All our conversation has been saved...Goodbye!"
        else:
            goodbye_text = "...Goodbye!"
        self.update_response(goodbye_text)
        threading.Thread(target=speak, args=(goodbye_text,), daemon=True).start()
        self.root.after(4500, self.root.quit)  # Closing after 4.5 seconds

# Application startup
if __name__ == "__main__":
    root = tk.Tk()  # Δημιουργία κύριου παραθύρου
    app = ChatbotGUI(root)  # Creating a main window
    root.mainloop()  # Start event loop