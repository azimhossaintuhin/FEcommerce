from  fastapi import FastAPI,Request
from  .config.cors import cors_origin,CORSMiddleware
from .routers.user_routers import router as user_routers
from .errors.errorHandlers import validation_exception_handler ,generic_exception_handler   
from fastapi.exceptions import RequestValidationError,HTTPException
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Including all the routes
app.include_router(user_routers)

# Register the exceptions
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, generic_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)




@app.get("/")
def read_root(request: Request):
    client_ip =  request.client.host if request.client else "Unknown"
    print(app.debug)
    return {"message": "Welcome To The User APi of FEcommerce",
            "data":{
                "version": "1.0.0",
                "description": "This is the user API for FEcommerce",
                "mode": "development",
                "your_ip": client_ip
            }}