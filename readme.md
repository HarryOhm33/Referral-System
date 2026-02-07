# Django Referral & Reward API 🎁

This project is a backend system built using **Django**, **MongoEngine**, and JWT authentication.  
It provides a complete infrastructure for:

- User authentication with OTP verification
- Referral code generation & application
- Fraud-safe referral tracking
- Reward configuration
- Reward ledger management
- User & admin analytics

---

## 🚀 Features

### Authentication

- Signup with OTP email verification
- Secure password hashing
- JWT token authentication
- Session tracking
- Logout & invalidation

### Referral System

- Unique referral code per user
- Idempotent generation
- Self-referral prevention
- One-time usage enforcement

### Reward System

- Config-driven reward values
- Automatic reward creation
- Admin credit system
- Full history tracking

### Analytics

- Referral summary
- Referral usage list
- Daily timeline
- Admin leaderboard

---

## 🛠️ Tech Stack

- Python & Django
- MongoDB (MongoEngine)
- JWT (PyJWT)
- Django REST Framework
- `python-decouple` for `.env`

---

## 🗂️ Project Structure

```
project-root/
├── core/
│   ├── main_project/
│   ├── user_auth/
│   ├── referrals/        # referral & reward system
│   └── env/              # environment variables
│
├── venv/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔐 Environment Variables

Create `.env` inside:

```
core/env/
```

### Example

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_password

MONGO_URI=your_mongo_uri

JWT_SECRET=supersecretkey
```

⚠️ Do NOT commit this file.

---

# 🧪 API Endpoints

---

## 🔑 Authentication

- `POST /signup`
- `POST /verify-otp`
- `POST /login`
- `POST /verify-session`
- `POST /logout`

---

## 🎁 Referral APIs (User)

### Generate code

```
POST /api/referral/generate
```

### Apply code

```
POST /api/referral/apply
```

### Referral Summary

```
GET /api/referral/analytics/summary
```

### Referral List

```
GET /api/referral/analytics/list
```

### Referral Timeline

```
GET /api/referral/analytics/timeline
```

---

## 💰 Rewards (User)

### Reward History

```
GET /api/rewards/history
```

---

## 👑 Admin APIs

### Create reward config

```
POST /api/admin/reward-config
```

### Credit reward

```
POST /api/admin/rewards/{reward_id}/credit
```

### Top referrers

```
GET /api/admin/referral/top
```

---

# 🧾 Setup Instructions

---

## 1️⃣ Clone repository

```bash
git clone https://github.com/HarryOhm33/Djano-JWT.git
cd Djano-JWT
```

---

## 2️⃣ Create virtual environment

```bash
python -m venv venv
```

### Activate

Windows

```bash
venv\Scripts\activate
```

Mac / Linux

```bash
source venv/bin/activate
```

---

## 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Add `.env`

As described above.

---

## 5️⃣ Make sure MongoDB is running

Local:

```bash
mongod
```

Or Atlas URI.

---

## 6️⃣ Run server

```bash
python manage.py runserver
```

---

## 🌐 Server URL

```
http://127.0.0.1:8000/
```

---

# 🔑 Authentication Requirement

Most APIs require JWT.

Use header:

```
Authorization: Bearer <token>
```

---

# 🧱 First-Time Setup Requirement (IMPORTANT)

Create at least **one active reward config** before applying referrals.

```
POST /api/admin/reward-config
```

Otherwise apply will fail.

---

# ⚠️ Notes

- Mongo handles TTL for sessions & OTPs
- Reward values are stored in ledger for historical accuracy
- Admin APIs are role protected
- All analytics are aggregation-friendly

---

# 👨‍💻 Author

Hari Om 🚀  
Full Stack Developer
