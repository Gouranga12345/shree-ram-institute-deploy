# Shree Ram Institute of Computer Science

A Python Flask website for Shree Ram Institute of Computer Science, Singla, Balasore. It includes institute information, courses, founder's message, alumni showcase and a 2027 admission application form.

## Technology

- Python + Flask
- HTML, CSS and JavaScript
- Flask-SQLAlchemy / SQLAlchemy
- Local development: MySQL
- Production: Neon PostgreSQL
- Deployment: GitHub + Vercel

## 1. Requirements

Install Python 3.10 or newer, MySQL Server / MySQL Workbench, and Git.

## 2. Create the local MySQL database

Open MySQL Workbench and run:

```sql
CREATE DATABASE shree_ram_institute
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Keep the database name exactly as shown.

## 3. Set up the project locally

Open a terminal in this project folder.

Windows PowerShell:

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and edit `DATABASE_URL` with your MySQL username and password:

```text
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@127.0.0.1:3306/shree_ram_institute
SECRET_KEY=use-a-long-random-secret
```

Do not put quotation marks around the values. If your MySQL password contains characters such as `@`, `#`, `/` or `:`, URL-encode those characters.

## 4. Run the website

```powershell
python -c "from main import app, db; app.app_context().push(); db.create_all(); print('Database ready')"
python main.py
```

Open http://127.0.0.1:5000

Submit a test admission form, then check the `admissions` table in MySQL Workbench.

## 5. Push the project to GitHub

Create a new empty GitHub repository. Then run:

```powershell
git init
git add .
git commit -m "Initial Shree Ram Institute website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Never commit `.env`. It is excluded by `.gitignore`.

## 6. Create the Neon production database

1. Create a project in Neon.
2. Open the Neon dashboard and copy its PostgreSQL connection string.
3. Use the pooled connection string if Neon provides one.
4. In Vercel, open your project Settings → Environment Variables.
5. Add `DATABASE_URL` with the Neon connection string.
6. Add `SECRET_KEY` with a long random value.
7. Redeploy after adding environment variables.

The app accepts Neon strings beginning with `postgresql://` or `postgres://` and configures the psycopg driver.

## 7. Deploy to Vercel

1. Sign in to Vercel.
2. Choose Add New → Project.
3. Import your GitHub repository.
4. Keep the project root as the repository root.
5. Add `DATABASE_URL` and `SECRET_KEY` under Environment Variables.
6. Deploy.

Vercel will use `api/index.py` and `vercel.json` to route requests to Flask.

## Important: initialise the Neon tables

The local MySQL database and Neon PostgreSQL database are separate databases. Creating tables locally does not create them in Neon.

For the first production setup, run this once from your computer with the Neon URL temporarily set as `DATABASE_URL`:

```powershell
$env:DATABASE_URL="YOUR_NEON_POSTGRES_CONNECTION_STRING"
python -c "from main import app, db; app.app_context().push(); db.create_all(); print('Neon tables created')"
```

Then restore your local `.env` value. Do not commit the Neon connection string or share it publicly.

## 8. Customise before public launch

- Replace the sample alumni names, roles and images with real alumni details only after obtaining their permission.
- Add the institute's approved logo, founder's real name/photo/message, phone number, email and exact address.
- Confirm course names, duration, fees, certificates, affiliation and recognition before advertising them. MCA guidance in this starter is explicitly not represented as an MCA degree.
- Add an admin login and protected application dashboard before allowing staff to view student applications. This starter saves applications but does not expose a public application-list page.
- Add a privacy notice and explain how applicant data will be used and retained.

## Routes

- `/` — public institute website
- `/apply` — admission form submission (POST)
- `/health` — database health check

## Troubleshooting

- MySQL connection error: check that MySQL Server is running, the database exists and the credentials are correct.
- `ModuleNotFoundError`: activate `.venv` and run `pip install -r requirements.txt`.
- Neon connection error: check the full connection string, password, SSL settings and Vercel environment variables.
- Vercel deployment error: inspect the deployment build/runtime logs and confirm `api/index.py`, `main.py`, `templates/` and `static/` are committed.
