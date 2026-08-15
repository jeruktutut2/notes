// Main App & Modal Controller

document.addEventListener('DOMContentLoaded', () => {
    // Tab Navigation
    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

            tab.classList.add('active');
            const targetId = tab.getAttribute('data-tab');
            document.getElementById(targetId).classList.add('active');
        });
    });
});

function openNodeModal(nodeKey) {
    const modal = document.getElementById('node-modal');
    const titleEl = document.getElementById('modal-title');
    const bodyEl = document.getElementById('modal-body');

    const data = ROADMAP_DATA[nodeKey] || {
        title: "Node Detail",
        content: "<p>Dokumentasi lengkap untuk node ini tersedia pada materi modul Markdown.</p>"
    };

    titleEl.textContent = data.title;
    bodyEl.innerHTML = data.content;

    modal.classList.add('active');
}

function closeNodeModal() {
    const modal = document.getElementById('node-modal');
    modal.classList.remove('active');
}

// Close modal when clicking backdrop
document.getElementById('node-modal')?.addEventListener('click', (e) => {
    if (e.target.id === 'node-modal') {
        closeNodeModal();
    }
});
