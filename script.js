/* RiceCookey — site interactions & i18n */
(function () {
  "use strict";

  var STORAGE_KEY = "ricecookey-lang";
  var currentLang = "en";

  function detectLang() {
    var saved = localStorage.getItem(STORAGE_KEY);
    if (saved === "ko" || saved === "en") return saved;
    return (navigator.language || "").toLowerCase().startsWith("ko") ? "ko" : "en";
  }

  function t(key) {
    var dict = window.RC_I18N[currentLang];
    return (dict && dict[key]) || (window.RC_I18N.en[key]) || key;
  }

  function applyLang(lang) {
    if (!window.RC_I18N[lang]) return;
    currentLang = lang;
    localStorage.setItem(STORAGE_KEY, lang);
    document.documentElement.lang = lang;

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      el.textContent = t(el.getAttribute("data-i18n"));
    });

    document.querySelectorAll("[data-i18n-html]").forEach(function (el) {
      el.innerHTML = t(el.getAttribute("data-i18n-html"));
    });

    document.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
      el.placeholder = t(el.getAttribute("data-i18n-placeholder"));
    });

    document.querySelectorAll("[data-i18n-aria]").forEach(function (el) {
      el.setAttribute("aria-label", t(el.getAttribute("data-i18n-aria")));
    });

    var title = t("meta.title");
    var desc = t("meta.description");
    document.title = title;
    var metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) metaDesc.setAttribute("content", desc);

    var footerCopy = document.querySelector("[data-i18n-footer]");
    if (footerCopy) {
      var year = new Date().getFullYear();
      footerCopy.innerHTML = t("footer.copy").replace("{year}", '<span id="year">' + year + "</span>");
    }

    document.querySelectorAll(".lang-switch__btn").forEach(function (btn) {
      var active = btn.getAttribute("data-lang") === lang;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    });
  }

  function initLangSwitch() {
    var group = document.querySelector(".lang-switch");
    if (!group) return;
    group.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-lang]");
      if (!btn) return;
      applyLang(btn.getAttribute("data-lang"));
    });
  }

  applyLang(detectLang());
  initLangSwitch();

  var form = document.getElementById("contact-form");
  var status = document.getElementById("form-status");

  if (form) {
    form.addEventListener("submit", function (e) {
      if (!window.fetch) return;

      e.preventDefault();

      if (form.querySelector('[name="_honey"]').value) return;

      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      btn.textContent = t("contact.sending");
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
          status.textContent = t("contact.success");
          status.classList.add("is-ok");
        })
        .catch(function () {
          status.textContent = t("contact.error");
          status.classList.add("is-err");
        })
        .finally(function () {
          btn.disabled = false;
          btn.textContent = t("contact.submit");
        });
    });
  }

  window.RC_setLang = applyLang;
  window.RC_t = t;
})();
