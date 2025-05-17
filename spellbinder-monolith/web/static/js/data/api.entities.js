// === web/static/js/data/api.entities.js ===

// API calls for entity CRUD using new backend

function getEntities(callback) {
    $.get("/entities/", callback);
}

function getEntity(edi, callback) {
    $.get(`/entities/${edi}`, callback);
}

function createEntity(entity, callback) {
    const safeEntity = Object.assign({}, entity);
    delete safeEntity.edi;

    $.ajax({
        url: "/entities/",
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(safeEntity),
        success: function(response) {
            entity.edi = response.edi; // Patch server eid back
            if (callback) callback(response);
        }
    });
}

function updateEntity(entity, callback) {
    $.ajax({
        url: `/entities/${entity.edi}`,
        type: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(entity),
        success: callback
    });
}

function deleteEntity(edi, callback) {
    $.ajax({
        url: `/entities/${edi}`,
        type: 'DELETE',
        success: callback
    });
}

// Export
window.DataAPI = {
    getEntities,
    getEntity,
    createEntity,
    updateEntity,
    deleteEntity
};