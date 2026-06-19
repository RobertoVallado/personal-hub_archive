---
date:
  created: 2025-12-23
  updated: 2026-06-10
readtime: 12
pin: true
links:
  - Knowledgebase Index: journal/index.md
categories:
  - Technical Interview Topics
tags:
  - C#
  - .NET
authors:
  - robertovallado
slug: csharp-technical-interview-topics
---

# C# Technical Interview Topics

Core C# concepts you need to know cold for a technical interview. Each entry is a compact read-and-recall card.

<!-- more -->

---

## Value Types vs Reference Types

**What it is:** Value types store data directly on the stack; reference types store a pointer on the stack that points to data on the heap.

- **Value types:** `int`, `float`, `bool`, `char`, `struct`, `enum`; copied on assignment
- **Reference types:** `class`, `string`, `array`, `delegate`; the reference is copied, not the object
- `struct` is a value type; avoid large structs because copying is expensive
- `string` is a reference type but behaves like a value type (immutable and interned)

```csharp
int a = 5; int b = a; b = 10; // a is still 5
var p1 = new Point(1, 1); var p2 = p1; p2.X = 99; // p1.X unchanged if Point is a struct
```

> **Note:** Know that `struct` copies on assignment and cannot inherit from another class (only interfaces).

---

## `ref` / `out` / `in` Parameters

**What it is:** Keywords that control how arguments are passed by reference instead of by value.

- `ref`: caller must initialize; callee can read and write
- `out`: caller does NOT need to initialize; callee MUST write before returning
- `in`: read-only reference; callee cannot modify; avoids copying large structs

```csharp
void Swap(ref int a, ref int b) { int t = a; a = b; b = t; }
bool TryParse(string s, out int result) { /* must set result */ }
void Process(in BigStruct s) { /* s is readonly */ }
```

> **Note:** `out` is the pattern behind `TryParse`. Interviewers love asking why `out` instead of a return value.

---

## Generics & Constraints

**What it is:** Generics allow type-safe, reusable code without boxing. Constraints restrict what types `T` can be.

- `where T : class`: reference type only
- `where T : struct`: value type only
- `where T : new()`: must have a parameterless constructor
- `where T : IComparable<T>`: must implement that interface
- Multiple constraints: `where T : class, IDisposable, new()`

```csharp
T Max<T>(T a, T b) where T : IComparable<T>
    => a.CompareTo(b) >= 0 ? a : b;
```

> **Note:** Generics avoid boxing (unlike `ArrayList`). A `List<int>` stores ints directly; an `ArrayList` boxes each int to `object`.

---

## Delegates, `Func` / `Action`, Events

**What it is:** A delegate is a type-safe function pointer. `Func` and `Action` are built-in generic delegate types.

- `Action<T>`: void return, up to 16 params
- `Func<T, TResult>`: non-void return, last type param is return type
- `Predicate<T>`: shorthand for `Func<T, bool>`
- **Event**: a multicast delegate with restricted access (`+=` and `-=` only from outside the class)

```csharp
Func<int, int, int> add = (a, b) => a + b;
Action<string> log = msg => Console.WriteLine(msg);
event EventHandler<MyArgs> DataReceived;
```

> **Note:** Events prevent external callers from invoking or clearing the delegate. They can only subscribe and unsubscribe.

---

## `async` / `await` and Task

**What it is:** `async`/`await` is compiler sugar over `Task`-based continuations that keeps code readable without blocking threads.

- `async` marks a method; `await` suspends it until a `Task` completes. The thread is released, not blocked
- Return `Task` (void-equivalent), `Task<T>` (value), or `ValueTask<T>` (low-alloc)
- `ConfigureAwait(false)`: do not capture the synchronization context; use this in library code
- Avoid `async void`; exceptions are unobservable and only acceptable for event handlers

```csharp
public async Task<string> FetchAsync(string url)
{
    var response = await _httpClient.GetAsync(url).ConfigureAwait(false);
    return await response.Content.ReadAsStringAsync().ConfigureAwait(false);
}
```

> **Note:** `await` does NOT create a new thread. It registers a continuation and returns the current thread to the pool while waiting.

---

## Interface vs Abstract Class

**What it is:** Both define contracts, but differ in inheritance, state, and intent.

