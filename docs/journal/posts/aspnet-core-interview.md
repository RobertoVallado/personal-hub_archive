---
date:
  created: 2026-06-10
  updated: 2026-06-10
readtime: 12
pin: true
links:
  - Knowledgebase Index: journal/index.md
categories:
  - Technical Interview Topics
tags:
  - ASP.NET Core
  - C#
  - .NET
authors:
  - robertovallado
slug: aspnet-core-technical-interview-topics
---

# ASP.NET Core Technical Interview Topics

Core ASP.NET Core concepts for technical interviews. Compact read-and-recall short form info.

<!-- more -->

---

## Middleware Pipeline

**What it is:** A chain of components that process HTTP requests and responses in order. Each middleware decides whether to call the next one.

- `app.Use`: calls next middleware (`await next(context)`)
- `app.Run`: terminal; never calls next
- `app.Map` / `app.MapWhen`: branch the pipeline based on path or condition
- **Order matters:** exception handling, HSTS, static files, routing, auth, endpoints
- Each middleware wraps the next (Russian-doll model) and can act on both request and response

```csharp
app.Use(async (ctx, next) => {
    // before
    await next(ctx);
    // after (response)
});
```

> **Note:** Always register `UseAuthentication()` before `UseAuthorization()`. Reversing them causes 401s even with valid tokens.

---

## Dependency Injection: Service Lifetimes

**What it is:** ASP.NET Core has a built-in IoC container. Every registered service gets one of three lifetimes.

| Lifetime | Created | Destroyed | Use for |
|----------|---------|-----------|---------|
| **Transient** | Every injection | When scope ends | Stateless lightweight services |
| **Scoped** | Once per HTTP request | End of request | DbContext, unit-of-work |
| **Singleton** | App startup | App shutdown | Caches, config wrappers, shared state |

- Injecting a **Scoped** service into a **Singleton** is a captive dependency. The scoped service outlives its intended lifetime and the DI container will throw at startup
- `IServiceScopeFactory` is the safe way to use scoped services from a singleton or background service

```csharp
builder.Services.AddTransient<IEmailSender, SmtpEmailSender>();
builder.Services.AddScoped<IOrderRepository, EfOrderRepository>();
builder.Services.AddSingleton<IMemoryCache, MemoryCache>();
```

> **Note:** `DbContext` is `Scoped` by default. One instance per request ensures consistent change tracking and avoids cross-request state leaks.

---

## IConfiguration & Options Pattern

**What it is:** Hierarchical key-value configuration from JSON, env vars, secrets, CLI args, merged in layered order.

- Sources (last wins): `appsettings.json`, `appsettings.{Environment}.json`, env vars, CLI
- `IConfiguration["Section:Key"]`: direct access (string only)
- **Options pattern:** bind a section to a typed POCO: `services.Configure<SmtpOptions>(config.GetSection("Smtp"))`
- Inject `IOptions<T>` (singleton snapshot), `IOptionsSnapshot<T>` (per-request reload), `IOptionsMonitor<T>` (live change notifications)

```csharp
public record SmtpOptions(string Host, int Port);
builder.Services.Configure<SmtpOptions>(builder.Configuration.GetSection("Smtp"));
// Inject: IOptions<SmtpOptions> opts => opts.Value.Host
```

> **Note:** `IOptions<T>` is a snapshot from startup and does not reflect runtime changes to `appsettings.json`. Use `IOptionsMonitor<T>` for live reloading.

---

## Routing: Attribute vs Conventional

**What it is:** Routing maps an incoming URL to an endpoint (controller action or minimal API handler).

- **Conventional routing:** defined in `Program.cs` with templates (`{controller}/{action}/{id?}`); used for MVC
- **Attribute routing:** decorators on controllers/actions (`[Route("api/orders")]`, `[HttpGet("{id}")]`)
- Route constraints: `[HttpGet("{id:int:min(1)}")]`
- `[ApiController]` enables attribute routing by convention and automatic model validation

```csharp
[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    [HttpGet("{id:int}")]
    public IActionResult Get(int id) => Ok(_repo.Find(id));
}
```

> **Note:** Attribute routing takes precedence over conventional routing for API controllers. Mix them only deliberately.

---

## Controllers vs Minimal APIs

**What it is:** Two ways to define HTTP endpoints in ASP.NET Core.

