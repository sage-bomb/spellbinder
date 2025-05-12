const globalTags = ['culture', 'elf', 'draft', 'chapter3', 'mystery', 'danger'];

function tagBarHTML() {
    return globalTags.map(tag => `<span style='border:1px solid #555; border-radius:5px; padding:2px 6px; margin:2px; display:inline-block;'>${tag}</span>`).join(' ');
}

// Reusable attachTagEditor function
function attachTagEditor(targetDiv) {
    targetDiv.append(`<div class="scene-tags"><a href='#' class='addTag'>+ add tag</a></div>`);
    
    $(document).on("click", ".removeTag", function(e) {
        e.preventDefault();
        $(this).parent("span").remove();
    });

    $(document).on("click", ".addTag", function(e) {
        e.preventDefault();
        let targetScene = $(this).closest(".scene-tags");
        $("#tagModal").data("target", targetScene).show();
        $("#existingTags").empty();
        globalTags.forEach(tag => {
            let tagBtn = $("<button>").text(tag).css({ margin: "2px", backgroundColor: "#555", color: "#eee", border: "none", borderRadius: "5px", padding: "4px 8px", cursor: "pointer" });
            tagBtn.on("click", function() {
                let color = $("#tagColorPicker").val();
                targetScene.prepend(`<span style='background:${color};'>[${tag}] <a href='#' class='removeTag'>×</a></span>`);
                $("#tagModal").hide();
            });
            $("#existingTags").append(tagBtn);
        });
    });

    $("#addNewTag").off("click").on("click", function() {
        let newTag = $("#newTagInput").val().trim();
        if (newTag && !globalTags.includes(newTag)) globalTags.push(newTag);
        let color = $("#tagColorPicker").val();
        let targetScene = $("#tagModal").data("target");
        targetScene.prepend(`<span style='background:${color};'>[${newTag}] <a href='#' class='removeTag'>×</a></span>`);
        $("#newTagInput").val("");
        $("#tagModal").hide();
    });
}