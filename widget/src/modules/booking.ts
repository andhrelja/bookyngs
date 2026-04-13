import type { WidgetConfig } from "../mount";

interface Resource {
  id: string;
  name: string;
  description?: string;
  price_per_night?: string;
  price_per_hour?: string;
}

export async function render(el: HTMLElement, config: WidgetConfig, apiBase: string): Promise<void> {
  const res = await fetch(`${apiBase}/booking/resources?tenant=${config.tenant}`);
  if (!res.ok) throw new Error(`Failed to load resources: ${res.status}`);
  const resources: Resource[] = await res.json();

  if (resources.length === 0) {
    el.innerHTML = `<p style="font-family:sans-serif;color:#6b7280;font-size:0.875rem;padding:1rem">
      ${config.locale === "hr" ? "Nema dostupnih resursa." : "No resources available."}
    </p>`;
    return;
  }

  el.innerHTML = `
    <div class="bky-booking" style="font-family:sans-serif">
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1rem">
        ${resources
          .map((r) => {
            const priceLabel = r.price_per_night
              ? `${r.price_per_night} EUR / ${config.locale === "hr" ? "noć" : "night"}`
              : r.price_per_hour
                ? `${r.price_per_hour} EUR / ${config.locale === "hr" ? "sat" : "hour"}`
                : "";
            return `
            <div style="border:1px solid #e5e7eb;border-radius:0.75rem;padding:1.25rem">
              <p style="font-weight:600;margin:0;font-size:0.9375rem">${r.name}</p>
              ${r.description ? `<p style="color:#6b7280;font-size:0.8125rem;margin:0.25rem 0">${r.description}</p>` : ""}
              ${priceLabel ? `<p style="font-weight:500;margin:0.5rem 0">${priceLabel}</p>` : ""}
              <button
                data-resource-id="${r.id}"
                onclick="console.log('[bookyngs] book resource', '${r.id}')"
                style="width:100%;background:#2563eb;color:#fff;border:none;padding:0.5rem;border-radius:0.5rem;cursor:pointer;font-size:0.875rem;margin-top:0.5rem"
              >
                ${config.locale === "hr" ? "Rezerviraj" : "Book now"}
              </button>
            </div>
          `;
          })
          .join("")}
      </div>
    </div>
  `;
}
