const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");
const themeToggler = document.querySelector(".theme-toggler");


//show sidebar
menuBtn.addEventListener('click', () => {
  sideMenu.style.display = 'block';
})

//close sidebar
closeBtn.addEventListener('click', () => {
  sideMenu.style.display = 'none';
})

//change theme
themeToggler.addEventListener('click', () => {
  document.body.classList.toggle("dark-theme-variables");
  themeToggler.querySelector('span:nth-child(1)').classList.toggle("active");
  themeToggler.querySelector('span:nth-child(2)').classList.toggle("active");
})

document.addEventListener("DOMContentLoaded", function () {
  const sidebarLinks = document.querySelectorAll(".sidebar a");
  const defaultActiveLink = document.querySelector(".sidebar a:first-child");

  let currentPath = window.location.pathname;
  let activeLinkFound = false;

  sidebarLinks.forEach((link) => {
    const linkPath = new URL(link.href, window.location.origin).pathname;

    // Ensure the link has a valid href (not "#") before checking
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
      sidebarLinks.forEach((link) => link.classList.remove("active"));
      this.classList.add("active");
    });
  });
});


let currentIndex = 0;
function moveSlide(direction) {
  const slides = document.querySelectorAll('.slide');
  currentIndex = (currentIndex + direction + slides.length) % slides.length;
  document.querySelector('.carousel').style.transform = `translateX(-${currentIndex * 100}%)`;
}