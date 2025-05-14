// === panel.texteditor.js (demo case) ===
class TextEditorPanel extends Panel {
    constructor() {
        super('#panel-texteditor');
        console.log("Text Editor panel loaded");
    }

    render(entity) {
        super.render(entity);  // Call base render first

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

// Export to global to stay compatible
window.textEditorPanel = () => new TextEditorPanel();
window.textEditorPanelRender = (entity) => new TextEditorPanel().render(entity);