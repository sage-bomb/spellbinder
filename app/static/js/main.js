document.getElementById('searchForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const query = document.getElementById('query').value;
    const top_k = document.getElementById('top_k').value;
    const formData = new FormData();
    formData.append("query", query);
    formData.append("top_k", top_k);

    const response = await fetch('/search', { method: 'POST', body: formData });
    const data = await response.json();
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<h3>Results</h3>' + data.results.map(r =>
        `<div><b>${r.file}</b>: ${r.text} (Score: ${r.score.toFixed(3)})</div>`
    ).join('');
});

document.getElementById('embedForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const dir = document.getElementById('embed_dir').value;
    const formData = new FormData();
    formData.append("directory_path", dir);
    formData.append("memory_only", "false");

    await fetch('/embed', { method: 'POST', body: formData });
    alert("Embedding complete.");
});

async function loadEmbeddings() {
    const formData = new FormData();
    formData.append("force_reload", "false");
    await fetch('/load', { method: 'POST', body: formData });
    alert("Embeddings loaded.");
}