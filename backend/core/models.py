from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# from typing import List, Dict, Any, Optional - это подсказки типов для аргументов и возвращаемых
# значений функций или атрибутов классов
# BaseModel и Field из Pydantic позволяют описывать структуру данных, проверять их и автоматически
# сериализовать/десериализовать


# StoryOptionLLM - модель, описывающая один вариант выбора в истории
# text - текст, который видит пользователь при выборе
# nextNode - словарь с произвольными ключами или значениями (Dict[str, Any]), описывающий, что будет
# дальше в истории
class StoryOptionLLM(BaseModel):
    text: str = Field(description="the text of the option shown to the user")
    nextNode: Dict[str, Any] = Field(description="the next node content and its options")


# StoryNodeLLM - модель узла сюжета
# content - текстовое содержание этой сцены
# isEnding - переключатель финала или продолжения истории
# isWinningEnding - переключатель победный финал или нет
# options - список объектов StoryNodeLLM, может быть None - если это финальный узел
class StoryNodeLLM(BaseModel):
    content: str = Field(description="The main content of the story node")
    isEnding: bool = Field(description="Whether this node is an ending node")
    isWinningEnding: bool = Field(description="Whether this node is a winning ending node")
    options: Optional[List[StoryOptionLLM]] = Field(default=None, description="The options for this node")


# StoryLLMResponse - корневая модель, описывающая весь ответ от LLM
# title - название истории
# rootNode - начальный узел истории
class StoryLLMResponse(BaseModel):
    title: str = Field(description="The title of the story")
    rootNode: StoryNodeLLM = Field(description="The root node of the story")