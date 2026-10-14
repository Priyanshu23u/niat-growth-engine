"""
NIAT ParentTrust AI — In-Memory Database & Analytics Ledger
Thread-safe store for Leads, Seat Reservations, and Funnel Telemetry.
"""

import threading
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional


class InMemoryDatabase:
    def __init__(self):
        self._lock = threading.Lock()
        now = datetime.now(timezone.utc)
        self.leads: List[Dict[str, Any]] = [
            {
                "id": "lead-1001",
                "studentName": "Sai Teja Reddy",
                "parentName": "K. Venkatesh",
                "parentPhone": "+91 98480 23456",
                "language": "te",
                "boardPercentage": 88,
                "natScore": 82,
                "state": "Telangana",
                "budgetAnnual": 300000,
                "objectionsAsked": ["accreditation", "roi_financial"],
                "matchedCampusId": "campus-chaitanya-hyd",
                "matchedCampusName": "NIAT @ Chaitanya (Deemed to be University)",
                "dossierGenerated": True,
                "seatReserved": True,
                "tokenAmount": 10000,
                "status": "converted",
                "createdAt": (now - timedelta(hours=5)).isoformat(),
                "source": "NAT Test Completion",
            },
            {
                "id": "lead-1002",
                "studentName": "Ananya Sharma",
                "parentName": "Rajesh Sharma",
                "parentPhone": "+91 98110 54321",
                "language": "hi",
                "boardPercentage": 91,
                "natScore": 78,
                "state": "Uttar Pradesh",
                "budgetAnnual": 320000,
                "objectionsAsked": ["ai_threat", "accreditation"],
                "matchedCampusId": "campus-niu-delhi",
                "matchedCampusName": "NIAT @ Noida International University",
                "dossierGenerated": True,
                "seatReserved": True,
                "tokenAmount": 10000,
                "status": "converted",
                "createdAt": (now - timedelta(hours=8)).isoformat(),
                "source": "Instagram Lead Ad",
            },
            {
                "id": "lead-1003",
                "studentName": "Karthik Raja",
                "parentName": "S. Murugan",
                "parentPhone": "+91 94440 67890",
                "language": "ta",
                "boardPercentage": 84,
                "natScore": 71,
                "state": "Tamil Nadu",
                "budgetAnnual": 300000,
                "objectionsAsked": ["campus_matching", "roi_financial"],
                "matchedCampusId": "campus-crescent-chennai",
                "matchedCampusName": "NIAT @ B.S. Abdur Rahman Crescent Institute",
                "dossierGenerated": True,
                "seatReserved": False,
                "tokenAmount": 0,
                "status": "dossier_sent",
                "createdAt": (now - timedelta(hours=12)).isoformat(),
                "source": "NAT Test Completion",
            },
            {
                "id": "lead-1004",
                "studentName": "Pooja Patil",
                "parentName": "Suresh Patil",
                "parentPhone": "+91 98220 11223",
                "language": "en",
                "boardPercentage": 86,
                "natScore": 84,
                "state": "Maharashtra",
                "budgetAnnual": 350000,
                "objectionsAsked": ["accreditation", "ai_threat", "roi_financial"],
                "matchedCampusId": "campus-dypatil-pune",
                "matchedCampusName": "NIAT @ Dr. D.Y. Patil University",
                "dossierGenerated": True,
                "seatReserved": True,
                "tokenAmount": 25000,
                "status": "converted",
                "createdAt": (now - timedelta(hours=16)).isoformat(),
                "source": "Web Search / Direct",
            },
            {
                "id": "lead-1005",
                "studentName": "Aditya Hegde",
                "parentName": "Ganesh Hegde",
                "parentPhone": "+91 99000 88776",
                "language": "kn",
                "boardPercentage": 82,
                "natScore": 75,
                "state": "Karnataka",
                "budgetAnnual": 320000,
                "objectionsAsked": ["roi_financial"],
                "matchedCampusId": "campus-yenepoya-mng",
                "matchedCampusName": "NIAT @ Yenepoya (Deemed to be University)",
                "dossierGenerated": True,
                "seatReserved": False,
                "tokenAmount": 0,
                "status": "in_consultation",
                "createdAt": (now - timedelta(hours=24)).isoformat(),
                "source": "NAT Test Completion",
            },
        ]

    def get_all_leads(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self.leads)

    def add_lead(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            self.leads.insert(0, lead)
            return lead

    def get_analytics(self) -> Dict[str, Any]:
        with self._lock:
            total_leads = len(self.leads)
            dossiers_generated = sum(1 for l in self.leads if l.get("dossierGenerated"))
            seats_reserved = sum(1 for l in self.leads if l.get("seatReserved"))
            total_token_revenue = sum(l.get("tokenAmount", 0) for l in self.leads)

            objection_counts = {"accreditation": 0, "ai_threat": 0, "roi_financial": 0, "campus_matching": 0}
            language_counts = {"te": 0, "ta": 0, "hi": 0, "kn": 0, "ml": 0, "en": 0}

            for lead in self.leads:
                for obj in lead.get("objectionsAsked", []):
                    if obj in objection_counts:
                        objection_counts[obj] += 1
                lang = lead.get("language", "en")
                if lang in language_counts:
                    language_counts[lang] += 1

            conversion_rate = f"{(seats_reserved / total_leads * 100):.1f}" if total_leads > 0 else "0.0"

            funnel_comparison = {
                "control": {
                    "label": "Control: Human Tele-Calling",
                    "contactRate": 58,
                    "consultationRate": 34,
                    "conversionRate": 2.1,
                    "avgCac": 47600,
                    "avgSalesCycleDays": 14,
                    "languagesSupported": 1,
                },
                "experiment": {
                    "label": "Track B: Parent Trust AI Engine",
                    "contactRate": 100,
                    "consultationRate": 89,
                    "conversionRate": 3.3,
                    "avgCac": 30300,
                    "avgSalesCycleDays": 6.2,
                    "languagesSupported": 6,
                },
                "baselineFunnel": {
                    "channel": "Standard Human Tele-Counselor Funnel",
                    "natLeadsMonthly": 10000,
                    "contactRatePercent": 52,
                    "engagedParents": 5200,
                    "dossierDeliveredPercent": 12,
                    "leadToPaidConversionRate": 2.1,
                    "totalEnrolledSeats": 210,
                    "blendedCacInr": 47600,
                    "annualTuitionRevenueInr": 252000000,
                },
                "parentTrustEngineVariant": {
                    "channel": "Autonomous Multilingual Parent Trust Engine (Track B)",
                    "natLeadsMonthly": 10000,
                    "instantEngagementPercent": 78,
                    "engagedParents": 7800,
                    "dossierDeliveredPercent": 68,
                    "leadToPaidConversionRate": 3.3,
                    "totalEnrolledSeats": 330,
                    "blendedCacInr": 30300,
                    "annualTuitionRevenueInr": 396000000,
                    "incrementalSeats": 120,
                    "incrementalRevenueInr": 144000000,
                    "cacReductionPercent": 36.3,
                },
            }

            return {
                "totalLeads": total_leads,
                "dossiersGenerated": dossiers_generated,
                "seatsReserved": seats_reserved,
                "conversionRate": conversion_rate,
                "totalTokenRevenue": total_token_revenue,
                "objectionCounts": objection_counts,
                "languageCounts": language_counts,
                "languageBreakdown": language_counts,
                "funnelComparison": funnel_comparison,
            }


# Singleton database instance
db = InMemoryDatabase()
