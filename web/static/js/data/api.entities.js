
// API calls for entity CRUD
function getEntities(callback) {
    $.get("/api/entities", callback);
}

function saveEntity(entity, callback) {
    $.ajax({
        url: '/api/entity/' + entity.edi,
        type: 'PATCH',
        contentType: 'application/json',
        data: JSON.stringify(entity),
        success: callback
    });
}

function deleteEntity(id, callback) {
    $.ajax({
        url: '/api/entity/' + id,
        type: 'DELETE',
        success: callback
    });
}
