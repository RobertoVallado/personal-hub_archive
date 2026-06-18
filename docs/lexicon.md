## Key Terms Glossary

A curated collection of important terms and definitions maintained as a personal reference, with clean explanations and supporting references.
>Entries may appear in both French and English.


---

### Authentication

**Definition**  
The process of verifying the identity of a user, system, or application.

**Context / Usage**  
Commonly used in web applications to control access to protected resources.

**References**

* [Wikipedia: Authentication / computer Science ](https://en.wikipedia.org/wiki/Authentication#In_computer_science)

---

### Role-Based Access Control (RBAC)

**Definition** A method of restricting network or application access based on the roles of individual users within an enterprise. In this model, permissions are assigned to specific roles (e.g., Admin, Editor, Viewer) rather than to individual users.

**Context / Usage** 
Used in corporate environments and SaaS applications to simplify permission management; when a user's job function changes, you simply change their role rather than updating dozens of individual permissions.

**References**

* [Wikipedia: Role-based access control](https://en.wikipedia.org/wiki/Role-based_access_control)

---

### Whitelist (Allowlist)

**Definition** 
A cybersecurity strategy that grants access or privileges only to a specific list of approved entities (IP addresses, applications, or email addresses), while blocking everything else by default.

**Context / Usage** 
Often used in firewall configurations or email filters to ensure that only "known-good" traffic can interact with a sensitive system. This is the opposite of a "Blacklist."

**References**

* [Wikipedia: Whitelisting](https://en.wikipedia.org/wiki/Whitelisting)

---

### Context-Based Authorization

**Definition** A dynamic access control method that evaluates the circumstances of a requests...such as the users location, the time of day, the device being used, and the security posture of the network, before granting access.

**Context / Usage** Crucial for **Zero Trust** architectures, where an authenticated user might be allowed to view data from a corporate laptop at the office but denied access if trying to login from a public IP address in a different country.

**References**

* [Wikipedia: Attribute-based access control](https://en.wikipedia.org/wiki/Attribute-based_access_control)

---

### Domain-Driven Design (DDD)

**Definition** A software development approach that focuses on matching the software implementation to a complex business domain. It emphasizes a "Ubiquitous Language" shared between developers and domain experts to ensure the code accurately reflects business logic.

**Context / Usage** Commonly applied in microservices architecture to define "Bounded Contexts," ensuring that different parts of a large system have clear boundaries and specific responsibilities.

**References**

* [Wikipedia: Domain-driven design](https://en.wikipedia.org/wiki/Domain-driven_design)

---

### Cross-Site Scripting (XSS)

**Definition** A security vulnerability where an attacker injects malicious scripts into content delivered to other users from a trusted website. This occurs when an application includes untrusted data in a web page without proper validation or escaping.

**Context / Usage** Used by attackers to steal session cookies or hijack user accounts. Preventing XSS is a primary focus of web developers using frameworks like React or Angular, which provide built-in protection against many XSS vectors.

**References**

* [Wikipedia: Cross-site scripting](https://en.wikipedia.org/wiki/Cross-site_scripting)

---

### Epitomize

**Definition** To serve as a perfect or typical example of a particular quality or type; to be the "core" of something.

**Context / Usage** Used in professional and academic writing to describe a person, project, or concept that embodies the highest standards of its category (e.g., "The new security protocols **epitomize** the company's commitment to user privacy").

**References**

* [Wikipedia: Paradigm](https://en.wikipedia.org/wiki/Paradigm)

---

### Data Transfer Objects (DTOs)

**Definition** An object that carries data between processes in order to reduce the number of method calls. DTOs are simple containers for data (usually just getters and setters) and do not contain any business logic.

**Context / Usage** Frequently used in REST APIs to transform internal database entities into a specific format that the client (frontend) needs, effectively decoupling the internal data model from the external API.

**References**

* [Wikipedia: Data transfer object](https://en.wikipedia.org/wiki/Data_transfer_object)

---

### Infrastructure as Code (IaC)

**Definition**
The practice of managing and provisioning computing infrastructure through machine-readable configuration files rather than through manual processes or interactive configuration tools.

**Context / Usage**
Used with tools like Terraform, Ansible, and AWS CloudFormation to version-control infrastructure alongside application code, reproduce environments consistently, and automate deployments. The Terraform lab (DY67) is a direct example: the entire Azure environment is defined in `.tf` files and can be created or destroyed with a single command.

**References**

* [Wikipedia: Infrastructure as code](https://en.wikipedia.org/wiki/Infrastructure_as_code)

---

### Dependency Injection (DI)

**Definition**
A design pattern in which an object receives its dependencies from an external source rather than creating them itself. The dependencies are "injected" into the object, typically through constructor parameters.

**Context / Usage**
Core to modern frameworks like ASP.NET Core and Spring. Enables loose coupling between components, simplifies unit testing (inject a mock instead of the real service), and supports the Dependency Inversion principle of SOLID. In ASP.NET Core, services are registered in the DI container with a lifetime (Transient, Scoped, Singleton) and injected automatically.

**References**

* [Wikipedia: Dependency injection](https://en.wikipedia.org/wiki/Dependency_injection)

---

### ORM (Object-Relational Mapper)

**Definition**
A technique that converts data between a relational database and an object-oriented programming language, letting developers work with database records as native objects without writing raw SQL.

**Context / Usage**
Used with tools like Entity Framework Core (C#), Hibernate (Java), and SQLAlchemy (Python). The ORM generates SQL from LINQ queries, manages change tracking, and handles migrations. The trade-off is that complex or performance-critical queries sometimes require dropping back to raw SQL.

**References**

* [Wikipedia: Object-relational mapping](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping)

---

### JWT (JSON Web Token)

**Definition**
A compact, URL-safe token format used to represent claims between two parties. A JWT encodes a JSON payload and is digitally signed so the receiver can verify its authenticity without contacting an authentication server.

**Context / Usage**
Widely used for stateless authentication in REST APIs and single-page applications. The server issues a JWT on login; subsequent requests include it in the `Authorization: Bearer` header. Because JWTs are self-contained, they cannot be revoked before expiry without a server-side blocklist; a key trade-off to know.
<!-- so 90's ̿' ̿'\̵͇̿̿\з=(◕_◕)=ε/̵͇̿̿/'̿'̿ ̿ -->

**References**

* [Wikipedia: JSON Web Token](https://en.wikipedia.org/wiki/JSON_Web_Token)

---

### CORS (Cross-Origin Resource Sharing)

**Definition**
A browser security mechanism that controls whether a web page may request resources from a different domain than the one that served it. Servers opt in by including specific HTTP response headers.

**Context / Usage**
Relevant whenever a frontend on one domain (e.g., `app.example.com`) calls an API on another (e.g., `api.example.com`). CORS is enforced by the browser, not the server; Direct API calls via curl or Postman are never blocked. Misconfigured CORS (e.g., `AllowAnyOrigin` combined with `AllowCredentials`) is a common security mistake.

**References**

* [Wikipedia: Cross-origin resource sharing](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing)

---

### OAuth 2.0

**Definition**
An open authorization framework that allows an application to obtain limited access to a user's account on a third-party service without the user sharing their credentials. The user grants consent; the service issues an access token.

**Context / Usage**
Widely used for "Sign in with Google / GitHub" flows and delegated API access. OAuth 2.0 handles authorization (what can the app access?). OpenID Connect (OIDC) is the identity layer built on top that adds authentication (who is the user?). In ASP.NET Core, `AddAuthentication().AddGoogle(...)` wires up OIDC under the hood.

**References**

* [Wikipedia: OAuth](https://en.wikipedia.org/wiki/OAuth)

---

### Middleware

**Definition**
Software that sits between two layers of a system, processing requests and responses as they pass through. In web frameworks, middleware is a pipeline of components where each handles a specific cross-cutting concern.

**Context / Usage**
In ASP.NET Core, middleware components handle authentication, logging, CORS, exception handling, and routing. Each component decides whether to pass the request to the next one in the chain. Order matters: registering `UseAuthorization` before `UseAuthentication` breaks token validation.

**References**

* [Wikipedia: Middleware](https://en.wikipedia.org/wiki/Middleware)

---

### Repository Pattern

**Definition**
A design pattern that abstracts the data access layer behind an interface, presenting a collection-like API for querying and persisting domain objects without exposing database details to the rest of the application.

**Context / Usage**
Common in enterprise applications to decouple business logic from the data access technology (Entity Framework, Dapper, etc.). Makes unit testing easier by allowing the repository to be replaced with an in-memory fake. The counter-argument: `DbContext` in Entity Framework Core already implements the repository and unit-of-work patterns, so adding another layer can be redundant overhead.

**References**

* [Wikipedia: Domain-driven design](https://en.wikipedia.org/wiki/Domain-driven_design)

---

### Garbage Collection (GC)

**Definition**
An automatic memory management technique in which the runtime periodically identifies and reclaims heap memory occupied by objects that are no longer reachable, freeing developers from manually deallocating memory.

**Context / Usage**
Used in .NET, Java, Go, and other managed runtimes. .NET's GC uses a generational model (Gen 0, Gen 1, Gen 2) based on the observation that most objects die young, collecting short-lived objects frequently and long-lived ones rarely. Important caveat: the GC only manages *managed* memory. Unmanaged resources (file handles, database connections, sockets) must be released explicitly via `IDisposable` and the `using` pattern.

**References**

* [Wikipedia: Garbage collection (computer science)](https://en.wikipedia.org/wiki/Garbage_collection_(computer_science))

---

### Optimistic Concurrency

**Definition**
A concurrency control strategy that allows multiple transactions to proceed simultaneously without locking shared resources, but checks for conflicts at commit time. If a conflict is detected, the operation is rejected and the caller must retry.

**Context / Usage**
Commonly used in databases and ORMs. In Entity Framework Core, a row version or timestamp column is used to detect whether another user modified the same record between read and write. Assumes conflicts are rare, making it more efficient than pessimistic locking (which holds a lock for the duration of the transaction) for read-heavy workloads.

**References**

* [Wikipedia: Optimistic concurrency control](https://en.wikipedia.org/wiki/Optimistic_concurrency_control)

---
