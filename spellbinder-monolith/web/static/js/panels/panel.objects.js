// === panel.objects.js ===
class ObjectsPanel extends Panel {
    constructor() {
        super('#panel-objects');
        console.log("Objects/Entities panel loaded");
    }

    render() {
        const panel = this.getPanel();
        panel.empty();
        panel.append('<h3 class="panel-header">All Entities</h3>');

        const list = $('<div></div>').css({
            marginTop: '10px',
            maxHeight: '400px',
            overflowY: 'auto'
        });
        panel.append(list);

        // ✅ New api layer call
        api.getEntities((data) => {
            data.forEach(entity => {
                list.append(window.createEntityListItem(entity));
            });
        });
    }
}

// Expose for button system
window.objectsPanel = () => new ObjectsPanel();
window.objectsPanelRender = () => new ObjectsPanel().render();
