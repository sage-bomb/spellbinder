// === panel.search.js ===
class SearchPanel extends Panel {
    constructor() {
        super('#panel-search');
        console.log("Search panel loaded");
    }

    render() {
        const panel = this.getPanel();
        panel.empty();
        panel.append('<h3>Search Panel</h3>');

        // Search input + button
        const input = $('<input type="text" placeholder="Enter search term">').css({ width: '80%' });
        const button = $('<button>Search</button>');
        const results = $('<div id="search-results"></div>').css({ marginTop: '15px' });

        panel.append(input);
        panel.append(button);
        panel.append(results);

        button.click(() => {
            const query = input.val().toLowerCase();
            results.empty();
            if (!query) return;

            // Fake search by scanning entities
            $.get("/api/entities", function(data) {
                const matches = data.filter(e =>
                    e.name.toLowerCase().includes(query) ||
                    (e.description && e.description.toLowerCase().includes(query))
                );
                if (matches.length === 0) {
                    results.append('<p>No results found.</p>');
                } else {
                    matches.forEach(entity => {
                        const item = $('<div class="entity"></div>')
                            .text(entity.name)
                            .data('entity', entity);
                        item.click(() => {
                            window.editorPanelRender(entity);
                            $('#panel-entityeditor').removeClass('hidden');
                        });
                        results.append(item);
                    });
                }
            });
        });
    }
}

// Expose for button + console call compatibility
window.searchPanel = () => new SearchPanel();
window.searchPanelRender = () => new SearchPanel().render();
