---
date:
  created: 2026-06-10
  updated: 2026-06-10
readtime: 14
pin: true
links:
  - Knowledgebase Index: journal/index.md
categories:
  - Technical Interview Topics
tags:
  - C#
  - ASP.NET Core
  - Entity Framework
  - LINQ
  - .NET
authors:
  - robertovallado
slug: technical-interview-qa
---

# Technical Interview Q&A

Questions and answers pulled from devinterview.io across C#, ASP.NET, EF Core, and LINQ; including the locked ones. Short, direct...keeping it simple.

> Questions sourced from [devinterview.io](https://devinterview.io). Answers are my own.

<!-- more -->

---

## C\#

---

### What is the difference between a class and a struct?

**What it is:** Both define custom types, but they have different memory models and behavior.

- `class` is a reference type; stored on the heap; assignment copies the reference
- `struct` is a value type; stored on the stack (or inline in the containing object); assignment copies the entire value
- `class` supports inheritance; `struct` does not (it can implement interfaces)
- `struct` cannot have a default (parameterless) constructor before C# 10; `class` can
- Use `struct` for small, short-lived, immutable data (e.g., `Point`, `Color`); use `class` for everything else

```csharp
struct Point { public int X, Y; }
class Person { public string Name; }

var p1 = new Point { X = 1 };
var p2 = p1;
p2.X = 99;
Console.WriteLine(p1.X); // 1  => struct was copied 
```

> **Note:** The rule of thumb is: if it's larger than 16 bytes, has mutable state, or needs to be passed around polymorphically, make it a class.

---

### What is polymorphism in C#?

**What it is:** Polymorphism lets you call the same method on different types and get different behavior. In C# it comes in two forms.

- **Compile-time (static):** method overloading; same method name, different signatures
- **Runtime (dynamic):** method overriding via `virtual` and `override`, the correct implementation is chosen at runtime based on the actual type of the object

```csharp
public class Animal
{
    public virtual string Speak() => "...";
}
public class Dog : Animal
{
    public override string Speak() => "Woof";
}
public class Cat : Animal
{
    public override string Speak() => "Meow";
}

Animal a = new Dog();
Console.WriteLine(a.Speak()); // "Woof" => runtime dispatch
//  .
 ..^____/
`-. ___ )
  ||  || mh
```

> **Note:** The key word is `virtual`. Without it, the base method is called regardless of the actual type. With `new` instead of `override`, you hide the base method but lose polymorphism.

---

### What is the difference between method overloading and method overriding?

**What it is:** Two different ways to have multiple methods with the same name.

- **Overloading:** same method name, different parameter list, in the same class. Resolved at compile time.
- **Overriding:** same method name and signature, in a derived class. The base method must be `virtual` or `abstract`. Resolved at runtime.

```csharp
// Overloading
int Add(int a, int b) => a + b;
double Add(double a, double b) => a + b;

// Overriding
class Base  { public virtual void Print() => Console.WriteLine("Base"); }
class Child : Base { public override void Print() => Console.WriteLine("Child"); }
```

> **Note:** `new` hides a base method without overriding it. If you call through a `Base` reference, the base version runs. With `override`, the derived version always runs regardless of the reference type.

---

### What is the difference between Task and Thread?

**What it is:** Both represent units of work that can run concurrently, but at very different levels of abstraction.

- `Thread` is an OS-level thread; expensive to create and destroy; you manage its lifecycle manually
- `Task` is a higher-level abstraction from the TPL; runs on the thread pool by default; supports `async`/`await`, continuations, cancellation, and composition (`WhenAll`, `WhenAny`)
- `Task` does NOT necessarily mean a new thread, it can represent any async operation (I/O wait, timer, etc.)
- Creating a new `Thread` for I/O is wasteful; `Task` with `async`/`await` releases the thread while waiting

```csharp
// Thread (low level, rarely needed today)
var thread = new Thread(() => DoWork());
thread.Start();

// Task (preferred)
await Task.Run(() => DoWork());

