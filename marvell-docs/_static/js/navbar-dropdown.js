/* Hover-to-open dropdowns for the top-level navbar section headlines
 * (About, Getting Started, etc.), listing each section's
 * sub-pages. Implemented in JS (rather than relying purely on a CSS
 * `:hover` selector) so behaviour is not at the mercy of specificity
 * fights with the theme's own bundled CSS, and so we can add a short
 * close-delay that keeps the menu open while the pointer travels from
 * the headline down into the menu itself. */
(function () {
  function init() {
    var dropdowns = document.querySelectorAll(".bd-navbar-dropdown");
    dropdowns.forEach(function (item) {
      var closeTimer = null;

      function open() {
        if (closeTimer) {
          clearTimeout(closeTimer);
          closeTimer = null;
        }
        item.classList.add("show-dropdown");
      }

      function scheduleClose() {
        if (closeTimer) {
          clearTimeout(closeTimer);
        }
        closeTimer = setTimeout(function () {
          item.classList.remove("show-dropdown");
        }, 150);
      }

      item.addEventListener("mouseenter", open);
      item.addEventListener("mouseleave", scheduleClose);
      item.addEventListener("focusin", open);
      item.addEventListener("focusout", scheduleClose);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
