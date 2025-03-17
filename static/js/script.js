const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");
const themeToggler = document.querySelector(".theme-toggler");

// Show sidebar
if (menuBtn && sideMenu) {
  menuBtn.addEventListener("click", () => {
    sideMenu.style.display = "block";
  });
}

// Close sidebar
if (closeBtn && sideMenu) {
  closeBtn.addEventListener("click", () => {
    sideMenu.style.display = "none";
  });
}

// Change theme
if (themeToggler) {
  themeToggler.addEventListener("click", () => {
    document.body.classList.toggle("dark-theme-variables");

    const firstSpan = themeToggler.querySelector("span:nth-child(1)");
    const secondSpan = themeToggler.querySelector("span:nth-child(2)");

    if (firstSpan && secondSpan) {
      firstSpan.classList.toggle("active");
      secondSpan.classList.toggle("active");
    }
  });
}

// Ensure code runs after DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  const sidebarLinks = document.querySelectorAll(".sidebar a");
  const defaultActiveLink = document.querySelector(".sidebar a:first-child");

  let currentPath = window.location.pathname;
  let activeLinkFound = false;

  sidebarLinks.forEach((link) => {
    const linkPath = new URL(link.href, window.location.origin).pathname;

    if (linkPath !== "#" && linkPath === currentPath) {
      link.classList.add("active");
      activeLinkFound = true;
    }
  });

  if (!activeLinkFound && defaultActiveLink) {
    defaultActiveLink.classList.add("active");
  }

  sidebarLinks.forEach((link) => {
    link.addEventListener("click", function () {
      sidebarLinks.forEach((l) => l.classList.remove("active"));
      this.classList.add("active");
    });
  });
});

// Dropdown Menu
document.addEventListener("DOMContentLoaded", function () {
  const dropdownToggle = document.querySelector(".dropdown-toggle");
  const dropdownIcon = document.querySelector(".dropdown-icon");
  const dropdown = document.querySelector(".dropdown");

  dropdownToggle.addEventListener("click", function (e) {
    // Check if the dropdown icon was clicked
    if (e.target.classList.contains("dropdown-icon")) {
      e.preventDefault(); // Prevent default link behavior
      dropdown.classList.toggle("active"); // Toggle dropdown visibility
    }
    // If the link itself is clicked, it will navigate to the calendar page
  });

  // Close dropdown when clicking outside
  document.addEventListener("click", function (e) {
    if (!dropdown.contains(e.target)) {
      dropdown.classList.remove("active");
    }
  });
});

// TABS

function openTab(event, tabName) {
  let i, tabcontent, tablinks;

  tabcontent = document.getElementsByClassName("tab-content");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  tablinks = document.getElementsByClassName("tab-button");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  document.getElementById(tabName).style.display = "block";
  event.currentTarget.className += " active";
}

// Show the first tab by default
document.addEventListener("DOMContentLoaded", function () {
  document.getElementsByClassName("tab-button")[0].click();
});