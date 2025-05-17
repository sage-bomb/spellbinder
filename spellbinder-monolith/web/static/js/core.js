// === web/static/js/core.js ===

// Core initialization logic
function initApp() {
    console.log('Spellbinder UI initialized');
}

// Legacy window.api shim now delegates to window.DataAPI
window.api = {
    getEntities: window.DataAPI.getEntities,
    getEntity: window.DataAPI.getEntity,
    createEntity: window.DataAPI.createEntity,
    updateEntity: window.DataAPI.updateEntity,
    deleteEntity: window.DataAPI.deleteEntity
};