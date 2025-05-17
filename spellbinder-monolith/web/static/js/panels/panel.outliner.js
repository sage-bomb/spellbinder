// === panel.outliner.js ===
class OutlinerPanel extends Panel {
    constructor() {
        super('#panel-outliner');
        console.log("Outliner panel loaded");
    }

    render() {
        api.getEntities((entities) => {
            const panel = this.getPanel();
            panel.empty();
            panel.append('<div class="panel-header">Outliner</div>');

            const addActBtn = $('<button>Add Act</button>');
            addActBtn.click(() => {
                const newAct = { type: "Act", name: "New Act", description: "", children: [], parent: null };
                api.createEntity(newAct, () => window.outlinerPanelRender());
            });

            panel.append(addActBtn);

            entities.filter(e => e.type === "Act").forEach(act => {
                panel.append(window.createActGroup(act, entities));
            });

            enableOutlinerSorting();
            enableSceneSorting();
        });
    }
}

// Expose for button + console call compatibility
window.outlinerPanel = () => new OutlinerPanel();
window.outlinerPanelRender = (entity) => new OutlinerPanel().render(entity);
