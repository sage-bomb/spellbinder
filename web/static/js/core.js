
// Core initialization logic
function initApp() {
    console.log('Spellbinder v6 initialized');
}
// core.js

window.api = {
    getEntities(callback) {
        $.get("/api/entities", callback);
    },

    getEntity(edi, callback) {
        $.get(`/api/entity/${edi}`, callback);
    },

    createEntity(entity, callback) {
        $.post("/api/entity", JSON.stringify(entity), "json").done(callback);
    },

    updateEntity(entity, callback) {
        $.ajax({
            url: `/api/entity/${entity.edi}`,
            type: 'PATCH',
            contentType: 'application/json',
            data: JSON.stringify(entity),
            success: callback
        });
    },

    deleteEntity(edi, callback) {
        $.ajax({
            url: `/api/entity/${edi}`,
            type: 'DELETE',
            success: callback
        });
    }
};
