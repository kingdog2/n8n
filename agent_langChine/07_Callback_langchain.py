##Callback回調 自定義回調LLM處理的時間
from langchain.callbacks.base import BaseCallbackHandler
import time, os
from langchain_ollama import OllamaLLM
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class TimerHandler(BaseCallbackHandler):

    def __init__(self) -> None:
        super().__init__()
        self.previous_ms = None
        self.durations = []

    def current_ms(self):
        return int(time.time() * 1000 + time.perf_counter() % 1 * 1000)

    def on_chain_start(self, serialized, inputs, **kwargs) -> None:
        self.previous_ms = self.current_ms()

    def on_chain_end(self, outputs, **kwargs) -> None:
        if self.previous_ms:
          duration = self.current_ms() - self.previous_ms
          self.durations.append(duration)

    def on_llm_start(self, serialized, prompts, **kwargs) -> None:
        self.previous_ms = self.current_ms()

    def on_llm_end(self, response, **kwargs) -> None:
        if self.previous_ms:
          duration = self.current_ms() - self.previous_ms
          self.durations.append(duration)

timerHandler = TimerHandler()
prompt = PromptTemplate.from_template("What is the HEX code of color {color_name}?")

os.environ["SERPAPI_API_KEY"] =  your_key

ollama_model = OllamaLLM(model= "gemma3:4b", callbacks=[timerHandler])
print(ollama_model)



llm_chain = LLMChain(
    llm=ollama_model,
    prompt=prompt,
    verbose=True,
    
)
response = llm_chain.run(color_name="blue")
print(response)
response = llm_chain.run(color_name="purple")
print(response)

timerHandler.durations

