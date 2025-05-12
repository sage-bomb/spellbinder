function renderPanelSearch() {
    clearPanels();
    $('#left_panel').append(`
        <div class="spellbinder-panel">
            <h2>Search Tools</h2>
            <div id='searchTags'></div><br>
            <input type="text" id="searchQuery" placeholder="Enter search..." />
            <input type="number" id="topK" value="5" min="1" max="20" />
            <button id="searchBtn">Search</button>
            <div id="searchResults"></div>
        </div>
    `);

    $('#searchBtn').on('click', function() {
        let results = [
            { type: 'Entity', name: "Test People", tags: ['culture', 'elf'] },
            { type: 'File', name: 'chapter_03.md', tags: ['draft', 'chapter3'] }
        ];
        $('#searchResults').empty();
        results.forEach(item => {
            let block = $(`
                <div class="spellbinder-panel">
                    <b>[${item.type}] ${item.name}</b><br>
                    <div class='scene-tags'></div>
                </div>
            `);

            // 👇 PREFILL EXISTING TAGS
            item.tags.forEach(tag => {
                block.find('.scene-tags').append(`<span style='background:#555;'>[${tag}] <a href='#' class='removeTag'>×</a></span>`);
            });

            $('#searchResults').append(block);

            block.on('click', function() {
                setTarget(item.eid);
                renderPanelEntity();
            });
            attachTagEditor(block.find(".scene-tags"));
        });
    });
}
