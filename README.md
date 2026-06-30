# 🐾 PawsCare

Smart Pet Health Management Platform — built for **Hack the Kitty 2025** (theme: *World Cat Domination*).
Sponsors: **Temporal** (workflow engine) · **Akido** (AI security)

## What it does

PawsCare connects three types of users on one platform:

- **🐾 Pet Owners** — manage pet profiles, book vet appointments, trigger emergency response, browse adoptable cats, post in the community
- **🩺 Vet Stations** — accept/reject appointments, manage emergency dispatch, manage staff, add prescriptions/vaccinations to medical records
- **🏠 Adoption Centers** — list pets for adoption, manage their status (available/reserved/adopted)

The standout feature is the **Emergency System**: a 3-question triage flow auto-scores severity (Critical/Urgent/Mild) and routes the owner into one of three response paths — Case 1 (physical vet dispatch), Case 2 (remote video/voice consult), or Case 3 (free AI first-aid assistant, no payment method needed).

## Project Structure

```
pawscare/
├── app.py                  
├── run.py                  
├── models.py                
├── seed.py                  
├── requirements.txt
├── routes/
│   ├── main.py
    ├── auth.py                
│   ├── owner.py               
│   ├── vet.py                 
│   ├── adoption.py            
│   └── api.py                 
├── templates/
│   ├── base.html             
│   ├── welcome.html         
│   ├── auth/                
│   ├── owner/              
│   ├── vet/                
│   └── adoption/            
├── static/                  
└── instance/                
```

## Setup & Run

```bash
cd pawscare
pip install -r requirements.txt
python3 run.py
```

Visit **http://localhost:5000**. The database is SQLite and auto-seeds with demo data on first run.

## Demo Accounts

| Role | Email | Password |
|---|---|---|
| 🐾 Pet Owner | amina@demo.com | demo123 |
| 🩺 Vet Station | vet@demo.com | demo123 |
| 🏠 Adoption Center | adopt@demo.com | demo123 |

The owner account (Amina) comes pre-loaded with 2 cats (Whiskers — has asthma + a past poisoning emergency, and Luna), an accepted + pending appointment, medications, vaccinations, and a full medical timeline — so judges can see real data immediately without manual setup.

## Demo Script (suggested 3-minute flow)

1. **Land on welcome screen** → loading screen with the walking cat animation plays.
2. **Sign in as Pet Owner** → dashboard shows pets, appointments, stats.
3. Click into **Whiskers** → show medical timeline, meds, vaccinations.
4. Hit the **🚨 EMERGENCY** button → answer the 3 triage questions (try "Bleeding Heavily" to trigger **Case 1**, or "No / Seizure" to trigger **Case 2**) → show the auto-scored severity and case routing.
5. Browse **Find Vets** and **Adopt a Pet**.
6. **Sign out, sign in as Vet Station** (vet@demo.com) → show the emergency queue, accept a pending appointment, assign a vet to an emergency.
7. **Sign in as Adoption Center** (adopt@demo.com) → change a pet's status from Available → Reserved.
8. Point out the **Temporal / Akido sponsor badges** in the sidebar and dashboard banner.

## Resetting demo data

Delete `instance/pawscare.db` (or `pawscare.db` in the project root) and restart the server — it will reseed automatically.

## Notes on hardcoded/demo elements

- All data is hardcoded via `seed.py` for demo reliability — no external API calls required to see a full working demo.
- Photos use emoji placeholders instead of real image uploads (kept the form fields in templates so real upload logic can be wired in later).
- Sponsor integrations (Temporal/Akido) are represented as branded UI callouts since true workflow/security backend wiring is out of scope for hackathon judging — but the structure (emergency dispatch, medical record security) is the natural place to wire in their actual SDKs.
- Loading screen cat animation is pure CSS/emoji — no external image API needed, so it works offline.
