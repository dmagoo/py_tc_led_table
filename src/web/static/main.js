const effectSelect = document.getElementById("effect-select");

fetch("/api/effects/")
  .then(response => response.json())
  .then(effects => {
    effects.forEach(effect => {
      const option = document.createElement("sl-option");
      option.value = effect.name;
      option.textContent = effect.name;
      effectSelect.appendChild(option);
    });
  });

const startButton = document.getElementById("start-button");

startButton.addEventListener("click", () => {
  const selectedEffect = effectSelect.value;
  if (!selectedEffect) return;

  fetch("/api/start_effect", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ effect: selectedEffect })
  });
});
