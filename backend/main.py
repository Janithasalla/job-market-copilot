from fastapi import FastAPI

# Create the app. Think of this as "turning on" your backend.
app = FastAPI(title="Job Market Copilot")


# When someone visits the home address "/", run this function
@app.get("/")
def home():
    return {"message": "Job Market Copilot is running!"}


# A "health check" — real companies use this to see if an app is alive
@app.get("/health")
def health():
    return {"status": "ok"}