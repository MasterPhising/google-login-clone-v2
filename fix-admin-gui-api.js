// Fix incorrect API keys in admin GUI

const fs = require('fs');
const path = require('path');

const ADMIN_GUI_PATH = 'admin-gui/index.html';

// Incorrect API key (has typo "rolEz" instead of "role")
const INCORRECT_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90YnN3dGtscGlkaGV6emlvdGFjIiwicm9sZUV6ImFub24iLCJpYXQiOjE3NTEwOTIyNTEsImV4cCI6MjA2NjY2ODI1MX0.cxOLFAy1UlAwu_Ho_B9hA1PMfvc7Wg3DnIwrRUalzck';

// Correct API key (fixed "role" spelling)
const CORRECT_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90YnN3dGtscGlkaGV6emlvdGFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEwOTIyNTEsImV4cCI6MjA2NjY2ODI1MX0.cxOLFAy1UlAwu_Ho_B9hA1PMfvc7Wg3DnIwrRUalzck';

function fixAdminGuiApiKeys() {
    console.log('🔧 Fixing Admin GUI API keys...\n');
    
    try {
        // Read the file
        console.log('📖 Reading admin GUI file...');
        const content = fs.readFileSync(ADMIN_GUI_PATH, 'utf8');
        
        // Count occurrences of incorrect key
        const incorrectMatches = (content.match(new RegExp(INCORRECT_KEY, 'g')) || []).length;
        console.log(`❌ Found ${incorrectMatches} instances of incorrect API key`);
        
        if (incorrectMatches === 0) {
            console.log('✅ No incorrect API keys found! Admin GUI is already correct.');
            return true;
        }
        
        // Replace all incorrect keys with correct ones
        console.log('🔄 Replacing all incorrect API keys...');
        const fixedContent = content.replace(new RegExp(INCORRECT_KEY, 'g'), CORRECT_KEY);
        
        // Verify the fix
        const remainingIncorrect = (fixedContent.match(new RegExp(INCORRECT_KEY, 'g')) || []).length;
        const correctMatches = (fixedContent.match(new RegExp(CORRECT_KEY, 'g')) || []).length;
        
        console.log(`✅ After fix: ${remainingIncorrect} incorrect, ${correctMatches} correct`);
        
        if (remainingIncorrect > 0) {
            console.log('⚠️ Warning: Some incorrect keys still remain!');
        }
        
        // Write the fixed content back
        console.log('💾 Writing fixed content back to file...');
        fs.writeFileSync(ADMIN_GUI_PATH, fixedContent, 'utf8');
        
        console.log('\n🎉 SUCCESS: Admin GUI API keys fixed!');
        console.log(`✅ Replaced ${incorrectMatches} incorrect API keys`);
        console.log('💡 Admin GUI should now be able to fetch data from database');
        
        return true;
        
    } catch (error) {
        console.error('❌ Error fixing admin GUI:', error.message);
        return false;
    }
}

// Run the fix
console.log('🚀 ADMIN GUI API KEY FIX UTILITY\n');
const success = fixAdminGuiApiKeys();

if (success) {
    console.log('\n📝 NEXT STEPS:');
    console.log('1. Refresh the Admin GUI in your browser');
    console.log('2. Test login on frontend');  
    console.log('3. Check if data appears in Admin GUI');
} else {
    console.log('\n❌ Fix failed! Please check the error above.');
} 