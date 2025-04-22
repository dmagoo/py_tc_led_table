export function renderParamControls(paramDefs, container, currentValues = {}) {
  container.innerHTML = '';

  Object.entries(paramDefs).forEach(([name, def]) => {
    let wrapper = document.createElement('div');
    wrapper.style.marginBottom = '1em';
    wrapper.dataset.paramName = name;

    let label = document.createElement('label');
    label.textContent = name;
    label.style.display = 'block';
    wrapper.appendChild(label);

    let input;

    if (def.type === 'float' || def.type === 'int') {
      input = document.createElement('sl-input');
      input.type = 'number';
      input.step = def.type === 'int' ? '1' : '0.01';
      input.min = def.min;
      input.max = def.max;
      input.value = currentValues[name] ?? def.default;
    }

    if (def.type === 'color') {
      input = document.createElement('sl-color-picker');
      input.value = rgbaArrayToHex(def.default);
      input.format = 'hex';
    }

    if (def.type === 'enum') {
      input = document.createElement('sl-select');
      def.options.forEach(option => {
        const opt = document.createElement('sl-option');
        opt.value = option;
        opt.textContent = option;
        input.appendChild(opt);
      });
      input.value = currentValues[name] ?? def.default;
    }

    if (input) {
      input.dataset.paramName = name;
      wrapper.appendChild(input);
      container.appendChild(wrapper);
    }
  });
}

function rgbaArrayToHex(arr) {
  const [r, g, b] = arr;
  return `#${[r, g, b].map(v => v.toString(16).padStart(2, '0')).join('')}`;
}
