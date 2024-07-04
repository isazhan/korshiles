function loadOptions(callback) {
fetch('../../static/base/cities.json')
    .then(response => response.json())
    .then(callback)
    .catch(error => console.error('Error loading options:', error));
}

function populateSelect(select, items) {
select.innerHTML = '<option value=""></option>';
items.forEach(item => {
    var option = new Option(item.name, item.id);
    select.add(option);
});
}

function loadCategories() {
loadOptions(data => populateSelect(document.getElementById('city'), data.cities));
}

function loadSubcategories() {
var categorySelect = document.getElementById('city');
var subcategorySelect = document.getElementById('district');
subcategorySelect.innerHTML = '<option value=""></option>';
var selectedCategory = categorySelect.value;
if (selectedCategory !== "") {
    loadOptions(data => {
    var selectedCategoryData = data.cities.find(category => category.id === selectedCategory);
    populateSelect(subcategorySelect, selectedCategoryData.districts);
    });
}
}

window.onload = loadCategories;