---
date:
  created: 2026-06-19
readtime: 8
pin: true
links:
  - Knowledgebase Index: journal/index.md
  - Angular Topics: journal/posts/angular-interview.md
  - React Topics: journal/posts/react-interview.md
categories:
  - Technical Interview Topics
tags:
  - Angular
  - React
  - TypeScript
  - JavaScript
  - Frontend
authors:
  - robertovallado
slug: angular-vs-react
---

# Angular vs React

Key differences for technical interviews. Compact read-and-recall short form info.

<!-- more -->

---

## Framework vs Library

**The core distinction:**

| | Angular | React |
|---|---|---|
| Type | Full framework | UI library |
| Maintained by | Google | Meta |
| Language | TypeScript (required) | JavaScript / TypeScript (optional) |
| Opinion level | High: prescribed patterns for everything | Low: you choose routing, state, HTTP |
| Learning curve | Steeper (more concepts upfront) | Gentler start, grows with ecosystem choices |

- Angular ships with routing, HTTP client, forms, DI, animations, and a CLI out of the box
- React ships with component rendering and hooks; everything else is third-party

> **Note:** "Framework vs library" matters in interviews. Angular dictates *how* you structure the app; React only manages the view layer, leaving architecture to you.

---

## Component Model

**Angular:**
- Components declared via `@Component` decorator with `templateUrl`, `styleUrls`
- Templates are HTML with Angular-specific syntax (`*ngIf`, `[binding]`, `(event)`)
- Strongly typed via TypeScript; template type-checking at compile time with strict mode

**React:**
- Components are JavaScript functions that return JSX
- Logic and markup coexist in the same file; styles are external or CSS-in-JS
- TypeScript is additive; JSX compiles to `React.createElement()`

> **Note:** Angular's template syntax and React's JSX are both compiled; neither is executed as raw HTML. The difference is where logic lives: Angular separates it into `.ts` + `.html`, React keeps it together.

---

## Data Binding

**Angular:**
- One-way property binding: `[value]="expr"`
- One-way event binding: `(click)="handler()"`
- Two-way binding: `[(ngModel)]="prop"` (syntactic sugar for both above)
- Change detection via Zone.js automatically patches async operations (setTimeout, Promise, XHR)

**React:**
- One-way data flow only: data flows down via props, events bubble up via callbacks
- No built-in two-way binding: you wire `value` + `onChange` manually
- No automatic change detection; explicit state updates (`useState` setter, `dispatch`) trigger re-renders

> **Note:** Angular's two-way binding can mask data flow direction in complex forms. React's explicit one-way flow is more predictable at the cost of more wiring.

---

## State Management

**Angular:**
- Local state: component class properties
- Cross-component: Angular services with `BehaviorSubject` (RxJS)
- App-scale: **NgRx** (Redux pattern) or **Akita** / **NgXs**
- Angular 16+: `signal()` for fine-grained reactive state without RxJS

**React:**
- Local state: `useState` / `useReducer`
- Cross-component: **Context API** (low frequency), props, or custom hooks
- App-scale: **Redux Toolkit**, **Zustand**, **Jotai**, **Recoil**
- React 19: experimental `use()` hook and server actions

> **Note:** Angular's RxJS-based state is powerful but requires learning Observables. React's state options are simpler to start and scale by adding libraries only when needed.

---

## Routing

**Angular:**
- `@angular/router` is built-in; zero additional install
- Route config is TypeScript objects: `{ path, component, children, guards }`
- Lazy loading: `loadChildren: () => import(...)`, defers bundle download
- Guards: `CanActivate`, `CanDeactivate`, `Resolve`, `CanLoad`

**React:**
- Routing is third-party; **React Router** (v6+) is the standard
- Route config: `<Routes>` / `<Route>` JSX or `createBrowserRouter()`
- Lazy loading: `React.lazy` + `<Suspense>`
- Guards: no built-in concept, implemented with redirect logic in components or loaders

> **Note:** With React Router v6 + Next.js App Router, React's routing has become significantly more powerful but also more fragmented across different APIs.

---

## Forms

