PRODUCTS = [
    {
        "id": "shoe-001",
        "name": "Runner Pro",
        "price": 4299,
        "category": "running shoes",
        "brand": "DemoBrand",
        "in_stock": True,
    },
    {
        "id": "shoe-002",
        "name": "Speed Runner",
        "price": 4799,
        "category": "running shoes",
        "brand": "DemoBrand",
        "in_stock": True,
    },
    {
        "id": "shoe-003",
        "name": "Trail Max",
        "price": 5999,
        "category": "running shoes",
        "brand": "DemoBrand",
        "in_stock": True,
    },
]


def search_products(query: str, max_price: float):
    if not isinstance(query, str) or not query.strip() :
        raise ValueError("query mst be a non-empty string")
    
    if isinstance(max_price, bool) or not isinstance(
        max_price, (int, float)
    ):
        raise ValueError("max_price must be a number")

    if max_price < 0 or max_price == float("inf"):
        raise ValueError("max_price must be a finite, non-negative number")    

    query = query.lower().strip()

    results = []

    for product in PRODUCTS:
        if (
            query not in product["category"].lower()
            and query not in product["name"].lower()
        ):
            continue

        if product["price"] > max_price:
            continue

        if not product["in_stock"]:
            continue

        results.append(product)

    return results


search_products_tool = {
    "name": "search_products",
    "description": (
        "Search the ecommerce product catalog for products "
        "matching the customer's request and maximum price."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The product the customer is looking for.",
            },
            "max_price": {
                "type": "number",
                "description": "The customer's maximum budget.",
            },
        },
        "required": ["query", "max_price"],
    },
}

AVAILABLE_TOOLS = {
    "search_products": search_products,
}