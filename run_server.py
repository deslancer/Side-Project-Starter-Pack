"""
Скрипт для запуска FastAPI сервера с обслуживанием статических файлов фронтенда
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
import sys

# Добавляем путь к бэкенду
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.main import app

# Путь к собранному фронтенду
frontend_dist = os.path.join(os.path.dirname(__file__), "frontend", "dist")

if os.path.exists(frontend_dist):
    # Монтируем статические файлы (CSS, JS, images) если папка существует
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
    
    # Обработчик для всех остальных маршрутов - обслуживание SPA
    # FastAPI автоматически приоритизирует более специфичные маршруты (/api/* и т.д.)
    # Этот catch-all маршрут будет обрабатывать только те пути, которые не совпали с API маршрутами
    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_frontend(full_path: str):
        # Исключаем API маршруты, документацию FastAPI и статические файлы
        if full_path.startswith(("api/", "docs", "redoc", "openapi.json", "assets")):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Not found")
        
        # Проверяем, существует ли файл в dist
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        
        # Для SPA - возвращаем index.html для всех остальных маршрутов
        # Это позволяет Svelte Router обрабатывать клиентскую маршрутизацию
        index_path = os.path.join(frontend_dist, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Frontend not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

