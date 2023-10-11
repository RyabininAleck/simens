# This is a sample Python script.
import os
import subprocess
import sys
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class Agent(BaseModel):
    """
    Model of Agent
    """
    task: str | None = None
    name: str | None = None
    is_busy: bool | None = None
    is_manager: bool | None = None





app = FastAPI()


# Здесь инициализируйте маршруты и настройки вашего FastAPI приложения



@app.get("/")
async def root():
    return {Agent: str(Agent)}


@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    # Проверяем, что файл был передан
    if file is None:
        return JSONResponse(content="No file provided", status_code=400)

    # Создайте директорию для сохранения файлов, если она не существует
    if not os.path.exists("uploads"):
        os.mkdir("uploads")

    # Сохраняем файл в директорию
    with open(f"agent/uploads/{file.filename}", "wb") as f:
        f.write(file.file.read())

    python_script_path = f"agent/uploads/{file.filename}"


    try:
        process = subprocess.Popen([sys.executable, python_script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True)
        stdout, stderr = process.communicate()
    except Exception as e:
        print(f"Ошибка при выполнении программы: {e}")
        sys.exit(1)

    if not os.path.exists("output"):
        os.mkdir("output")

    # Путь к файлу, в который записать результаты (замените на свой путь)
    output_file_path = f"agent/output/{file.filename[:-3]}.txt"

    # Записываем результаты в файл
    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write("stdout:\n")
            output_file.write(stdout)
            output_file.write("\nstderr:\n")
            output_file.write(stderr)
        print(f"Результаты выполнения программы записаны в {output_file_path}")
    except Exception as e:
        print(f"Ошибка при записи результатов в файл: {e}")


    return JSONResponse(content=f"result { open(output_file_path, 'r').read() }", status_code=200)



if __name__ == "__main__":
    import uvicorn
    host = "127.0.0.1"  # Хост, на котором будет доступно приложение
    port = 8001  # Порт, на котором будет запущено приложение
    #agent = Agent(name=port, is_busy=False, is_manager=False)
    uvicorn.run(app, host=host, port=port)