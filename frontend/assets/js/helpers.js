const modelType = document.getElementById("modelType");
const degreeSlider = document.getElementById("degree").parentElement.parentElement;

modelType.addEventListener("change", () => {

    if(modelType.value === "polynomial"){
        degreeSlider.style.display = "block";
    } else {
        degreeSlider.style.display = "none";
    }

});