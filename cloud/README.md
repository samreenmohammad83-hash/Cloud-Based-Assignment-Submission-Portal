# Cloud mode

Recommended student-friendly architecture: React/Vite frontend + FastAPI backend + Supabase PostgreSQL + Supabase Storage.

1. Create a Supabase project.
2. Create a private Storage bucket named `submissions`.
3. Run `supabase_schema.sql`.
4. Set backend `DATABASE_URL` to the Supabase Postgres connection string.
5. Set `STORAGE_PROVIDER=supabase` and the Supabase variables in `.env`.
6. Deploy frontend to a static frontend host and backend to a Python-compatible host.

The sample implementation uses the backend for authentication in local mode so the project can be developed offline. For a production deployment, Supabase Auth can replace the local password/token layer; the UI/API boundaries remain the same.
