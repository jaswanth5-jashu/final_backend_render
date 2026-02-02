document.addEventListener("DOMContentLoaded", function () {
  const typeField = document.getElementById("id_item_type");
  const workshopBox = document.querySelector(".workshop-fields");
  const galleryBox = document.querySelector(".gallery-fields");

  function toggle() {
    if (typeField.value === "workshop") {
      workshopBox.style.display = "block";
      galleryBox.style.display = "none";
    } else if (typeField.value === "gallery") {
      workshopBox.style.display = "none";
      galleryBox.style.display = "block";
    }
  }

  if (typeField) {
    toggle();
    typeField.addEventListener("change", toggle);
  }
});
