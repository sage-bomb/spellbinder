function renderPanelGraph() {
    $('#left_panel').empty();
    $('#left_panel').append(`
        <div class="spellbinder-panel">
            <h2>Entity Graph</h2>
            
            <pre>
  [Test People]──[Horse]──[Hero]
              │
              └──[Wizzard]
            </pre>
            <small>(Example static graph)</small>
        </div>
    `);
}