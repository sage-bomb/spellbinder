// === panel.editor.js ===
class EditorPanel extends Panel {
    constructor() {
        super('#panel-editor');
        console.log("Entity Editor panel loaded");
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

        super.render(entity);  // Base render for name + description

        const panel = this.getPanel();

        // Add entity type dropdown + new type option
        const typeLabel = $('<label>Type:</label>');
        const typeSelect = $('<select></select>');
        const typeOptions = ['Unknown', 'Act', 'Scene', 'Character', 'Item', 'Place'];

        typeOptions.forEach(type => {
            const option = $('<option></option>').val(type).text(type);
            if (entity.type === type) option.attr('selected', true);
            typeSelect.append(option);
        });

        const customOption = $('<option></option>').val('custom').text('Custom...');
        typeSelect.append(customOption);

        panel.find('.panel-body').prepend(typeSelect).prepend(typeLabel);

        typeSelect.change(function() {
            if ($(this).val() === 'custom') {
                const newType = prompt("Enter custom entity type:");
                if (newType) {
                    const newOpt = $('<option></option>').val(newType).text(newType);
                    $(this).append(newOpt).val(newType);
                } else {
                    $(this).val('Unknown');
                }
            }
        });

        // Save + Delete buttons
        const saveBtn = $('<button>Save</button>');
        const deleteBtn = $('<button>Delete</button>');
        panel.append(saveBtn, deleteBtn);

        const nameInput = panel.find('input[type="text"]');
        const descInput = panel.find('textarea');

        saveBtn.click(() => {
            entity.type = typeSelect.val();
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

// Expose for button system
window.editorPanel = () => new EditorPanel();
window.editorPanelRender = (entity) => new EditorPanel().render(entity);
