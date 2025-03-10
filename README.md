# Hostname Generator API

## Overview

This project provides a **fully containerized hostname generator API** that allows you to generate random server hostnames based on predefined themes. It includes a **FastAPI backend**, a **Vue.js Web UI**, **MongoDB for storage**, and **MQTT for auto-assigning hostnames to Raspberry Pi devices**.

### Features

- ✅ **Random hostname generation** based on different themes
- ✅ **MongoDB-backed persistence** for themes and names
- ✅ **Web UI for managing themes and names**
- ✅ **Auto-assign hostnames to Raspberry Pi devices** via MQTT
- ✅ **Podman/Docker Compose for easy deployment**
- ✅ **Swagger API documentation**

---

## 🚀 Getting Started

### **1. Clone the Repository**

```bash
git clone https://github.com/your-username/hostname-generator.git
cd hostname-generator
```

### **2. Setup Environment Variables**

Create a `.env` file inside `webui/`:

```bash
echo "VITE_API_BASE_URL=http://backend:8000" > webui/.env
```

### **3. Build and Run the Services**

```bash
podman-compose up -d --build
```

### **4. Access the Web UI**

Once everything is running, open your browser and go to:

```
http://localhost:8080
```

### **5. Verify Running Containers**

To check if all containers are running properly:

```bash
podman ps
```

---

## 📌 API Endpoints

### **Swagger Docs**

You can access the **Swagger API Documentation** at:

```
http://localhost:8000/docs
```

This provides an interactive way to test API calls.

### **Sample API Requests**

#### **Get a Random Hostname from a Theme**

```bash
curl http://localhost:8000/dc
```

**Response:**

```json
{ "batman" }
```

#### **List All Themes**

```bash
curl http://localhost:8000/themes
```

**Response:**

```json
["dc", "marvel", "dinosaurs"]
```

#### **View Names in a Theme**

```bash
curl http://localhost:8000/theme/dc
```

**Response:**

```json
["batman", "superman", "joker"]
```

#### **Add a New Theme**

```bash
curl -X POST "http://localhost:8000/add_theme/starwars" -H "Content-Type: application/json" -d '["yoda", "vader", "skywalker"]'
```

#### **Add Names to an Existing Theme**

```bash
curl -X POST "http://localhost:8000/add_names/starwars" -H "Content-Type: application/json" -d '["chewbacca", "han-solo"]'
```

#### **Delete a Theme**

```bash
curl -X DELETE "http://localhost:8000/remove_theme/starwars"
```

#### **Remove a Specific Name from a Theme**

```bash
curl -X DELETE "http://localhost:8000/remove_name/dc/joker"
```

#### **Update a Name within a Theme**

```bash
curl -X PUT "http://localhost:8000/update_name/dc?old_name=superman&new_name=man-of-steel"
```

---

## 🛠️ Automating Hostname Assignment on Raspberry Pi

This project supports **automatic hostname assignment** using **MQTT**. When a Raspberry Pi boots up, it can request a hostname from a specific theme and automatically set it.

### **1. Install Mosquitto MQTT Client**

```bash
sudo apt install mosquitto mosquitto-clients
```

### **2. Create the Auto-Hostname Script**

Save this as `/home/pi/get_hostname.sh`:

```bash
#!/bin/bash
THEME="dc"
MQTT_BROKER="mqtt"

# Request hostname
mosquitto_pub -h $MQTT_BROKER -t "hostname/request" -m "$THEME"

# Listen for response
mosquitto_sub -h $MQTT_BROKER -t "hostname/response/$THEME" -C 1 | xargs sudo hostnamectl set-hostname
```

### **3. Run the Script on Boot**

Edit `/etc/rc.local` and add:

```bash
bash /home/pi/get_hostname.sh &
```

Reboot the Raspberry Pi, and it will automatically request a hostname from the API! 🎉

---

## 🐳 Managing Containers

### **View Running Containers**

```bash
podman ps
```

### **Stop Everything**

```bash
podman-compose down
```

### **Rebuild Everything**

```bash
podman-compose up -d --build
```

### **View Logs**

```bash
podman logs backend
podman logs webui
```

---

## 🎯 Future Enhancements

- **✅ DNS Integration** – Auto-map hostnames to IP addresses
- **✅ Webhook Support** – Notify when a hostname is assigned
- **✅ More Themes** – Star Trek, Harry Potter, LOTR, Cyberpunk, etc.

---

## 📜 License

This project is **open-source** under the [MIT License](LICENSE).

---

## 🎉 Credits

Created with ❤️ by **Adam Stracener** 🚀
