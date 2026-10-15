# Beacon Brew Café - Backend API (Member 3)

This is the backend server for the Beacon Brew Café Proximity Beacon Simulation project. It provides REST API endpoints to manage and serve café details, beacon metadata, and proximity offers.

---

## Features & Responsibilities

1. **Store Café Details**: Stores café metadata (name, address, contact, operating hours, description) in SQLite (`cafe.db`).
2. **Store Beacon ID (`CAFE001`)**: Configures the entrance beacon with ID `CAFE001`, location, signal range (10 meters), and status.
3. **Store Offer (`20% OFF on coffee`)**: Associates beacon `CAFE001` with the active promotional offer of 20% discount on coffee.
4. **Offer API**: Exposes `GET /api/offer/CAFE001` to provide real-time offer information to the frontend.
5. **CORS Enabled**: Configured with Cross-Origin Resource Sharing (`flask-cors` and HTTP headers) for seamless communication with the frontend client.

---

## Project Structure

```
backend/
├── app.py             # Main Flask application with API routes & CORS handling
├── database.py        # SQLite database schema, initialization, and queries
├── cafe.db            # Auto-generated SQLite database file
├── requirements.txt   # Python dependencies
└── README.md          # Backend documentation
```

---

## Setup & Running

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python app.py
```

The server will initialize the SQLite database (`cafe.db`) automatically and start listening on:
`http://127.0.0.1:5000`

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API status and overview of available endpoints |
| `GET` | `/api/offer/CAFE001` | Returns the active 20% OFF coffee offer for Beacon `CAFE001` |
| `GET` | `/api/offer` | Alias endpoint returning the active café offer |
| `GET` | `/api/cafe` | Returns Beacon Brew Café details |
| `GET` | `/api/beacons` | Returns all registered beacons |
| `GET` | `/api/beacons/CAFE001` | Returns details for beacon `CAFE001` |
| `GET` | `/api/health` | Health check endpoint |

---

## Example API Response (`GET /api/offer/CAFE001`)

```json
{
  "status": "success",
  "beacon_id": "CAFE001",
  "offer": "Welcome! Get 20% OFF on Coffee!",
  "offer_text": "Welcome! Get 20% OFF on Coffee!",
  "discount": "20% OFF",
  "item": "Coffee",
  "promo_code": "BEACON20",
  "description": "20% OFF on any coffee for customers within 10 m.",
  "range_meters": 10,
  "beacon_name": "Main Entrance Beacon",
  "cafe": {
    "name": "Beacon Brew Café",
    "address": "12 Coffee Lane, University Campus",
    "phone": "+91 98765 43210",
    "email": "hello@beaconbrew.cafe",
    "opening_hours": "08:00 AM - 10:00 PM"
  }
}
```
