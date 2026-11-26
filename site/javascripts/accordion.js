document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.querySelector(".md-sidebar--primary");
  if (!sidebar) return;

  // Enforce single-open accordion behavior across every nesting level
  sidebar.addEventListener("change", (event) => {
    const target = event.target;
    if (!target.classList.contains("md-nav__toggle") || !target.checked) return;

    const currentItem = target.closest(".md-nav__item");
    const parentList = currentItem ? currentItem.parentElement : null;
    if (!parentList) return;

    Array.from(parentList.children).forEach((sibling) => {
      if (sibling !== currentItem) {
        const siblingToggle = sibling.querySelector(":scope > input.md-nav__toggle");
        if (siblingToggle && siblingToggle.checked) {
          siblingToggle.checked = false;
        }
      }
    });
  });
});
