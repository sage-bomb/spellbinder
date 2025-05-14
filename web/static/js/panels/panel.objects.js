// === panel.objects.js ===
class ObjectsPanel extends Panel {
    constructor() {
        super('#panel-objects');
        console.log("Objects/Entities panel loaded");
    }

    render() {
        const panel = this.getPanel();
        panel.empty();
        panel.append('<h3>All Entities</h3>');

        const list = $('<div></div>').css({ marginTop: '10px', maxHeight: '400px', overflowY: 'auto' });
        panel.append(list);

        $.get("/api/entities", function(data) {
            // Sort by type first, then name
            data.sort((a, b) => {
                if (a.type !== b.type) return a.type.localeCompare(b.type);
                return a.name.localeCompare(b.name);
            });

            data.forEach(entity => {
                const item = $('<div class="entity"></div>')
                    .text(`[${entity.type}] ${entity.name}`)
                    .data('entity', entity);
                item.click(() => {
                    window.editorPanelRender(entity);
                    $('#panel-entityeditor').removeClass('hidden');
                });
                list.append(item);
            });
        });
    }
}

// Expose for button system
window.objectsPanel = () => new ObjectsPanel();
window.objectsPanelRender = () => new ObjectsPanel().render();
