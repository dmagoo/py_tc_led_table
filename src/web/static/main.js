import { renderParamControls } from './paramRenderer.js';

const effectSelect = document.getElementById("effect-select");
const paramControls = document.getElementById("param-controls");
const startButton = document.getElementById("start-button");

let effects = {};

fetch("/api/effects/")
  .then(response => response.json())
  .then(data => {
    effects = Object.fromEntries(data.map(e => [e.name, e]));
    data.forEach(effect => {
      const option = document.createElement("sl-option");
      option.value = effect.name;
      option.textContent = effect.name;
      effectSelect.appendChild(option);
    });
  });

effectSelect.addEventListener("sl-change", () => {
  const effect = effects[effectSelect.value];
  if (effect) {
    renderParamControls(effect.params, paramControls);
  }
});

startButton.addEventListener("click", () => {
  const selectedEffect = effectSelect.value;
  if (!selectedEffect) return;

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

  fetch("/api/effects/start", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ effect: selectedEffect, params: paramData })
  })
  .then(res => res.json())
  .then(data => console.log("Started:", data))
  .catch(err => console.error("Start error:", err));
});

function hexToRgbaArray(hex) {
  const bigint = parseInt(hex.replace('#', ''), 16);
  return [(bigint >> 16) & 255, (bigint >> 8) & 255, bigint & 255, 0];
}
