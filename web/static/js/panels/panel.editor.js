// === panel.editor.js ===
class EditorPanel extends Panel {
    constructor() {
        super('#panel-entityeditor');
        console.log("Editor panel loaded");
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

        super.render(entity); // base renders name + description

        const panel = this.getPanel();
        const saveBtn = $('<button>Save</button>');
        const deleteBtn = $('<button>Delete</button>');
        panel.append(saveBtn).append(deleteBtn);

        const nameInput = panel.find('input[type="text"]');
        const descInput = panel.find('textarea');

        saveBtn.click(() => {
            entity.name = nameInput.val();
            entity.description = descInput.val();
            $.ajax({
                url: '/api/entity/' + entity.edi,
                type: 'PATCH',
                contentType: 'application/json',
                data: JSON.stringify(entity),
                success: function() { location.reload(); }
            });
        });

        deleteBtn.click(() => {
            if (confirm('Delete this entity?')) {
                $.ajax({
                    url: '/api/entity/' + entity.edi,
                    type: 'DELETE',
                    success: function() { location.reload(); }
                });
            }
        });
    }
}

// Expose for button system
window.editorPanel = () => new EditorPanel();
window.editorPanelRender = (entity) => new EditorPanel().render(entity);
