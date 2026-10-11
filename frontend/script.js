
 // ===== Member 1: Frontend UI =====

 const slider = document.getElementById('distance');
 const distanceValue = document.getElementById('distanceValue');
 const status = document.getElementById('status');
 const statusTitle = document.getElementById('statusTitle');
 const statusText = document.getElementById('statusText');
 const popup = document.getElementById('offerPopup');
 const offerText = document.getElementById('offerText');

 // Start simulation button
 document.getElementById('startBtn').addEventListener('click', () => {
   document.getElementById('demo').scrollIntoView({
     behavior: 'smooth'
   });
   slider.focus({ preventScroll: true });
 });

 // Show promotional offer
 function showOffer(text) {
   offerText.textContent = text;
   popup.hidden = false;

   status.className = 'status in';
   statusTitle.textContent = 'Inside beacon range';
   statusText.textContent =
     'You are close to the café. Your offer is ready!';
 }

 // Hide promotional offer
 function hideOffer() {
   popup.hidden = true;

   status.className = 'status out';
   statusTitle.textContent = 'Outside beacon range';
   statusText.textContent =
     'Move within 10 metres to unlock your café offer.';
 }

 // ===== Member 2: Beacon Simulation Integration =====
 // Uses checkProximity() from simulation/beacon.js

 // ===== Member 3: Backend =====
 // Temporary offer until backend is connected
 let currentOffer = 'Welcome! Get 20% OFF on Coffee!';

 // Distance slider functionality
 slider.addEventListener('input', () => {
   const distance = Number(slider.value);

   distanceValue.textContent = distance;

   const result = window.checkProximity(distance);

   if (result === 'OFFER_AVAILABLE') {
     showOffer(currentOffer);
   } else {
     hideOffer();
   }
 });

 // Check initial distance
 slider.dispatchEvent(new Event('input'));


 
