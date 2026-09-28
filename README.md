# Cloud-Based Student Assignment Submission & Feedback Portal

A cloud-oriented full-stack project for assignment creation, secure student submission, object storage, grading, feedback and role-based access control.

## Problem
Traditional assignment collection often relies on email, messaging apps or physical files. That makes deadlines, versions, feedback and submission tracking difficult to manage centrally.

## Solution
Students authenticate, view assignments, upload files and see their status/feedback. Teachers create assignments, review private submissions, grade them and provide feedback. Metadata belongs in a relational database while files belong in object storage.

## Architecture

```text
Student / Teacher
       |
       v
 React + Vite Web App
       |
       v
 FastAPI REST API
   |           |
   v           v
Database   Object Storage
(Postgres/ (Supabase Storage
 SQLite)   or local uploads)
       |
       v
 Logging / Monitoring / Tests
```

Cloud deployment can replace local SQLite with managed PostgreSQL and local uploads with private object storage.

## Main Features
- Student and teacher accounts
- Role-based authorization
- Assignment CRUD
- Deadline validation using server time
- PDF/DOCX/ZIP/image upload validation
- Configurable late submission policy
- Private submission download
- Teacher grading and written feedback
- Student/teacher dashboard metrics
- REST API and automatic OpenAPI documentation
- Local mode for zero cloud cost during development
- Cloud adapter for PostgreSQL + Supabase Storage
- Environment-based secrets

## Technology Stack
- Frontend: React + Vite
- Backend: Python + FastAPI
- ORM: SQLAlchemy
- Local database: SQLite
- Cloud database: PostgreSQL/Supabase
- Local storage: filesystem
- Cloud storage: Supabase Storage
- Authentication in the included local demo: bcrypt password hashing + JWT

## Roles
| Capability | Student | Teacher |
|---|---:|---:|
| Register/login | Yes | Yes |
| View assignments | Yes | Yes |
| Create/update/delete assignment | No | Yes |
| Submit/resubmit | Yes | No |
| View own submission | Yes | No |
| Download permitted submission | Own | Course submissions |
| Grade | No | Yes |
| Feedback | Read own | Create |

## Data Model
`User -> Course -> Assignment -> Submission`, with `Submission.student_id` linking a submission to its student.

Files are deliberately not stored as database BLOBs. The database stores `file_name`, `storage_path`, timestamps, status, marks and feedback; object storage stores the actual bytes.

## Local Setup — Windows PowerShell

### 1. Prerequisites
Install Python 3.11+ and Node.js LTS.

### 2. Backend
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python seed_demo.py
uvicorn app.main:app --reload --port 8000
```

If `python` is not recognized, install Python and enable **Add Python to PATH**, then reopen PowerShell. You can also use `python --version` to verify the installation.

API: `http://localhost:8000`  
Docs: `http://localhost:8000/docs`  
Health: `http://localhost:8000/health`

### 3. Frontend — new PowerShell window
```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Open the Vite URL shown in the terminal, normally `http://localhost:5173`.

### Demo accounts
- Teacher: `teacher@demo.local` / `Teacher@123`
- Student: `student@demo.local` / `Student@123`

These are dummy accounts for local demonstration only.

## Cloud Mode

Recommended student-friendly architecture:

```text
React/Vite hosting
      |
      v
FastAPI hosting
  |         |
  v         v
Supabase  Supabase Storage
Postgres   private bucket
```

1. Create a Supabase project.
2. Create a private `submissions` bucket.
3. Run `cloud/supabase_schema.sql` in the SQL editor.
4. Use the Supabase PostgreSQL connection string as `DATABASE_URL`.
5. Set `STORAGE_PROVIDER=supabase`.
6. Fill the Supabase URL/service-role variables in the backend environment.
7. Deploy frontend and backend to suitable free/student hosting where available.

**Security:** never put `SUPABASE_SERVICE_ROLE_KEY`, database passwords or JWT secrets in the frontend or GitHub repository.

