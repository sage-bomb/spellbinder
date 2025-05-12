
// ===== GLOBAL OBJECT STATE =====
let globalData = {
    objects: [
        { eid: "outline-001", type: "Outline", name: "Main Story Outline", tags: ['draft'], data: {
            acts: [
                { name: "Act I: The Awakening", scenes: [{name: "Scene 1: Caravan approaches",tags:["Hero","Horse"]}, {name:"Scene 2: Hero scouts the ruins"}] },
                { name: "Act II: Threads of Fate", scenes: [{name:"Scene 1: Whispered warnings at dusk"}, {name:"Scene 2: The unexpected arrival at camp"}] }
            ]
        }}
,
        { eid: "entity-001", type: "Entity", name: "Test People", tags: ['culture', 'elf'], data: "An ancient nomadic society." },
        { eid: "file-001", type: "File", name: "chapter_03.md", tags: ['draft', 'chapter3'], data: "Some file text..." }
    ],
    targetEID: null
};

function setTarget(eid) {
    globalData.targetEID = eid;
}

function getTarget() {
    return globalData.objects.find(obj => obj.eid === globalData.targetEID) || null;
}

function clearTarget() {
    globalData.targetEID = null;
}


// Spellbinder V2 main.js - CLEAN UNIFIED BUILD


function apiCall(method, url, data = null) {
    return $.ajax({
        url: url,
        method: method,
        contentType: 'application/json',
        data: data ? JSON.stringify(data) : null
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.error(`API Call Failed: ${textStatus} - ${errorThrown}`);
        alert(`Error: ${textStatus}`);
    });
}

function tagBarHTML() {
}

function clearPanels() {
    $('#left_panel').empty();
    $('#right_panel').empty();
}





function renderPanelText() {
    $('#right_panel').empty();
    $('#right_panel').append(`
        <div class="spellbinder-panel">
            <h2>Text Reader / Editor</h2>
            <div><b>Global Tags:</b> ${tagBarHTML()}</div><br>
            <button id="modeSwitch">Toggle Edit Mode</button><br><br>
            <div id="textContent" style="border:1px solid #444; padding:10px; border-radius:5px;">
                Lorem ipsum dolor sit amet, <b>[Ara'net Clans]</b> adipiscing elit.
            </div>
        </div>
    `);

    let editMode = false;
    $('#modeSwitch').on('click', function() {
        editMode = !editMode;
        $('#textContent').attr('contenteditable', editMode);
        $(this).text(editMode ? 'Switch to Read Mode' : 'Switch to Edit Mode');
    });
}