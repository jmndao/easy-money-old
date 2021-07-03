// Setting up the Modal
const modal = document.querySelector('.modal');
M.Modal.init(modal, {});

// Setting up the Select
const select = document.querySelectorAll('select');
M.FormSelect.init(select, {});

// Setting up the Dropdown
const dropdown = document.querySelectorAll('.dropdown-trigger');
M.Dropdown.init(dropdown, {
    coverTrigger: false,
    inDuration: 300,
    alignment: 'right',
    outDuration: 250,
    hover: false,
    constrainWidth: false,
    gutter: 0, // Spacing from edge
    belowOrigin: true, // Displays dropdown
});

const chips = document.querySelectorAll('.chips');
M.Chips.init(chips, {});