# Implementation, Proof and Interview Strategy

## Three implementation options

| Option | Stack | Difficulty | Cost model | Concepts | Advantages | Limitations |
|---|---|---|---|---|---|---|
| A Beginner | HTML/CSS/JS + Flask + SQLite + local uploads | Low | Free | Client/server, REST, DB, files | Easiest learning path | Few genuine managed-cloud services |
| B Recommended | React + FastAPI + PostgreSQL/Supabase + Supabase Storage | Medium | Local free; managed free tier where available | DB, object storage, auth boundary, REST, deployment, RBAC | Strong balance for a student portfolio | Requires cloud configuration |
| C Advanced | React/Next.js + FastAPI/functions + AWS/Azure/GCP managed services | High | Local emulators + cloud free allowances where available | API Gateway, serverless, load balancing, CDN, monitoring, IAM | Closest to enterprise architecture | More setup and cloud complexity |

**Recommended learning path:** build the included local B-style application first, then migrate database/storage to managed cloud services. This demonstrates the difference between local development and cloud deployment without making paid infrastructure a prerequisite.

## Where each cloud concept appears
- Cloud computing: deploy the same application to managed hosting.
- SaaS: hosted portal is consumed by students/teachers.
- PaaS: managed database/application hosting.
- IaaS: optional VM deployment of FastAPI.
- Cloud DB: PostgreSQL/Supabase.
- Object storage: Supabase Storage/private bucket.
- Auth: local JWT in MVP; managed identity can replace it in production.
- RBAC: `require_role()` and ownership checks.
- REST: `/api/...` endpoints.
- Serverless: optional function-based deployment for notifications/processing.
- Scalability/elasticity: multiple stateless API instances + managed services.
- Availability: redundant managed services and multiple instances.
- Load balancing: place API instances behind a managed load balancer.
- CDN: frontend/static assets and controlled file delivery.
- API Gateway: managed routing/throttling in advanced architecture.
- Environment variables: `.env` locally and deployment environment settings in cloud.
- Secrets: service-role/database credentials stay server-side.
- Logging: platform logs plus application logs.
- Monitoring: `/health`, platform metrics and alerts.
- Backup: managed database/object-storage backup policies.
- CI/CD: GitHub workflow can run tests/build/deploy.

## Cloud data model
Database = structured metadata. Object storage = large file bytes. The storage reference in `Submission.storage_path` connects the two.

## Failure and reliability design
Use retries only for transient failures, exponential backoff for external services, idempotency keys for repeated submission requests, and never report success until the required storage/database operation has succeeded.

## 13-day GitHub proof plan
| Day | Files/features | Suggested commit | Screenshot proof |
|---|---|---|---|
| 1 | README, folder architecture | Initialize cloud assignment portal | `01_project_structure.png` |
| 2 | auth endpoints/UI | Implement authentication and role management | `02_login_registration.png` |
| 3 | role checks | Add security and authorization | `03_authorization_error.png` |
| 4 | assignment CRUD | Add assignment management module | `04_assignment_creation.png` |
| 5 | SQLAlchemy/Postgres plan | Integrate cloud database | `05_database_record.png` |
| 6 | storage service | Implement cloud file storage | `06_object_storage.png` |
| 7 | upload workflow | Add student assignment submission workflow | `07_successful_upload.png` |
| 8 | deadline status | Implement deadline validation | `08_late_submission.png` |
| 9 | grading | Add teacher grading and feedback | `09_grading_feedback.png` |
| 10 | dashboards | Build student and teacher dashboards | `10_dashboards.png` |
| 11 | tests/security docs | Add automated tests | `11_test_results.png` |
| 12 | deployment config | Deploy application to cloud | `12_cloud_deployment.png` |
| 13 | README/report | Complete README and documentation | `13_github_readme.png` |

## Screenshot naming checklist
1. `01_project_structure.png` — folders and files prove organization.
2. `02_architecture_diagram.png` — proves cloud architecture understanding.
3. `03_login_page.png` — authentication UI.
4. `04_student_registration.png` — registration.
5. `05_teacher_dashboard.png` — teacher metrics.
6. `06_assignment_creation.png` — assignment configuration.
7. `07_student_dashboard.png` — student metrics.
8. `08_assignment_list.png` — available coursework.
9. `09_assignment_details.png` — deadline and rules.
10. `10_file_selection.png` — upload screen.
11. `11_successful_upload.png` — submission confirmation.
12. `12_cloud_storage_object.png` — stored file/object.
13. `13_database_submission_record.png` — metadata row.
14. `14_on_time_status.png` — on-time status.
15. `15_late_status.png` — late submission.
16. `16_teacher_submission_list.png` — teacher review.
17. `17_submission_file_review.png` — permitted file access.
18. `18_marks_feedback.png` — grading.
19. `19_student_feedback.png` — student view.
20. `20_unauthorized_access.png` — RBAC failure response.
21. `21_api_response.png` — REST API response.
22. `22_automated_tests.png` — test output.
23. `23_cloud_dashboard.png` — hosting/database/storage dashboard.
24. `24_live_application.png` — deployed application.
25. `25_github_commits.png` — development history.
26. `26_github_repository.png` — repository overview.
27. `27_readme_preview.png` — documentation.

