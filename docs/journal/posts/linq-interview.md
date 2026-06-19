---
date:
  created: 2026-06-10
  updated: 2026-06-10
readtime: 10
pin: true
links:
  - Knowledgebase Index: journal/index.md
categories:
  - Technical Interview Topics
tags:
  - LINQ
  - C#
  - .NET
authors:
  - robertovallado
slug: linq-technical-interview-topics
---

# LINQ Technical Interview Topics

LINQ interview cards covering deferred execution, operators, IEnumerable vs IQueryable, and expression trees.

<!-- more -->

---

## Deferred vs Immediate Execution

**What it is:** Most LINQ queries are not executed when defined; they execute when iterated. Some operators force immediate execution.

- **Deferred:** `Where`, `Select`, `OrderBy`, `GroupBy`, `SelectMany`, `Take`, `Skip`; they build a query plan and execute on iteration (`foreach` or a terminal operator)
- **Immediate:** `ToList()`, `ToArray()`, `ToDictionary()`, `Count()`, `Sum()`, `First()`, `Any()`; trigger execution and return a concrete value
- Each `foreach` re-executes the deferred query; cache with `ToList()` when reusing the result

```csharp
var query = numbers.Where(n => n > 0); // no execution yet
var list = query.ToList();             // executed here
var count = query.Count();             // executed AGAIN here
```

> **Note:** A deferred query over a live `IEnumerable` can yield different results each time if the source changes between enumerations. This is usually a bug.

---

## `IEnumerable<T>` vs `IQueryable<T>`

**What it is:** The core distinction between LINQ-to-Objects (in-memory) and LINQ-to-SQL/EF (translated to query language).

| | `IEnumerable<T>` | `IQueryable<T>` |
|---|---|---|
| Execution | In-memory (CLR) | Translated to SQL / remote |
| Lambdas | Compiled delegates | Expression trees |
| `Where` call | Filters in C# | Adds SQL `WHERE` clause |
| Use when | In-memory collections | DB queries (EF Core, etc.) |

- Calling `.AsEnumerable()` on an `IQueryable` forces the rest of the chain to run in-memory
- Calling `.AsQueryable()` on a list does NOT make it hit a DB; it's still in-memory

```csharp
// All filtering done in SQL:
var orders = context.Orders.Where(o => o.Total > 100).ToList();

// WHERE runs in SQL, everything after AsEnumerable runs in C#:
var orders = context.Orders.AsEnumerable().Where(o => o.Total > 100).ToList();
```

> **Note:** If you accidentally call `AsEnumerable()` before a `Where`, you load ALL rows into memory and filter them in C#. Always keep filtering on `IQueryable` until you need in-memory operations.

---

## Method Syntax vs Query Syntax

**What it is:** Two equivalent ways to write LINQ; both compile to the same method calls.

```csharp
// Query syntax (SQL-like)
var result = from p in products
             where p.Price > 10
             orderby p.Name
             select p.Name;

// Method syntax (fluent)
var result = products
    .Where(p => p.Price > 10)
    .OrderBy(p => p.Name)
    .Select(p => p.Name);
```

- Query syntax requires `select` or `group` at the end
- Method syntax is more powerful; some operators (`Distinct`, `Take`, `Zip`) have no query syntax equivalent
- Both are identical at runtime

> **Note:** Prefer method syntax. It's more concise, universally used, and covers all operators. Know query syntax exists but don't rely on it.

---

## `Select` / `Where` / `OrderBy`

**What it is:** The three most fundamental LINQ operators.

- `Select`: projection; transforms each element: `Select(x => new { x.Id, x.Name })`
- `Where`: filter; keeps elements matching a predicate: `Where(x => x.Active)`
- `OrderBy` / `OrderByDescending`: sort ascending or descending
- `ThenBy` / `ThenByDescending`: secondary sort (chain after `OrderBy`, NOT another `OrderBy`)

```csharp
var names = users
    .Where(u => u.IsActive)
    .OrderBy(u => u.LastName)
    .ThenBy(u => u.FirstName)
    .Select(u => $"{u.FirstName} {u.LastName}");
```

> **Note:** Calling `.OrderBy().OrderBy()` does NOT sort by two columns. The second `OrderBy` replaces the first. Always use `ThenBy` for multi-column sorts.

---

## `GroupBy`

**What it is:** Groups elements by a key; returns `IEnumerable<IGrouping<TKey, TElement>>`.

