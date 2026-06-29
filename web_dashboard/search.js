document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.querySelector('.nav-search input');
    const tableBody = document.getElementById('reportsTableBody');
    if (!searchInput || !tableBody) return;

    let debounceTimer;

    const renderReports = (reports) => {
        if (!reports || reports.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="7" style="text-align:center;">No reports found.</td></tr>';
            return;
        }

        tableBody.innerHTML = reports.map(r => {
            const verdict = r.verdict && r.verdict.toLowerCase().includes('tumor') ? 'Tumor' : 'Normal';
            const badgeClass = verdict === 'Tumor' ? 'positive' : 'negative';
            const date = new Date(r.created_at).toLocaleDateString();
            
            return `
                <tr>
                    <td><strong>${r.scan_id || '-'}</strong></td>
                    <td>${r.patient_name || '-'}</td>
                    <td>${date}</td>
                    <td><span class="status-badge ${badgeClass}">${verdict}</span></td>
                    <td>${r.confidence || '-'}</td>
                    <td>${r.risk_level || '-'}</td>
                    <td>
                        <button class="btn btn-small btn-outline" onclick="alert('View feature coming soon!')">View</button>
                    </td>
                </tr>
            `;
        }).join('');
    };

    const fetchReports = async (query = '') => {
        try {
            const res = await fetch(`/search?q=${encodeURIComponent(query)}`);
            if (res.ok) {
                const data = await res.json();
                renderReports(data);
            }
        } catch (e) {
            console.error('Failed to fetch reports:', e);
        }
    };

    // Load initially
    fetchReports('');

    searchInput.addEventListener('input', (e) => {
        const reportsTab = document.querySelector('.nav-item[data-tab="reports"]');
        if (reportsTab && !reportsTab.classList.contains('active')) {
            reportsTab.click();
        }
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            fetchReports(e.target.value);
        }, 300);
    });
});
