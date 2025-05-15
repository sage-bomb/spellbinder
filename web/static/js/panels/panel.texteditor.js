// === panel.texteditor.js ===
class TextEditorPanel extends Panel {
    constructor() {
        super('#panel-texteditor');
        console.log("Text Editor panel loaded");
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

        super.render(entity);  // Call base render first

        const panel = this.getPanel();
        const saveBtn = $('<button>Save</button>');
        const deleteBtn = $('<button>Delete</button>');
        panel.append(saveBtn, deleteBtn);

        const nameInput = panel.find('input[type="text"]');
        const descInput = panel.find('textarea');

        saveBtn.click(() => {
            entity.name = nameInput.val();
            entity.description = descInput.val();
            api.updateEntity(entity, () => location.reload());
        });

        deleteBtn.click(() => {
            if (confirm('Delete this entity?')) {
                api.deleteEntity(entity.edi, () => location.reload());
            }
        });
    }
}

// Export to global to stay compatible
window.texteditorPanel = () => new TextEditorPanel();
window.texteditorPanelRender = (entity) => new TextEditorPanel().render(entity);
