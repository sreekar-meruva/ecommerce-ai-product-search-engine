const searchButton = document.getElementById("searchButton");
const queryInput = document.getElementById("queryInput");
const resultsContainer = document.getElementById("resultsContainer");
const sourceTiles = document.querySelectorAll(".source-tile");

const API_URL = "http://127.0.0.1:8000/search";

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

function buildSearchPayload() {
    const query = queryInput.value.trim();

    const selectedCategory =
        typeof getSelectedCategory === "function"
            ? getSelectedCategory()
            : null;

    return {
        query: query,
        category: selectedCategory,
        sources: selectedSources,
        min_price: null,
        max_price: null,
        min_rating: null,
        top_k: 10
    };
}

async function searchProducts() {
    const payload = buildSearchPayload();

    console.log("Search button clicked");
    console.log("Sending payload:", payload);

    if (selectedSources.length === 0) {
        showErrorState("Please select at least one shopping site.");
        return;
    }

    if (!payload.query && !payload.category) {
        showErrorState("Please enter a search query or select a category.");
        return;
    }

    showLoadingState();

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        console.log("API response:", data);
        console.log(data.results);

        if (!response.ok) {
            throw new Error(data.detail || "API request failed.");
        }

        renderProductCards(data.results);

    } catch (error) {
        console.error("Search error:", error);
        showErrorState(error.message);
    }
}

searchButton.addEventListener("click", searchProducts);

queryInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        searchProducts();
    }
});