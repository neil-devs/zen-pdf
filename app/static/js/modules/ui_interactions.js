/* * UI INTERACTIONS MODULE
 * Handles: Dropdowns, Page Transitions, Alerts
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. USER DROPDOWN MENU ---
    const userMenu = document.querySelector('.user-menu-container');
    
    if (userMenu) {
        // Toggle on click
        userMenu.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent closing immediately
            userMenu.classList.toggle('active');
        });

        // Close when clicking anywhere else
        document.addEventListener('click', (e) => {
            if (!userMenu.contains(e.target)) {
                userMenu.classList.remove('active');
            }
        });
    }

    // --- 2. FLASH MESSAGES (Auto Dismiss) ---
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length > 0) {
        setTimeout(() => {
            alerts.forEach(alert => {
                alert.style.transition = "opacity 0.5s ease";
                alert.style.opacity = "0";
                setTimeout(() => alert.remove(), 500); // Remove from DOM after fade
            });
        }, 4000); // Disappear after 4 seconds
    }

    // --- 3. PAGE TRANSITION CURTAIN (Fade In) ---
    // This removes the black screen when page is fully loaded
    document.body.classList.add('page-loaded');

    // --- 4. PAGE TRANSITION CURTAIN (Fade Out) ---
    // This adds the black screen before moving to a new page
    const transitionLinks = document.querySelectorAll('a:not([target="_blank"]):not([href^="#"])');
    
    transitionLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Only transition if it's an internal link
            if (href && href.startsWith('/')) {
                e.preventDefault();
                document.body.classList.remove('page-loaded'); // Fade to black
                
                setTimeout(() => {
                    window.location.href = href;
                }, 600); // Wait 600ms for animation
            }
        });
    });
});