/* RiceCookey — site interactions */
(function () {
  "use strict";

  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  var form = document.getElementById("contact-form");
  var status = document.getElementById("form-status");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    if (!window.fetch) return;

    e.preventDefault();

    if (form.querySelector('[name="_honey"]').value) return;

    var btn = form.querySelector('button[type="submit"]');
    var original = btn.textContent;
    btn.disabled = true;
    btn.textContent = "Sending…";
    status.textContent = "";
    status.className = "form__status";

    fetch("https://formsubmit.co/ajax/ricecookey.official@gmail.com", {
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
        status.textContent = "Thanks! Your message is on its way — we'll get back to you soon.";
        status.classList.add("is-ok");
      })
      .catch(function () {
        status.textContent =
          "Something went wrong. Please email ricecookey.official@gmail.com directly.";
        status.classList.add("is-err");
      })
      .finally(function () {
        btn.disabled = false;
        btn.textContent = original;
      });
  });
})();
