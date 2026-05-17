let selectedCategory = "";

async function loadCategorySection() {
    const container = document.getElementById("categorySectionContainer");

    if (!container) {
        console.error("categorySectionContainer not found.");
        return;
    }

    const response = await fetch("components/category-section.html");
    const html = await response.text();

    container.innerHTML = html;

    initializeCategoryEvents();
}

function initializeCategoryEvents() {
    const categoryTiles = document.querySelectorAll(".category-tile");
    const customCategoryInput = document.getElementById("customCategoryInput");
    const selectedCategoryText = document.getElementById("selectedCategoryText");

    categoryTiles.forEach((tile) => {
        tile.addEventListener("click", function () {
            categoryTiles.forEach((item) => item.classList.remove("selected"));

            tile.classList.add("selected");

            selectedCategory = tile.dataset.category;

            customCategoryInput.value = "";

            updateSelectedCategoryText(selectedCategoryText);

            console.log("Selected category:", selectedCategory);
        });
    });

    customCategoryInput.addEventListener("input", function () {
        const customValue = customCategoryInput.value.trim();

        if (customValue) {
            categoryTiles.forEach((item) => item.classList.remove("selected"));
            selectedCategory = customValue.toLowerCase();
        } else {
            selectedCategory = "";
        }

        updateSelectedCategoryText(selectedCategoryText);

        console.log("Selected category:", selectedCategory);
    });
}

function updateSelectedCategoryText(selectedCategoryText) {
    if (!selectedCategory) {
        selectedCategoryText.textContent = "No category selected";
    } else {
        selectedCategoryText.textContent = `Selected category: ${selectedCategory}`;
    }
}

function getSelectedCategory() {
    return selectedCategory || null;
}

loadCategorySection();