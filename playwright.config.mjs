import { defineConfig, devices } from "@playwright/test";
export default defineConfig({
  testDir:"./tests",
  // Scénarios du prototype invalidé conservés, sans les présenter comme contrats U01.1.
  testIgnore:"**/historique/**",
  timeout:30000,
  expect:{timeout:8000},
  use:{...devices["Desktop Chrome"],baseURL:"http://127.0.0.1:8765"},
  webServer:{command:"python -m http.server 8765 --bind 127.0.0.1",url:"http://127.0.0.1:8765",reuseExistingServer:!process.env.CI,timeout:15000},
  reporter:process.env.CI?"github":"list"
});
