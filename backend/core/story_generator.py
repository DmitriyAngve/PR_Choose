from sqlalchemy.orm import Session

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode
from core.models import StoryLLMResponse, StoryNodeLLM

# from sqlalchemy.orm import Session - это для работы с БД

# from core.config import settings - подтягивает конфигурацию из core.configuration

# from core.prompts import STORY_PROMPT - загружает шаблон промпта STORY_PROMPT из core.prompts

# from langchain_core.output_parsers import PydanticOutputParser - использование PydanticOutputParser
# для парсинга результата от LLM

class StoryGenerator:

    @classmethod
    def _get_llm(cls): 
        return ChatOpenAI(model="gpt-4-turbo")
    
    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy")-> Story:
        llm = cls._get_llm()
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                STORY_PROMPT
            ),
            (
                "human",
                f"Create the story with this theme: {theme}"
            )
        ]).partial(format_instructions=story_parser.get_format_instructions())

        raw_response = llm.invoke(prompt.invoke({}))

        response_text = raw_response
        if hasattr(raw_response, "content"):
            response_text = raw_response.content

        story_structure = story_parser.parse(response_text)

        story_db = Story(title=story_structure.title, session_id=session_id)
        db.add(story_db)
        db.flush()

        root_node_data = story_structure.rootNode
        if isinstance(root_node_data, dict):
            root_node_data = StoryNodeLLM.model_validate(root_node_data)

        # todo: process data

        db.commit()
        return story_db
    
    @classmethod
    def _process_story_node(cls, db:Session, story_id: int, node_date: StoryNodeLLM, is_root: bool = False)
        

