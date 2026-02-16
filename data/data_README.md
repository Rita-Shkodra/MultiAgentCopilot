Data Sources

This folder contains the documents relating to Supply Chain used to build the vector database for the Multi-Agent Supply Chain Copilot.

All documents are publicly available corporate reports and industry research.
They are the only knowledge source used for retrieval and grounding.
No web browsing or external data is used.

Documents Included

 UPS 2024 Form 10-K
Transportation network, fuel exposure, operational risks, cost structure.

 FedEx 2024 Annual Report
Fuel surcharge mechanisms, air transport costs, efficiency programs.

 DHL 2024 Report
Global logistics performance, multimodal transport mix, sustainability.

 Target 2024 Annual Report
Retail supply chain exposure, supplier risks, cost pressures.

Inventory Turnover handbook

Amazon 2024 Annual Report
Fulfillment network complexity, transportation investments.

McKinsey OTIF Report
Lead time variability, service reliability.

BCG Resilience Report
Supply chain resilience, supplier concentration risk.

Deloitte Supply Chain Report
Risk monitoring, digital supply chain trends.

CSCMP Glossary
Standardized supply chain terminology.

 World Bank Logistics Performance Index 2023
Connectivity, trade facilitation, logistics performance metrics.

Processing

Documents are chunked and embedded.

Stored in a Chroma vector database.

Retrieved with similarity search.

All outputs are strictly grounded in retrieved evidence.

If no evidence exists, the system states so.