The included code keeps local JWT authentication as the zero-cost offline baseline. For a production cloud deployment, Supabase Auth can be introduced as the managed identity provider; keep role checks in the backend rather than trusting the browser.

## REST API
| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/register` | Register demo user |
| POST | `/api/login` | Login |
| POST | `/api/logout` | Logout acknowledgement |
| GET | `/api/courses` | List courses |
| POST | `/api/courses` | Teacher creates course |
| GET | `/api/assignments` | List assignments |
| POST | `/api/assignments` | Teacher creates assignment |
| GET | `/api/assignments/{id}` | Assignment details |
| PUT | `/api/assignments/{id}` | Update assignment |
| DELETE | `/api/assignments/{id}` | Delete assignment |
| POST | `/api/assignments/{id}/submit` | Student upload |
| GET | `/api/submissions/me` | Student submissions |
| GET | `/api/assignments/{id}/submissions` | Teacher reviews submissions |
| GET | `/api/submissions/{id}` | Authorized submission detail |
| GET | `/api/submissions/{id}/download` | Authorized file download |
| POST | `/api/submissions/{id}/grade` | Teacher grade + feedback |
| GET | `/api/submissions/{id}/feedback` | Read feedback |

## Security Controls
- bcrypt password hashing
- signed/expiring JWTs in local mode
- backend role checks
- ownership checks for courses and assignments
- private file download through authorization
- extension and size validation
- server-side deadline check
- environment variables for secrets
- CORS configuration
- database indexes on high-query columns

Production improvements should include HTTPS, managed identity, signed short-lived object URLs, rate limiting, malware scanning, audit logs, centralized logging, backups and secret management.

## Scalability
For small deployments, a single API instance and managed database are enough. For higher traffic, place the API behind a load balancer, run multiple stateless API instances, use object storage + CDN for large files, add caching and queues, and use managed database scaling/replicas.

For a deadline spike with 100,000 students, the browser should upload directly to object storage using short-lived signed URLs where possible. Metadata writes can be queued or rate-controlled, while grading/notifications can run as background jobs. This prevents large files from passing through every API instance.

## Testing
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest ../tests -q
```

Test categories should cover registration, login, role authorization, assignment CRUD, file validation, on-time/late submissions, privacy, grading limits, file retrieval, database/storage failures, logout and protected routes.

## GitHub
Repository name: `Cloud-Based-Assignment-Submission-Portal`

Suggested topics: `cloud-computing`, `edtech`, `python`, `fastapi`, `react`, `cloud-storage`, `postgresql`, `rest-api`, `full-stack`, `authentication`

Suggested commits:
1. `Initialize cloud assignment portal`
2. `Create frontend and backend architecture`
3. `Implement authentication and role management`
4. `Add assignment management module`
5. `Integrate cloud database`
6. `Implement cloud file storage`
7. `Add student assignment submission workflow`
8. `Implement deadline validation`
9. `Add teacher grading and feedback`
10. `Build student and teacher dashboards`
11. `Add security and authorization`
12. `Add automated tests`
13. `Deploy application to cloud`
14. `Complete README and documentation`

## Limitations of the student/demo implementation
- Local mode uses SQLite and filesystem storage.
- Local registration permits choosing the teacher role for demonstration; production systems should use an admin/invitation workflow.
- Malware scanning and advanced audit logging are architectural recommendations rather than bundled services.
- Direct-to-object-storage signed uploads are a recommended scale optimization rather than required for the local MVP.

## Future Improvements
- Managed Supabase Auth
- Signed upload/download URLs
- Course enrollment table
- Admin role and teacher invitations
- Plagiarism detection integration
- Malware scanning worker
- Email notifications
- Assignment version history
- Audit log table
- Redis caching and a queue worker
- CI/CD with automated tests
- Infrastructure as Code

## Project Proof Checklist
Capture screenshots for architecture, login, registration, teacher dashboard, assignment creation, student dashboard, assignment details, upload, stored object, database record, on-time/late status, teacher review, grading, feedback, authorization error, API response, automated tests, cloud deployment, live application, Git history and README.
