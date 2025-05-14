// === panel.outliner.js ===
class OutlinerPanel extends Panel {
    constructor() {
        super('#panel-outliner');
        console.log("Outliner panel loaded");
    }

    render(entity) {
        // entity is ignored, but accepted for API compatibility
        getEntities((entities) => {
            const panel = this.getPanel();
            panel.empty();
            panel.append('<h3>Outliner</h3>');

            const addActBtn = $('<button>Add Act</button>');
            panel.append(addActBtn);
            addActBtn.click(() => {
                const newAct = { type: "Act", name: "New Act", description: "", children: [], parent: null };
                $.post('/api/entity', JSON.stringify(newAct), "json").done(() => window.outlinerPanelRender());
            });

            entities.filter(e => e.type === "Act").forEach(act => {
                const actGroup = $('<div class="act-group"></div>').attr('data-act-id', act.edi);
                const actDiv = $('<div class="entity act"></div>').text(act.name).data('entity', act);
                const flipper = $('<span class="flipper">▾</span>');
                actDiv.prepend(flipper);
                const delActBtn = $('<span class="delete-btn">✕</span>');
                delActBtn.click((e) => { e.stopPropagation(); if (confirm(`Delete Act?`)) deleteEntity(act.edi, () => window.outlinerPanelRender()); });
                actDiv.append(delActBtn);

                const desc = $('<div class="entity-desc"></div>').text(act.description).hide();
                const sceneList = $('<div class="scenes-list"></div>');
                flipper.click((e) => { e.stopPropagation(); desc.toggle(); sceneList.toggle(); flipper.text(flipper.text() === '▾' ? '▸' : '▾'); });
                actGroup.append(actDiv).append(desc);

                act.children.forEach(sceneId => {
                    const scene = entities.find(e => e.edi === sceneId);
                    if (scene) {
                        const sceneDiv = $('<div class="entity scene"></div>').text(scene.name).data('entity', scene);
                        const sceneFlipper = $('<span class="flipper">▾</span>');
                        sceneDiv.prepend(sceneFlipper);
                        const delSceneBtn = $('<span class="delete-btn">✕</span>');
                        delSceneBtn.click((e) => { e.stopPropagation(); if (confirm(`Delete Scene?`)) deleteEntity(scene.edi, () => window.outlinerPanelRender()); });
                        sceneDiv.append(delSceneBtn);

                        const sceneDesc = $('<div class="entity-desc"></div>').text(scene.description).hide();
                        sceneFlipper.click((e) => { e.stopPropagation(); sceneDesc.toggle(); sceneFlipper.text(sceneFlipper.text() === '▾' ? '▸' : '▾'); });

                        sceneList.append(sceneDiv).append(sceneDesc);
                    }
                });

                const addSceneBtn = $('<button class="small-btn">+ Scene</button>');
                addSceneBtn.click(() => {
                    const newScene = { type: "Scene", name: "New Scene", description: "", children: [], parent: act.edi };
                    $.post('/api/entity', JSON.stringify(newScene), "json").done(scene => {
                        act.children.push(scene.edi);
                        saveEntity(act, () => window.outlinerPanelRender());
                    });
                });

                actGroup.append(addSceneBtn).append(sceneList);
                panel.append(actGroup);
            });

            enableOutlinerSorting();
            enableSceneSorting();
        });
    }
}

// Expose for button + console call compatibility
window.outlinerPanel = () => new OutlinerPanel();
window.outlinerPanelRender = (entity) => new OutlinerPanel().render(entity);