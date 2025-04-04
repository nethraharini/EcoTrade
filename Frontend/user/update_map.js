async function updateMap(material, color) {
    // Load the JSON data from data.json
    const response = await fetch("data.json");
    const data = await response.json();

    // Get the selected material data
    const materialData = data[material];

    // Update the map dynamically
    document.getElementById("mapFrame").contentWindow.postMessage({ materialData, color }, "*");
}

// Listen for messages in map.html to update the map dynamically
window.addEventListener("message", (event) => {
    const { materialData, color } = event.data;
    const mapFrame = document.getElementById("mapFrame").contentWindow;

    // Apply new styles to districts based on material data
    mapFrame.document.querySelectorAll(".leaflet-interactive").forEach((district) => {
        const districtName = district.getAttribute("title").toLowerCase();
        const tons = materialData[districtName] || 0;
        const opacity = tons > 0 ? 0.7 : 0.1;

        district.style.fill = color;
        district.style.fillOpacity = opacity;
    });
});
