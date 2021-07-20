// Setting up collapsible
const collapsible = document.querySelectorAll('.collapsible');
M.Collapsible.init(collapsible, {});

// Setting up tooltip
const tooltip = document.querySelectorAll('.tooltipped');
M.Tooltip.init(tooltip, {});

// Setting up Textarea
const textarea = document.getElementById('id_description');
M.textareaAutoResize(textarea, {});