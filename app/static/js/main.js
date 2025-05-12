
async function showAllFiles() {
    const response = await fetch('/list_files');
    const data = await response.json();
    const resultsDiv = document.getElementById('results');

    resultsDiv.innerHTML = '<h3>All Files</h3>' + data.files.map(file => `
        <div class="file-card">
            <div>
                <b>${file.filename}</b> (Size: ${file.size} bytes)<br>
                <small>EID: ${file.eid}</small>
            </div>
            <div class="result-tags">
                ${file.tags.map(tag => `<span class="tag" onclick="removeTag('${file.eid}', '${tag}')">${tag} ✕</span>`).join('')}
            </div>
            <div>
                <button onclick="openFileByEid('${file.eid}')">Open</button>
                <button onclick="promptAddTag('${file.eid}')">Add Tag</button>
            </div>
        </div>
    `).join('');
}

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

    resultsDiv.innerHTML = '<h3>Results</h3>' + data.results.map(r => {
        const tagsHTML = (r.tags || []).map(tag => `
    <span class="tag" onclick="removeTag('${r.file_eid}', '${tag}', refreshSearch)">${tag} ✕</span>
`).join('');
const addTagButton = `<button onclick="promptAddTag('${r.file_eid}', refreshSearch)">+ Add Tag</button>`;
        return `
            <div class="result-card">
                <div>
                    <b><a href="#" onclick="readFile('${r.file}')">${r.file}</a></b>: ${r.text} (Score: ${r.score.toFixed(3)})
                </div>
                <div>
                    <a href="#" onclick="toggleTags('${r.eid}')">[▼ Show Tags]</a>
                </div>
<div id="tags-${r.eid}" class="result-tags" style="display:none;">
    ${tagsHTML}
    ${addTagButton}
</div>
            </div>
        `;
    }).join('');
});

function setReaderTags(eid, tags) {
    const tagDiv = document.getElementById('readerTags');
    tagDiv.innerHTML = tags.map(tag => `
        <span class="tag" onclick="removeTagAndRefresh('${eid}', '${tag}')">${tag} ✕</span>
    `).join('');
    tagDiv.innerHTML += `<button onclick="promptAddTagReader('${eid}')">+ Add Tag</button>`;
}

async function promptAddTag(eid, refreshCallback = showAllFiles) {
    const tag = prompt("Enter tag to add:");
    if (tag) {
        const formData = new FormData();
        formData.append("eid", eid);
        formData.append("tag", tag);
        await fetch('/add_tag', { method: 'POST', body: formData });
        alert("Tag added.");
        refreshCallback();    // 🪄 now calls whichever view you want
    }
}

function refreshSearch() {
    document.getElementById("searchForm").requestSubmit();
}

async function removeTag(eid, tag) {
    const formData = new FormData();
    formData.append("eid", eid);
    formData.append("tag", tag);
    await fetch('/remove_tag', { method: 'POST', body: formData });
    alert("Tag removed.");
    showAllFiles();
}

async function readFile(filename) {
    const response = await fetch(`/read?file=${encodeURIComponent(filename)}`);
    const text = await response.text();
    document.getElementById('readerFilename').textContent = filename;
    document.getElementById('readerContent').textContent = text;
    document.getElementById('readerApp').style.display = 'flex';
}

async function openFileByEid(eid) {
    const response = await fetch(`/open_file?eid=${encodeURIComponent(eid)}`);
    const data = await response.json();
    document.getElementById('readerFilename').textContent = `File: ${data.filename}`;
    document.getElementById('readerContent').textContent = data.content;
    document.getElementById('readerApp').style.display = 'flex';
    await refreshReaderTags(eid);
}

async function removeTagAndRefresh(eid, tag) {
    await removeTag(eid, tag);   // ← this works, don't rename!
    await refreshReaderTags(eid);
}

async function promptAddTagReader(eid) {
    const tag = prompt("Enter tag to add:");
    if (tag) {
        await addTag(eid, tag);   // ← same addTag function from File Manager
        await refreshReaderTags(eid);
    }
}

async function addTag(eid, tag) {
    const formData = new FormData();
    formData.append("eid", eid);
    formData.append("tag", tag);
    await fetch('/add_tag', { method: 'POST', body: formData });
}


async function refreshReaderTags(eid) {
    const response = await fetch(`/get_file_metadata?eid=${eid}`);
    const data = await response.json();
    setReaderTags(eid, data.tags);
}

function closeReader() {
    document.getElementById('readerApp').style.display = 'none';
}

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

function copyReader() {
    const text = document.getElementById('readerContent').textContent;
    navigator.clipboard.writeText(text).then(() => {
        alert("Content copied to clipboard.");
    });
}

function saveReader() {
    alert("Save function coming soon.");
}

function summarizeReader() {
    alert("Summarize function coming soon.");
}

function annotateReader() {
    alert("Annotate function coming soon.");
}

function toggleTags(eid) {
    const tagDiv = document.getElementById(`tags-${eid}`);
    if (tagDiv.style.display === "none") {
        tagDiv.style.display = "flex";
    } else {
        tagDiv.style.display = "none";
    }
}