## Resume proof
### Three bullets
- Built a cloud-oriented assignment portal with React, FastAPI, SQLAlchemy and PostgreSQL/Supabase architecture, separating relational metadata from object storage for student file submissions.
- Implemented JWT authentication, role-based authorization and ownership checks to protect teacher grading workflows and private student submissions.
- Designed deadline-aware upload, grading and feedback workflows with REST APIs, file validation, automated tests and a migration path from local SQLite/filesystem storage to managed cloud services.

### Two-line project description
**Cloud-Based Student Assignment Submission & Feedback Portal** — Full-stack cloud computing project for assignment management, secure file submission, grading and feedback using React, FastAPI, relational database and object storage. Demonstrates RBAC, REST APIs, cloud deployment, security, scalability and failure-handling concepts.

### LinkedIn description
Built a cloud-oriented Student Assignment Submission & Feedback Portal that separates structured metadata from file objects, applies role-based authorization, validates deadlines/uploads, and provides teacher grading and student feedback workflows. Developed a local-first architecture that can migrate to managed PostgreSQL and object storage for cloud deployment.

### Skills demonstrated
Cloud Computing, React, FastAPI, Python, REST APIs, SQLAlchemy, PostgreSQL, SQLite, Object Storage, JWT, RBAC, Authentication, Authorization, File Uploads, API Security, Git, GitHub, Testing, Deployment Architecture, Scalability, Failure Handling.

## GitHub repository description
Cloud-based student assignment submission and feedback platform featuring role-based authentication, REST APIs, managed database/object-storage architecture, secure file submission, deadline validation, grading and feedback.

## Interview — exactly 10 questions and answers

### 1. Explain your project.
**Answer:** My project is a Cloud-Based Student Assignment Submission and Feedback Portal. Teachers create assignments with deadlines and file rules. Students log in, view their assignments and upload files. The backend stores structured submission metadata in a relational database and stores the actual file in object storage. Teachers can review, grade and provide feedback, and students can see their results. I also designed the system so the local SQLite/filesystem version can be migrated to managed PostgreSQL and cloud object storage.

### 2. Why did you use cloud computing for this project?
**Answer:** The main reason is centralized remote access and independent scalability. Database records and large assignment files have different storage characteristics, so a managed database and object storage are a natural fit. Cloud deployment also makes the portal available to users without requiring a server inside the college.

### 3. Why should files be stored in object storage instead of the database?
**Answer:** The database is optimized for structured records and queries, while object storage is designed for large binary files. I keep the file name, storage path, status, marks and feedback in the database and keep the actual PDF or document in storage.

### 4. How does authentication differ from authorization in your project?
**Answer:** Authentication verifies identity using login credentials and a token. Authorization happens after authentication and checks the user's role and ownership. For example, a student can submit an assignment but cannot call the teacher grading endpoint.

### 5. How do you protect a student's private submission?
**Answer:** The download endpoint checks the authenticated user. A student can download only their own submission. A teacher can download a submission only when the assignment belongs to that teacher. The production cloud version should additionally use private storage and short-lived signed URLs.

### 6. How does the REST API work?
**Answer:** The React frontend sends HTTP requests to FastAPI endpoints. For example, `POST /api/assignments/{id}/submit` uploads a file and creates metadata. The API returns HTTP status codes and JSON responses, and the backend performs validation and authorization before changing data.

### 7. How did you implement file upload security?
**Answer:** I validate the extension, reject empty files and enforce the assignment's maximum file size. I also avoid trusting the browser for authorization. A production version should add MIME/content validation, malware scanning, private buckets and signed URLs.

### 8. How would you scale this to many students?
**Answer:** I would keep the API stateless and run multiple instances behind a load balancer. Files would go directly to object storage using signed URLs where possible. A managed database would handle metadata, while queues and background workers could process notifications or scanning asynchronously. Caching and database indexes would reduce repeated query load.

### 9. What happens if an upload succeeds but the database write fails?
**Answer:** The system should not report a successful submission until both required operations are complete. A production implementation can use a submission state machine and cleanup/reconciliation job for orphaned objects. Idempotency keys also prevent a retry from creating duplicate logical submissions.

### 10. How would you deploy the project?
**Answer:** During development I use React/Vite locally, FastAPI locally, SQLite and local uploads. For cloud deployment I can replace SQLite with managed PostgreSQL and local uploads with private object storage. The frontend and backend can be deployed separately, and secrets are supplied through environment variables rather than committed to Git.
