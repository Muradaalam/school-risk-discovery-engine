## School Service – API Contract

## 1. Project Information

- **Project Name:** School Service
- **Framework:** Spring Boot
- **Language:** Java
- **Database:** MySQL
- **Base URL:** `http://localhost:8080`
- **API Prefix:** `/school-service`
- **Authentication:** JWT Bearer Token
- **Request/Response Format:** JSON
- **Total Controllers:** 9
- **Total Endpoints:** 30

## 2. Authentication

All secured API requests must include a JWT token in the Authorization header.

**Header:**

`Authorization: Bearer <JWT_TOKEN>`

## 3. API Endpoints

### 3.1. School Controller – 6 Endpoints

- `GET /school/getSchool/schoolId`
- `GET /school/getSchool/id`
- `GET /school/getTop50Schools`
- `GET /school/getAllSchools`
- `POST /school/createSchool`
- `DELETE /school/deleteSchool/{schoolId}`

### 3.2. Document Controller – 3 Endpoints

- `GET /document/getDocument/objectId`
- `GET /document/getDocument/id`
- `POST /document/createDocument`

### 3.3. Event Controller – 3 Endpoints

- `GET /event/getEvent/schoolId`
- `GET /event/getEvent/id`
- `POST /event/createEvent`

### 3.4. Inspection Controller – 3 Endpoints

- `GET /inspection/getInspection/schoolId`
- `GET /inspection/getInspection/id`
- `POST /inspection/createInspection`

### 3.5. Issue Controller – 3 Endpoints

- `GET /issue/getIssue/schoolId`
- `GET /issue/getIssue/id`
- `POST /issue/createIssue`

### 3.6. Priority Snapshot Controller – 3 Endpoints

- `GET /prioritySnapshot/getPrioritySnapshot/schoolId`
- `GET /prioritySnapshot/getPrioritySnapshot/id`
- `POST /prioritySnapshot/createPrioritySnapshot`

### 3.7. Project Controller – 3 Endpoints

- `GET /project/getProject/issueId`
- `GET /project/getProject/id`
- `POST /project/createProject`

### 3.8. Source Controller – 3 Endpoints

- `GET /source/getSource/schoolId`
- `GET /source/getSource/id`
- `POST /source/createSource`

### 3.9. Tender Controller – 3 Endpoints

- `GET /tender/getTender/projectId`
- `GET /tender/getTender/id`
- `POST /tender/createTender`

**Postman Collection:**

Refer to `schoolrde.postman_collection.json`.

Import `schoolrde.postman_collection.json` into Postman to explore and test all available API endpoints.

## 4. Error Handling

The application uses a centralized `CustomExceptionHandler`. Business exceptions are identified using application-specific error codes.

## 5. Version History

- **Version 1.0** – Initial API contract.
- **Last Updated:** 23 November 2026.
