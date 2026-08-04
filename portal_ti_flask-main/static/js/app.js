const sidebar = document.getElementById("sidebar");
const sidebarToggle = document.getElementById("sidebarToggle");
const sidebarBackdrop = document.getElementById("sidebarBackdrop");

function closeSidebar() {
    sidebar?.classList.remove("open");
    sidebarBackdrop?.classList.remove("show");
}

sidebarToggle?.addEventListener("click", () => {
    sidebar?.classList.toggle("open");
    sidebarBackdrop?.classList.toggle("show");
});

sidebarBackdrop?.addEventListener("click", closeSidebar);
