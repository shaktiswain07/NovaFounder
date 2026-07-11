// NovaFounder — UI behaviors

document.addEventListener("DOMContentLoaded", () => {

  // ---- Ignition sequence overlay on the generator form ----
  const form = document.getElementById("generatorForm");
  if (form) {
    form.addEventListener("submit", () => {
      const btn = document.getElementById("generateBtn");
      if (btn) btn.disabled = true;

      const overlay = document.createElement("div");
      overlay.className = "ignition-overlay";
      overlay.innerHTML = `
        <div class="ignition-panel">
          <div class="ignition-ring"></div>
          <p class="ignition-text" id="ignitionText">IGNITION SEQUENCE STARTED</p>
        </div>
      `;
      document.body.appendChild(overlay);

      const messages = [
        "IGNITION SEQUENCE STARTED",
        "DRAFTING POSITIONING...",
        "MAPPING THE COMPETITION...",
        "SCOPING THE MVP...",
        "RUNNING THE NUMBERS...",
        "WRITING THE PITCH...",
      ];
      let i = 0;
      const textEl = overlay.querySelector("#ignitionText");
      setInterval(() => {
        i = (i + 1) % messages.length;
        if (textEl) textEl.textContent = messages[i];
      }, 1400);
    });
  }

  // ---- Sidebar scroll-spy on the result dashboard ----
  const sidenavLinks = document.querySelectorAll(".sidenav-link");
  const sections = Array.from(sidenavLinks)
    .map((link) => document.querySelector(link.getAttribute("href")))
    .filter(Boolean);

  if (sidenavLinks.length && sections.length) {
    const setActive = (id) => {
      sidenavLinks.forEach((link) => {
        link.classList.toggle("active", link.getAttribute("href") === `#${id}`);
      });
    };

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) setActive(entry.target.id);
        });
      },
      { rootMargin: "-20% 0px -70% 0px", threshold: 0 }
    );
    sections.forEach((sec) => observer.observe(sec));
  }

  // ---- Copy-to-clipboard buttons (pitch, resume description) ----
  document.querySelectorAll(".copy-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetId = btn.dataset.copyTarget;
      const target = document.getElementById(targetId);
      if (!target) return;

      navigator.clipboard.writeText(target.innerText).then(() => {
        const original = btn.textContent;
        btn.textContent = "Copied!";
        setTimeout(() => (btn.textContent = original), 1500);
      });
    });
  });

  // ---- Export dossier to PDF (client-side, via jsPDF) ----
  const exportBtn = document.getElementById("exportPdfBtn");
  if (exportBtn) {
    exportBtn.addEventListener("click", () => {
      if (!window.jspdf) return;
      const { jsPDF } = window.jspdf;
      const doc = new jsPDF({ unit: "pt", format: "a4" });
      const margin = 42;
      const pageWidth = doc.internal.pageSize.getWidth() - margin * 2;
      let y = 54;

      const addHeading = (text, size = 14) => {
        if (y > 780) { doc.addPage(); y = 54; }
        doc.setFont("helvetica", "bold");
        doc.setFontSize(size);
        doc.text(text, margin, y);
        y += size * 1.15;
      };
      const addParagraph = (text, size = 10.5) => {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(size);
        const lines = doc.splitTextToSize(text || "-", pageWidth);
        lines.forEach((line) => {
          if (y > 780) { doc.addPage(); y = 54; }
          doc.text(line, margin, y);
          y += size * 1.35;
        });
        y += 8;
      };

      const startupName = document.querySelector(".result-name")?.innerText || "Startup";
      const tagline = document.querySelector(".result-tagline")?.innerText || "";

      addHeading(startupName, 20);
      addParagraph(tagline, 12);

      document.querySelectorAll(".dossier .card, .dossier .cluster-tag").forEach((el) => {
        if (el.classList.contains("cluster-tag")) {
          addHeading(el.innerText, 13);
          return;
        }
        const heading = el.querySelector("h2");
        if (heading) addHeading(heading.innerText.trim(), 12.5);
        addParagraph(el.innerText.replace(heading ? heading.innerText : "", "").trim());
      });

      doc.save(`${startupName.replace(/\s+/g, "_")}_Dossier.pdf`);
    });
  }

});