**Angular:**
- **Template-driven:** `ngModel` in HTML, simple but harder to test
- **Reactive:** `FormGroup` / `FormControl` in the component class; synchronous, easily unit-tested
- Built-in validators + custom validator functions
- `FormArray` for dynamic lists of controls

**React:**
- Controlled components: `value` + `onChange` wired manually
- Third-party libraries dominate: **React Hook Form** (performance-first, uncontrolled), **Formik** (controlled)
- Validation: **Zod** / **Yup** schemas integrated via resolver adapters

> **Note:** React Hook Form outperforms Formik on large forms because it avoids re-rendering on every keystroke. Angular Reactive Forms are synchronous and equally testable without a third-party library.

---

## Change Detection vs Reconciliation

**Angular (Change Detection):**
- Zone.js patches async APIs; Angular runs change detection after any async operation
- Default: checks every component top-down; `OnPush`: only checks when inputs change or an event fires inside
- Manual control: `ChangeDetectorRef.markForCheck()`, `detach()`

**React (Reconciliation):**
- Re-renders triggered explicitly by state/prop changes
- Virtual DOM diff determines minimal DOM updates
- Concurrent Mode (React 18): rendering is interruptible; `useTransition` marks low-priority updates

> **Note:** Angular's Zone.js means "it just works" for most async code with no setup. React's explicit model is more predictable but requires careful management of `useEffect` and `useMemo` to avoid performance issues.

---

## TypeScript

**Angular:**
- TypeScript is mandatory; the Angular CLI, decorators, and template type-checking all require it
- Strict template type-checking catches binding errors at compile time
- AOT compilation validates template expressions against the component class

**React:**
- TypeScript is optional but widely used
- JSX types via `@types/react`; props typed with `interface` or `type`
- No compile-time template checking; type errors surface in `.tsx` files but not in JSX expressions like `{someObject.missingProp}`

> **Note:** Angular's stricter TypeScript integration catches more errors at build time. React's flexibility lets teams adopt TypeScript incrementally.

---

## Testing

**Angular:**
- `TestBed`: Angular's testing utility to compile components with their real DI context
- `HttpClientTestingModule` for mocking HTTP; `RouterTestingModule` for routing
- Default test runner: **Jasmine** + **Karma**; increasingly replaced by **Jest** + `jest-preset-angular`

**React:**
- **Jest** + **React Testing Library** (RTL) is the universal standard
- RTL philosophy: test user behavior, not implementation details
- `render()`, `screen.getByRole()`, `userEvent`; no component internals exposed
- Enzyme (legacy) is effectively deprecated

> **Note:** Both ecosystems converge on "test behavior, not internals." Angular's `TestBed` setup is heavier than RTL's `render()` but more representative of the real DI environment.

---

## Performance Comparison

| Concern | Angular | React |
|---|---|---|
| Initial bundle | Larger (framework code) | Smaller (just react + react-dom) |
| Change detection | Zone.js overhead; OnPush mitigates | Explicit; Concurrent Mode prioritizes |
| Large lists | `trackBy` + OnPush | `key` + `React.memo` |
| Code splitting | Lazy-loaded route modules | `React.lazy` + `Suspense` |
| SSR | Angular Universal / Analog | Next.js, Remix, React 18 streaming |

> **Note:** For most production apps, both perform adequately without optimization. The difference matters at scale; Angular OnPush + trackBy and React memo + key are the first optimizations to reach for.

---

## When to Choose Which

**Choose Angular when:**
- Large enterprise team with strict conventions needed
- Full TypeScript enforcement is required
- You want everything bundled: routing, HTTP, forms, DI, CLI, testing
- The team already knows Angular or comes from a Java/.NET background

**Choose React when:**
- Flexibility in library choices matters
- Team is stronger in JavaScript / JSX ecosystem
- Building with Next.js for SSR/SSG
- Smaller team or startup moving fast with less boilerplate

> **Note:** Neither is universally better. The real differentiator is the team's existing knowledge and the project's long-term maintenance model.

---

*Questions referenced from [devinterview.io](https://devinterview.io). Answers written independently.*
