const searchButton = document.getElementById("searchButton");
const queryInput = document.getElementById("queryInput");
const resultsContainer = document.getElementById("resultsContainer");
const sourceTiles = document.querySelectorAll(".source-tile");

let selectedSources = [];

sourceTiles.forEach((tile) => {
    tile.addEventListener("click", function () {
        const sourceName = tile.textContent.trim();

        tile.classList.toggle("selected");

        if (selectedSources.includes(sourceName)) {
            selectedSources = selectedSources.filter((source) => source !== sourceName);
        } else {
            selectedSources.push(sourceName);
        }

        console.log("Selected sources:", selectedSources);
    });
});

searchButton.addEventListener("click", function () {
    const query = queryInput.value.trim();

    if (!query) {
        resultsContainer.innerHTML = `<p>Please enter a search query.</p>`;
        return;
    }

    if (selectedSources.length === 0) {
        resultsContainer.innerHTML = `<p>Please select at least one shopping site.</p>`;
        return;
    }

    resultsContainer.innerHTML = `
        <div style="
            background: rgba(255,255,255,0.14);
            border: 1px solid rgba(255,255,255,0.20);
            padding: 24px;
            border-radius: 20px;
            color: white;
            backdrop-filter: blur(10px);
        ">
            <h4 style="margin-bottom: 12px;">Search Payload Preview</h4>
            <p><strong>Query:</strong> ${query}</p>
            <p><strong>Selected Sources:</strong> ${selectedSources.join(", ")}</p>
        </div>
    `;

    console.log("Query:", query);
    console.log("Selected sources:", selectedSources);
});