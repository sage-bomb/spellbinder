function setupTopbar() {
    $('.panel-toggle').click(function() {
        const panel = $(this).data('panel');
        const panelDiv = $(`#panel-${panel}`);
        panelDiv.removeClass('hidden');

        // Force the corresponding panel render call
        const renderFunctionName = `${panel}PanelRender`;
        const renderFunc = window[renderFunctionName];
        if (typeof renderFunc === 'function') {
            renderFunc();
        }
    });
}