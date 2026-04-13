export interface WidgetConfig {
  tenant: string;
  module: "webshop" | "booking" | "loyalty";
  locale: "hr" | "en";
}

const API_BASE =
  (typeof window !== "undefined" && (window as Window & { BOOKYNGS_API?: string }).BOOKYNGS_API) ||
  "https://api.bookyngs.hr";

export function mount(el: HTMLElement, config: WidgetConfig): void {
  el.innerHTML = `<div style="font-family:sans-serif;padding:1rem;color:#6b7280;font-size:0.875rem">
    ${config.locale === "hr" ? "Učitavanje..." : "Loading..."}
  </div>`;

  import(`./modules/${config.module}`)
    .then((mod) => (mod as { render: (el: HTMLElement, cfg: WidgetConfig, api: string) => void }).render(el, config, API_BASE))
    .catch((err: unknown) => {
      el.innerHTML = `<p style="color:#ef4444;font-size:0.875rem;padding:1rem">
        ${config.locale === "hr" ? "Greška pri učitavanju." : "Failed to load."}
      </p>`;
      console.error("[bookyngs]", err);
    });
}
