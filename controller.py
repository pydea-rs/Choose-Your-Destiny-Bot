from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import CassandraChatMessageHistory, ConversationBufferMemory

DEFAULT_TEMPLATE = '''
Create an interactive horror story.
like a person who one day finds himself in an apoclyptic situation among some deadly creatures.
I give you the freedom to improvise and change the story in any way you want, but the story theme is horror, or maybe science fiction.
the player will face different situations in this game that will have to decide what to do and his choices must effect his and others future. he/she can even fall in love or make enemies.
The player can be alone in the story, or maybe find some other person or even group of people in the same situation fighting for survival.
the player must at least make 20 decisions in game before the game ends. his decisions may effect the situation, destiny of himself or others, get himself or others killed or rescued.
its cool to have some plot twists in the story too. player can obtain things or money or etc in the game and use that in the future, esp when making future decisions.

here are the rules to follow:
1. start by asking the name, age and gender of the player.
2. have some decisions to make that effect the story. even causing success or death.
3. if the user dies or the story comes to the end, explain the ending contains a "**The End**" expression at the end.
'''

class GameController:

    def __init__(self, memory: ConversationBufferMemory, openai_api_key:str, game_template=DEFAULT_TEMPLATE) -> None:
        self.openai_api_key = openai_api_key
        self.llm = OpenAI(api_key=self.openai_api_key)
        self.game_template = game_template + '\n\nHere is the chat history, use this to understand what to say next: {' + memory.memory_key + '}\nHuman: {human}\nAI:'
        self.prompt = PromptTemplate(
            input_variables=[memory.memory_key, "human"],
            template=self.game_template
        )
        self.llm_chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=memory
        )

    def telltale(self):
        choice = 'start'
        response = ''
        is_game_ended = False
        while not is_game_ended:
            answer, is_game_ended = self.react(choice)
            print(answer)
            choice = input('What do you want to do? ')

    async def react(self, human_choice):
        answer = await self.llm_chain.predict(human=human_choice).strip()
        return answer, '**The End**' in response

