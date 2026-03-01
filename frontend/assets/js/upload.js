document.getElementById("uploadBtn")
.addEventListener("click", async () => {

    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(
        "http://localhost:8000/data/upload",
        {
            method: "POST",
            body: formData
        }
    );

    const data = await res.json();

    document.getElementById("uploadStatus")
        .innerText = "Uploaded: " + data.filename;
});