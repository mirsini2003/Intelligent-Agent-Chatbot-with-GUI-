from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
from langchain_core.tools import tool



#custom tool
def save_to_file(data:str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text= f"--- Research Output ---\n{timestamp}\n\n{data}\n\n"
    with open(filename, "a",encoding="utf-8") as f:
        f.write(formatted_text)
    return f"Data saved to {filename}"
    
save_tool = Tool(
    name="save_text_to_file",
    func=save_to_file,
    description="Saves the output to a file."#you have to ask for it
)


search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="DuckDuckGoSearch",
    func=search.run,
    description="Search the web to find information."
)


api_wrapper = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=100)
wiki_tool=WikipediaQueryRun(api_wrapper=api_wrapper)


