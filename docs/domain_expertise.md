# Manufacturing × data analytics : Domain knowledge

## Output in the previous company

### Project : Salesforce / ERP data integration
**Role** Data base design/implementation

#### Issues
1. Stored data into S/4 HANA and Salesforce separately. 
2. Worlload increased because of the separate data management.

#### What we did
1. **Data model desinging**
    - Star schema design (Fact: Pipeline data, Dim: Customer, product masters.)
    - Extract sales result data from S/4 HANA
    - Integarate pipeline data from Salesforce.
2. **Tool selection/implementation**
    - ETL: QlikSense
    - DWH: Qlik server
    - BI: QlikSense

3. **Visulization**
    - Sales KPI dashboard
    - Monitoring pipeline progress
    - Result vs Fcst diff analysis

#### Outcome
- Time lag improvement : 1 week -> 1 day (Batch / day)
- Data driven decision making

#### Takeaway
- Issues in integarating data in ERP/CRM
- Designing a star schema
- Importance of stakeholders' management

---

## Daya analytics issues in manufacturing industry.
### 1. SCM optimization
    - Need to connect the total SCM return, in the end, even though there are some technical gap amoung departments. 

### 2. Improce the demand forecasting quality.
    - Together with the macro data, it is expected to foresee the sales numbers in a higher precision. The issues is how to varify the logic and how to deliver to the users within company, in a very clear way. 

### 3. Culture against Data analysis 
    - Need to make it clear, Why/What/How data analysis contribute to the user's and management requirements on top of the contribution to the bussiness/customers. 