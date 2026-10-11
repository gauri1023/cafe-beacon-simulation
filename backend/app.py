from flask import Flask, jsonify, request
try:
    from flask_cors import CORS
    CORS_AVAILABLE = True
except ImportError:
    CORS_AVAILABLE = False

from database import (
    init_db,
    get_cafe_details,
    get_beacon_by_id,
    get_all_beacons,
    get_offer_by_beacon,
    get_all_offers
)

app = Flask(__name__)

# Initialize CORS
if CORS_AVAILABLE:
    CORS(app, resources={r"/*": {"origins": "*"}})

# Ensure CORS headers are present on all responses regardless of environment
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

@app.route("/", methods=["GET"])
def index():
    """API Root endpoint."""
    return jsonify({
        "name": "Beacon Brew Café API",
        "version": "1.0.0",
        "status": "online",
        "description": "Backend API providing café details, beacon configurations, and proximity offers.",
        "endpoints": {
            "cafe_details": "/api/cafe",
            "all_beacons": "/api/beacons",
            "specific_beacon": "/api/beacons/<beacon_id>",
            "offer_by_beacon": "/api/offer/<beacon_id> (e.g. /api/offer/CAFE001)",
            "all_offers": "/api/offers",
            "health_check": "/api/health"
        }
    })

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "cafe-beacon-api"
    }), 200

@app.route("/api/cafe", methods=["GET"])
def get_cafe():
    """Retrieve details for Beacon Brew Café."""
    cafe = get_cafe_details()
    if not cafe:
        return jsonify({"status": "error", "message": "Café details not found"}), 404
    return jsonify({
        "status": "success",
        "cafe": cafe
    }), 200

@app.route("/api/beacons", methods=["GET"])
def get_beacons():
    """Retrieve all registered beacons."""
    beacons = get_all_beacons()
    return jsonify({
        "status": "success",
        "count": len(beacons),
        "beacons": beacons
    }), 200

@app.route("/api/beacons/<beacon_id>", methods=["GET"])
def get_beacon(beacon_id):
    """Retrieve specific beacon by ID."""
    beacon = get_beacon_by_id(beacon_id.upper())
    if not beacon:
        return jsonify({
            "status": "error",
            "message": f"Beacon '{beacon_id}' not found"
        }), 404
    return jsonify({
        "status": "success",
        "beacon": beacon
    }), 200

@app.route("/api/offer/<beacon_id>", methods=["GET"])
def get_offer_for_beacon(beacon_id):
    """Retrieve the proximity offer for a specific beacon ID (e.g., CAFE001)."""
    beacon_id_upper = beacon_id.upper()
    offer = get_offer_by_beacon(beacon_id_upper)
    cafe = get_cafe_details()

    if not offer:
        return jsonify({
            "status": "error",
            "beacon_id": beacon_id_upper,
            "message": f"No active offer found for beacon '{beacon_id_upper}'"
        }), 404

    return jsonify({
        "status": "success",
        "beacon_id": beacon_id_upper,
        "offer": offer["title"],
        "offer_text": offer["title"],
        "discount": offer["discount"],
        "item": offer["item"],
        "promo_code": offer["promo_code"],
        "description": offer["description"],
        "beacon_name": offer.get("beacon_name"),
        "range_meters": offer.get("range_meters"),
        "cafe": cafe
    }), 200

@app.route("/api/offer", methods=["GET"])
def get_default_offer():
    """Default offer endpoint - returns CAFE001 offer."""
    return get_offer_for_beacon("CAFE001")

@app.route("/api/offers", methods=["GET"])
def get_offers():
    """Retrieve all offers in the system."""
    offers = get_all_offers()
    return jsonify({
        "status": "success",
        "count": len(offers),
        "offers": offers
    }), 200

if __name__ == "__main__":
    # Initialize the database on startup
    init_db()
    print("Database initialized successfully.")
    print("Starting Beacon Brew Café Backend API on http://127.0.0.1:5000")
    print("Serving offer for Beacon CAFE001 at http://127.0.0.1:5000/api/offer/CAFE001")
    app.run(host="0.0.0.0", port=5000, debug=True)