- Each `IGrouping<TKey, T>` has a `.Key` and is itself an `IEnumerable<T>`
- `GroupBy` is deferred for `IEnumerable` but may load all data before grouping
- In EF Core, `GroupBy` translates to SQL `GROUP BY` and is usually paired with aggregates

```csharp
var byCategory = products
    .GroupBy(p => p.Category)
    .Select(g => new { Category = g.Key, Count = g.Count(), Avg = g.Average(p => p.Price) });
```

> **Note:** `IGrouping` is NOT a dictionary. To get a dictionary use `ToDictionary(g => g.Key, g => g.ToList())` or `ToLookup`.

---

## `Join` / `GroupJoin`

**What it is:** Combine two sequences by a matching key.

- `Join`: inner join; only elements with a match in both sequences appear
- `GroupJoin`: left outer join; every element from the left appears, with a (possibly empty) collection from the right

```csharp
// Inner join
var result = orders.Join(customers,
    o => o.CustomerId,
    c => c.Id,
    (o, c) => new { o.Id, c.Name });

// Left outer join via GroupJoin + SelectMany
var result = customers.GroupJoin(orders,
    c => c.Id,
    o => o.CustomerId,
    (c, orderGroup) => new { c.Name, Orders = orderGroup });
```

> **Note:** In EF Core, `Join` is rarely needed because navigation properties and `Include` handle joins. `Join` in LINQ-to-Objects is for merging in-memory collections.

---

## `SelectMany`: Flattening

**What it is:** Projects each element to a sequence, then flattens all sequences into one.

- Use when each element has a collection property and you want all items in a single sequence
- Equivalent to a nested `foreach` loop

```csharp
// All tags across all posts, flat list
var allTags = posts.SelectMany(p => p.Tags);

// With result selector, cartesian product style
var pairs = students.SelectMany(
    s => courses,
    (s, c) => new { s.Name, c.Title });
```

> **Note:** If `Select` gives you `IEnumerable<IEnumerable<T>>`, you need `SelectMany` to get `IEnumerable<T>`. It flattens one level.

---

## `Any` / `All` / `Contains`

**What it is:** Existence and membership checks that short-circuit on the first match.

- `Any()`: true if the sequence has at least one element
- `Any(predicate)`: true if any element satisfies the predicate; stops at first match
- `All(predicate)`: true if ALL elements satisfy; stops at first failure
- `Contains(value)`: true if the value exists; uses `EqualityComparer<T>.Default`

```csharp
bool hasAdmins = users.Any(u => u.Role == "Admin");
bool allActive = users.All(u => u.IsActive);
bool exists = ids.Contains(targetId);
```

> **Note:** Prefer `Any()` over `Count() > 0`. `Any()` stops at the first element; `Count()` enumerates everything.

---

## `First` / `FirstOrDefault` / `Single` / `SingleOrDefault`

**What it is:** Operators that return a single element; differ in how they handle zero or multiple matches.

| Operator | Zero matches | Multiple matches |
|----------|-------------|-----------------|
| `First` | `InvalidOperationException` | Returns first |
| `FirstOrDefault` | `default(T)` / null | Returns first |
| `Single` | `InvalidOperationException` | `InvalidOperationException` |
| `SingleOrDefault` | `default(T)` / null | `InvalidOperationException` |

```csharp
var user = users.FirstOrDefault(u => u.Id == id); // null if not found
var admin = users.Single(u => u.Role == "SuperAdmin"); // throws if 0 or 2+
```

> **Note:** Use `Single` when the data model guarantees exactly one match (e.g., by primary key). Use `FirstOrDefault` when zero results is a valid case.

---

## Aggregates: `Count` / `Sum` / `Min` / `Max` / `Average`

**What it is:** Terminal operators that compute a scalar value from the sequence.

- All trigger immediate execution
- Overloads accept a selector: `Sum(x => x.Price)`, `Max(x => x.Score)`
- `Count()` vs `LongCount()` for sequences with more than `int.MaxValue` elements
- On an empty sequence: `Sum` returns 0, `Min`/`Max`/`Average` throw. Use nullable overloads or `DefaultIfEmpty` to handle empty sets

```csharp
decimal total = orders.Sum(o => o.Amount);
int oldest = people.Max(p => p.Age);
double avg = scores.DefaultIfEmpty(0).Average();
```

