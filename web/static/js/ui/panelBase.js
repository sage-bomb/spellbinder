// === panelBase.js ===
class Panel {
    constructor(panelSelector) {
        this.panelSelector = panelSelector;
    }

    getPanel() {
        const panel = $(this.panelSelector);
        if (!panel.hasClass('panel')) panel.addClass('panel');
        return panel;
    }

    render(entity) {
        entity = entity || {
            edi: "new",
            type: "Unknown",
            name: "",
            description: "",
            children: [],
            parent: null
        };

        const panel = this.getPanel();
        panel.empty();

        const header = $('<div class="panel-header"></div>').text('Edit ' + entity.type);
        const body = $('<div class="panel-body"></div>');

        panel.append(header, body);

        body.append('<label>Name:</label>');
        const nameInput = $('<input type="text">').val(entity.name);
        body.append(nameInput);

        body.append('<label>Description:</label>');
        const descInput = $('<textarea></textarea>').val(entity.description);
        body.append(descInput);
    }
}

// Expose globally
window.Panel = Panel;

// 💫 Add global draggable panels behavior once DOM ready
$(document).ready(() => {
    $('.panel-column').sortable({
        connectWith: '.panel-column',
        handle: '.panel-header',
        placeholder: 'panel-placeholder',
        tolerance: 'pointer'
    }).disableSelection();

    console.log("Draggable panels initialized by panelBase.js");
});
