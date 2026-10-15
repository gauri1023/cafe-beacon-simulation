
 // Virtual Bluetooth Beacon for our Café
 const cafeBeacon = {
   id: "CAFE001",
   name: "Cafe Beacon",
   range: 10,
   active: true
 };

 // Check customer's simulated distance from café
 function checkProximity(distance) {
   if (!Number.isFinite(distance) || distance < 0 || distance > 100) {
     return "INVALID_DISTANCE";
   }

   if (!cafeBeacon.active) {
     return "BEACON_INACTIVE";
   }

   if (distance <= cafeBeacon.range) {
     return "OFFER_AVAILABLE";
   }

   return "OUT_OF_RANGE";
 }

 // Test our virtual beacon
 console.log("Beacon:", cafeBeacon.name);
 console.log("5 metres:", checkProximity(5));
 console.log("20 metres:", checkProximity(20));
