import type { WidgetConfig } from "../mount";

interface Product {
  id: string;
  name: string;
  price: string;
  image_url?: string;
  description?: string;
}

export async function render(el: HTMLElement, config: WidgetConfig, apiBase: string): Promise<void> {
  const res = await fetch(`${apiBase}/webshop/products?tenant=${config.tenant}`);
  if (!res.ok) throw new Error(`Failed to load products: ${res.status}`);
  const products: Product[] = await res.json();

  if (products.length === 0) {
    el.innerHTML = `<p style="font-family:sans-serif;color:#6b7280;font-size:0.875rem;padding:1rem">
      ${config.locale === "hr" ? "Nema dostupnih proizvoda." : "No products available."}
    </p>`;
    return;
  }

  el.innerHTML = `
    <div class="bky-webshop" style="font-family:sans-serif">
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:1rem">
        ${products
          .map(
            (p) => `
          <div style="border:1px solid #e5e7eb;border-radius:0.75rem;overflow:hidden">
            ${p.image_url ? `<img src="${p.image_url}" alt="${p.name}" style="width:100%;height:160px;object-fit:cover">` : ""}
            <div style="padding:1rem">
              <p style="font-weight:600;margin:0;font-size:0.9375rem">${p.name}</p>
              ${p.description ? `<p style="color:#6b7280;font-size:0.8125rem;margin:0.25rem 0">${p.description}</p>` : ""}
              <p style="font-weight:500;margin:0.5rem 0 0.75rem">${p.price} EUR</p>
              <button
                data-product-id="${p.id}"
                onclick="console.log('[bookyngs] add to cart', '${p.id}')"
                style="width:100%;background:#2563eb;color:#fff;border:none;padding:0.5rem;border-radius:0.5rem;cursor:pointer;font-size:0.875rem"
              >
                ${config.locale === "hr" ? "Dodaj u košaricu" : "Add to cart"}
              </button>
            </div>
          </div>
        `,
          )
          .join("")}
      </div>
    </div>
  `;
}