// Async I/O => no thread blocked at all
var result = await httpClient.GetStringAsync(url);
```

> **Note:** In modern .NET, you almost never need to create a `Thread` directly. Use `Task`, `Task.Run`, or `async`/`await`. Reserve `Thread` for interop with legacy code or when you need specific thread properties.

---

### What is the difference between List and LinkedList?

**What it is:** Two different data structures that both store ordered sequences but have opposite performance trade-offs.

- `List<T>`: backed by an array; index access is O(1); insert/delete at the middle requires shifting elements: O(n); best for read-heavy or append-only scenarios
- `LinkedList<T>`: doubly-linked nodes; insert/delete anywhere is O(1) once you have the node; index access requires traversal: O(n); best when you frequently insert or remove from the middle

```csharp
var list = new List<int> { 1, 2, 3 };
list.Insert(1, 99); // shifts elements => O(n)

var linked = new LinkedList<int>(new[] { 1, 2, 3 });
var node = linked.Find(2);
linked.AddAfter(node, 99); // O(1) => just pointer updates ...da heck!
```

> **Note:** In practice `List<T>` wins almost every time because CPU cache performance on a contiguous array beats the pointer chasing of a linked list, even for many inserts. Reach for `LinkedList<T>` only when profiling confirms the bottleneck.

---

### What is the difference between HashTable and Dictionary?

**What it is:** Both are hash-based key-value stores, but `Dictionary<TKey, TValue>` is the modern replacement for `Hashtable`.

- `Hashtable`: non-generic; keys and values are `object`; thread-safe for one writer + multiple readers; boxing overhead
- `Dictionary<TKey, TValue>`: generic; type-safe; no boxing for value types; NOT thread-safe; use `ConcurrentDictionary` for thread safety
- `Dictionary` is faster in single-threaded scenarios due to no boxing and better JIT optimization

```csharp
// Legacy
Hashtable ht = new Hashtable();
ht["key"] = 42; // boxes the int

// Modern
var dict = new Dictionary<string, int>();
dict["key"] = 42; // no boxing
```

> **Note:** `Hashtable` is essentially obsolete in new code. Use `Dictionary<TKey, TValue>` for single-threaded and `ConcurrentDictionary<TKey, TValue>` for multi-threaded scenarios.

---

## LINQ

---

### What is the difference between First and FirstOrDefault?

**What it is:** Both return the first element that matches a predicate, but they handle an empty result set differently.

- `First()`: throws `InvalidOperationException` if no match is found
- `FirstOrDefault()`: returns `default(T)` (null for reference types, 0 for int, etc.) if no match

```csharp
var numbers = new[] { 1, 2, 3 };

numbers.First(n => n > 10);          // throws InvalidOperationException
numbers.FirstOrDefault(n => n > 10); // returns 0 (default int)

var users = new List<User>();
users.First();          // throws => list is empty
users.FirstOrDefault(); // returns null
```

> **Note:** The same pattern applies to `Single` / `SingleOrDefault` and `Last` / `LastOrDefault`. The `OrDefault` variants are the safe option when empty results are expected. With C# 10+ you can provide a fallback: `FirstOrDefault(predicate, fallbackValue)`.

---

### How do you perform pagination with LINQ?

**What it is:** `Skip` and `Take` together implement offset-based pagination.

- `Skip(n)` skips the first n elements
- `Take(n)` takes the next n
- Always sort first; without `OrderBy`, results are non-deterministic

```csharp
int page = 2;
int pageSize = 10;

var results = dbContext.Products
    .Where(p => p.IsActive)
    .OrderBy(p => p.Name)
    .Skip((page - 1) * pageSize)
    .Take(pageSize)
    .ToList();
```

> **Note:** Offset pagination has a known limitation: it becomes slow on very large datasets (skipping 100,000 rows still scans them). For high-performance scenarios, keyset pagination (WHERE Id > lastSeenId) is more efficient.

---

### What is the role of expression trees in LINQ?

**What it is:** Expression trees let LINQ providers (like EF Core) inspect your C# lambda and translate it to another language (SQL), rather than just running it as compiled code.

- A `Func<T, bool>` is compiled code; it can only be called
- An `Expression<Func<T, bool>>` is a data structure; it can be read, inspected, and translated
- When you call `Where(x => x.Age > 18)` on `IQueryable<T>`, the lambda becomes an expression tree that EF Core converts to `WHERE Age > 18`
- If you use a `Func` on `IQueryable`, it falls back to loading all records into memory first

```csharp
// Expression tree => stays as SQL
Expression<Func<User, bool>> expr = u => u.Age > 18;
context.Users.Where(expr); // → WHERE Age > 18

