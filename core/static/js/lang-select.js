document.addEventListener("DOMContentLoaded", () => {
  // Language select
  const selected = document.getElementById("selectedLang");
  const options = document.getElementById("langOptions");
  const langInput = document.getElementById("languageInput");
  const langForm = document.getElementById("langForm");

  if (selected && options && langInput && langForm) {
    selected.addEventListener("click", () => {
      options.style.display = options.style.display === "block" ? "none" : "block";
    });

    options.querySelectorAll("li").forEach(li => {
        li.addEventListener("click", (event) => {
          const lang = li.getAttribute("data-value");

          selected.textContent = li.textContent;
          langInput.value = lang;

          options.style.display = "none";

          setTimeout(() => {
            langForm.submit();
          }, 50);
        });
    });

    document.addEventListener("click", e => {
      if (!e.target.closest(".custom-select")) {
        options.style.display = "none";
      }
    });
  }
});