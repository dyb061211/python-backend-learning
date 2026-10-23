import asyncio

async def mock_generate_listing(product: dict) -> dict:
    product_id = product["id"]
    name = product["name"]
    delay = product["delay"]
    try:
        if product.get("should_fail",False):
            raise ValueError("LLM generation failed")
        await asyncio.sleep(delay)
        return {
            "id": product_id,
            "status": "success",
            "listing": f"Listing for {name}"
        }
    finally:
        print("Request resource released")

async def run_sequential(products: list[dict]) -> list[dict]:
    results=[]
    for product in products:
        results.append(await mock_generate_listing(product))
    return results

async def mock_get_llm_listing(semaphore, product: dict,timeout) -> dict:
    try:
        async with semaphore:
            async with asyncio.timeout(timeout):
                result = await mock_generate_listing(product)
        return result
    except TimeoutError:
        return{
            "id": product["id"],
            "status": "failed",
            "error": "TimeoutError"
        }
    except ValueError:
        return{
            "id": product["id"],
            "status": "failed",
            "error": "ValueError"
        }


async def run_concurrent(products: list[dict],max_concurrency=3,timeout=3) -> list[dict]:
    semaphore=asyncio.Semaphore(max_concurrency)
    tasks=[mock_get_llm_listing(semaphore, product,timeout) for product in products]
    results=await asyncio.gather(*tasks)
    return results