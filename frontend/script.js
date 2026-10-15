
 // ===== Member 1: Frontend UI =====
const slider = document.getElementById('distance');
const distanceValue = document.getElementById('distanceValue');
const status = document.getElementById('status');
const statusTitle = document.getElementById('statusTitle');
const statusText = document.getElementById('statusText');
const popup = document.getElementById('offerPopup');
const offerText = document.getElementById('offerText');

document.getElementById('startBtn').addEventListener('click', () => {
  document.getElementById('demo').scrollIntoView({
    behavior: 'smooth'
  });
  slider.focus({ preventScroll: true });
});

function showOffer(text) {
  offerText.textContent = text;
  popup.hidden = false;
  status.className = 'status in';
  statusTitle.textContent = 'Inside beacon range';
  statusText.textContent = 'You are close to the café. Your offer is ready!';
}

function hideOffer() {
  popup.hidden = true;
  status.className = 'status out';
  statusTitle.textContent = 'Outside beacon range';
  statusText.textContent =
    'Move within 10 metres to unlock your café offer.';
}

// ===== Member 2: Beacon Simulation =====
// Uses checkProximity() from simulation/beacon.js

// ===== Member 3: Backend Integration =====
const BEACON_ID = 'CAFE001';
const API_URL = `http://127.0.0.1:5000/api/offer/${BEACON_ID}`;

let currentOffer = 'Welcome! Get 20% OFF on Coffee!';

function updateProximity() {
  const distance = Number(slider.value);
  distanceValue.textContent = distance;

  const result = window.checkProximity(distance);

  if (result === 'OFFER_AVAILABLE') {
    showOffer(currentOffer);
  } else {
    hideOffer();
  }
}

// Fetch offer from Flask backend
async function fetchOfferFromBackend() {
  try {
    const res = await fetch(API_URL);

    if (!res.ok) {
      throw new Error(`HTTP status ${res.status}`);
    }

    const data = await res.json();

    if (data.offer) {
      currentOffer = data.offer;
    } else if (data.offer_text) {
      currentOffer = data.offer_text;
    }

    updateProximity();
  } catch (error) {
    console.warn(
      'Backend connection failed, using default offer:',
      error
    );
  }
}

slider.addEventListener('input', updateProximity);

// Check initial distance
updateProximity();

// Get the latest offer from backend
fetchOfferFromBackend();
