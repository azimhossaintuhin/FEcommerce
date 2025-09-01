from  fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import UserRouter,categoryRouter,productsRouter,OrderRouter,cartRouter
from app.events import userevents
from  fastapi.staticfiles import StaticFiles
app = FastAPI(
    
)

# add static files
app.mount("/media", StaticFiles(directory="uploads"), name="media")


app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],)


app.include_router(UserRouter.router)
app.include_router(categoryRouter.router)
app.include_router(productsRouter.router)
app.include_router(OrderRouter.router)
app.include_router(cartRouter.router)