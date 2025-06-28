// ===============================================
// SUPABASE CONFIG FOR NEW PROJECT
// Project: otbswtklpidhezziotac
// ===============================================

const SUPABASE_CONFIG = {
    // NEW PROJECT CREDENTIALS
    url: 'https://otbswtklpidhezziotac.supabase.co',
    anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90YnN3dGtscGlkaGV6emlvdGFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEwOTIyNTEsImV4cCI6MjA2NjY2ODI1MX0.cxOLFAy1UlAwu_Ho_B9hA1PMfvc7Wg3DnIwrRUalzck',
    
    // API ENDPOINTS
    adminApiUrl: 'https://otbswtklpidhezziotac.supabase.co/functions/v1/admin-api',
    
    // PROJECT INFO
    project: 'otbswtklpidhezziotac',
    github: 'https://github.com/MasterPhising/10musd',
    version: '2.0-AUTO-LOGIN-NEW-PROJECT'
};

// HELPER FUNCTIONS
function getApiUrl(endpoint) {
    return `${SUPABASE_CONFIG.adminApiUrl}${endpoint}`;
}

function getHeaders() {
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${SUPABASE_CONFIG.anonKey}`,
        'apikey': SUPABASE_CONFIG.anonKey
    };
}

// API CALL WRAPPER
async function callSupabaseAPI(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: getHeaders(),
            cache: 'no-cache'
        };
        
        if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(getApiUrl(endpoint), options);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error(`API Error [${method} ${endpoint}]:`, error);
        throw error;
    }
}

// EXPORT FOR USAGE
window.SUPABASE_CONFIG = SUPABASE_CONFIG;
window.callSupabaseAPI = callSupabaseAPI;

console.log('🚀 Supabase Config Loaded:', SUPABASE_CONFIG.project);
console.log('📡 Admin API URL:', SUPABASE_CONFIG.adminApiUrl); 