| | Controllers | Minimal APIs |
|---|---|---|
| Base class | `ControllerBase` | None |
| Routing | Attributes | `MapGet`, `MapPost`, etc. |
| Model binding | Automatic | Automatic |
| Filters | Full support | Limited (endpoint filters) |
| Overhead | Higher (reflection) | Lower (delegates) |
| Best for | Large, structured APIs | Small services, prototypes |

```csharp
// Minimal API
app.MapGet("/orders/{id}", async (int id, IOrderRepo repo) =>
    await repo.FindAsync(id) is { } order ? Results.Ok(order) : Results.NotFound());
```

> **Note:** Minimal APIs support dependency injection via method parameters. The framework resolves registered services automatically.

---

## Model Binding & Validation

**What it is:** Automatic mapping of HTTP request data (route, query, body, headers) to action method parameters.

- `[FromRoute]`, `[FromQuery]`, `[FromBody]`, `[FromHeader]`, `[FromForm]`: explicit binding sources
- `[ApiController]` infers `[FromBody]` for complex types and `[FromQuery]` for primitives
- Validation: `[Required]`, `[Range]`, `[MaxLength]`, `[RegularExpression]` on model properties
- `ModelState.IsValid`: check manually in MVC; `[ApiController]` auto-returns 400 if invalid
- `IValidatableObject`: custom cross-property validation

```csharp
public record CreateOrderRequest(
    [Required] string ProductId,
    [Range(1, 100)] int Quantity);
```

> **Note:** `[ApiController]` short-circuits the action entirely when the model is invalid. You never reach your action body.

---

## Filters

**What it is:** Cross-cutting concerns applied before/after actions without cluttering the action itself.

- **Authorization:** runs first; short-circuits if unauthorized
- **Resource:** wraps model binding; good for caching
- **Action:** before/after action method execution; has access to arguments
- **Result:** before/after the result (e.g., `IActionResult`) is executed
- **Exception:** handles unhandled exceptions from action or other filters
- Apply via attribute, globally in `AddControllers(o => o.Filters.Add(...))`, or per-controller

```csharp
public class LogActionFilter : IActionFilter
{
    public void OnActionExecuting(ActionExecutingContext ctx) => Log("before");
    public void OnActionExecuted(ActionExecutedContext ctx) => Log("after");
}
```

> **Note:** Filter order (inside-out): Authorization, Resource, Action, Result, Exception. The Exception filter catches exceptions from all other filters.

---

## Authentication vs Authorization

**What it is:** Authentication = who you are. Authorization = what you can do.

- **Authentication:** `UseAuthentication()` validates credentials and populates `HttpContext.User`
- **Authorization:** `UseAuthorization()` checks if the authenticated user can access the resource
- `[Authorize]`: requires authenticated user; `[AllowAnonymous]`: bypasses
- Policies: `[Authorize(Policy = "AdminOnly")]` combined with `builder.Services.AddAuthorization(o => o.AddPolicy(...))`
- Claims-based: policies can require specific claims (`context.User.HasClaim(...)`)

```csharp
builder.Services.AddAuthorization(options =>
    options.AddPolicy("AdminOnly", p => p.RequireRole("Admin")));
```

> **Note:** Authorization policies are evaluated AFTER authentication. If there's no identity (unauthenticated), the policy is never reached and the user gets 401, not 403.

---

## JWT Bearer Tokens

**What it is:** Stateless auth token; a Base64-encoded JSON payload signed with a secret or key pair.

- Structure: `header.payload.signature`; payload contains claims (`sub`, `exp`, `roles`, custom)
- Flow: client POSTs credentials, server returns JWT, client sends `Authorization: Bearer <token>`
- Validate with `AddAuthentication().AddJwtBearer(o => o.TokenValidationParameters = ...)`
- Key validations: issuer, audience, expiry, signature
- Refresh tokens are separate (opaque, stored server-side); JWTs themselves are stateless

```csharp
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(o => {
        o.TokenValidationParameters = new() {
            ValidIssuer = "myapp",
            ValidAudience = "myapi",
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secret))
        };
    });
```

> **Note:** JWTs can't be revoked before expiry without a server-side blocklist. Keep expiry short (15 min) and use refresh tokens for longevity.

---

## CORS

**What it is:** Cross-Origin Resource Sharing; a browser security mechanism that restricts cross-domain requests. Server opts in via response headers.

- `UseCors()` must come before `UseRouting()` / `UseAuthorization()`
- Named policy: `builder.Services.AddCors(o => o.AddPolicy("AllowFrontend", p => p.WithOrigins("https://myapp.com")))`
- `AllowAnyOrigin()` combined with `AllowCredentials()` is invalid; credentials require explicit origins
- Preflight: browser sends `OPTIONS` request before the real one; ASP.NET Core handles it automatically

