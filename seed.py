from models import (User, Pet, VetStation, Employee, AdoptionCenter, AdoptionPet,
                    Appointment, EmergencyRequest, Medication, Vaccination,
                    CommunityPost, CommunityComment, TimelineEvent)
from datetime import datetime, timedelta

def seed_data(db):
    if User.query.first():
        return  # already seeded

    # ── Pet Owner ──────────────────────────────────────────────
    owner = User(
        full_name='Amina Wanjiku',
        phone='+254 712 345 678',
        email='amina@demo.com',
        role='owner',
        address='Kilimani, Nairobi',
        gps_lat=-1.2921,
        gps_lng=36.7874,
        secondary_contact_name='David Kamau',
        secondary_contact_phone='+254 700 111 222',
        secondary_contact_relation='Spouse',
        payment_method_added=True,
        card_last4='4242',
        terms_accepted=True,
        avatar='🐾'
    )
    owner.set_password('demo123')
    db.session.add(owner)

    # ── Vet Station User ───────────────────────────────────────
    vet_user = User(
        full_name='Nairobi Paws Clinic',
        phone='+254 722 999 001',
        email='vet@demo.com',
        role='vet_station',
        address='Westlands, Nairobi',
        terms_accepted=True,
        avatar='🩺'
    )
    vet_user.set_password('demo123')
    db.session.add(vet_user)

    # ── Adoption Center User ───────────────────────────────────
    adopt_user = User(
        full_name='Happy Tails Center',
        phone='+254 733 456 789',
        email='adopt@demo.com',
        role='adoption_center',
        address='Karen, Nairobi',
        terms_accepted=True,
        avatar='🏠'
    )
    adopt_user.set_password('demo123')
    db.session.add(adopt_user)

    db.session.flush()

    # ── Pets for Amina ─────────────────────────────────────────
    cat1 = Pet(
        owner_id=owner.id,
        name='Whiskers',
        species='Cat',
        breed='Maine Coon',
        age='3 years',
        gender='Male',
        weight='5.2 kg',
        known_conditions='Mild asthma',
        allergies='Dust, certain fish proteins',
        photo='🐱',
        pet_pk=f'PET-{owner.id}-001'
    )
    cat2 = Pet(
        owner_id=owner.id,
        name='Luna',
        species='Cat',
        breed='Siamese',
        age='1.5 years',
        gender='Female',
        weight='3.8 kg',
        known_conditions='None',
        allergies='None',
        photo='🐈',
        pet_pk=f'PET-{owner.id}-002'
    )
    db.session.add_all([cat1, cat2])
    db.session.flush()

    # ── Vet Station ────────────────────────────────────────────
    station = VetStation(
        user_id=vet_user.id,
        name='Nairobi Paws Clinic',
        address='Westlands, Nairobi',
        gps_lat=-1.2673,
        gps_lng=36.8112,
        phone='+254 722 999 001',
        opening_hours='08:00',
        closing_hours='20:00',
        services='General Checkup, Dental, Surgery, Vaccinations, Emergency',
        emergency_available=True,
        rating=4.8,
        station_pk='VS-001'
    )
    station2 = VetStation(
        user_id=None,
        name='Karen Veterinary Hospital',
        address='Karen, Nairobi',
        gps_lat=-1.3231,
        gps_lng=36.7117,
        phone='+254 700 234 567',
        opening_hours='07:00',
        closing_hours='22:00',
        services='General Checkup, Neurology, Radiology, Emergency',
        emergency_available=True,
        rating=4.6,
        station_pk='VS-002'
    )
    station3 = VetStation(
        user_id=None,
        name='Lavington Pet Care',
        address='Lavington, Nairobi',
        gps_lat=-1.2887,
        gps_lng=36.7724,
        phone='+254 711 777 888',
        opening_hours='09:00',
        closing_hours='18:00',
        services='General Checkup, Vaccinations, Grooming',
        emergency_available=False,
        rating=4.3,
        station_pk='VS-003'
    )
    db.session.add_all([station, station2, station3])
    db.session.flush()

    # ── Employees ──────────────────────────────────────────────
    dr_emily = Employee(
        station_id=station.id,
        full_name='Dr. Emily Muthoni',
        phone='+254 701 111 222',
        email='emily@pawsclinic.com',
        gender='Female',
        years_experience=8,
        specialty='Feline Medicine',
        photo='👩‍⚕️',
        available_today=True,
        on_duty=True,
        employee_pk='EMP-001'
    )
    dr_james = Employee(
        station_id=station.id,
        full_name='Dr. James Otieno',
        phone='+254 702 333 444',
        email='james@pawsclinic.com',
        gender='Male',
        years_experience=12,
        specialty='Surgery & Emergency',
        photo='👨‍⚕️',
        available_today=True,
        on_duty=True,
        employee_pk='EMP-002'
    )
    dr_aisha = Employee(
        station_id=station2.id,
        full_name='Dr. Aisha Omondi',
        phone='+254 703 555 666',
        email='aisha@karen.vet',
        gender='Female',
        years_experience=6,
        specialty='General Practice',
        photo='👩‍⚕️',
        available_today=True,
        on_duty=False,
        employee_pk='EMP-003'
    )
    db.session.add_all([dr_emily, dr_james, dr_aisha])
    db.session.flush()

    # ── Appointments ───────────────────────────────────────────
    apt1 = Appointment(
        owner_id=owner.id,
        pet_id=cat1.id,
        station_id=station.id,
        employee_id=dr_emily.id,
        date='2025-07-05',
        time='10:00',
        reason='Annual checkup and asthma review',
        status='accepted'
    )
    apt2 = Appointment(
        owner_id=owner.id,
        pet_id=cat2.id,
        station_id=station.id,
        employee_id=dr_james.id,
        date='2025-07-10',
        time='14:30',
        reason='Vaccination booster',
        status='pending'
    )
    db.session.add_all([apt1, apt2])

    # ── Emergency Requests ─────────────────────────────────────
    emg = EmergencyRequest(
        owner_id=owner.id,
        pet_id=cat1.id,
        station_id=station.id,
        severity='urgent',
        symptoms_q1='No',
        symptoms_q2='Poisoning',
        symptoms_q3='Vomiting',
        case_type='case2',
        status='resolved',
        vet_eta='15 mins',
        assigned_vet_id=dr_emily.id
    )
    db.session.add(emg)

    # ── Medications ────────────────────────────────────────────
    med1 = Medication(
        pet_id=cat1.id,
        name='Salbutamol Inhaler',
        dosage='1 puff',
        method='Inhaled',
        duration='As needed',
        prescribed_by='Dr. Emily Muthoni',
        start_date='2025-01-15',
        active=True
    )
    med2 = Medication(
        pet_id=cat1.id,
        name='Antihistamine Tablets',
        dosage='5mg',
        method='Oral',
        duration='7 days',
        prescribed_by='Dr. Emily Muthoni',
        start_date='2025-06-20',
        active=False
    )
    db.session.add_all([med1, med2])

    # ── Vaccinations ───────────────────────────────────────────
    vax1 = Vaccination(
        pet_id=cat1.id,
        vaccine_name='FVRCP (3-in-1)',
        date_given='2025-01-10',
        next_due='2026-01-10',
        administered_by='Dr. Emily Muthoni'
    )
    vax2 = Vaccination(
        pet_id=cat1.id,
        vaccine_name='Rabies',
        date_given='2024-12-01',
        next_due='2025-12-01',
        administered_by='Dr. James Otieno'
    )
    vax3 = Vaccination(
        pet_id=cat2.id,
        vaccine_name='FVRCP (3-in-1)',
        date_given='2025-03-15',
        next_due='2026-03-15',
        administered_by='Dr. Emily Muthoni'
    )
    db.session.add_all([vax1, vax2, vax3])

    # ── Timeline Events ────────────────────────────────────────
    tl_events = [
        TimelineEvent(pet_id=cat1.id, event_type='vaccination', title='FVRCP Vaccination',
                      description='Annual 3-in-1 vaccination administered', date=datetime(2025,1,10),
                      vet_name='Dr. Emily Muthoni'),
        TimelineEvent(pet_id=cat1.id, event_type='diagnosis', title='Asthma Diagnosis',
                      description='Mild feline asthma confirmed via X-ray. Inhaler prescribed.',
                      date=datetime(2025,1,15), vet_name='Dr. Emily Muthoni'),
        TimelineEvent(pet_id=cat1.id, event_type='emergency', title='Suspected Poisoning',
                      description='Remote consultation for vomiting episode. Induced vomiting, monitoring recommended.',
                      date=datetime(2025,5,22), vet_name='Dr. Emily Muthoni'),
        TimelineEvent(pet_id=cat1.id, event_type='checkup', title='6-month Checkup',
                      description='General health good. Weight stable at 5.2kg. Asthma under control.',
                      date=datetime(2025,6,10), vet_name='Dr. James Otieno'),
        TimelineEvent(pet_id=cat2.id, event_type='vaccination', title='FVRCP Vaccination',
                      description='First FVRCP vaccination. Next due in 12 months.',
                      date=datetime(2025,3,15), vet_name='Dr. Emily Muthoni'),
        TimelineEvent(pet_id=cat2.id, event_type='checkup', title='Initial Health Assessment',
                      description='Luna is in excellent health. Playful and responsive.',
                      date=datetime(2025,3,15), vet_name='Dr. Emily Muthoni'),
    ]
    db.session.add_all(tl_events)

    # ── Adoption Center ────────────────────────────────────────
    center = AdoptionCenter(
        user_id=adopt_user.id,
        name='Happy Tails Adoption Center',
        address='Karen, Nairobi',
        gps_lat=-1.3312,
        gps_lng=36.7090,
        phone='+254 733 456 789',
        opening_hours='09:00',
        closing_hours='17:00',
        center_pk='AC-001'
    )
    center2 = AdoptionCenter(
        user_id=None,
        name='Paws & Claws Rescue',
        address='Ngong Road, Nairobi',
        gps_lat=-1.3044,
        gps_lng=36.7617,
        phone='+254 711 987 654',
        opening_hours='10:00',
        closing_hours='16:00',
        center_pk='AC-002'
    )
    db.session.add_all([center, center2])
    db.session.flush()

    # ── Adoption Pets ──────────────────────────────────────────
    adopt_pets = [
        AdoptionPet(center_id=center.id, name='Mochi', species='Cat', breed='Scottish Fold',
                    estimated_age='1 year', gender='Female', health_status='Healthy',
                    status='available', photo='😺', description='Mochi is a playful and affectionate Scottish Fold who loves cuddles and toy mice.', pet_pk='AP-001'),
        AdoptionPet(center_id=center.id, name='Shadow', species='Cat', breed='Bombay',
                    estimated_age='3 years', gender='Male', health_status='Requires Medication',
                    status='available', photo='🐈‍⬛', description='Shadow is a calm and mysterious Bombay cat. Requires daily heart medication but is otherwise healthy.', pet_pk='AP-002'),
        AdoptionPet(center_id=center.id, name='Cleo', species='Cat', breed='Abyssinian',
                    estimated_age='2 years', gender='Female', health_status='Healthy',
                    status='reserved', photo='🐱', description='Cleo is an energetic Abyssinian who loves to explore and climb. Reserved — visit pending.', pet_pk='AP-003'),
        AdoptionPet(center_id=center2.id, name='Simba', species='Cat', breed='Savannah',
                    estimated_age='6 months', gender='Male', health_status='Recovering',
                    status='available', photo='🦁', description='Simba was found injured on the streets. He is recovering well and will be ready for a forever home soon.', pet_pk='AP-004'),
        AdoptionPet(center_id=center2.id, name='Nala', species='Cat', breed='Ragdoll',
                    estimated_age='4 years', gender='Female', health_status='Special Needs',
                    status='available', photo='😻', description='Nala is a gentle Ragdoll with three legs. She is fully mobile, loving, and simply needs a patient family.', pet_pk='AP-005'),
        AdoptionPet(center_id=center2.id, name='Jasper', species='Cat', breed='British Shorthair',
                    estimated_age='2 years', gender='Male', health_status='Healthy',
                    status='adopted', photo='🐾', description='Jasper found his forever home! Adopted by the Njoroge family.', pet_pk='AP-006'),
    ]
    db.session.add_all(adopt_pets)

    # ── Community Posts ────────────────────────────────────────
    posts = [
        CommunityPost(author_id=owner.id, display_name='Amina W.',
                      title='My cat loves watermelon — is this safe? 🍉',
                      content='I caught Whiskers licking watermelon slices and he seems to love it! Is it safe for cats to eat watermelon?',
                      post_type='question', likes=12),
        CommunityPost(author_id=owner.id, display_name='Amina W.',
                      title='MYTH: Cats always land on their feet',
                      content='This is only partially true! Cats have a righting reflex but this doesn\'t mean they\'re injury-proof from falls. Always keep windows screened.',
                      post_type='myth', likes=34),
        CommunityPost(author_id=owner.id, display_name='Cat Lover 🐾',
                      title='Tips for keeping indoor cats entertained',
                      content='My two indoor cats were getting restless. Here\'s what worked: puzzle feeders, window bird feeders, rotating toys, and cardboard boxes. The boxes were a HIT!',
                      post_type='general', likes=27),
    ]
    db.session.add_all(posts)
    db.session.flush()

    comments = [
        CommunityComment(post_id=posts[0].id, author_id=owner.id, display_name='Vet Emily',
                         content='Yes, small amounts of seedless watermelon are safe for cats. Remove the rind and seeds though!'),
        CommunityComment(post_id=posts[0].id, author_id=owner.id, display_name='TabbyMom_KE',
                         content='My cat does the same thing 😂 Glad to know it\'s safe!'),
    ]
    db.session.add_all(comments)

    db.session.commit()
    print("✅ PawsCare demo data seeded successfully.")
