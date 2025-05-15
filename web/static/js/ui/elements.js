// === ui.elements.js ===

function createActGroup(act, entities) {
    const actGroup = $('<div class="act-group"></div>').attr('data-act-id', act.edi);
    const actDiv = createActDiv(act);
    const desc = $('<div class="entity-desc"></div>').text(act.description).hide();
    const sceneList = $('<div class="scenes-list"></div>');

    act.children.forEach(sceneId => {
        const scene = entities.find(e => e.edi === sceneId);
        if (scene) sceneList.append(createSceneDiv(scene));
    });

    const addSceneBtn = $('<button class="small-btn">+ Scene</button>');
    addSceneBtn.click(() => {
        const newScene = { type: "Scene", name: "New Scene", description: "", children: [], parent: act.edi };
        $.post('/api/entity', JSON.stringify(newScene), "json").done(scene => {
            act.children.push(scene.edi);
            saveEntity(act, () => window.outlinerPanelRender());
        });
    });

    actGroup.append(actDiv, desc, addSceneBtn, sceneList);
    return actGroup;
}

function createActDiv(act) {
    const actDiv = $('<div class="entity act"></div>').text(act.name).data('entity', act);
    const flipper = $('<span class="flipper">▾</span>');
    const delActBtn = $('<span class="delete-btn">✕</span>');

    delActBtn.click((e) => { 
        e.stopPropagation();
        if (confirm(`Delete Act?`)) deleteEntity(act.edi, () => window.outlinerPanelRender());
    });

    const desc = $('<div class="entity-desc"></div>').text(act.description).hide();
    const sceneList = $('<div class="scenes-list"></div>');

    flipper.click((e) => {
        e.stopPropagation();
        desc.toggle();
        sceneList.toggle();
        flipper.text(flipper.text() === '▾' ? '▸' : '▾');
    });

    actDiv.prepend(flipper).append(delActBtn);
    return actDiv;
}

function createSceneDiv(scene) {
    const sceneDiv = $('<div class="entity scene"></div>').text(scene.name).data('entity', scene);
    const flipper = $('<span class="flipper">▾</span>');
    const delSceneBtn = $('<span class="delete-btn">✕</span>');
    const sceneDesc = $('<div class="entity-desc"></div>').text(scene.description).hide();

    delSceneBtn.click((e) => {
        e.stopPropagation();
        if (confirm(`Delete Scene?`)) deleteEntity(scene.edi, () => window.outlinerPanelRender());
    });

    flipper.click((e) => {
        e.stopPropagation();
        sceneDesc.toggle();
        flipper.text(flipper.text() === '▾' ? '▸' : '▾');
    });

    sceneDiv.prepend(flipper).append(delSceneBtn);
    return $('<div>').append(sceneDiv, sceneDesc);
}

// === objects.elements.js ===
window.createEntityListItem = function(entity) {
    const item = $('<div class="entity"></div>')
        .text(`[${entity.type}] ${entity.name}`)
        .data('entity', entity);

    item.click(() => {
        window.editorPanelRender(entity);
        $('#panel-entityeditor').removeClass('hidden');
    });

    return item;
}