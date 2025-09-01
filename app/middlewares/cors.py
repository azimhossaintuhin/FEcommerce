from  fastapi.middleware.cors import CORSMiddleware

CorsMiddleware = CORSMiddleware(
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)