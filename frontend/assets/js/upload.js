document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById("uploadArea");
    const fileInput = document.getElementById("fileInput");
    const statusElement = document.getElementById("uploadStatus");
    const uploadedFilesContainer = document.getElementById("uploadedFiles");

    // Click to upload
    uploadArea.addEventListener("click", () => {
        fileInput.click();
    });

    // Handle file selection
    fileInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) {
            uploadFile(file);
        }
    });

    // Drag and drop
    uploadArea.addEventListener("dragover", (e) => {
        e.preventDefault();
        uploadArea.classList.add("dragover");
    });

    uploadArea.addEventListener("dragleave", () => {
        uploadArea.classList.remove("dragover");
    });

    uploadArea.addEventListener("drop", (e) => {
        e.preventDefault();
        uploadArea.classList.remove("dragover");
        const file = e.dataTransfer.files[0];
        console.log("Dropped file:", file);
        if (file) {
            uploadFile(file);
        }
    });

    async function uploadFile(file) {
        // Validar que se haya seleccionado un archivo
        if (!file) {
            statusElement.innerText = "Error: Por favor selecciona un archivo";
            statusElement.classList.add("error");
            statusElement.classList.remove("success");
            return;
        }

        // Validar que sea un archivo CSV
        if (!file.name.toLowerCase().endsWith('.csv')) {
            statusElement.innerText = "Error: Solo se permiten archivos CSV";
            statusElement.classList.add("error");
            statusElement.classList.remove("success");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            const res = await fetch(
                "http://localhost:8000/data/upload",
                {
                    method: "POST",
                    body: formData
                }
            );

            // Validar que la respuesta sea exitosa
            if (!res.ok) {
                const errorData = await res.json();
                statusElement.innerText = `Error: ${errorData.detail || 'No se pudo cargar el archivo'}`;
                statusElement.classList.add("error");
                statusElement.classList.remove("success");
                return;
            }

            const data = await res.json();

            // Validar que la respuesta contenga el filename
            if (!data.filename) {
                statusElement.innerText = "Error: Respuesta inválida del servidor";
                statusElement.classList.add("error");
                statusElement.classList.remove("success");
                return;
            }

            // Mostrar archivo subido
            displayUploadedFile(data.filename, file.size);
            fileInput.value = "";
            statusElement.innerText = "Archivo cargado correctamente";
            statusElement.classList.add("success");
            statusElement.classList.remove("error");

        } catch (error) {
            statusElement.innerText = "Error: " + error.message;
            statusElement.classList.add("error");
            statusElement.classList.remove("success");
        }
    }

    function displayUploadedFile(filename, fileSize) {
        const fileSizeKB = (fileSize / 1024).toFixed(2);
        const fileItem = document.createElement("div");
        fileItem.className = "file-item";
        fileItem.innerHTML = `
            <div class="file-info">
                <span class="file-icon">📄</span>
                <div class="file-details">
                    <span class="file-name">${filename}</span>
                    <span class="file-size">${fileSizeKB} KB · Uploaded 0s ago</span>
                </div>
            </div>
            <span class="file-status">✓ Ready</span>
        `;
        uploadedFilesContainer.innerHTML = "";
        uploadedFilesContainer.appendChild(fileItem);
    }
});