// Delegate => loads everything into memory
Func<User, bool> func = u => u.Age > 18;
context.Users.Where(func); // → SELECT * (then filters in C#)
```

> **Note:** This is one of the most important conceptual questions in LINQ. The whole power of LINQ providers depends on expression trees. If you can't translate your code, it can't run on the server.

---

### What is IAsyncEnumerable and how does it work with async streams?

**What it is:** `IAsyncEnumerable<T>` (C# 8+) lets you stream data asynchronously, yielding each item as it becomes available without buffering the entire result set.

- Iterate with `await foreach` instead of a normal `foreach`
- Useful for: streaming DB results, paginating API responses, processing large files
- `yield return` works inside `async` methods when the return type is `IAsyncEnumerable<T>`

```csharp
// Producer
public async IAsyncEnumerable<Product> StreamProductsAsync()
{
    await foreach (var batch in FetchBatchesAsync())
        foreach (var item in batch)
            yield return item;
}

// Consumer
await foreach (var product in StreamProductsAsync())
{
    Console.WriteLine(product.Name); // processed one at a time
}
```

> **Note:** Compare with `Task<List<T>>`: that loads everything into memory before returning. `IAsyncEnumerable<T>` processes each item as it arrives, keeping memory usage flat even for millions of rows.

---

## Entity Framework Core

---

### What are navigation properties?

**What it is:** Properties on an entity class that reference related entities, letting you traverse relationships in code instead of writing joins.

- **Reference navigation:** points to a single related entity (`Order.Customer`)
- **Collection navigation:** points to a collection of related entities (`Customer.Orders`)
- EF Core uses them to infer foreign key relationships when building the model
- They drive loading strategies: eager (`Include`), lazy (proxy), and explicit (`Entry().Collection().Load()`)

```csharp
public class Order
{
    public int Id { get; set; }
    public int CustomerId { get; set; }
    public Customer Customer { get; set; }       // reference nav
    public List<OrderItem> Items { get; set; }   // collection nav
}
```

> **Note:** If a navigation property is null when you expect it to be populated, you probably forgot an `Include()`. EF Core does not automatically load navigation properties unless lazy loading proxies are configured.

---

### How does cascade delete work in EF Core?

**What it is:** Cascade delete automatically deletes dependent entities when a principal entity is deleted, rather than leaving orphaned rows.

- **Cascade:** deleting `Customer` also deletes their `Orders` (default for required relationships)
- **SetNull:** FK is set to null when principal is deleted (only works if FK is nullable)
- **Restrict / NoAction:** prevents deletion if dependents exist; throws
- Configure via Fluent API: `.OnDelete(DeleteBehavior.Cascade)`

```csharp
modelBuilder.Entity<Order>()
    .HasOne(o => o.Customer)
    .WithMany(c => c.Orders)
    .OnDelete(DeleteBehavior.Cascade);
```

> **Note:** Be careful with cascade delete in many-to-many or multi-level relationships. EF Core can generate circular cascade paths that SQL Server rejects. In those cases, use `Restrict` and handle cleanup manually.

---

### How do you seed data in EF Core?

**What it is:** Database seeding pre-populates tables with initial or reference data. EF Core provides `HasData()` for code-first seeding via migrations.

- Configured in `OnModelCreating` with `modelBuilder.Entity<T>().HasData(...)`
- Seed data is included in migrations and applied with `Update-Database`
- Keys must be explicit, EF Core needs them to detect changes across migrations
- For environment-specific or large datasets, consider custom seed logic in `Program.cs` using `context.Database.EnsureCreated()` or a seeder service

```csharp
modelBuilder.Entity<Category>().HasData(
    new Category { Id = 1, Name = "Electronics" },
    new Category { Id = 2, Name = "Books" }
);
```

> **Note:** `HasData` seeds are meant for static reference data that rarely changes. Changing seeded values generates a new migration. For dynamic or environment-specific data, use a startup seeder class instead.

---

### How does EF Core handle inheritance? (TPH vs TPT)

**What it is:** When multiple entity types share a base class, EF Core can map the hierarchy to the database in different ways.

- **TPH (Table Per Hierarchy):** all types in one table; a discriminator column identifies the type. Default in EF Core. Efficient queries but nullable columns for subtype-specific properties.
- **TPT (Table Per Type):** each type gets its own table; base columns in the base table, subtype columns in subtype tables. Cleaner schema but JOIN required for every query.
- Configure TPT with `[Table("SubTypeName")]` or `.ToTable("name")` on subtype in `OnModelCreating`

```csharp
// TPH (default)
public abstract class Animal { public int Id; public string Name; }
public class Dog : Animal { public string Breed; }
public class Cat : Animal { public bool IsIndoor; }
// → one Animals table with Discriminator column

