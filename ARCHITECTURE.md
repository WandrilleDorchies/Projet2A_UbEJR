# Architecture 

```mermaid
---
title: Architecture Ub'EJR
---
flowchart LR
 subgraph Services["Service Controllers"]
        AUTH["Auth Service"]
        MENU["Menu Service"]
        ORDR["Orders Service"]
        DELIV["Delivery Service"]
  end
 subgraph Interfaces["Interface Layer"]
        CLI["CLI"]
        API["API Webservice"]
  end
 subgraph PythonApp["Python App"]
        DAO["Data Acces Object"]
        Services
        Interfaces
  end
    STRIPE["Stripe API"] --> ORDR
    ADM(("Admin")) <--> API
    CUS(("Customer")) <--> CLI
    DEL(("Deliverer")) <--> CLI
    DAO --> Services
    DELIV --> GMAPI["Google Maps API
        Trajets/Distance Matrix"]
    GMAPI <--> GMDB[("Google Maps Database")]
    Interfaces <--> Services
    DB[("PostgreSQL Database")] --> DAO

```