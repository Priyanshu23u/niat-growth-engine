"""
NIAT vs Traditional Tier-3 College — 8-Semester Curriculum Comparison
Used by tool_compare_curriculum in AI Agent reasoning pipeline.
"""

from typing import List, Dict, Any


CURRICULUM_COMPARISON: List[Dict[str, Any]] = [
    {
        "semester": 1,
        "year": 1,
        "traditional_tier3": {
            "focus": "Rote Basic Science & Chemistry Labs",
            "subjects": ["Engineering Chemistry", "Basic Electrical", "Engineering Drawing (Paper/Drafting)", "Physics Theory"],
            "coding_hours_per_week": 2,
            "industry_relevance": "Obsolete",
            "limitations": "Zero software building; students write theoretical programs on paper with blue ink pens.",
        },
        "niat_program": {
            "focus": "Day 1 Coding Foundations & Full-Stack Web",
            "subjects": ["Modern Python & JavaScript (ES6+)", "Git/GitHub Workflows & Clean Code", "Responsive UI/UX Engineering", "Foundations of AI Problem Solving"],
            "coding_hours_per_week": 18,
            "industry_relevance": "Cutting-Edge",
            "real_world_outcome": "Deploy 4 responsive web apps and 1 collaborative open-source tool to live public URLs.",
        },
    },
    {
        "semester": 2,
        "year": 1,
        "traditional_tier3": {
            "focus": "Legacy C Programming & Theory",
            "subjects": ["C Programming Syntax", "Workshop Practice (Carpentry/Welding)", "Mathematics II", "Environmental Studies"],
            "coding_hours_per_week": 3,
            "industry_relevance": "Obsolete",
            "limitations": "Outdated Turbo C++ compiler; no version control, no APIs, no team engineering practices.",
        },
        "niat_program": {
            "focus": "Data Structures, Algorithms & Backend Systems",
            "subjects": ["Modern DSA in Python & C++", "Relational & NoSQL Databases (Postgres, Redis)", "REST & GraphQL API Architecture", "Algorithmic Complexity & Optimization"],
            "coding_hours_per_week": 22,
            "industry_relevance": "Cutting-Edge",
            "real_world_outcome": "Solve 200+ industry-standard algorithmic challenges; build and document production-grade REST APIs.",
        },
    },
    {
        "semester": 3,
        "year": 2,
        "traditional_tier3": {
            "focus": "Abstract Computer Architecture Theory",
            "subjects": ["Digital Logic Design", "Discrete Mathematics", "Data Structures on Paper", "Object-Oriented Programming using C++ 98"],
            "coding_hours_per_week": 4,
            "industry_relevance": "Low",
            "limitations": "Memorizing textbook definitions of stacks and queues without building real distributed services.",
        },
        "niat_program": {
            "focus": "Full-Stack System Architecture & Cloud DevOps",
            "subjects": ["Microservices Architecture", "Docker, Kubernetes & Containerization", "Next.js / Node.js High-Concurrency Backends", "CI/CD Pipelines & Cloud Deployments (AWS/GCP)"],
            "coding_hours_per_week": 25,
            "industry_relevance": "Cutting-Edge",
            "real_world_outcome": "Architect, dockerize, and deploy a multi-tenant SaaS application handling 1,000+ concurrent requests.",
        },
    },
    {
        "semester": 4,
        "year": 2,
        "traditional_tier3": {
            "focus": "Rote Database & OS Concepts",
            "subjects": ["Database Management Systems (Theoretical SQL)", "Operating Systems Theory", "Formal Languages & Automata Theory"],
            "coding_hours_per_week": 4,
            "industry_relevance": "Low",
            "limitations": "Running 1990s Oracle commands without index tuning, scaling considerations, or query caching.",
        },
        "niat_program": {
            "focus": "Applied AI, LLMs & Autonomous Agents",
            "subjects": ["Machine Learning Mathematics & PyTorch", "Large Language Model Fine-Tuning & Prompt Architecture", "Vector Databases (Pinecone, pgvector) & RAG Systems", "Multi-Agent Orchestration (LangChain, LangGraph)"],
            "coding_hours_per_week": 28,
            "industry_relevance": "Cutting-Edge",
            "real_world_outcome": "Build an autonomous AI agent capable of multi-step web research and structured API automation.",
        },
    },
    {
        "semester": 5,
        "year": 3,
        "traditional_tier3": {
            "focus": "Dry Compiler Design & Computer Networks",
            "subjects": ["Compiler Design", "Computer Networks (Cisco Packet Tracer simulation)", "Web Technology (basic HTML4)"],
            "coding_hours_per_week": 4,
            "industry_relevance": "Low",
            "limitations": "No real cloud infrastructure exposure; completely unaware of how modern AI applications are deployed.",
        },
        "niat_program": {
            "focus": "Enterprise Industry Apprenticeship & Hackathons",
            "subjects": ["Production AI Systems & MLOps", "High-Volume System Design (Distributed Caching, Kafka)", "Security, Compliance & GDPR in AI", "Corporate Sponsored Capstone Projects"],
            "coding_hours_per_week": 30,
            "industry_relevance": "Cutting-Edge",
            "real_world_outcome": "Complete an industry-sponsored enterprise capstone project evaluated by practicing tech leads.",
        },
    },
    {
        "semester": 6,
        "year": 3,
        "traditional_tier3": {
            "focus": "Generic Mini-Project (often bought readymade)",
            "subjects": ["Software Engineering Waterfall Theory", "Generic Mini-Project", "Elective 1"],
            "coding_hours_per_week": 2,
            "industry_relevance": "Obsolete",
            "limitations": "Students frequently download pre-made Java/PHP projects from CD shops; zero genuine GitHub activity.",
        },
        "niat_program": {
            "focus": "Paid Industry Internships & Product Building",
            "subjects": ["6-Month Corporate Internship Track", "Advanced Low-Level & High-Level System Design (LLD/HLD)", "Tech Leadership & Behavioral Mock Interviews"],
            "coding_hours_per_week": 35,
            "industry_relevance": "Cutting-Edge",
            "real_world_outcome": "Securing ₹25,000 to ₹60,000/month paid corporate internships; verified GitHub contribution graph.",
        },
    },
    {
        "semester": 7,
        "year": 4,
        "traditional_tier3": {
            "focus": "Mass Recruiter Aptitude Training (TCS/Wipro/Infosys)",
            "subjects": ["Basic Verbal & Quantitative Aptitude for Mass IT", "Elective 2 & 3", "Final Major Project"],
            "coding_hours_per_week": 2,
            "industry_relevance": "Obsolete",
            "limitations": "Geared for ₹3.3 LPA to ₹4.0 LPA legacy IT service company mass hiring test patterns.",
        },
        "niat_program": {
            "focus": "High-Tier Product & AI Company Placement Drives",
            "subjects": ["Exclusive Placement Drives with 1,500+ Tech Hiring Partners", "FAANG / High-Growth Startup Interview Preparation", "Production LLM Architecture Reviews"],
            "coding_hours_per_week": 30,
            "industry_relevance": "Cutting-Edge",
            "real_world_outcome": "Targeting ₹8.0 LPA to ₹25.0 LPA product development, AI engineering, and full-stack software engineer roles.",
        },
    },
    {
        "semester": 8,
        "year": 4,
        "traditional_tier3": {
            "focus": "Graduation Waiting Period & Unplaced Anxiety",
            "subjects": ["Project Viva", "Comprehensive Viva Voce"],
            "coding_hours_per_week": 0,
            "industry_relevance": "Obsolete",
            "limitations": "Less than 28% of tier-3 CS students get software engineering offers; majority face delayed onboarding.",
        },
        "niat_program": {
            "focus": "Career Launch, Continuous Mentorship & Alumni Network",
            "subjects": ["Full-Time Corporate Onboarding Support", "NxtWave Fellowship Transition", "Senior Engineer Mentorship Group"],
            "coding_hours_per_week": 20,
            "industry_relevance": "Cutting-Edge",
            "real_world_outcome": "Graduating with dual credentials (UGC B.Tech Degree + NSDC Industry Ready Certificate) and 2+ years of real build history.",
        },
    },
]
