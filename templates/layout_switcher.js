/**
 * Layout Switcher
 * Allows switching between different layout templates (A, B, C, D, E)
 * for the same page content
 */

// Get current page name from URL
function getCurrentPage() {
    const path = window.location.pathname;
    const page = path.split('/').pop().replace('.html', '');
    return page;
}

// Switch to a different layout
function switchLayout(layoutKey) {
    const currentPage = getCurrentPage();
    const newUrl = `${currentPage}-layout-${layoutKey}.html`;

    // Store preference
    localStorage.setItem(`layout_${currentPage}`, layoutKey);

    // Reload with new layout (in production, this would regenerate)
    alert(`Layout ${layoutKey.toUpperCase()} selected!\n\nTo fully implement: Regenerate site with layout override for ${currentPage}.`);

    // Update active button
    document.querySelectorAll('.layout-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
}

// Initialize layout switcher on page load
document.addEventListener('DOMContentLoaded', function() {
    // Check for saved layout preference
    const currentPage = getCurrentPage();
    const savedLayout = localStorage.getItem(`layout_${currentPage}`);

    if (savedLayout) {
        const btn = document.querySelector(`[data-layout="${savedLayout}"]`);
        if (btn) btn.classList.add('active');
    }
});

// Export for use in HTML
window.switchLayout = switchLayout;
