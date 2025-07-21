from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Choose Your Own Adventure Game API",
    description="api to generate cool stories",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
# добавляю middleware CORSMiddleware к FastAPI-приложению для управления политикой CORS
# allow_origins=["*"] - разрешаю запросы с любых источников
# allow_credentials=True - разрешаю отправку cookies и авториз. заголовков
# allow_methods=["*"] - разрешаю все HTTP-методы (GET/POST/PUT...)
# allow_headers=["*"] - разрешаю любые заголовки в запросах
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Для запуска приложения с помощью Uvicorn
# main -имя файла / app - переменная в этом файле, содержащая FastAPI-приложение
# host="0.0.0.0" - значит, что приложение будет доступно извне (не только через localhost)
# port=8000 - порт, на котором будет запущен сервер
# reload - автом-ки запу-ет сервер при изменениях в коде
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)