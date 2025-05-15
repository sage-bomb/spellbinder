// === panel.search.js ===
class SearchPanel extends Panel {
    constructor() {
        super('#panel-search');
        console.log("Search panel loaded");
    }

    render() {
        const panel = this.getPanel();
        panel.empty();
        panel.append('<h3 class="panel-header">Search Panel</h3>');

        const input = $('<input type="text" placeholder="Enter search term">').css({ width: '80%' });
        const button = $('<button>Search</button>');
        const results = $('<div id="search-results"></div>').css({ marginTop: '15px' });

        panel.append(input, button, results);

        button.click(() => {
            const query = input.val().toLowerCase();
            results.empty();
            if (!query) return;

            // ✅ Use api layer instead of raw $.get
            api.getEntities((data) => {
                const matches = data.filter(e =>
                    e.name.toLowerCase().includes(query) ||
                    (e.description && e.description.toLowerCase().includes(query))
                );

                if (matches.length === 0) {
                    results.append('<p>No results found.</p>');
                } else {
                    matches.forEach(entity => {
                        results.append(window.createEntityListItem(entity));
                    });
                }
            });
        });
    }
}

// Expose for button + console call compatibility
window.searchPanel = () => new SearchPanel();
window.searchPanelRender = () => new SearchPanel().render();
