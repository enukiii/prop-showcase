(() => {
    const pickers = [...document.querySelectorAll('[data-multiselect-picker]')];
    if (!pickers.length) return;

    pickers.forEach(picker => {
        const filterName = picker.dataset.multiselectPicker;
        const checkboxes = [...picker.querySelectorAll(`input[name="${filterName}"]`)];
        const summary = picker.querySelector('[data-filter-summary]');
        const count = picker.querySelector('[data-filter-count]');
        const clearButton = picker.querySelector('[data-clear-filter]');
        const allLabel = filterName === 'district' ? 'All districts' : 'All property types';
        const selectedLabel = filterName === 'district' ? 'districts' : 'types';

        const updateLabels = () => {
            const selected = checkboxes.filter(checkbox => checkbox.checked).map(checkbox => checkbox.value);
            if (summary) {
                summary.textContent = selected.length === 0
                    ? allLabel
                    : selected.length === 1
                        ? selected[0]
                        : `${selected.length} ${selectedLabel} selected`;
            }
            if (count) count.textContent = `${selected.length} selected`;
        };

        checkboxes.forEach(checkbox => checkbox.addEventListener('change', updateLabels));
        clearButton?.addEventListener('click', () => {
            checkboxes.forEach(checkbox => { checkbox.checked = false; });
            updateLabels();
        });
        document.addEventListener('click', event => {
            if (!picker.contains(event.target)) picker.open = false;
        });
    });

    document.addEventListener('keydown', event => {
        if (event.key === 'Escape') pickers.forEach(picker => { picker.open = false; });
    });
})();
