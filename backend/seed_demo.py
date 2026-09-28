from app.core.db import Base,engine,SessionLocal
from app.models import User,Course,Assignment
from app.services.auth import hash_password
from datetime import datetime,timedelta,timezone
Base.metadata.create_all(bind=engine)
db=SessionLocal()
try:
 t=db.query(User).filter_by(email='teacher@demo.local').first() or User(name='Demo Teacher',email='teacher@demo.local',role='teacher',password_hash=hash_password('Teacher@123'))
 db.add(t); db.commit(); db.refresh(t)
 s=db.query(User).filter_by(email='student@demo.local').first() or User(name='Demo Student',email='student@demo.local',role='student',password_hash=hash_password('Student@123'))
 db.add(s); db.commit()
 c=db.query(Course).filter_by(course_name='Cloud Computing',teacher_id=t.user_id).first() or Course(course_name='Cloud Computing',teacher_id=t.user_id)
 db.add(c); db.commit(); db.refresh(c)
 if not db.query(Assignment).filter_by(title='Cloud Architecture Report',course_id=c.course_id).first():
  db.add(Assignment(course_id=c.course_id,title='Cloud Architecture Report',description='Prepare a short report explaining object storage, managed databases and scalability.',deadline=datetime.now(timezone.utc)+timedelta(days=7),max_marks=100,created_by=t.user_id,allowed_file_types='pdf,docx',max_file_size_mb=10));db.commit()
 print('Demo teacher: teacher@demo.local / Teacher@123')
 print('Demo student: student@demo.local / Student@123')
 print(f'Demo course id: {c.course_id}')
finally: db.close()
