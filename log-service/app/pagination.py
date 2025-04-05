from fastapi import Depends, Request
from fastapi.requests import HTTPConnection
from motor.motor_asyncio import AsyncIOMotorCursor
from pydantic import BaseModel
from urllib.parse import urlencode


PAGE_NUMBER = 1
PAGE_SIZE = 10


async def extract_pagination(request: Request) -> tuple[int, int]:
    page = int(request.query_params.get('page_number', PAGE_NUMBER))
    size = int(request.query_params.get('page_size', PAGE_SIZE))

    return page, size


async def create_page_url(page_num: int, request: Request) -> str:
    url = str(request.base_url).rstrip('/') \
        + str(request.url.path)

    query_params = request.query_params._dict.copy()
    query_params["page_number"] = page_num
    encoded_query_string = urlencode(query_params)

    return f"{url}?{encoded_query_string}"


async def paginate(request: Request, cursor: AsyncIOMotorCursor, schema: BaseModel):
    page, size = await extract_pagination(request)

    skip = (page - 1) * size
    cursor = cursor.skip(skip).limit(size)

    next_page = await create_page_url(page + 1, request)

    prev_page_number = page - 1 if page > 1 else 1
    prev_page = await create_page_url(prev_page_number, request)

    documents = await cursor.to_list(length=size)
    result = [schema(**doc) for doc in documents]

    return {
        'total' : len(result),
        'next': next_page,
        'prev': prev_page,
        'results': result
    }
