// Setting up the Modal
const modal = document.querySelector('.modal');
M.Modal.init(modal, {});

// Setting up the Select
const select = document.querySelectorAll('select');
M.FormSelect.init(select, {});

// Setting up the Autocomplete
const req_autocomplete = document.querySelector('.req_autocomplete');
M.Autocomplete.init(req_autocomplete, {
    data: {
        "Alassane Ouattara": null,
        "Souleymane Faye": null,
        "Anta Lo": null
    },
});