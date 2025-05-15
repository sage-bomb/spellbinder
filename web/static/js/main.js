function loadScript(url, callback) {
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = url;
    script.onload = callback;
    script.onerror = () => console.error(`Failed to load ${url}`);
    document.head.appendChild(script);
}

const scripts = [
    '/static/js/data/api.entities.js',    
    '/static/js/core.js',
    '/static/js/data/state.js',

    '/static/js/ui/panelBase.js',
    '/static/js/ui/sortable.js',
    '/static/js/ui/topbar.js',
    '/static/js/ui/elements.js',
    '/static/js/panels/panel.outliner.js',
    '/static/js/panels/panel.editor.js',
    '/static/js/panels/panel.texteditor.js',
    '/static/js/panels/panel.search.js',
    '/static/js/panels/panel.objects.js'
];

// Load all scripts in strict order
(function loadAllScripts(index = 0) {
    if (index >= scripts.length) {
        console.log("All Spellbinder scripts loaded.");

        // ✅ safe startup AFTER guaranteed load
        try {
            initApp?.();
            setupTopbar?.();
            outlinerPanel?.();
//            editorPanel?.();
            texteditorPanel?.();
        } catch (e) {
            console.error("Spellbinder startup error:", e);
        }

        return;
    }

    loadScript(scripts[index], () => loadAllScripts(index + 1));
})();
