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
    
    # тут метод класса cls принимает db(SQLAlchemy-сессию для работы с базой данных). Возвращает объект Story - как модель базы
    # llm = cls._get_llm() - получение LLM модели с которым класс будет работать
    #  story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse) - подготовка парсера, который будет приводить сырой текст ответа LLM к строгой структуре StoryLLMResponse (pydantic-модель)
    # prompt = ChatPromptTemplate.from_messages([ - формирование промпта. Промпт будет состоять из двух сообщений (system/human). Через partial встраиваются подсказка для LLM, как форматировать ответ
    # raw_response = llm.invoke(prompt.invoke({})) - запрос к LLM. Тут превращается шаблон в конкретный промпт и отправляется в модель и получает ответ
    # response_text = raw_response - это чтобы достать текст, потому что LLM иногда возвращает объект
    # story_structure = story_parser.parse(response_text) - ответ LLM превращается в объект StoryLLMResponse (теперь это строго типизированая структура с title, rootNode и тд)
    # story_db = Story(title=story_structure.title, session_id=session_id) - сохранение истории в БД. Создается запись в таблице Story с заголовком session_id. flush() - нужен чтобы SQLAlchemy протолкнул INSERT в базу и у обхекта появился свой id
    # root_node_data = story_structure.rootNode - обработка корневого узла
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

        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)

        db.commit()
        return story_db
    
    @classmethod
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False) -> StoryNode:
        node = StoryNode(
            story_id=story_id,
            content=node_data.content if hasattr(node_data, "content") else node_data["content"],
            is_root=is_root,
            is_ending=node_data.isEnding if hasattr(node_data, "isEnding") else node_data["isEnding"],
            is_winning_ending=node_data.isWinningEnding if hasattr(node_data, "isWinningEnding") else node_data["isWinningEnding"],
            options=[]
        )
        db.add(node)
        db.flush()

        if not node.is_ending and (hasattr(node_data, "options") and node_data.options):
            options_list = []
            for option_data in node_data.options:
                next_node = option_data.nextNode

                if isinstance(next_node, dict):
                    next_node = StoryNodeLLM.model_validate(next_node)

                child_node = cls._process_story_node(db, story_id, next_node, False)

                options_list.append({
                    "text": option_data.text,
                    "node_id": child_node.id
                })

            node.options = options_list

        db.flush()
        return node