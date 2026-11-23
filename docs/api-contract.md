School Service – API Contract
1. Project Information
    Project Name: School Service
    Framework: Spring Boot
    Language: Java
    Database: MySQL
    Base URL: http://localhost:8080
    API Prefix: /school-service
    Authentication: JWT Bearer Token
    Request/Response Format: JSON
    Total Controllers: 9
    Total Endpoints: 30


2. Authentication
All secured API requests must include a JWT token in the Authorization header.
Header: Authorization: Bearer <JWT_TOKEN>


3. API Endpoints
School Controller – 6 endpoints
    GET /school/getSchool/schoolId
    GET /school/getSchool/id
    GET /school/getTop50Schools
    GET /school/getAllSchools
    POST /school/createSchool
    DELETE /school/deleteSchool/{schoolId}

Document Controller – 3 endpoints
    GET /document/getDocument/objectId
    GET /document/getDocument/id
    POST /document/createDocument

Event Controller – 3 endpoints
    GET /event/getEvent/schoolId
    GET /event/getEvent/id
    POST /event/createEvent

Inspection Controller – 3 endpoints
    GET /inspection/getInspection/schoolId
    GET /inspection/getInspection/id
    POST /inspection/createInspection

Issue Controller – 3 endpoints
    GET /issue/getIssue/schoolId
    GET /issue/getIssue/id
    POST /issue/createIssue

Priority Snapshot Controller – 3 endpoints
    GET /prioritySnapshot/getPrioritySnapshot/schoolId
    GET /prioritySnapshot/getPrioritySnapshot/id
    POST /prioritySnapshot/createPrioritySnapshot

Project Controller – 3 endpoints
    GET /project/getProject/issueId
    GET /project/getProject/id
    POST /project/createProject

Source Controller – 3 endpoints
    GET /source/getSource/schoolId
    GET /source/getSource/id
    POST /source/createSource

Tender Controller – 3 endpoints
    GET /tender/getTender/projectId
    GET /tender/getTender/id
    POST /tender/createTender

**Refer to the Postman collection: schoolrde.postman_collection.json
Import schoolrde.postman_collection.json into Postman to explore and test all available API endpoints.

4. Error Handling
The application uses a centralized CustomExceptionHandler. Business exceptions are identified using application-specific error codes.

5. Version History
    Version 1.0 – Initial API contract.
    Last Updated: 23 November 2026.
