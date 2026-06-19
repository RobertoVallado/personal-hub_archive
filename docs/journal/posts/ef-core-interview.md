---
date:
  created: 2026-06-10
  updated: 2026-06-10
readtime: 11
pin: true
links:
  - Knowledgebase Index: journal/index.md
categories:
  - Technical Interview Topics
tags:
  - Entity Framework
  - EF Core
  - C#
  - .NET
authors:
  - robertovallado
slug: ef-core-technical-interview-topics
---

# Entity Framework Core Technical Interview Topics

EF Core concepts you need cold for interviews. Covers the full lifecycle from DbContext to performance optimizations.

<!-- more -->

---

## DbContext & DbSet

**What it is:** `DbContext` is the unit of work and the entry point to EF Core. `DbSet<T>` represents a table.

- `DbContext` manages connections, change tracking, and transaction scoping
- Register with `AddDbContext<T>()`; lifetime is **Scoped** by default (one per HTTP request)
- `DbSet<T>` exposes LINQ querying plus `Add`, `Remove`, `Update`, `Find`, `Attach`
- `SaveChanges()` / `SaveChangesAsync()` flushes all tracked changes to the DB in a single transaction

```csharp
public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<Product> Products => Set<Product>();
}
```

> **Note:** `DbContext` is NOT thread-safe. Never share one instance across threads. The scoped lifetime ensures one per request in ASP.NET Core.

---

## Code-First vs Database-First

**What it is:** Two approaches to managing the relationship between your C# model and the database schema.

- **Code-First:** you define C# classes; EF generates migrations and schema from them
- **Database-First:** database exists first; EF scaffolds C# classes from it (`Scaffold-DbContext`)
- Code-First is the modern default; Database-First is useful when integrating with legacy DBs
- Both approaches result in the same EF Core runtime behavior

> **Note:** Code-First doesn't mean the database doesn't exist yet. It means your C# model is the source of truth for schema changes.

---

## Migrations

**What it is:** Version-controlled incremental scripts to evolve your database schema alongside your model.

- `Add-Migration <Name>`: generates `Up()` and `Down()` methods based on model diff
- `Update-Database`: applies pending migrations to the DB
- `Script-Migration`: generates idempotent SQL for production deployments
- `MigrationHistory` table (`__EFMigrationsHistory`) tracks applied migrations
- Migrations can be applied at runtime: `dbContext.Database.MigrateAsync()`

```bash
dotnet ef migrations add AddOrderStatus
dotnet ef database update
dotnet ef migrations script --idempotent -o deploy.sql
```

> **Note:** Never edit a migration that has already been applied to a shared environment. Add a new migration to correct it instead.

---

## Relationships

**What it is:** EF Core maps navigation properties to SQL foreign key relationships.

- **One-to-Many:** `Order` has many `OrderItems`; FK on the "many" side
- **One-to-One:** share PK or unique FK; configure with `HasOne(...).WithOne(...).HasForeignKey<T>(...)`
- **Many-to-Many:** EF Core 5+ creates join table automatically; use explicit join entity for payload columns
- Navigation properties: reference nav (`Order.Customer`) vs collection nav (`Customer.Orders`)

```csharp
// Many-to-many with payload
modelBuilder.Entity<StudentCourse>()
    .HasKey(sc => new { sc.StudentId, sc.CourseId });
```

> **Note:** EF Core 5+ can infer many-to-many from two collection navigations and create the join table automatically. You only need the explicit join entity if you want extra columns on the join table.

---

## Eager / Lazy / Explicit Loading

**What it is:** Three strategies for loading related data (navigation properties).

- **Eager loading:** `Include()` / `ThenInclude()` loads related data in the same SQL query (JOIN)
- **Lazy loading:** navigating a property triggers an automatic query; requires proxies (`UseLazyLoadingProxies()`) or `ILazyLoader`
- **Explicit loading:** manual via `context.Entry(order).Collection(o => o.Items).LoadAsync()`

```csharp
// Eager
var orders = await context.Orders
    .Include(o => o.Customer)
    .ThenInclude(c => c.Address)
    .ToListAsync();
```

> **Note:** Lazy loading in loops causes the N+1 problem: 1 query for orders plus N queries for each order's items. Always prefer eager loading in performance-critical paths.

