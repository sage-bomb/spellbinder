function renderPanelEntity() {
    $('#left_panel').empty();
    $('#left_panel').append(`
        <div class="spellbinder-panel">
            <h2>Entity Editor</h2>
            <div class='scene-tags'></div><br>
            <input type="text" placeholder="Entity Name" value="test people" /><br>
            <select><option selected>Culture</option><option>Character</option><option>Artifact</option></select><br>
            <textarea rows="5">Test Data....</textarea><br>
            <button>Save Entity</button>
        </div>
    `);

    attachTagEditor($("#left_panel .scene-tags"));
}
