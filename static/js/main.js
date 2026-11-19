
document.addEventListener("DOMContentLoaded", function () {

  // MOBILE NAVIGATION
  const menuButton = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav");

  if (menuButton && nav) {

    menuButton.addEventListener("click", function () {
      const isOpen = nav.classList.toggle("is-open");

      menuButton.setAttribute("aria-expanded", String(isOpen));
      menuButton.textContent = isOpen ? "✕" : "☰";
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        nav.classList.remove("is-open");
        menuButton.setAttribute("aria-expanded", "false");
        menuButton.textContent = "☰";
      });
    });

    document.addEventListener("click", function (event) {
      if (
        !nav.contains(event.target) &&
        !menuButton.contains(event.target)
      ) {
        nav.classList.remove("is-open");
        menuButton.setAttribute("aria-expanded", "false");
        menuButton.textContent = "☰";
      }
    });
  }

  // COURSE SELECTION
  document.querySelectorAll(".course-link").forEach(function (link) {

    link.addEventListener("click", function () {

      const courseSelect = document.getElementById("course_interest");

      if (courseSelect) {
        const selectedCourse = link.dataset.course;

        Array.from(courseSelect.options).forEach(function (option) {
          if (option.text.trim() === selectedCourse.trim()) {
            courseSelect.value = option.value;
          }
        });
      }

    });

  });

  // AUTOMATIC COPYRIGHT YEAR
  const year = document.getElementById("year");

  if (year) {
    year.textContent = new Date().getFullYear();
  }

  // MOBILE NUMBER VALIDATION
  const form = document.getElementById("admissionForm");

  if (form) {

    form.addEventListener("submit", function (event) {

      const mobile = document.getElementById("mobile");

      if (!mobile) return;

      const digits = mobile.value.replace(/\D/g, "");

      if (digits.length !== 10) {

        event.preventDefault();

        mobile.setCustomValidity(
          "Please enter a valid 10-digit mobile number."
        );

        mobile.reportValidity();

      } else {

        mobile.setCustomValidity("");

      }

    });

    const mobile = document.getElementById("mobile");

    if (mobile) {
      mobile.addEventListener("input", function () {
        mobile.setCustomValidity("");
      });
    }

  }

});
