import { renderParamControls } from './paramRenderer.js';

const appSelect = document.getElementById("app-select");
const paramControls = document.getElementById("param-controls");
const startButton = document.getElementById("start-button");
const stopButton = document.getElementById("stop-button");

let apps = {};

fetch("/api/apps/")
  .then(response => response.json())
  .then(data => {
    apps = Object.fromEntries(data.map(e => [e.name, e]));
    data.forEach(app => {
      const option = document.createElement("sl-option");
      option.value = app.name;
      option.textContent = app.name;
      appSelect.appendChild(option);
    });
  });

appSelect.addEventListener("sl-change", () => {
  const app = apps[appSelect.value];
  if (app) {
    renderParamControls(app.params, paramControls);
  }
});

startButton.addEventListener("click", () => {
  const selectedApp = appSelect.value;
  if (!selectedApp) return;

  const paramData = {};
  paramControls.querySelectorAll("[data-param-name]").forEach(wrapper => {
    const name = wrapper.dataset.paramName;
    const input = wrapper.querySelector("[data-param-name]");
    if (!input) return;

    if (input.tagName === "SL-COLOR-PICKER") {
	const [r, g, b, a] = hexToRgbaArray(input.value);
	paramData[name] = [0, r, g, b]; // convert to WRGB format
    } else if (input.tagName === "SL-SELECT") {
      paramData[name] = input.value;
    } else {
      paramData[name] = input.valueAsNumber;
    }
  });

  fetch("/api/apps/start", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ app: selectedApp, params: paramData })
  })
  .then(res => res.json())
  .then(data => console.log("Started:", data))
  .catch(err => console.error("Start error:", err));
});

stopButton.addEventListener("click", () => {
  const paramData = {};

  fetch("/api/apps/stop", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(paramData)
  })
  .then(res => res.json())
  .then(data => console.log("Stopped"))
  .catch(err => console.error("Stop error:", err));
});

const serviceList = document.getElementById("service-list");

fetch("/api/services/")
  .then(res => res.json())
  .then(services => {
    services.forEach(service => {
      const wrapper = document.createElement("div");
      wrapper.style.display = "flex";
      wrapper.style.alignItems = "center";
      wrapper.style.gap = "1em";

      const label = document.createElement("span");
      label.textContent = `${service.label} (${service.name})`;

      const status = document.createElement("sl-badge");
      status.variant = service.status === "active" ? "success" : "neutral";
      status.textContent = service.status;

      wrapper.appendChild(label);
      wrapper.appendChild(status);

      if (service.controllable) {
        ["start", "stop", "restart"].forEach(action => {
          const btn = document.createElement("sl-button");
          btn.textContent = action;
          btn.size = "small";
          btn.addEventListener("click", () => {
            fetch(`/api/services/${service.name}/${action}`, { method: "POST" })
              .then(res => res.json())
              .then(data => console.log(`${action} result:`, data))
              .catch(err => console.error(`${action} error:`, err));
          });
          wrapper.appendChild(btn);
        });
      }

      serviceList.appendChild(wrapper);
    });
  });



function hexToRgbaArray(hex) {
  const bigint = parseInt(hex.replace('#', ''), 16);
  return [(bigint >> 16) & 255, (bigint >> 8) & 255, bigint & 255, 0];
}
