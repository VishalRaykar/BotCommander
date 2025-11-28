// Authentication utility functions

async function checkAuth() {
    try {
        const response = await api.get('/api/me');
        if (response.ok) {
            const data = await response.json();
            await updateNavUser(data.user);
            return true;
        } else {
            if (window.location.pathname !== '/' && !window.location.pathname.includes('index')) {
                window.location.href = '/';
            }
            return false;
        }
    } catch (error) {
        console.error('Auth check failed:', error);
        return false;
    }
}

async function updateNavUser(user) {
    const navUser = document.getElementById('navUser');
    const btnLogout = document.getElementById('btnLogout');
    const navDashboard = document.getElementById('navDashboard');
    const navAdmin = document.getElementById('navAdmin');
    
    if (navUser && user) {
        navUser.textContent = user.name || user.email;
        navUser.style.display = 'inline-block';
    }
    
    if (navDashboard) {
        navDashboard.style.display = 'inline-block';
    }
    
    // Check if user is admin
    if (navAdmin && user && user.is_admin) {
        navAdmin.style.display = 'inline-block';
    }
    
    if (btnLogout) {
        btnLogout.style.display = 'inline-block';
        // Remove existing listeners to avoid duplicates
        const newBtn = btnLogout.cloneNode(true);
        btnLogout.parentNode.replaceChild(newBtn, btnLogout);
        newBtn.addEventListener('click', async () => {
            try {
                await api.post('/api/logout');
                window.location.href = '/';
            } catch (error) {
                console.error('Logout failed:', error);
                window.location.href = '/';
            }
        });
    }
}

// Auto-check auth on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', checkAuth);
} else {
    checkAuth();
}

