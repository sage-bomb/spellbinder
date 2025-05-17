function setupTopbar() {
 $('.panel-toggle').click(function() {
    const panel = $(this).data('panel');
    const panelDiv = $(`#panel-${panel}`);

    if (panelDiv.hasClass('inactive')) {
        panelDiv.removeClass('inactive');
        const renderFunctionName = `${panel}PanelRender`;
        const renderFunc = window[renderFunctionName];
        if (typeof renderFunc === 'function') {
            renderFunc();
        }
    } else {
        panelDiv.addClass('inactive');
    }
});

}
