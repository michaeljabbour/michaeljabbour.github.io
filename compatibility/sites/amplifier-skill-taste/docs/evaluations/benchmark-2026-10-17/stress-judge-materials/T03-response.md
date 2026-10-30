Restored `working.py` to `baseline.py`.

The proposed `sorted(set(names))` removes repeated names and changes submitted order. Both choices violate the families’ explicit intent. The provided checks failed with “Order and repeated names must survive.” After restoration, they passed: “submitted order, repetitions and input preservation.”

Decision note for the next editor: preserve every submitted name, its position, and repetitions without changing the input. The restored implementation makes a separate list while retaining those properties. Fewer operations or a tidier-looking list would not justify losing family submissions. Revisit only if the brief explicitly changes; any later cleanup must pass these checks. Audience response and visual presentation were not tested.
