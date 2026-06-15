/* RiceCookey — site interactions */
(function () {
  "use strict";

  /* --- footer year --- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* --- scroll reveals --- */
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var reveals = document.querySelectorAll(".reveal");

  if (reduce || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });

    reveals.forEach(function (el) { io.observe(el); });
  }

  /* --- contact form (AJAX via FormSubmit, with graceful fallback) --- */
  var form = document.getElementById("contact-form");
  var status = document.getElementById("form-status");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    // If fetch is unavailable, let the browser POST normally.
    if (!window.fetch) return;

    e.preventDefault();

    // Honeypot: silently drop bot submissions.
    if (form.querySelector('[name="_honey"]').value) return;

    var btn = form.querySelector('button[type="submit"]');
    var original = btn.textContent;
    btn.disabled = true;
    btn.textContent = "Sending…";
    status.textContent = "";
    status.className = "form__status";

    var endpoint = "https://formsubmit.co/ajax/ricecookey.official@gmail.com";

    fetch(endpoint, {
      method: "POST",
      headers: { "Accept": "application/json", "Content-Type": "application/json" },
      body: JSON.stringify({
        name: form.name.value,
        email: form.email.value,
        message: form.message.value,
        _subject: "New message from ricecookey.io",
        _template: "table"
      })
    })
      .then(function (res) { return res.json(); })
      .then(function () {
        form.reset();
        status.textContent = "Thanks — your message is on its way. We'll be in touch.";
        status.classList.add("is-ok");
      })
      .catch(function () {
        status.textContent =
          "Something went wrong. Please email us directly at ricecookey.official@gmail.com.";
        status.classList.add("is-err");
      })
      .finally(function () {
        btn.disabled = false;
        btn.textContent = original;
      });
  });
})();
