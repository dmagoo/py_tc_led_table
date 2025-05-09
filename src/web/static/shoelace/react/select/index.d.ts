import Component from '../../components/select/select.component.js';
import { type EventName } from '@lit/react';
import type { SlChangeEvent } from '../../events/events.js';
import type { SlClearEvent } from '../../events/events.js';
import type { SlInputEvent } from '../../events/events.js';
import type { SlFocusEvent } from '../../events/events.js';
import type { SlBlurEvent } from '../../events/events.js';
import type { SlShowEvent } from '../../events/events.js';
import type { SlAfterShowEvent } from '../../events/events.js';
import type { SlHideEvent } from '../../events/events.js';
import type { SlAfterHideEvent } from '../../events/events.js';
import type { SlInvalidEvent } from '../../events/events.js';
export type { SlChangeEvent } from '../../events/events.js';
export type { SlClearEvent } from '../../events/events.js';
export type { SlInputEvent } from '../../events/events.js';
export type { SlFocusEvent } from '../../events/events.js';
export type { SlBlurEvent } from '../../events/events.js';
export type { SlShowEvent } from '../../events/events.js';
export type { SlAfterShowEvent } from '../../events/events.js';
export type { SlHideEvent } from '../../events/events.js';
export type { SlAfterHideEvent } from '../../events/events.js';
export type { SlInvalidEvent } from '../../events/events.js';
/**
 * @summary Selects allow you to choose items from a menu of predefined options.
 * @documentation https://shoelace.style/components/select
 * @status stable
 * @since 2.0
 *
 * @dependency sl-icon
 * @dependency sl-popup
 * @dependency sl-tag
 *
 * @slot - The listbox options. Must be `<sl-option>` elements. You can use `<sl-divider>` to group items visually.
 * @slot label - The input's label. Alternatively, you can use the `label` attribute.
 * @slot prefix - Used to prepend a presentational icon or similar element to the combobox.
 * @slot suffix - Used to append a presentational icon or similar element to the combobox.
 * @slot clear-icon - An icon to use in lieu of the default clear icon.
 * @slot expand-icon - The icon to show when the control is expanded and collapsed. Rotates on open and close.
 * @slot help-text - Text that describes how to use the input. Alternatively, you can use the `help-text` attribute.
 *
 * @event sl-change - Emitted when the control's value changes.
 * @event sl-clear - Emitted when the control's value is cleared.
 * @event sl-input - Emitted when the control receives input.
 * @event sl-focus - Emitted when the control gains focus.
 * @event sl-blur - Emitted when the control loses focus.
 * @event sl-show - Emitted when the select's menu opens.
 * @event sl-after-show - Emitted after the select's menu opens and all animations are complete.
 * @event sl-hide - Emitted when the select's menu closes.
 * @event sl-after-hide - Emitted after the select's menu closes and all animations are complete.
 * @event sl-invalid - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
 *
 * @csspart form-control - The form control that wraps the label, input, and help text.
 * @csspart form-control-label - The label's wrapper.
 * @csspart form-control-input - The select's wrapper.
 * @csspart form-control-help-text - The help text's wrapper.
 * @csspart combobox - The container the wraps the prefix, suffix, combobox, clear icon, and expand button.
 * @csspart prefix - The container that wraps the prefix slot.
 * @csspart suffix - The container that wraps the suffix slot.
 * @csspart display-input - The element that displays the selected option's label, an `<input>` element.
 * @csspart listbox - The listbox container where options are slotted.
 * @csspart tags - The container that houses option tags when `multiselect` is used.
 * @csspart tag - The individual tags that represent each multiselect option.
 * @csspart tag__base - The tag's base part.
 * @csspart tag__content - The tag's content part.
 * @csspart tag__remove-button - The tag's remove button.
 * @csspart tag__remove-button__base - The tag's remove button base part.
 * @csspart clear-button - The clear button.
 * @csspart expand-icon - The container that wraps the expand icon.
 */
declare const reactWrapper: import("@lit/react").ReactWebComponent<Component, {
    onSlChange: EventName<SlChangeEvent>;
    onSlClear: EventName<SlClearEvent>;
    onSlInput: EventName<SlInputEvent>;
    onSlFocus: EventName<SlFocusEvent>;
    onSlBlur: EventName<SlBlurEvent>;
    onSlShow: EventName<SlShowEvent>;
    onSlAfterShow: EventName<SlAfterShowEvent>;
    onSlHide: EventName<SlHideEvent>;
    onSlAfterHide: EventName<SlAfterHideEvent>;
    onSlInvalid: EventName<SlInvalidEvent>;
}>;
export default reactWrapper;