```csharp
app.UseCors("AllowFrontend");
```

> **Note:** CORS is enforced by the **browser**, not the server. A direct HTTP call (curl, Postman) is never blocked by CORS.

---

## Response Caching & Output Caching

**What it is:** Server-side mechanisms to avoid re-executing expensive logic for identical requests.

- **Response caching:** respects HTTP cache headers (`Cache-Control`); uses `[ResponseCache]` attribute or middleware
- **Output caching** (ASP.NET Core 7+): server-controlled, not dependent on client headers; more flexible
- `AddOutputCache()` + `UseOutputCache()` + `[OutputCache(Duration = 60)]`
- Can vary cache by query string, route, or custom policy

```csharp
builder.Services.AddOutputCache();
app.UseOutputCache();
app.MapGet("/products", GetProducts).CacheOutput(p => p.Expire(TimeSpan.FromMinutes(5)));
```

> **Note:** Output caching is independent of client `Cache-Control` headers. Response caching can be bypassed by clients sending `no-cache`.

---

## `IHostedService` / `BackgroundService`

**What it is:** Run long-running background work (queue consumers, scheduled jobs, health polling) within the ASP.NET Core host lifetime.

- `IHostedService`: `StartAsync` / `StopAsync` lifecycle; wired up via `AddHostedService<T>()`
- `BackgroundService`: abstract base that wraps `IHostedService`; override `ExecuteAsync(CancellationToken)`
- Use `IServiceScopeFactory` to get scoped services (like DbContext) inside a singleton hosted service
- Exceptions in `ExecuteAsync` stop the background service but don't crash the host by default

```csharp
public class QueueWorker(IServiceScopeFactory factory) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            using var scope = factory.CreateScope();
            var repo = scope.ServiceProvider.GetRequiredService<IOrderRepo>();
            await ProcessNextAsync(repo, ct);
        }
    }
}
```

> **Note:** `ExecuteAsync` is called once at startup. Loop inside it with a `CancellationToken` check; the token is cancelled on app shutdown.

---

## IHttpClientFactory

**What it is:** The correct way to create `HttpClient` instances in ASP.NET Core. Avoids the socket exhaustion problem that comes from instantiating `HttpClient` directly.

- `new HttpClient()` in a loop or per-request does not release sockets promptly, exhausting the OS port pool
- `IHttpClientFactory` manages a pool of `HttpMessageHandler` instances internally, reusing connections
- **Named client:** `services.AddHttpClient("github", c => c.BaseAddress = ...)`
- **Typed client:** a class that takes `HttpClient` in its constructor and is registered via `services.AddHttpClient<GitHubClient>()`
- Typed clients are the cleanest pattern; they get a fresh `HttpClient` facade but share the underlying handler pool

```csharp
builder.Services.AddHttpClient<WeatherClient>(c =>
    c.BaseAddress = new Uri("https://api.weather.com"));

public class WeatherClient(HttpClient client)
{
    public Task<Forecast> GetAsync() => client.GetFromJsonAsync<Forecast>("/forecast");
}
```

> **Note:** `HttpClient` is safe to reuse (it's thread-safe). The problem is creating and disposing it too often. `IHttpClientFactory` solves this transparently.

---

## Logging (`ILogger`)

**What it is:** ASP.NET Core has a built-in structured logging abstraction (`ILogger<T>`) with pluggable providers and configurable log levels.

- Log levels in order: `Trace`, `Debug`, `Information`, `Warning`, `Error`, `Critical`
- Inject `ILogger<MyClass>` via constructor; the generic type shows up as the category in logs
- Providers: Console, Debug, EventSource, EventLog (Windows), and third-party (Serilog, NLog, seq)
- Configure minimum level per category in `appsettings.json` under `"Logging":`
- Use message templates (not string interpolation) for structured logging: `_logger.LogInformation("Order {Id} created", orderId)`

```csharp
public class OrderService(ILogger<OrderService> logger)
{
    public void Create(Order order)
    {
        logger.LogInformation("Creating order {OrderId}", order.Id);
        // ...
        logger.LogError(ex, "Failed to create order {OrderId}", order.Id);
    }
}
```

> **Note:** Avoid string interpolation in log calls (`$"Order {id} created"`). Use message templates so providers can serialize structured properties separately rather than just a flat string.

---

*Questions referenced from [devinterview.io](https://devinterview.io). Answers written independently.*
