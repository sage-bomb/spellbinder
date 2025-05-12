function renderPanelOutliner() {
    // Set default target if none set
    if (!getTarget()) {
        const firstOutline = globalData.objects.find(obj => obj.type === "Outline");
        if (firstOutline) setTarget(firstOutline.eid);
    }

    const obj = getTarget();
    $('#left_panel').empty();
    $('#left_panel').append(`
        <div class="spellbinder-panel">
            <h2>Story Outliner</h2>
            <p>Drag scenes within acts, or drag out to create new acts.</p>
            <div id="outline"></div>
        </div>
    `);

    if (obj && obj.type === "Outline") {
        $('#left_panel .spellbinder-panel').prepend(`<div class='scene-tags'></div>`);
        obj.tags.forEach(tag => {
            $('#left_panel .spellbinder-panel .scene-tags').append(`<span style='background:#555;'>[${tag}] <a href='#' class='removeTag'>×</a></span>`);
        });
        attachTagEditor($('#left_panel .spellbinder-panel .scene-tags'));

        obj.data.acts.forEach(act => {
            let actBlock = $(`
                <div class="outliner-act">
                    <div class="outliner-act-header">${act.name}</div>
                    <div class="scene-tags"></div>
                </div>
            `);
            if (act.tags) {
                act.tags.forEach(tag => {
                    actBlock.find('.scene-tags').append(`<span style='background:#555;'>[${tag}] <a href='#' class='removeTag'>×</a></span>`);
                });
            }
            attachTagEditor(actBlock.find('.scene-tags'));

            act.scenes.forEach(scene => {
                let sceneBlock = $(`
                    <div class="outliner-scene">
                        <div class="outliner-scene-header">${scene.name}</div>
                        <div class="scene-summary">Summary of ${scene.name}...</div>
                        <div class="scene-tags"></div>
                    </div>
                `);
                if (scene.tags) {
                    scene.tags.forEach(tag => {
                        sceneBlock.find('.scene-tags').append(`<span style='background:#555;'>[${tag}] <a href='#' class='removeTag'>×</a></span>`);
                    });
                }
                attachTagEditor(sceneBlock.find('.scene-tags'));
                actBlock.append(sceneBlock);
            });
            $('#outline').append(actBlock);
        });
    }

    $(".outliner-act-header").on("click", function() {
        $(this).parent(".outliner-act").toggleClass("collapsed");
    });

    $(".outliner-scene-header").on("click", function() {
        $(this).parent(".outliner-scene").toggleClass("collapsed");
    });

    $(".scene-summary").on("dblclick", function() {
        var currentText = $(this).text();
        var input = $('<textarea>').val(currentText).css({
            width: "95%",
            backgroundColor: "#2d2d30",
            color: "#e0e0e0",
            border: "1px solid #555",
            borderRadius: "5px",
            padding: "5px"
        });
        var container = $(this);
        container.empty().append(input);
        input.focus();
        input.on("blur", function() {
            var newText = $(this).val();
            container.text(newText);
        });
    });

    $(".outliner-act-header").on("dblclick", function() {
        var currentText = $(this).text().replace(/▼|▶/g, "").trim();
        var input = $('<input type="text">').val(currentText).css({
            width: "95%",
            backgroundColor: "#2d2d30",
            color: "#e0e0e0",
            border: "1px solid #555",
            borderRadius: "5px",
            padding: "5px"
        });
        var container = $(this);
        container.empty().append(input);
        input.focus();
        input.on("blur", function() {
            var newText = $(this).val();
            container.text(newText);
            container.append(container.hasClass("collapsed") ? " ▶" : " ▼");
        });
    });

    $(".outliner-scene-header").on("dblclick", function() {
        var currentText = $(this).text();
        var input = $('<input type="text">').val(currentText).css({
            width: "95%",
            backgroundColor: "#2d2d30",
            color: "#e0e0e0",
            border: "1px solid #555",
            borderRadius: "5px",
            padding: "5px"
        });
        var container = $(this);
        container.empty().append(input);
        input.focus();
        input.on("blur", function() {
            var newText = $(this).val();
            container.text(newText);
        });
    });

    $(".outliner-act").sortable({
        items: ".outliner-scene",
        connectWith: ".outliner-act",
        placeholder: "ui-state-highlight"
    });
}