// TPT: add [Table("Dogs")] to Dog, [Table("Cats")] to Cat
```

> **Note:** TPH is almost always the better default. TPT looks cleaner in the DB but the JOINs add up quickly. Only switch to TPT if you have a specific schema requirement.

---

## ASP.NET Core

---

### What is ASP.NET Core and how does it differ from classic ASP.NET?

**What it is:** ASP.NET Core is a complete rewrite of ASP.NET. Cross-platform, modular, and built for cloud and microservices from the ground up.

| | ASP.NET (classic) | ASP.NET Core |
|---|---|---|
| Platform | Windows only | Windows, Linux, macOS |
| Hosting | IIS only | Kestrel, IIS, Docker, etc. |
| `System.Web` | Required | Removed |
| DI | Optional/external | Built-in |
| Performance | Slower | Significantly faster |
| Configuration | `web.config` (XML) | JSON, env vars, code |

> **Note:** `System.Web` is the biggest break. Everything that depended on it (WebForms, HttpContext as a global static, etc.) was redesigned. If you're asked about migration, the answer is usually "rewrite, not upgrade."

---

### What is the difference between Web API and MVC in ASP.NET Core?

**What it is:** In ASP.NET Core, the distinction largely collapsed, both use the same controller/routing infrastructure. The difference is in intent and output.

- **MVC:** returns HTML views rendered server-side via Razor
- **Web API:** returns data (JSON/XML) consumed by clients (browser JS, mobile, other services)
- Both inherit from `ControllerBase`; MVC controllers additionally inherit from `Controller` which adds `View()` support
- `[ApiController]` attribute opts a controller into Web API conventions (automatic 400 responses, binding inference, no view lookup)

```csharp
// MVC controller
public class HomeController : Controller         // inherits Controller
{
    public IActionResult Index() => View();       // returns Razor view
}

// API controller
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase // ControllerBase only
{
    public IActionResult Get() => Ok(products);  // returns JSON
}
```

> **Note:** In ASP.NET Core, there's no longer a separate "Web API" project type. The same project can serve both Razor views and JSON endpoints. The `[ApiController]` attribute is what distinguishes API behaviour.

---

### What is OAuth and how is it used in ASP.NET Core?

**What it is:** OAuth 2.0 is an authorization framework that lets users grant a third-party application limited access to their resources without sharing credentials.

- The app redirects the user to an identity provider (Google, GitHub, Microsoft, etc.)
- The provider authenticates the user and issues an authorization code
- The app exchanges the code for an access token
- The access token is used to access protected resources on behalf of the user
- ASP.NET Core supports it via `AddAuthentication().AddGoogle(...)`, `AddGitHub(...)`, etc.

```csharp
builder.Services.AddAuthentication()
    .AddGoogle(options => {
        options.ClientId = config["Auth:Google:ClientId"];
        options.ClientSecret = config["Auth:Google:ClientSecret"];
    });
```

> **Note:** OAuth is for **authorization** (what can the app access?), not authentication (who is the user?). OpenID Connect (OIDC) is the identity layer built on top of OAuth 2.0 that adds the "who are you?" part. In practice, `AddGoogle()` in ASP.NET Core wires up OIDC under the hood.

---

*Questions sourced from [devinterview.io](https://devinterview.io). Answers written independently.*
