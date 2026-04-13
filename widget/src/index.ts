/**
 * Bookyngs embeddable widget entry point.
 *
 * Embed on any page with:
 *
 *   <div data-bookyngs data-tenant="your-slug" data-module="webshop"></div>
 *   <script src="https://cdn.bookyngs.hr/widget.iife.js" defer></script>
 *
 * Attributes:
 *   data-tenant   — tenant slug (required)
 *   data-module   — "webshop" | "booking" | "loyalty" (required)
 *   data-locale   — "hr" | "en" (optional, defaults to "hr")
 */

import { mount } from "./mount";

function init(): void {
  const containers = document.querySelectorAll<HTMLElement>("[data-bookyngs]");
  containers.forEach((el) => {
    const tenant = el.dataset.tenant;
    const mod = el.dataset.module as "webshop" | "booking" | "loyalty" | undefined;
    const locale = (el.dataset.locale ?? "hr") as "hr" | "en";

    if (!tenant || !mod) {
      console.warn("[bookyngs] Element missing data-tenant or data-module.", el);
      return;
    }

    mount(el, { tenant, module: mod, locale });
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
