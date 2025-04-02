document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll("abbr[title]").forEach(function(el) {
        el.setAttribute("data-title", el.getAttribute("title")); // Копируем title в data-title
        el.removeAttribute("title"); // Убираем стандартный тултип
    });
});