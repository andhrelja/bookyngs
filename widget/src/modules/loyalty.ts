import type { WidgetConfig } from "../mount";

export async function render(el: HTMLElement, config: WidgetConfig, _apiBase: string): Promise<void> {
  const t = (hr: string, en: string) => (config.locale === "hr" ? hr : en);

  el.innerHTML = `
    <div class="bky-loyalty" style="font-family:sans-serif;max-width:400px;margin:0 auto">
      <div style="border:1px solid #e5e7eb;border-radius:0.75rem;padding:1.5rem">
        <h3 style="margin:0 0 1rem;font-size:1.0625rem;font-weight:600">
          ${t("Provjeri svoju karticu", "Check your card")}
        </h3>
        <input
          id="bky-loyalty-email"
          type="email"
          placeholder="${t("Vaša e-mail adresa", "Your email address")}"
          style="width:100%;border:1px solid #d1d5db;border-radius:0.5rem;padding:0.625rem;font-size:0.875rem;box-sizing:border-box"
        />
        <button
          onclick="(function(){
            var email = document.getElementById('bky-loyalty-email').value;
            console.log('[bookyngs] check loyalty card', email);
          })()"
          style="width:100%;background:#2563eb;color:#fff;border:none;padding:0.625rem;border-radius:0.5rem;cursor:pointer;font-size:0.875rem;margin-top:0.75rem"
        >
          ${t("Provjeri", "Check")}
        </button>
        <div id="bky-loyalty-result" style="margin-top:1rem"></div>
      </div>
    </div>
  `;
}