---

## Tracking vs No-Tracking

**What it is:** EF Core tracks loaded entities by default; no-tracking skips the snapshot and is faster for read-only queries.

- **Tracking** (default): EF snapshots entity state; `SaveChanges` detects and persists changes automatically
- **No-tracking:** `AsNoTracking()` means no snapshot; entities are plain objects; cannot be updated without re-attaching
- `AsNoTrackingWithIdentityResolution()`: no-tracking but de-duplicates related entities (EF Core 5+)

```csharp
var products = await context.Products
    .AsNoTracking()
    .Where(p => p.IsActive)
    .ToListAsync();
```

> **Note:** Use `AsNoTracking()` for any read-only query (list pages, reports, exports). The memory and CPU savings are significant at scale.

---

## Change Tracking

**What it is:** EF Core records the state of every tracked entity so `SaveChanges` knows what SQL to emit.

- States: `Added`, `Modified`, `Deleted`, `Unchanged`, `Detached`
- `context.Entry(entity).State`: inspect or set state manually
- `Update(entity)`: marks all properties as modified (full update), even unchanged ones
- `Attach(entity)` then set a specific property to modified: partial update
- `ChangeTracker.Entries()`: enumerate all tracked entities

```csharp
context.Attach(order);
context.Entry(order).Property(o => o.Status).IsModified = true;
await context.SaveChangesAsync(); // only Status column in UPDATE
```

> **Note:** `Update()` generates `UPDATE ... SET all_columns`. For large tables, `Attach` plus marking specific properties produces a smaller, more targeted SQL statement.

---

## Transactions

**What it is:** Group multiple `SaveChanges` calls (or raw SQL) into one atomic unit that commits or rolls back together.

- Default: each `SaveChanges` call runs in its own implicit transaction
- Explicit: `await context.Database.BeginTransactionAsync()`
- `UseTransaction`: participate in an existing `DbTransaction` (e.g., from Dapper)
- `context.Database.ExecutionStrategy`: retries on transient failures (important for cloud DBs)

```csharp
await using var tx = await context.Database.BeginTransactionAsync();
try {
    context.Orders.Add(order);
    await context.SaveChangesAsync();
    context.Invoices.Add(invoice);
    await context.SaveChangesAsync();
    await tx.CommitAsync();
} catch { await tx.RollbackAsync(); throw; }
```

> **Note:** `SaveChanges` wraps all changes in one transaction automatically. Only use explicit transactions when you need multiple `SaveChanges` calls to be atomic together.

---

## Raw SQL

**What it is:** Execute raw SQL when LINQ can't express the query or performance requires it.

- `FromSqlRaw` / `FromSqlInterpolated`: query entities with raw SQL; result is tracked and composable with LINQ
- `ExecuteSqlRaw` / `ExecuteSqlInterpolated`: non-query (INSERT, UPDATE, DELETE, stored procs)
- Always use parameterized overloads to prevent SQL injection; never string-concatenate user input

```csharp
// Safe - parameterized
var orders = context.Orders.FromSqlInterpolated($"SELECT * FROM Orders WHERE Status = {status}");
await context.Database.ExecuteSqlInterpolatedAsync($"UPDATE Orders SET Status = {status} WHERE Id = {id}");
```

> **Note:** `FromSqlInterpolated` is safe because the interpolated values become SQL parameters. `FromSqlRaw` with string concatenation is NOT safe.

---

## Fluent API vs Data Annotations

**What it is:** Two ways to configure the EF Core model. Data Annotations are attributes on the entity class; Fluent API is configured in `OnModelCreating`.

- **Data Annotations:** simple, co-located with the model; `[Required]`, `[MaxLength(100)]`, `[Key]`, `[ForeignKey]`
- **Fluent API:** more powerful; can configure things annotations can't (composite keys, table splitting, owned entities, shadow properties)
- Fluent API takes precedence over Data Annotations when both are used
- Convention: keep simple constraints as annotations; use Fluent API for anything involving relationships or multi-column config

```csharp
// Data annotation
public class Product
{
    [Key]
    [MaxLength(50)]
    public string Sku { get; set; }
}

// Fluent API equivalent (and more)
modelBuilder.Entity<Product>(e => {
    e.HasKey(p => p.Sku);
    e.Property(p => p.Sku).HasMaxLength(50);
    e.HasIndex(p => p.Name).IsUnique();
});
```

