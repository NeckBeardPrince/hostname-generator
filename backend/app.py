from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import random
import paho.mqtt.client as mqtt

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Setup
MONGO_URI = "mongodb://mongo:27017"
client = MongoClient(MONGO_URI)
db = client["hostname_generator"]
collection = db["themes"]

# MQTT Setup
MQTT_BROKER = "mqtt"
MQTT_TOPIC_REQUEST = "hostname/request"
MQTT_TOPIC_RESPONSE = "hostname/response"

mqtt_client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker!")
    client.subscribe(MQTT_TOPIC_REQUEST)


def on_message(client, userdata, msg):
    theme = msg.payload.decode()
    theme_data = collection.find_one({"theme": theme})

    if theme_data and theme_data["names"]:
        hostname = random.choice(theme_data["names"])
        client.publish(f"{MQTT_TOPIC_RESPONSE}/{theme}", hostname)
        print(f"Assigned hostname '{hostname}' from theme '{theme}'.")


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, 1883, 60)
mqtt_client.loop_start()


# API Endpoints
def format_hostname(name: str) -> str:
    """Normalize hostname by making it lowercase and replacing spaces."""
    return name.lower().replace(" ", "-")  # Use "-" for readability


@app.get("/themes")
def list_themes():
    """List all available themes"""
    themes = collection.distinct("theme")
    return themes


@app.get("/{theme}")
def get_random_hostname(theme: str):
    theme = theme.lower()  # Convert theme name to lowercase before querying

    theme_data = collection.find_one({"theme": theme})
    if not theme_data or not theme_data["names"]:
        raise HTTPException(status_code=404, detail="Theme not found or empty")

    hostname = random.choice(theme_data["names"])
    return {format_hostname(hostname)}


@app.get("/theme/{theme}")
def get_theme_names(theme: str):
    """Get all names in a specific theme"""
    theme = theme.lower()
    theme_data = collection.find_one({"theme": theme})
    if not theme_data:
        raise HTTPException(status_code=404, detail="Theme not found")
    return theme_data["names"]


@app.post("/add_theme/{theme}")
def add_theme(theme: str, names: list[str]):
    theme = theme.lower()  # Convert theme name to lowercase
    formatted_names = [format_hostname(name) for name in names]

    if collection.find_one({"theme": theme}):
        raise HTTPException(status_code=400, detail="Theme already exists")

    collection.insert_one({"theme": theme, "names": formatted_names})
    return {"message": f"Theme '{theme}' added successfully!"}


@app.post("/add_names/{theme}")
def add_names(theme: str, names: list[str]):
    theme = theme.lower()  # Convert theme name to lowercase before querying
    formatted_names = [format_hostname(name) for name in names]

    result = collection.update_one(
        {"theme": theme}, {"$push": {"names": {"$each": formatted_names}}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Theme not found")

    return {"message": f"Names added to theme '{theme}'!"}


@app.delete("/remove_theme/{theme}")
def remove_theme(theme: str):
    theme = theme.lower()  # Convert theme name to lowercase before querying

    result = collection.delete_one({"theme": theme})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Theme not found")

    return {"message": f"Theme '{theme}' removed successfully!"}


@app.delete("/remove_name/{theme}/{name}")
def remove_name(theme: str, name: str):
    """Remove a specific name from a theme"""
    theme = theme.lower()
    formatted_name = format_hostname(name)

    result = collection.update_one(
        {"theme": theme}, {"$pull": {"names": formatted_name}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Theme or name not found")

    return {"message": f"Removed '{formatted_name}' from theme '{theme}'"}


@app.put("/update_name/{theme}")
def update_name(theme: str, old_name: str, new_name: str):
    """Modify a specific name within a theme"""
    theme = theme.lower()
    formatted_old_name = format_hostname(old_name)
    formatted_new_name = format_hostname(new_name)

    result = collection.update_one(
        {"theme": theme, "names": formatted_old_name},
        {"$set": {"names.$": formatted_new_name}},
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Name not found in theme")

    return {
        "message": f"Updated '{formatted_old_name}' to '{formatted_new_name}' in theme '{theme}'"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
