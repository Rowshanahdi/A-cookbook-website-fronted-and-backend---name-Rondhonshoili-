
window.addEventListener("DOMContentLoaded", () => {
    const recipeImage = document.querySelector(".recipe-img img");
    recipeImage.addEventListener("click", () => {
      alert("You clicked the recipe image! Try it at home!");
    });
  });
  


  const stars = document.querySelectorAll('.stars i');

stars.forEach((star, index) => {
    star.addEventListener('click', () => {
        stars.forEach((s, i) => {
            s.classList.toggle('selected', i <= index);
        });
    });
});
