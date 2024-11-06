from .bd import SessionLocal

async def get_db():
    bd = SessionLocal()
    try:
        yield bd
    finally:
        bd.close()