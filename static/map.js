((g) => {
  var h,
    a,
    k,
    p = "The Google Maps JavaScript API",
    c = "google",
    l = "importLibrary",
    q = "__ib__",
    m = document,
    b = window;
  b = b[c] || (b[c] = {});
  var d = b.maps || (b.maps = {}),
    r = new Set(),
    e = new URLSearchParams(),
    u = () =>
      h ||
      (h = new Promise(async (f, n) => {
        await (a = m.createElement("script"));
        e.set("libraries", [...r] + "");
        for (k in g)
          e.set(
            k.replace(/[A-Z]/g, (t) => "_" + t[0].toLowerCase()),
            g[k]
          );
        e.set("callback", c + ".maps." + q);
        a.src = `https://maps.${c}apis.com/maps/api/js?` + e;
        d[q] = f;
        a.onerror = () => (h = n(Error(p + " could not load.")));
        a.nonce = m.querySelector("script[nonce]")?.nonce || "";
        m.head.append(a);
      }));
  d[l]
    ? console.warn(p + " only loads once. Ignoring:", g)
    : (d[l] = (f, ...n) => r.add(f) && u().then(() => d[l](f, ...n)));
})({
  key: "AIzaSyCjwKcGho_HjOMWI8dtcvejbMNyPWv4AnU",
});

// Initialize and add the map
let map;
const apiKey = "AIzaSyCjwKcGho_HjOMWI8dtcvejbMNyPWv4AnU";
async function initMap() {
  // The location of US
  const position = { lat: 39.8283, lng: -98.5795 };
  // Request needed libraries.
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");
  const { Marker } = await google.maps.importLibrary("marker");

  // The map, centered at US
  map = new Map(document.getElementById("map"), {
    zoom: 3.75,
    center: position,
    mapId: "DEMO_MAP_ID",
  });

  const resp = await axios.get("/api/v1/user_id");
  user_id = resp.data["user_id"];

  // Get job locations from API
  const response = await axios.get(`/api/v1/users/${user_id}/jobs/locations`);
  const locations = JSON.parse(await response.data.jobs);
  console.log(locations);

  // Create markers for each job location
  locations.forEach(async (location) => {
    console.log(location);
    // make a request to the Geocoding API
    // @todo: lets get rid of this API hit inside a loop
    const response = await axios.get(
      `https://maps.googleapis.com/maps/api/geocode/json?address=${location}&key=${apiKey}`
    );

    // get the response data as JSON
    const data = await response.data;

    // check if there are any results before accessing the first result's geometry
    if (data.results.length > 0) {
      // extract the latitude and longitude from the response data
      const { lat, lng } = data.results[0].geometry.location;
      console.log(lat);
      // create a new marker
      const marker = new Marker({
        map: map,
        position: { lat, lng },
        title: location.title,
      });

      google.maps.event.addListener(marker, "click", function () {
        window.location.href = "https://google.com";
      });
    }
  });
}

initMap();
