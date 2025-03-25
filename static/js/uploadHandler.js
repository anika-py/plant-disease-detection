document.addEventListener("DOMContentLoaded", function () {
    const uploadBtn = document.getElementById("uploadBtn");
    const fileInput = document.getElementById("imageUpload");
    const fileNameDisplay = document.getElementById("fileName");

    uploadBtn.addEventListener("click", function () {
        if (uploadBtn.innerText === "Get Diagnosis") {
            fetch("/predict", { method: "POST" }) // Trigger prediction on backend
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.href = data.redirect_url; // Redirect based on model output
                    } else {
                        alert("Prediction failed: " + data.error);
                    }
                })
                .catch(error => console.error("Error:", error));
        } else {
            fileInput.click(); // Open file dialog
        }
    });

    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            fileNameDisplay.innerText = "Uploaded: " + file.name;
            fileNameDisplay.style.display = "block";
            uploadBtn.innerText = "Get Diagnosis";

            const formData = new FormData();
            formData.append("file", file);

            fetch("/upload", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    alert("Upload failed: " + data.error);
                }
            })
            .catch(error => console.error("Error:", error));
        }
    });
});