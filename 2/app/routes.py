from fastapi import APIRouter, HTTPException
from app.models import ScrapeRequest
from app.services import jumbo_service
import asyncio

router = APIRouter()


@router.post("/")
async def scrape_jumbo(request: ScrapeRequest):

    products = await asyncio.to_thread(jumbo_service, request.url)
    return {"url": request.url, "products": products}
