function initDashboard() {

    const container = document.querySelector("#salesDataContainer");
    const canvas = document.querySelector("#salesChart");

    if (!container || !canvas) return;

    if (typeof Chart === "undefined") {
        console.error("Chart.js is not loaded");
        return;
    }

    const labels = (container.dataset.labels || "")
        .split(",")
        .filter(x => x.trim() !== "");

    const values = (container.dataset.values || "")
        .split(",")
        .map(x => Number(x))
        .filter(x => !isNaN(x));

    new Chart(canvas, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Revenue (€)',
                data: values,
                borderWidth: 2
            }]
        }
    });

    // ================= ARROW COLLAPSE =================
    document.querySelectorAll(".order-toggle").forEach(toggle => {

        const targetId = toggle.dataset.bsTarget;
        const target = document.querySelector(targetId);
        const icon = toggle.querySelector(".arrow-icon");

        if (!target || !icon) return;

        target.addEventListener("show.bs.collapse", () => {
            icon.classList.add("rotate");
        });

        target.addEventListener("hide.bs.collapse", () => {
            icon.classList.remove("rotate");
        });

    });

}

// ================= CATEGORY FILTER (ADMIN BOOKS) =================
function initCategoryFilter() {

    const parent = document.querySelector("#parentCategory");
    const sub = document.querySelector("#subCategory");

    if (!parent || !sub) return;

    function filterSubcategories() {

        const parentId = parent.value;

        sub.querySelectorAll("option").forEach(option => {

            if (!option.value) return; // skip "All"

            if (option.dataset.parent === parentId) {
                option.style.display = "block";
            } else {
                option.style.display = "none";
            }

        });

        // reset subcategory when parent changes
        sub.value = "";
    }

    parent.addEventListener("change", filterSubcategories);

    // run on page load
    filterSubcategories();
}

function initAutoCategoryFilter() {

    const categorySelect = document.querySelector("#categoryFilter");

    if (!categorySelect) return;

    function handleCategoryChange(event) {
        event.target.form.submit();
    }

    categorySelect.addEventListener("change", handleCategoryChange);
}

// ================= MODAL  =================

function initDeleteModal() {

    const deleteButtons = document.querySelectorAll(".js-delete-book");
    const confirmBtn = document.querySelector("#confirmDeleteBtn");
    const modalElement = document.querySelector("#deleteModal");

    if (!deleteButtons.length || !confirmBtn || !modalElement) return;

    function handleDeleteClick(event) {

        event.preventDefault();

        const url = event.currentTarget.dataset.url;

        confirmBtn.href = url;

        const modal = bootstrap.Modal.getOrCreateInstance(modalElement);
        modal.show();
    }

    deleteButtons.forEach(function (btn) {
        btn.addEventListener("click", handleDeleteClick);
    });
}


// ========================== PROFILE =======================
function initProfilePreview() {

    const input = document.querySelector("#id_image");
    const preview = document.querySelector("#previewImage");

    if (!input || !preview) return;

    input.addEventListener("change", handleImageChange);
}


// ================= HANDLE FILE CHANGE =================
function handleImageChange(event) {

    const file = getSelectedFile(event);

    if (!file) return;

    readImageFile(file, updatePreviewImage);
}


// ================= GET FILE FROM INPUT =================
function getSelectedFile(event) {
    return event.target.files[0];
}


// ================= READ FILE =================
function readImageFile(file, callback) {

    const reader = new FileReader();

    reader.onload = function (e) {
        callback(e.target.result);
    };

    reader.readAsDataURL(file);
}


// ================= UPDATE IMAGE PREVIEW =================
function updatePreviewImage(imageSrc) {

    const preview = document.querySelector("#previewImage");

    if (!preview) return;

    preview.src = imageSrc;
}


// ================= INIT =================



initDashboard();
initCategoryFilter();
initAutoCategoryFilter();
initDeleteModal();
initProfilePreview();