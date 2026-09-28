# Project Report — Cloud-Based Student Assignment Submission & Feedback Portal

## Abstract
The Cloud-Based Student Assignment Submission & Feedback Portal is a web application that centralizes assignment creation, file submission, grading and feedback. A relational database stores structured metadata while object storage stores assignment files. Authentication and role-based authorization protect teacher and student operations. The design can run locally for learning and can be moved to managed cloud database and object-storage services for deployment.

## Introduction
Students need a reliable way to discover coursework, submit files and review feedback. Teachers need centralized control over deadlines, submissions and grades. Cloud computing is suitable because the application can be accessed remotely, storage can scale independently from database metadata, and managed services can improve availability and operational simplicity.

## Problem Statement
Email and manual file collection make it difficult to enforce deadlines, track versions, protect private submissions and return feedback consistently.

## Objectives
1. Provide secure role-based login.
2. Allow teachers to manage assignments.
3. Allow students to submit files and view status.
4. Store metadata separately from file content.
5. Provide grading and written feedback.
6. Demonstrate cloud database, object storage, REST APIs and deployment concepts.
7. Demonstrate security, scalability, testing and GitHub proof of work.

## Existing System
Manual submission, email attachments or disconnected LMS workflows may require repeated manual tracking. Common issues include duplicate versions, difficult deadline verification and scattered feedback.

## Proposed System
The proposed portal provides a central application with a React client, FastAPI REST backend, relational database and object storage. The API applies authentication and authorization before reading or modifying protected data.

## User Roles
**Student:** register/login, view assignments, upload/resubmit, view own status, download own files, view marks and feedback.

**Teacher:** login, create/update/delete assignments, set deadlines, review submissions, download permitted files, grade and provide feedback.

**Optional administrator:** manage users, courses and teacher assignments.

## Cloud Computing Concepts
- **Cloud Computing:** the same application can be deployed on managed hosting, database and object-storage services.
- **SaaS:** students and teachers consume the portal as a hosted application.
- **PaaS:** managed application/database hosting removes server-management work.
- **IaaS:** a VM-based deployment can host FastAPI when desired.
- **Cloud database:** PostgreSQL stores users, courses, assignments and submission metadata.
- **Object storage:** files are stored as objects instead of database BLOBs.
- **Authentication:** verifies identity.
- **Authorization/RBAC:** verifies whether a role can perform an action.
- **REST API:** frontend communicates with backend HTTP endpoints.
- **Serverless:** optional future architecture can move upload processing or notifications to functions.
- **Scalability/elasticity:** stateless API instances and managed services can scale independently.
- **Availability:** managed services and multiple API instances can reduce single-server dependence.
- **Load balancing:** routes requests across API instances in a larger deployment.
- **CDN:** can accelerate public/static frontend assets and, with correct security design, file delivery.
- **API Gateway:** can provide a managed entry point, throttling and routing in advanced cloud architecture.
- **Environment variables:** separate configuration from source code.
- **Secrets management:** prevents credentials being committed to Git.
- **Logging/monitoring:** health endpoints and platform logs provide operational visibility.
- **Backup:** database and object-storage backup policies protect data.
- **CI/CD:** tests and deployment can run automatically on Git pushes.

## Industry Relevance
The architecture maps to LMS platforms, universities, schools, corporate training portals, certification systems, bootcamps and EdTech platforms. Benefits include centralized data, remote access, scalable storage, automated tracking, reduced paperwork, centralized feedback and controlled access.

## Technology Stack
Frontend: React/Vite. Backend: FastAPI. Database abstraction: SQLAlchemy. Local database: SQLite. Cloud database: PostgreSQL/Supabase. Local file storage: filesystem. Cloud object storage: Supabase Storage. Authentication baseline: bcrypt + JWT.

## System Architecture
```text
Users
  |
  v
React Web Application
  |
  v
FastAPI REST API
  |-------------|
  v             v
Database      Object Storage
  |
  v
Logging / Monitoring
```

Advanced cloud form:
```text
Users -> CDN -> Frontend Hosting -> API Gateway -> API/Functions
                                             |-> Managed DB
                                             |-> Object Storage
                                             |-> Monitoring/Logging
```

## Database Design
Tables: USERS, COURSES, ASSIGNMENTS, SUBMISSIONS.

