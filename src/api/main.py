from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import api.routines as routines
import api.auth as auth
import api.exercises as exercises


app = FastAPI(title="OpenAPI Test Server")


app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(exercises.router, prefix="/api", tags=["Exercises"])
app.include_router(routines.router, prefix="/api", tags=["Routines"])


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs/")


@app.get("/health")
def health() -> dict[str, str]:
	return {"status": "ok"}


def main():
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=7000)

if __name__ == "__main__":
	main()
