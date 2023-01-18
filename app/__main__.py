import os

import uvicorn

uvicorn.run(
    "app.app:app",
    host=os.getenv("HOST") or "0.0.0.0",
    port=int(os.getenv("PORT") or 8000),
    reload=bool(os.getenv("DEBUG", True)),
    ssl_cert_reqs=False,
)