| | Interface | Abstract Class |
|---|---|---|
| Multiple inheritance | Yes | No (single) |
| State (fields) | No | Yes |
| Constructor | No | Yes |
| Default implementation | Yes (C# 8+) | Yes |
| Use when | Capability contract | Shared base implementation |

> **Note:** Prefer interfaces for cross-cutting capabilities (`ILogger`, `IDisposable`). Use abstract classes when subclasses need to share concrete code.

---

## IDisposable / `using` / Finalizers

**What it is:** Pattern for deterministic release of unmanaged resources (file handles, DB connections, sockets).

- Implement `IDisposable.Dispose()` to release resources
- `using (var r = new Resource())` calls `Dispose()` on exit, even on exception
- `using var r = new Resource();`: C# 8+ scoped form, disposed at end of enclosing scope
- Finalizer (`~ClassName()`) is a fallback called by GC. Non-deterministic, avoid if possible
- Standard pattern: `Dispose(bool disposing)` separates managed vs unmanaged cleanup

```csharp
using var conn = new SqlConnection(connString);
await conn.OpenAsync();
// conn.Dispose() called automatically
```

> **Note:** The GC only collects managed memory. Unmanaged resources MUST be released via `Dispose` or a finalizer.

---

## Garbage Collection (Gen 0 / 1 / 2, LOH)

**What it is:** The .NET GC automatically reclaims managed heap memory using a generational model.

- **Gen 0:** short-lived objects (most allocations); collected most frequently
- **Gen 1:** survived one Gen 0 collection; buffer between 0 and 2
- **Gen 2:** long-lived objects; collected least frequently (full GC)
- **LOH** (Large Object Heap): objects >= 85 KB; collected with Gen 2; not compacted by default
- `GC.Collect()` exists but avoid calling it manually

> **Note:** The GC is generational because most objects die young. Minimizing long-lived allocations reduces Gen 2 (expensive) collections.

---

## Nullable Types & Null Operators

**What it is:** `T?` makes a value type nullable; null operators provide safe null handling without explicit checks.

- `int?` is `Nullable<int>` and has `.HasValue` and `.Value`
- `??`: null-coalescing; `a ?? b` returns `b` if `a` is null
- `?.`: null-conditional; `obj?.Property` returns null instead of throwing
- `??=`: null-coalescing assignment; `list ??= new List<int>()`
- Enable nullable reference types in project: `<Nullable>enable</Nullable>`

```csharp
string? name = GetName();
int len = name?.Length ?? 0;
cache ??= new Dictionary<string, string>();
```

> **Note:** With nullable reference types enabled, `string` and `string?` are distinct and the compiler warns on potential null dereferences.

---

## Extension Methods

**What it is:** Static methods you can call as if they were instance methods on any type, including types you don't own.

- Defined in a static class, first parameter is `this T value`
- LINQ is entirely built on extension methods (`IEnumerable<T>`)
- Resolution: instance methods take precedence; extension methods are a fallback

```csharp
public static class StringExtensions
{
    public static bool IsNullOrEmpty(this string? s) => string.IsNullOrEmpty(s);
}
"hello".IsNullOrEmpty(); // false
```

> **Note:** Extension methods don't modify the original type. They're syntactic sugar for a static call.

---

## Records vs Classes

**What it is:** Records (C# 9+) are reference types with value-based equality, immutability, and built-in `with` expression support.

- `record Person(string Name, int Age)`: positional record; properties are `init`-only
- `==` compares by value (all properties), not reference
- `with` creates a copy with changed properties: `p with { Age = 31 }`
- `record struct` (C# 10) has the same semantics as record but is a value type

```csharp
record Point(double X, double Y);
var p1 = new Point(1, 2);
var p2 = p1 with { Y = 5 };
Console.WriteLine(p1 == p2); // false
```

> **Note:** Use `record` for immutable DTOs or value objects. Use `class` when you need mutable state or complex inheritance.

---

## Pattern Matching

**What it is:** Concise syntax to test a value's shape, type, or properties without explicit casts.

- `is` type pattern: `if (obj is string s)` casts and binds in one step
- `switch` expression (C# 8): returns a value based on patterns
- Property pattern: `obj is { Name: "Alice", Age: > 18 }`
- Tuple pattern: `(x, y) switch { (0, 0) => "origin", _ => "other" }`
- Relational pattern: `n is > 0 and < 100`

```csharp
string Describe(object obj) => obj switch
{
    int n when n < 0 => "negative",
    int n            => $"positive int {n}",
    string s         => $"string of length {s.Length}",
    null             => "null",
    _                => "other"
};
```

> **Note:** `switch` expressions are exhaustive. If no arm matches and there's no `_`, a `MatchFailedException` is thrown at runtime.

---

## SOLID Principles

**What it is:** Five design principles for maintainable OO code.

- **S**: Single Responsibility; a class has one reason to change
- **O**: Open/Closed; open for extension, closed for modification (use interfaces/inheritance)
- **L**: Liskov Substitution; subtypes must be substitutable for their base type without breaking behavior
- **I**: Interface Segregation; prefer many small interfaces over one large one
- **D**: Dependency Inversion; depend on abstractions, not concretions (inject `IRepository`, not `SqlRepository`)

> **Note:** Be ready to give a one-sentence example of each. LSP is the tricky one; a `Square` inheriting from `Rectangle` violates it.

---

## Boxing and Unboxing

**What it is:** Boxing converts a value type to `object` (or an interface it implements), allocating it on the heap. Unboxing extracts it back.

- Boxing is implicit; unboxing requires an explicit cast
- Each boxing operation allocates a new object on the heap, adding GC pressure
- Generics (`List<int>`) avoid boxing entirely; `ArrayList` boxes every element
- Common hidden boxing: calling an interface method on a struct that isn't stored as the interface type

```csharp
int x = 42;
object boxed = x;       // boxing: heap allocation
int y = (int)boxed;     // unboxing: explicit cast required
```

> **Note:** In tight loops or high-frequency paths, boxing adds measurable GC pressure. The fix is almost always generics.

---

## `const` vs `readonly`

**What it is:** Two ways to define a value that should not change, with different timing and flexibility.

- `const`: compile-time constant; value is inlined at every use site; must be a literal or another `const`; implicitly `static`
- `readonly`: runtime constant; set once in declaration or constructor; can hold reference types and complex values
- `static readonly`: the closest equivalent to `const` for non-literal values (e.g., `new DateTime(...)`)

```csharp
const double Pi = 3.14159;       // inlined at compile time
readonly DateTime StartTime;     // set in constructor, never again
```

> **Note:** Prefer `static readonly` over `public const` for shared values that might ever change. A `const` change requires every referencing assembly to be recompiled because the value is baked in at the call site.

---

*Questions referenced from [devinterview.io](https://devinterview.io). Answers written independently.*
