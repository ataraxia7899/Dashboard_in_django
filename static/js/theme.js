document.addEventListener('DOMContentLoaded', () => {
	const themeToggleBtn = document.getElementById('theme-toggle-btn');
	const root = document.documentElement;

	/**
	 * Applies the given theme to the page and updates the toggle button icon.
	 * Dispatches a 'themeChanged' event.
	 * @param {string} theme - The theme to apply ('light' or 'dark').
	 */
	const applyTheme = (theme) => {
		if (theme === 'dark') {
			root.dataset.theme = 'dark';
			if (themeToggleBtn) {
				themeToggleBtn.querySelector('.material-icons').textContent = 'light_mode';
			}
		} else {
			delete root.dataset.theme;
			if (themeToggleBtn) {
				themeToggleBtn.querySelector('.material-icons').textContent = 'dark_mode';
			}
		}
		// Dispatch a custom event that other scripts can listen to
		document.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
	};

	// Apply saved theme on page load
	const savedTheme = localStorage.getItem('theme') || 'light';
	applyTheme(savedTheme);

	// Add event listener to the toggle button
	if (themeToggleBtn) {
		themeToggleBtn.addEventListener('click', () => {
			const newTheme = root.dataset.theme === 'dark' ? 'light' : 'dark';
			localStorage.setItem('theme', newTheme);
			applyTheme(newTheme);
		});
	}
});