> **Note:** Fluent API is the preferred approach in enterprise projects because it keeps entity classes clean (no EF-specific attributes) and gives you full control over the schema.

---

## Global Query Filters

**What it is:** Automatically applied `WHERE` clause on every query for an entity; great for soft delete or multi-tenancy.

- Configured in `OnModelCreating`: `modelBuilder.Entity<Order>().HasQueryFilter(o => !o.IsDeleted)`
- Applied to every LINQ query against that entity, including `Include`
- Override per-query: `context.Orders.IgnoreQueryFilters()`

```csharp
// In OnModelCreating
modelBuilder.Entity<Post>().HasQueryFilter(p => p.TenantId == _currentTenantId && !p.IsDeleted);
```

> **Note:** Global query filters affect `Include()` too. If you soft-delete a `Customer`, their related `Orders` won't appear in queries unless you call `IgnoreQueryFilters()`.

---

## Optimistic Concurrency

**What it is:** Detect and reject conflicting updates when two users edit the same row simultaneously, without locking.

- **Row version:** `[Timestamp]` / `IsRowVersion()` is a DB-generated binary stamp; EF adds `WHERE RowVersion = @original` to UPDATE
- **Concurrency token:** any property marked `[ConcurrencyCheck]` or `.IsConcurrencyToken()` uses the same WHERE clause logic
- On conflict: `DbUpdateConcurrencyException`; handle by reloading and retrying or showing a conflict UI

```csharp
public byte[] RowVersion { get; set; }
// In OnModelCreating:
modelBuilder.Entity<Order>().Property(o => o.RowVersion).IsRowVersion();
```

> **Note:** Optimistic concurrency assumes conflicts are rare. Pessimistic concurrency (row locks) assumes conflicts are frequent. EF Core only supports optimistic out of the box.

---

## Repository Pattern with EF Core

**What it is:** An abstraction layer over `DbContext` that exposes domain-specific data access methods instead of raw LINQ.

- Wraps EF Core behind an interface (`IOrderRepository`) so business logic doesn't depend on EF directly
- Makes unit testing easier: swap the real repository for an in-memory fake
- **The counter-argument:** `DbContext` and `DbSet<T>` already implement the Repository and Unit of Work patterns. Adding another layer can be redundant overhead
- Generic repository (`IRepository<T>`) is often over-abstracted; prefer specific repositories per aggregate root

```csharp
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(int id);
    Task<List<Order>> GetPendingAsync();
    void Add(Order order);
}

public class EfOrderRepository(AppDbContext ctx) : IOrderRepository
{
    public Task<Order?> GetByIdAsync(int id) => ctx.Orders.FindAsync(id).AsTask();
    public Task<List<Order>> GetPendingAsync() =>
        ctx.Orders.Where(o => o.Status == OrderStatus.Pending).ToListAsync();
    public void Add(Order order) => ctx.Orders.Add(order);
}
```

> **Note:** Know both sides of the debate. Many teams skip the repository layer entirely and inject `DbContext` directly. Be ready to argue for or against it based on project size and test strategy.

---

## Split Queries & N+1 Avoidance

**What it is:** Strategies to load related data efficiently without generating either cartesian product rows or N+1 queries.

- **Cartesian explosion:** a single `Include` on a collection multiplies result rows (1 order × 100 items = 100 rows just for 1 order)
- `AsSplitQuery()`: EF Core 5+ runs separate SQL queries for each `Include` and stitches results in memory
- Default can be changed globally: `optionsBuilder.UseQuerySplittingBehavior(QuerySplittingBehavior.SplitQuery)`
- **N+1:** lazy loading inside a loop; fix with eager loading or explicit batch loading

```csharp
var orders = await context.Orders
    .Include(o => o.Items)
    .AsSplitQuery()  // 2 queries instead of JOIN
    .ToListAsync();
```

> **Note:** Split queries trade bandwidth for round-trips. Use them when JOINs produce huge result sets (wide collections). A single query is better for small includes.

---

*Questions referenced from [devinterview.io](https://devinterview.io). Answers written independently.*
