from datetime import datetime

from blacksheep import Application


app = Application()

@app.route("/")
async def home():
    return f"Hello, World! {datetime.utcnow().isoformat()}"
