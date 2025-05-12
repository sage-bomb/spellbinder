function renderPanelText() {
    const obj = getTarget();
    let text = obj ? obj.data : "No target selected.";
    $('#right_panel').empty();
    $('#right_panel').append(`
        <div class="spellbinder-panel">
            <h2>Text Reader / Editor</h2>
            <div class="scene-tags"></div><br>
            <button id="modeSwitch">Toggle Edit Mode</button><br><br>
            <div id="textContent" style="border:1px solid #444; padding:10px; border-radius:5px;">${text}</div>
        </div>
    `);

    attachTagEditor($("#right_panel .scene-tags"));

    let editMode = false;
    $('#modeSwitch').on('click', function() {
        editMode = !editMode;
        $('#textContent').attr('contenteditable', editMode);
        $(this).text(editMode ? 'Switch to Read Mode' : 'Switch to Edit Mode');
    });

}
 