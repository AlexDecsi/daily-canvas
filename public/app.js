// The Daily Canvas — gallery front end.
// Loads entries.json (built by src/pipeline/build_site.py), shows the newest
// entry as the featured artwork, the rest as a newest-first grid, and opens a
// detail view at #/YYYY-MM-DD so every entry has a shareable link.
//
// All entry text is inserted with textContent (never innerHTML) so content can
// never inject markup into the page.

(function () {
  "use strict";

  const featuredEl = document.getElementById("featured");
  const gridEl = document.getElementById("grid");
  const dialog = document.getElementById("detail");
  let entries = [];
  let lastFocus = null;

  // ---------- helpers ----------

  function el(tag, props, children) {
    const node = document.createElement(tag);
    Object.assign(node, props || {});
    (children || []).forEach((c) => c && node.append(c));
    return node;
  }

  // Format "2026-10-24" as "Saturday, October 24, 2026" without timezone
  // shifting (the date is already a Boston news date, not a timestamp).
  function formatDate(iso) {
    const [y, m, d] = iso.split("-").map(Number);
    return new Date(Date.UTC(y, m - 1, d)).toLocaleDateString("en-US", {
      weekday: "long", year: "numeric", month: "long", day: "numeric", timeZone: "UTC",
    });
  }

  function artwork(entry) {
    const art = entry.artwork || {};
    if (!art.path) {
      return el("div", { className: "missing-art", textContent: "Artwork unavailable" });
    }
    const img = el("img", { src: art.path, alt: art.alt || entry.title || "Untitled illustration" });
    img.decoding = "async";
    img.addEventListener("error", () => {
      img.replaceWith(el("div", { className: "missing-art", textContent: "Artwork could not be loaded" }));
    });
    return img;
  }

  function sourcesList(entry) {
    const links = [];
    (entry.stories || []).forEach((story) => {
      (story.sources || []).forEach((s) => {
        if (s.url) links.push(el("li", {}, [el("a", { href: s.url, textContent: s.publisher || s.url, rel: "noopener", target: "_blank" }),
          s.title ? document.createTextNode(" — " + s.title) : null]));
      });
    });
    if (!links.length) return el("p", { textContent: "Sources not listed." });
    return el("div", {}, [el("span", { textContent: "Sources" }), el("ul", {}, links)]);
  }

  function backfillNote(entry) {
    if (entry.status !== "backfilled") return "";
    // Show the creation day in Boston time, like the news date (a UTC timestamp can already be "tomorrow").
    const when = entry.published_at
      ? new Date(entry.published_at).toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric", timeZone: "America/New_York" })
      : "a later date";
    const newsDay = formatDate(entry.date).replace(/^\w+, /, "");
    return "Created after its news date (on " + when + "), using only reporting available on " + newsDay + ".";
  }

  // ---------- featured + grid ----------

  function renderFeatured(entry) {
    const open = el("button", { className: "featured-open", type: "button" }, [el("div", { className: "frame" }, [artwork(entry)])]);
    open.setAttribute("aria-label", "Enlarge: " + entry.title);
    open.addEventListener("click", () => openDetail(entry.date));

    const more = el("button", { className: "more-link", type: "button", textContent: "View sources and details" });
    more.addEventListener("click", () => openDetail(entry.date));

    const note = backfillNote(entry);
    const label = el("figcaption", { className: "label" }, [
      el("p", { className: "label-date", textContent: "Latest · " + formatDate(entry.date) }),
      el("h2", { className: "label-title", textContent: entry.title || "Untitled" }),
      el("p", { className: "label-caption", textContent: entry.caption || "" }),
      note ? el("p", { className: "label-note", textContent: note }) : null,
      more,
    ]);
    featuredEl.replaceChildren(el("figure", { className: "featured-figure" }, [open, label]));
  }

  function renderGrid(rest) {
    if (!rest.length) {
      gridEl.replaceChildren(el("li", { className: "empty-archive", textContent: "Earlier entries will appear here." }));
      return;
    }
    gridEl.replaceChildren(...rest.map((entry) => {
      const img = artwork(entry);
      if (img.tagName === "IMG") img.loading = "lazy";
      const btn = el("button", { type: "button" }, [
        el("div", { className: "frame" }, [img]),
        el("p", { className: "label-date", textContent: formatDate(entry.date) }),
        el("h3", { className: "label-title", textContent: entry.title || "Untitled" }),
      ]);
      btn.addEventListener("click", () => openDetail(entry.date));
      return el("li", { className: "grid-item" }, [btn]);
    }));
  }

  // ---------- detail dialog ----------

  function fillDetail(entry) {
    document.getElementById("detail-frame").replaceChildren(artwork(entry));
    document.getElementById("detail-date").textContent = formatDate(entry.date);
    document.getElementById("detail-title").textContent = entry.title || "Untitled";
    document.getElementById("detail-caption").textContent = entry.caption || "";
    const note = document.getElementById("detail-note");
    note.textContent = backfillNote(entry);
    note.hidden = !note.textContent;
    document.getElementById("detail-sources").replaceChildren(sourcesList(entry));
    const i = entries.indexOf(entry);
    document.getElementById("detail-newer").disabled = i <= 0;
    document.getElementById("detail-older").disabled = i >= entries.length - 1;
  }

  function openDetail(date) {
    if (location.hash !== "#/" + date) {
      location.hash = "/" + date; // triggers route()
      return;
    }
    route();
  }

  function closeDetail() {
    if (dialog.open) dialog.close();
  }

  function step(delta) {
    const current = entries.findIndex((e) => "#/" + e.date === location.hash);
    const next = entries[current + delta];
    if (next) history.replaceState(null, "", "#/" + next.date), route();
  }

  function route() {
    const match = location.hash.match(/^#\/(\d{4}-\d{2}-\d{2})$/);
    const entry = match && entries.find((e) => e.date === match[1]);
    if (!entry) return closeDetail();
    fillDetail(entry);
    if (!dialog.open) {
      lastFocus = document.activeElement;
      dialog.showModal();
    }
  }

  dialog.addEventListener("close", () => {
    if (location.hash) history.replaceState(null, "", location.pathname + location.search);
    if (lastFocus) lastFocus.focus();
  });
  dialog.addEventListener("click", (e) => { if (e.target === dialog) closeDetail(); }); // backdrop click
  dialog.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") step(-1);
    if (e.key === "ArrowRight") step(1);
  });
  document.getElementById("detail-close").addEventListener("click", closeDetail);
  document.getElementById("detail-newer").addEventListener("click", () => step(-1));
  document.getElementById("detail-older").addEventListener("click", () => step(1));
  window.addEventListener("hashchange", route);

  // ---------- load ----------

  fetch("entries.json", { cache: "no-cache" })
    .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then((data) => {
      entries = (data.entries || []).slice().sort((a, b) => b.date.localeCompare(a.date));
      document.getElementById("sample-banner").hidden = !entries.some((e) => e.sample);
      if (!entries.length) {
        featuredEl.replaceChildren(el("p", { className: "status-message", textContent: "The first illustration is on its way." }));
        renderGrid([]);
        return;
      }
      renderFeatured(entries[0]);
      renderGrid(entries.slice(1));
      route();
    })
    .catch(() => {
      featuredEl.replaceChildren(el("p", { className: "status-message", textContent: "The gallery could not be loaded. Please try again later." }));
    });
})();
