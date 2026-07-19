import os
import django
import datetime

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_system.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from events.models import Event, Registration

def seed():
    print("Seeding database...")
    
    # Configure the default Django Site (required by django-allauth)
    site = Site.objects.get_current()
    site.domain = '127.0.0.1:8000'
    site.name = 'BookMyAishow'
    site.save()
    print(f"Updated default Site domain to {site.domain}")

    # 1. Create Superuser (Organizer)
    admin_user, created = User.objects.get_or_create(username='admin')
    if created:
        admin_user.set_password('password123')
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.email = 'admin@example.com'
        admin_user.save()
        print("Created superuser: admin / password123")
    else:
        print("Superuser 'admin' already exists.")

    # 2. Create some attendee users for testing
    user_alice, _ = User.objects.get_or_create(username='alice')
    user_alice.set_password('password123')
    user_alice.save()

    user_bob, _ = User.objects.get_or_create(username='bob')
    user_bob.set_password('password123')
    user_bob.save()

    # 3. Create 11 Sample AI Events (all with at least 50 capacity)
    events_data = [
        {
            "title": "BookMyAishow Grand Opening: The AI Revolution",
            "description": "Welcome to the official launch event of BookMyAishow! Join us for live demonstrations of next-generation autonomous AI agents, multi-modal LLM integrations, and a fireside chat with industry leading researchers on the future of code generation.\n\nNetworking cocktail party to follow.",
            "date": datetime.date.today() + datetime.timedelta(days=5),
            "time": datetime.time(18, 0),
            "location": "Aether Grand Hall, San Francisco",
            "capacity": 300,
            "organizer": admin_user
        },
        {
            "title": "Generative Art & Neural Networks Showcase",
            "description": "An immersive exhibition presenting artwork, music, and interactive environments crafted entirely using diffusion models, GANs, and generative audio architectures.\n\nInteract directly with the creators and witness real-time model interpolation galleries.",
            "date": datetime.date.today() + datetime.timedelta(days=7),
            "time": datetime.time(19, 30),
            "location": "Metropolitan Digital Art Gallery, NY",
            "capacity": 150,
            "organizer": admin_user
        },
        {
            "title": "Google DeepMind Agentic Systems Masterclass",
            "description": "Step-by-step engineering masterclass covering state-of-the-art agentic workflows, memory retrieval systems, tool calling optimization, and self-reflection loops using Gemini models.\n\nPractical hands-on lab sessions included.",
            "date": datetime.date.today() + datetime.timedelta(days=12),
            "time": datetime.time(9, 0),
            "location": "Tech Hub Convention Center, Austin",
            "capacity": 200,
            "organizer": admin_user
        },
        {
            "title": "Large Language Model Hackathon & Code Showdown",
            "description": "A 36-hour code sprint where developers build production-ready autonomous coding agents, customer assistants, or workflow automation integrations.\n\n$10,000 in cloud credits and hardware prizes up for grabs.",
            "date": datetime.date.today() + datetime.timedelta(days=15),
            "time": datetime.time(9, 30),
            "location": "Developer Co-working Space, Seattle",
            "capacity": 80,
            "organizer": admin_user
        },
        {
            "title": "AI in Cinema: Generative Video Film Festival",
            "description": "Enjoy a screening of award-winning short films created by independent directors using AI video generators, neural voice synthesis, and dynamic background scoring.\n\nIncludes Q&A sessions on prompt-driven cinema pipelines.",
            "date": datetime.date.today() + datetime.timedelta(days=18),
            "time": datetime.time(20, 0),
            "location": "Starlight Theater, Los Angeles",
            "capacity": 250,
            "organizer": admin_user
        },
        {
            "title": "PostgreSQL & Django: Building Scalable Backend for AI Apps",
            "description": "Learn database optimization tricks essential for AI-driven backends. We cover storing embeddings in PostgreSQL (using pgvector), connection pooling, caching strategies, and robust transaction concurrency configurations in Django.",
            "date": datetime.date.today() + datetime.timedelta(days=22),
            "time": datetime.time(14, 0),
            "location": "Virtual Webinar / Zoom",
            "capacity": 500,
            "organizer": admin_user
        },
        {
            "title": "Prompt Engineering & Cognitive Architecture Meetup",
            "description": "A community meetup for AI engineers, prompt designers, and cognitive architects to share findings, tricks, and benchmarks on prompt-chaining frameworks like LangChain, LlamaIndex, and custom state machines.",
            "date": datetime.date.today() + datetime.timedelta(days=25),
            "time": datetime.time(16, 0),
            "location": "Innovate Labs, Boston",
            "capacity": 120,
            "organizer": admin_user
        },
        {
            "title": "The AI Ethics & Alignment Forum 2026",
            "description": "Engage with prominent philosophers, policy advocates, and tech leaders as they dissect bias evaluation in large models, safety guards, reinforcement learning from human feedback (RLHF), and global AI governance frameworks.",
            "date": datetime.date.today() + datetime.timedelta(days=30),
            "time": datetime.time(10, 0),
            "location": "National Academy of Sciences, DC",
            "capacity": 180,
            "organizer": admin_user
        },
        {
            "title": "Robotics & Embodied AI Live Demo & Mixer",
            "description": "Witness next-gen quadruped and humanoid robots navigating complex physical terrains using real-time vision-language-action (VLA) models.\n\nAn excellent opportunity to network with hardware engineers, software developers, and investors.",
            "date": datetime.date.today() + datetime.timedelta(days=35),
            "time": datetime.time(13, 0),
            "location": "Robotics Innovation Warehouse, Boston",
            "capacity": 75,
            "organizer": admin_user
        },
        {
            "title": "AI-Powered Game Dev & Procedural Worlds Workshop",
            "description": "Explore how developers are incorporating dynamic LLM-driven NPCs, real-time procedural asset generation, and adaptive AI difficulty adjustment into modern game engines like Unreal Engine and Unity.",
            "date": datetime.date.today() + datetime.timedelta(days=40),
            "time": datetime.time(11, 0),
            "location": "Game Hub Studio, Vancouver",
            "capacity": 90,
            "organizer": admin_user
        },
        {
            "title": "Next-Gen UI/UX for AI Assistants Design Sprint",
            "description": "Collaborate in teams to conceptualize and prototype next-generation chat interfaces, voice-driven canvases, and non-intrusive ambient assistants. Perfect for product designers and frontend developers.",
            "date": datetime.date.today() + datetime.timedelta(days=45),
            "time": datetime.time(10, 30),
            "location": "Design Lab Collective, Chicago",
            "capacity": 60,
            "organizer": admin_user
        }
    ]

    for data in events_data:
        event, created = Event.objects.get_or_create(
            title=data["title"],
            defaults=data
        )
        if created:
            print(f"Created event: {event.title} (Capacity: {event.capacity})")
        else:
            # Update capacity and date to match the new seeding requirement
            event.capacity = data["capacity"]
            event.description = data["description"]
            event.location = data["location"]
            event.date = data["date"]
            event.time = data["time"]
            event.save()
            print(f"Updated event details for: {event.title} (Capacity: {event.capacity})")

    # 4. Fill registration for the Design Sprint to demonstrate active registration dashboard flows
    design_sprint = Event.objects.get(title="Next-Gen UI/UX for AI Assistants Design Sprint")
    Registration.objects.get_or_create(user=user_alice, event=design_sprint, defaults={'status': 'REGISTERED'})
    Registration.objects.get_or_create(user=user_bob, event=design_sprint, defaults={'status': 'REGISTERED'})
    
    print("Seeding complete! Database has 11 events (each with 50+ seats availability) and is fully ready to use.")

if __name__ == "__main__":
    seed()
