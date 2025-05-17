
// Sorting utilities for outliner + scenes
function enableOutlinerSorting() {
    $('#panel-outliner').sortable({
        items: '.act-group',
        handle: '.entity.act',
        update: function() {
            let order = [];
            $('.act-group').each(function() {
                order.push($(this).data('act-id'));
            });
            $.post('/api/entity_order', JSON.stringify(order), "json");
        }
    });
}

function enableSceneSorting() {
    $('.scenes-list').each(function() {
        $(this).sortable({
            items: '.entity.scene',
            connectWith: '.scenes-list',
            update: function() {
                let actId = $(this).closest('.act-group').data('act-id');
                let sceneOrder = [];
                $(this).children('.entity.scene').each(function() {
                    sceneOrder.push($(this).data('entity').edi);
                });
                console.log(`Scenes reordered for Act ${actId}:`, sceneOrder);
            }
        });
    });
}