> **Note:** `Min` and `Max` throw on empty sequences. If the sequence might be empty, use `.DefaultIfEmpty()` or the nullable overloads (`Min?` / `Max?` in C# 10+).

---

## `Distinct` / `Union` / `Intersect` / `Except`

**What it is:** Set operations that remove duplicates or combine sequences like mathematical sets.

- `Distinct()`: unique elements; uses `EqualityComparer<T>.Default`
- `Union(other)`: all unique elements from both sequences
- `Intersect(other)`: only elements present in BOTH
- `Except(other)`: elements in the first that are NOT in the second
- All use value equality; for custom types, provide an `IEqualityComparer<T>`

```csharp
var allIds = sourceA.Union(sourceB);       // merged, no duplicates
var common = listA.Intersect(listB);       // overlap only
var onlyInA = listA.Except(listB);         // A minus B
```

> **Note:** `Union` = OR, `Intersect` = AND, `Except` = NOT IN. The set analogy makes them impossible to mix up.

---

## `Skip` / `Take` : Pagination

**What it is:** Offset-based pagination; skip a number of elements and take the next batch.

- `Skip(n)`: skip first n elements
- `Take(n)`: take next n elements
- `SkipWhile(predicate)` / `TakeWhile(predicate)`: predicate-based versions
- In EF Core, translates to `OFFSET ... FETCH NEXT ... ROWS ONLY` (or equivalent)

```csharp
int page = 2, pageSize = 10;
var paged = query
    .OrderBy(x => x.Id)
    .Skip((page - 1) * pageSize)
    .Take(pageSize)
    .ToList();
```

> **Note:** Always `OrderBy` before `Skip`/`Take`. SQL has no guaranteed row order without an `ORDER BY`. Without it, "page 2" might return the same rows as "page 1."

---

## `Concat` / `Append` / `Prepend`

**What it is:** Operators that combine sequences or add single elements without deduplication (unlike `Union`).

- `Concat(other)`: joins two sequences end-to-end; keeps duplicates; both must be `IEnumerable<T>`
- `Append(element)`: adds a single element to the end; returns a new sequence
- `Prepend(element)`: adds a single element to the front; returns a new sequence
- All three are deferred

```csharp
var combined = listA.Concat(listB);         // all items from both, duplicates included
var withExtra = list.Append(newItem);       // list + newItem at end
var withFirst = list.Prepend(header);       // header + list

// contrast with Union:
var noDupes = listA.Union(listB);           // deduplicates
```

> **Note:** `Concat` does not deduplicate. If you need a merged set with no duplicates, use `Union`. If order and duplicates are intentional, use `Concat`.

---

## `Aggregate()`

**What it is:** The general-purpose fold/reduce operator; all named aggregates (`Sum`, `Average`, etc.) are special cases of `Aggregate`.

- `Aggregate(seed, (accumulator, element) => ...)`: starts from a seed and folds each element into it
- `Aggregate((accumulator, element) => ...)`: no seed; uses the first element as the initial accumulator; throws on empty sequence
- Useful when no named aggregate matches (e.g., building a string, product of all values, custom reduction)

```csharp
// Sum via Aggregate
int sum = new[] { 1, 2, 3, 4 }.Aggregate(0, (acc, x) => acc + x); // 10

// String join manually
string result = words.Aggregate((a, b) => $"{a}, {b}"); // "one, two, three"

// Custom: product of all elements
long product = numbers.Aggregate(1L, (acc, x) => acc * x);
```

> **Note:** Know that `Sum(x => x)` is equivalent to `Aggregate(0, (acc, x) => acc + x)`. Interviewers use `Aggregate` to test whether you understand LINQ beyond the named operators.

---

## Expression Trees

**What it is:** A representation of code as a data structure (tree of nodes) rather than compiled IL; this is what makes `IQueryable` work.

- When you write a lambda for `IQueryable<T>`, it's compiled as an `Expression<Func<T, bool>>`, NOT a `Func<T, bool>`
- EF Core walks the expression tree and translates it to SQL
- `Func<T, bool>`: compiled delegate, executes in C#
- `Expression<Func<T, bool>>`: data structure, can be inspected and translated

```csharp
// Compiled delegate, runs in C#
Func<Order, bool> filter = o => o.Total > 100;

// Expression tree, can be translated to SQL by EF Core
Expression<Func<Order, bool>> expr = o => o.Total > 100;
context.Orders.Where(expr);   // SQL: WHERE Total > 100
context.Orders.Where(filter); // loads all rows, filters in C#
```

> **Note:** Passing a `Func` to `IQueryable.Where` silently switches to in-memory filtering. Always use `Expression<Func<T, bool>>` with `IQueryable` to keep the filter in SQL.

---

*Questions referenced from [devinterview.io](https://devinterview.io). Answers written independently.*
