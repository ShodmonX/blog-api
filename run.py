import uvicorn
import asyncio
from app.create_tables import init_models

if __name__ == "__main__":
    # asyncio.run(init_models())
    uvicorn.run("app.main:app", host="127.0.0.1", port=8080, reload=True, reload_includes=["app.*"])