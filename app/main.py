from contextlib import asynccontextmanager
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.api.router import master_router
# from fastapi.params import Depends as depends
from app.database.session import create_db_tables


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_db_tables()
    yield


app = FastAPI(
    # server startup and shutdown listerner
    lifespan=lifespan_handler)

app.include_router(master_router)


# @app.get("/shipment/{id}")
# def get_shipment(id: int) -> dict[str, str | int | Any]:
#     if id not in shipments:
#         return {"error": "Shipment not found"}
#     return shipments[id]



@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )