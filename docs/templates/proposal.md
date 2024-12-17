# Templates

## Master Schedule

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'taskBkgColor': '#7BB2E5',
    'taskTextColor': '#000000',
    'taskBorderColor': '#534fbc',
    'sectionBkgColor': '#f4f4f4',
    'activeTaskBkgColor': '#B784ED',
    'activeTaskBorderColor': '#534fbc',
    'activeTaskTextColor': '#000000',
    'critBkgColor': '#FFE44D',
    'critBorderColor': '#534fbc',
    'critTextColor': '#000000',
    'fontSize': '16px',
    'headerFontSize': '20px'
  },
  'gantt': {
    'leftPadding': 100,
    'rightPadding': 20
  }
}}%%
gantt
    title     Project Schedule Template
    dateFormat  MM
    axisFormat  Month %m
    
    section Development
    Task 1 Name            :active, dev1, 01, 03
    Task 2 Name            :active, dev2, 02, 04
    Task 3 Name            :active, dev3, 03, 05
    
    section Testing
    Task 4 Name            :crit, test1, 02, 04
    Task 5 Name            :crit, test2, 03, 05
    Task 6 Name            :crit, test3, 04, 06
    
    section Deployment
    Task 7 Name            :deploy1, 05, 07
```

## Timeline

```mermaid
%%{init: {
    'theme': 'base', 
    'themeVariables': { 
        'fontSize': '24px',
        'fontFamily': 'trebuchet ms',
        'timelineTitleTextAlignment': 'left'
    },
    'timeline': {
        'padding': 50,
        'titleTopMargin': 25
    }
}}%%
    timeline
        title [Your Project/Organization Name] Strategic Timeline
        section 2027
            ⚑ Milestone 1 : [Primary Goal], [Key Initiative], [Expected Outcome]
            note left : [Timeline/ Quarter]
        section 2028
            ⚑ Milestone 2 : [Primary Goal], [Key Initiative], [Expected Outcome]
            note right : [Key Metric]
        section 2029
            ⚑ Milestone 3 : [Primary Goal], [Key Initiative], [Expected Outcome]
            note left : [Target/Goal]
        section 2030
            ⚑ Milestone 4 : [Primary Goal], [Key Initiative], [Expected Outcome]
            note right : [Resources/ Budget]
        section 2031
            ⚑ Milestone 5 : [Primary Goal], [Key Initiative], [Expected Outcome]
            note left : [Success Criteria]
```

## Detailed Project Tasks Planning

| NO. | FEATURE CATEGORY | FEATURE (EPIC) | DETAIL (TASK) | DEFINITION OF DONE |
|-----|-----------------|----------------|---------------|-------------------|
| 1 | Category | Epic | - Task 1<br>- Task 2<br>| - DOD 1<br>- DOD 2<br> |

This template uses:
- Pipe characters (`|`) to separate columns
- Hyphens (`-`) in the header row separator
- `<br>` for line breaks within cells
- Consistent spacing for readability

## Team Role and Responsibility

| No | Account | Role | Responsibility | Email |
|----|---------|------|----------------|-------|
| 1 | John Smith | Sales Manager | Manage customer relationships and sales pipeline | john.smith@company.com |
| 2 | Jane Doe | Account Manager | Handle client accounts and contract negotiations | jane.doe@company.com |

The structure uses:
- Pipes (`|`) to separate columns
- Hyphens (`-`) in the second row to create the header separation
- Each field can contain multiple lines of text if needed

## Org Chart

```mermaid
flowchart TB
    %% Company 2 at top
    subgraph C2[COMPANY 2]
        direction LR
        GL["**Group Leader**<br>John Smith"] --> PS["**Project Sponsor**<br>David Wilson"] --> PD["**Program Director**<br>Michael Brown"] --> PM["**Project Manager**<br>Sarah Johnson"]
    end

    %% Company 1 main container
    subgraph C1[COMPANY 1]
        direction TB
        %% Leadership Layer
        subgraph LEAD[LEADERSHIP LAYER]
            direction TB
            L1["**Leader Company Level**<br>James Anderson"]
            
            %% Force Chief Officers to be horizontal
            subgraph CEO_GROUP[CHIEF OFFICERS]
                direction LR
                CO1["**Chief AI Officer**<br>Robert Lee"] --- CO2["**Chief Executive Officer**<br>Emma Davis"]
            end
            
            L1 --> CEO_GROUP
        end

        %% Operations Group - adjusted layout
        subgraph OPS[OPERATIONS ORG.]
            direction LR
            %% Delivery Organization
            subgraph DEL[DELIVERY ORG.]
                direction LR
                DM["**Delivery Manager**<br>Thomas Chen"]
                RM["**Resource Manager**<br>Lisa Wang"]
                TL["**Technical Lead**<br>Alex Zhang"]
                DM --> RM
                DM --> TL
            end

            %% Sales Organization
            subgraph SALES[SALES ORG.]
                direction TB
                SM["**Sales Manager**<br>Mark Taylor"]
                AM["**Account Manager**<br>Rachel Kim"]
            end
        end

        %% Project Delivery Team
        subgraph PDT[PROJECT DELIVERY TEAM]
            direction TB
            subgraph TM[TEAM MEMBERS]
                direction TB
                DA["**Data Architect**<br>1 HC"]
                DE["**Data Engineers**<br>3 HC"]
                AE["**AI Engineer**<br>0.5 HC"]
                TST["**Testers**<br>2 HC"]
            end
            PO["**Project Owner**<br>Daniel Park"]
            SCM["**Scrum Master**<br>Maria Garcia"]
        end
    end

    %% Relationships between subgraphs
    L1 -.-> GL
    LEAD --> OPS
    OPS --> PDT
    PO --> TM
    SCM -.-> TM
    PD <--> SALES
    PM <--> PO

    %% Styling
    classDef company1 fill:#FBE5D6,stroke:#333
    classDef company2 fill:#2B579A,stroke:#333,color:#fff
    classDef subgraphStyle fill:#fff,stroke:#999,stroke-width:1px
    classDef company2BG fill:#E6EEF9,stroke:#333
    classDef leadershipBG fill:#F0F7FF,stroke:#333
    classDef deliveryBG fill:#E8F5E9,stroke:#333
    classDef salesBG fill:#F5F5F5,stroke:#333
    classDef projectBG fill:#E3F2FD,stroke:#333
    classDef teamBG fill:#F3E5F5,stroke:#333
    classDef ceoGroupBG fill:#FFF8E1,stroke:#333
    classDef opsBG fill:#E8EAF6,stroke:#333

    %% Apply styles to nodes
    class L1,CO1,CO2,DM,RM,TL,SM,AM,PO,SCM,DA,DE,AE,TST company1
    class GL,PS,PD,PM company2

    %% Apply styles to subgraphs
    class C2 company2BG
    class LEAD leadershipBG
    class DEL deliveryBG
    class SALES salesBG
    class PDT projectBG
    class TM teamBG
    class CEO_GROUP ceoGroupBG
    class OPS opsBG
```