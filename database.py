from sqlalchemy import create_engine, text
import os

db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(
  db_connection_string, 
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  })


def load_jobs_from_db():
  # CREATE "LIST" OF all rows of database table with id
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    column_names = result.keys()
      
    result_dicts = []
      
    for row in result.all():
      result_dicts.append(dict(zip(column_names, row)))
    return (result_dicts)

def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(
      text("SELECT * FROM jobs WHERE id = :val"),
      {"val": id}
    )
    rows = result.mappings().all()
    if len(rows) == 0:
      return None
    else:
      return dict(rows[0])


def add_application_to_db(job_id, data):
  with engine.connect() as conn:
    query = text("INSERT INTO careers.applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)")

    conn.execute(query, {
                 'job_id':job_id, 
                 'full_name': data['full_name'],
                 'email': data['email'],
                 'linkedin_url': data['linkedin_url'],
                 'education': data['education'],
                 'work_experience': data['work_experience'],
                 'resume_url': data['resume_url']
                }
    )