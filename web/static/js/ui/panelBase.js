// === panelBase.js (put this in /static/js/ui/) ===
class Panel {
    constructor(panelSelector) {
        this.panelSelector = panelSelector;
    }

    getPanel() {
        return $(this.panelSelector);
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
        panel.append('<h3>Edit ' + entity.type + '</h3>');
        panel.append('<label>Name:</label>');
        const nameInput = $('<input type="text">').val(entity.name);
        panel.append(nameInput);
        panel.append('<label>Description:</label>');
        const descInput = $('<textarea></textarea>').val(entity.description);
        panel.append(descInput);
    }
}