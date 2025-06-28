-- 🔧 FIX: Add missing page_status column to requests table

-- Add page_status column if it doesn't exist
DO $$
BEGIN
  -- Add page_status column if it doesn't exist
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'requests' AND column_name = 'page_status' AND table_schema = 'public') THEN
    ALTER TABLE public.requests ADD COLUMN page_status TEXT DEFAULT 'Login';
    RAISE NOTICE 'Added page_status column to requests table';
  ELSE
    RAISE NOTICE 'page_status column already exists';
  END IF;
END $$;

-- Create index on page_status if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_requests_page_status') THEN
    CREATE INDEX idx_requests_page_status ON public.requests(page_status);
    RAISE NOTICE 'Created index on page_status column';
  END IF;
END $$;

-- Success message
DO $$
BEGIN
  RAISE NOTICE '✅ page_status column fix completed!';
  RAISE NOTICE 'Edge function should now work properly';
END $$; 