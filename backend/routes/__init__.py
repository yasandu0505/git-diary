from .contributions import router as contributions_router

all_routers = [
    (contributions_router, "/api/v1", ["Contributions"])
]