Primary keys uniquely identify rows. Foreign keys maintain relationships. Indexes are placed on email, role, course ownership, assignment deadlines and student/assignment submission lookups. File bytes are not normally stored in the database because object storage is designed for large binary objects and can scale separately.

## Cloud Storage Design
Example path:
```text
assignments/
  assignment_001/
    student_001/
      submission.pdf
```

The implementation uses generated IDs in the storage path to reduce collisions. Production systems should keep buckets private and issue short-lived signed URLs for authorized downloads.

## Authentication and Authorization
Authentication answers “Who are you?” Authorization answers “What are you allowed to do?” A student cannot use teacher-only endpoints, grade a submission or download another student's private file. A teacher can only review submissions belonging to assignments they created.

## Assignment Management
Teachers provide title, description, course, deadline, maximum marks, allowed types and maximum file size. Input validation is performed using Pydantic and server-side authorization checks.

## Submission Workflow
```text
Select assignment
 -> choose file
 -> validate extension and size
 -> upload to storage
 -> save metadata
 -> show status
```

The server generates the submission timestamp so browser clock manipulation cannot determine whether a submission is late.

## Deadline Management
The server compares the submission timestamp with the assignment deadline. If late submissions are enabled, the status becomes `LATE`; otherwise the request is rejected. Timezone-aware timestamps should be used consistently in production.

## Feedback and Grading
Teachers can enter marks and feedback. Marks cannot exceed maximum marks. Students can read but cannot modify teacher feedback or marks.

## API Design
Authentication: `/api/register`, `/api/login`, `/api/logout`. Assignment operations use `/api/assignments`. Submission operations use `/api/assignments/{id}/submit`, `/api/submissions/me`, `/api/assignments/{id}/submissions`, `/api/submissions/{id}` and `/api/submissions/{id}/download`. Grading uses `/api/submissions/{id}/grade`.

## Security
Controls include password hashing, JWT expiration, RBAC, ownership checks, private file access, file-type and size validation, CORS, environment variables and server-side timestamps. Production hardening should add HTTPS, signed URLs, rate limiting, malware scanning, audit logs, centralized secret management and backup policies.

## Scalability
At 10 students, one API process and SQLite can demonstrate the workflow. At 1,000 students, managed PostgreSQL, object storage and multiple API instances become useful. At 100,000 students, direct-to-object-storage uploads, CDN delivery, queues, background workers, autoscaling and database optimization reduce pressure on the API.

For a deadline spike, the API should not stream every large file through application memory. A production design can issue a signed upload URL so the browser uploads directly to object storage. Metadata can then be written to the database and heavy post-processing can run asynchronously.

## Failure Handling
- Upload failure: do not create a successful submission record; retry safely.
- Database outage: return a temporary error and avoid claiming submission success.
- Storage outage: keep metadata unchanged and report failure; retry where safe.
- Token expiry: require re-authentication.
- Duplicate request: use idempotency keys or a unique submission/version identifier.
- Network interruption: client can retry using the same idempotency key.
- Backend failure: use stateless instances behind a load balancer.

## Testing
Test registration, authentication, authorization, assignment CRUD, file validation, deadlines, resubmission, privacy, grading, download, failure paths and logout. The project includes a small automated health/login test suite and is structured for expansion into full API integration tests.

## Deployment
Local development uses SQLite and filesystem storage. Cloud deployment replaces these with PostgreSQL and object storage and uses environment variables for credentials. Frontend and backend can be deployed independently.

## Results
A successful demonstration shows teacher-created coursework, authenticated student access, file upload, metadata persistence, private retrieval, grading and feedback.

## Advantages
Centralized records, remote access, scalable file storage, clear roles, automated deadline status and centralized feedback.

## Limitations
The student MVP intentionally keeps some production controls as extension points: managed identity, signed direct uploads, malware scanning, advanced audit logs and high-scale queue processing.

## Future Scope
Add admin/invitation workflows, course enrollment, notifications, plagiarism detection, malware scanning, audit trails, direct-to-storage uploads, queue workers, CI/CD and Infrastructure as Code.

## Conclusion
The project demonstrates cloud-oriented application design rather than only a file-upload form. It separates compute, database metadata and object storage, applies authorization to data operations and provides a migration path from a local learning environment to managed cloud infrastructure.
