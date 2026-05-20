let productCardTemplate = "";

async function loadProductCardTemplate() {
    try {
        const response = await fetch("components/product-card.html");

        if (!response.ok) {
            throw new Error("Unable to load product card template.");
        }

        productCardTemplate = await response.text();

        console.log("Product card template loaded.");

    } catch (error) {
        console.error("Product card template error:", error);
    }
}

function formatProductPrice(price) {
    if (price === null || price === undefined || isNaN(Number(price))) {
        return "N/A";
    }

    return Number(price).toFixed(2);
}

function getSimilarityText(similarityScore) {
    if (similarityScore === null || similarityScore === undefined) {
        return "Category match";
    }

    return `${(similarityScore * 100).toFixed(1)}% match`;
}

function safeValue(value, fallback = "N/A") {
    if (value === null || value === undefined || value === "") {
        return fallback;
    }

    return String(value);
}

function buildProductCard(product) {
    const fallbackImage = "https://via.placeholder.com/400x300?text=Product";

    let card = productCardTemplate;

    card = card.replaceAll("{{image_url}}", safeValue(product.image_url, fallbackImage));
    card = card.replaceAll("{{name}}", safeValue(product.name, "Product"));
    card = card.replaceAll("{{source}}", safeValue(product.source, "Unknown"));
    card = card.replaceAll("{{brand}}", safeValue(product.brand, "Brand"));
    card = card.replaceAll("{{category}}", safeValue(product.category, "Category"));
    card = card.replaceAll("{{price}}", formatProductPrice(product.price));
    card = card.replaceAll("{{description}}", safeValue(product.description, "No description available."));
    card = card.replaceAll("{{rating}}", safeValue(product.rating, "N/A"));
    card = card.replaceAll("{{review_count}}", safeValue(product.review_count, "0"));
    card = card.replaceAll("{{similarity_text}}", getSimilarityText(product.similarity_score));
    card = card.replaceAll("{{availability}}", safeValue(product.availability, "Check availability"));
    card = card.replaceAll("{{product_url}}", safeValue(product.product_url, "#"));

    return card;
}

function renderProductCards(products) {
    const resultsContainer = document.getElementById("resultsContainer");

    if (!resultsContainer) {
        console.error("resultsContainer not found.");
        return;
    }

    if (!products || products.length === 0) {
        resultsContainer.innerHTML = `
            <div class="status-card">
                <h4>No products found</h4>
                <p>Try changing your query, category, or selected shopping sites.</p>
            </div>
        `;
        return;
    }

    if (!productCardTemplate) {
        resultsContainer.innerHTML = `
            <div class="status-card error-card">
                <h4>Product template not loaded</h4>
                <p>Please refresh the page or check product-card.html.</p>
            </div>
        `;
        return;
    }

    const productCardsHTML = products
        .map((product) => buildProductCard(product))
        .join("");

    resultsContainer.innerHTML = productCardsHTML;
}

function showLoadingState() {
    const resultsContainer = document.getElementById("resultsContainer");

    resultsContainer.innerHTML = `
        <div class="status-card">
            <h4>Searching products...</h4>
            <p>Please wait while ShopSmart finds the best matches.</p>
        </div>
    `;
}

function showErrorState(message) {
    const resultsContainer = document.getElementById("resultsContainer");

    resultsContainer.innerHTML = `
        <div class="status-card error-card">
            <h4>Something went wrong</h4>
            <p>${message}</p>
        </div>
    `;
}

loadProductCardTemplate();