from typing import  Literal, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

# Admission number: C027-01-0889/2024


app = FastAPI(
    title="GigHub Nairobi Freelance Gigs API",

)


gigs_db = [
    {
        "id": 1,
        "title": "A digital marketing campaign",
        "description": "Targeted digital marketing campaign for the brand.",
        "category": "Marketing",
        "budget": 200000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Faith Gitahi",
    },
    {
        "id": 2,
        "title": "Build an interactive dashboard",
        "description": "Build a dashboard that visualizes customer behaviour and sales performance.",
        "category": "Data",
        "budget": 30000.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Timothy Mwangi",
    },
    {
        "id": 3,
        "title": "Customer research and consulting support",
        "description": "Provide consulting advice and research on customer preferences for a new product.",
        "category": "Consulting",
        "budget": 48000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Brian Gitahi",
    },
    {
        "id": 4,
        "title": "Develop a social media strategy",
        "description": "Create a social media strategy and content calendar for a lifestyle brand.",
        "category": "Marketing",
        "budget": 15000.0,
        "currency": "KES",
        "status": "Closed",
        "client_name": "Jane Wangui",
    },
    {
        "id": 5,
        "title": "Data cleaning and analysis",
        "description": "Clean transactional data and deliver a summary report for executive review.",
        "category": "Data",
        "budget": 17500.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Kevin Kimani",
    },
    {
        "id": 6,
        "title": "Consulting for pricing strategy",
        "description": "Advise on pricing strategy for a new product launch in the Kenyan market.",
        "category": "Consulting",
        "budget": 22000.0,
        "currency": "KES",
        "status": "Closed",
        "client_name": "Mary Wangechi",
    },
    {
        "id": 7,
        "title": "Marketing research for product launch",
        "description": "Conduct market research and produce a  report.",
        "category": "Marketing",
        "budget": 16000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "David Kariuki",
    },
    {
        "id": 8,
        "title": "Build a sales forecasting model",
        "description": "Create a sales forecasting model using historical sales and seasonality data.",
        "category": "Data",
        "budget": 24000.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Wahu Chege",
    },
    {
        "id": 9,
        "title": "Consulting on freelancer onboarding",
        "description": "Design a freelancer onboarding process and training materials for a new platform.",
        "category": "Consulting",
        "budget": 13500.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Aisha Juma",
    },
    {
        "id": 10,
        "title": "Paid search campaign optimization",
        "description": "Optimize a paid search campaign and improve conversion rates for a local service.",
        "category": "Marketing",
        "budget": 19500.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Nuru Mwikali",
    },
    {
        "id": 11,
        "title": "Analyze customer satisfaction data",
        "description": "Find out how customers feel and if they are happy with our service.",
        "category": "Data",
        "budget": 17000.0,
        "currency": "KES",
        "status": "Closed",
        "client_name": "Josephine Wanjiku",
    },
    {
        "id": 12,
        "title": "Consult on remote team collaboration",
        "description": "Check our teamwork tools and suggest ways to make them better.",
        "category": "Consulting",
        "budget": 14500.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Conrad Kamau",
    },
    {
        "id": 13,
        "title": "Brand positioning plan",
        "description": "Create a brand positioning plan for a new fintech product targeting young professionals.",
        "category": "Marketing",
        "budget": 21000.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Kenzie A",
    },
    {
        "id": 14,
        "title": "Create a KPI dashboard for sales",
        "description": "Design and deliver a KPI dashboard that tracks sales performance and team goals.",
        "category": "Data",
        "budget": 23000.0,
        "currency": "KES",
        "status": "Closed",
        "client_name": "Melanie Katana",
    },
]


class GigCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10, max_length=100)
    category:  Literal["Marketing", "Data", "Consulting"]
    budget: float = Field(..., gt=0)
    client_name: str = Field(..., min_length=2, max_length=50)



class GigUpdate(BaseModel):
    budget: Optional[float] = Field(None, gt=0)
    status: Optional[Literal["Open", "In Progress", "Closed"]] = None
   
    
#GET All Gigs


@app.get("/gigs")
def get_gigs(
    category: str = None,
    min_budget: float = None,
    max_budget: float = None
):
    results = gigs_db

    if category:
        results = [g for g in results if g["category"] == category]

    if min_budget is not None:
        results = [g for g in results if g["budget"] >= min_budget]

    if max_budget is not None:
        results = [g for g in results if g["budget"] <= max_budget]

    return results


# SEARCH

@app.get("/gigs/search")
def search_gigs(q: str = Query(..., min_length=1, description="Search query for gig titles.")):
    query = q.strip().lower()
    return [gig for gig in gigs_db if query in gig["title"].lower()]



# GET BY ID

@app.get("/gigs/{gig_id}")
def find_gig(gig_id: int):
    for gig in gigs_db:
        if gig["id"] == gig_id:
            return gig
    return None



# CREATE

@app.post("/gigs")
def create_gig(gig: GigCreate):
    
    new_gig = {
        "id":len(gigs_db) + 1,
        "title": gig.title,
        "description": gig.description,
        "category": gig.category,
        "budget": gig.budget,
        "currency": "KES",
        "status": "Open",
        "client_name": gig.client_name,
    }
    gigs_db.append(new_gig)
    return new_gig

# UPDATE

@app.put("/gigs/{gig_id}")
def update_gig(gig_id: int, gig_update: GigUpdate):
    gig = find_gig(gig_id)
    if gig is None:
        raise HTTPException(status_code=404, detail="Gig not found")

    if gig_update.budget is None and gig_update.status is None:
        raise HTTPException(status_code=400,detail="Please provide a budget or status to update.")

    if gig_update.budget is not None:
        gig["budget"] = gig_update.budget
    if gig_update.status is not None:
        gig["status"] = gig_update.status

    return gig

# DELETE

@app.delete("/gigs/{gig_id}")
def delete_gig(gig_id: int):
    gig = find_gig(gig_id)
    if gig is None:
        raise HTTPException(status_code=404, detail="Gig not found")
    gigs_db.remove(gig)

    return {"Message": "Gig deleted successfully"}
