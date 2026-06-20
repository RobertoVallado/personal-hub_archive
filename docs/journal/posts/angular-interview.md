---
date:
  created: 2026-06-19
readtime: 10
pin: true
links:
  - Knowledgebase Index: journal/index.md
categories:
  - Technical Interview Topics
tags:
  - Angular
  - TypeScript
  - Frontend
authors:
  - robertovallado
slug: angular-technical-interview-topics
---

# Angular Technical Interview Topics

Core Angular concepts for technical interviews. Compact read-and-recall short form info.

<!-- more -->

---

## Architecture & Modules

**What it is:** Angular is a full opinionated MVC framework by Google. Applications are organized into `NgModule`s that group related components, services, pipes, and directives.

- Every app has a root `AppModule` bootstrapped at startup; feature modules load eagerly or lazily
- `@NgModule({ declarations, imports, providers, exports, bootstrap })` defines the module boundary
- `declarations`: components/directives/pipes owned by this module
- `imports`: other modules whose exports are needed here
- `exports`: what this module exposes to other modules
- Angular 14+ **standalone components** skip NgModule; dependencies declared directly in `@Component({ imports: [] })`

> **Note:** `providedIn: 'root'` on services is preferred over listing them in `NgModule.providers` because unused services are tree-shaken out of the production bundle.

---

## Data Binding

**What it is:** The mechanism that syncs data between the component class and its template.

| Type | Syntax | Direction |
|------|--------|-----------|
| Interpolation | `{{ value }}` | Class → Template |
| Property binding | `[property]="expr"` | Class → Template |
| Event binding | `(event)="handler()"` | Template → Class |
| Two-way binding | `[(ngModel)]="prop"` | Both |

- Two-way binding is syntactic sugar: `[(x)]` expands to `[x]="val" (xChange)="val=$event"`
- `[(ngModel)]` requires `FormsModule`

> **Note:** `[innerHTML]="html"` sanitizes by default. To bypass, use `DomSanitizer.bypassSecurityTrustHtml()`, but avoid unless absolutely necessary.

---

## Components vs Directives

**What it is:** Both are Angular classes with decorators, but with different purposes.

- **Component:** a directive with a template. Always has `@Component({ selector, templateUrl, styleUrls })`. Owns a view.
- **Attribute directive:** modifies appearance/behavior of an existing element (`ngClass`, `ngStyle`, custom). No template.
- **Structural directive:** changes DOM layout by adding/removing elements (`*ngIf`, `*ngFor`, `*ngSwitch`). The `*` prefix desugars to `<ng-template>`.

> **Note:** A component is a directive, but a directive is not a component. Multiple directives can be applied to one element; only one component can be.

---

## Dependency Injection

**What it is:** Angular's built-in IoC container. Services are registered in an injector and resolved automatically via constructor injection.

- `providedIn: 'root'` → app-wide singleton; tree-shakeable
- `providedIn: SomeModule` → scoped to that module's injector
- `providers: [MyService]` in `@Component` → new instance per component subtree
- Injectors are hierarchical: child injectors walk up to parent until resolved

```typescript
@Injectable({ providedIn: 'root' })
export class AuthService {
  constructor(private http: HttpClient) {}
}
```

> **Note:** Injecting a service with `providers: [MyService]` at the component level breaks the singleton pattern. Useful for intentional instance isolation (e.g., state-per-form).

---

## Lifecycle Hooks

**What it is:** Interface methods Angular calls at specific points in a component/directive's lifetime.

| Hook | When called |
|------|-------------|
| `ngOnChanges` | Input property changes (fires before `ngOnInit`) |
| `ngOnInit` | After first `ngOnChanges`; component fully initialized |
| `ngDoCheck` | Every change detection run |
| `ngAfterContentInit` | After `<ng-content>` projection |
| `ngAfterViewInit` | After component view + children initialized |
| `ngOnDestroy` | Before destruction; unsubscribe, cancel timers |

> **Note:** `ngOnChanges` only fires for `@Input()` property changes. It does not fire for mutations inside an object or array; Angular sees the same reference and skips it.

---

## Services & HttpClient

**What it is:** Services encapsulate reusable logic. `HttpClient` is Angular's HTTP layer, returning Observables.

- Import `HttpClientModule` (or `provideHttpClient()` for standalone)
- `.get<T>()`, `.post<T>()`, `.put<T>()`, `.delete<T>()` all return `Observable<T>`
- Interceptors (`HTTP_INTERCEPTORS`) add headers, handle tokens, and log globally

```typescript
@Injectable({ providedIn: 'root' })
export class UserService {
  constructor(private http: HttpClient) {}
  getUser(id: number) {
    return this.http.get<User>(`/api/users/${id}`).pipe(
      catchError(err => throwError(() => err))
    );
  }
}
```

> **Note:** `HttpClient` returns cold Observables; no request fires until something subscribes. Unsubscribing cancels the in-flight HTTP request.

---

## Routing & Lazy Loading

**What it is:** `RouterModule` maps URL paths to components. Lazy loading defers downloading a feature module until its route is first visited.

- `<router-outlet>` is the placeholder where routed components render
- `routerLink` for declarative navigation; `Router.navigate()` for imperative
- Lazy: `loadChildren: () => import('./feature/feature.module').then(m => m.FeatureModule)`
- Route guards: `CanActivate`, `CanDeactivate`, `CanLoad`, `Resolve`
- `ActivatedRoute.params` and `.queryParams` are Observables

```typescript
const routes: Routes = [
  {
    path: 'admin',
    canActivate: [AuthGuard],
    loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule)
  }
];
```

> **Note:** `CanLoad` prevents the module bundle from downloading at all. `CanActivate` allows the download but blocks rendering. Use `CanLoad` to hide privileged code from unauthorized users.

---

## Template-driven vs Reactive Forms

**What it is:** Angular's two approaches to handling user input and validation.

| | Template-driven | Reactive |
|---|---|---|
| Module | `FormsModule` | `ReactiveFormsModule` |
| Model lives | In the template (`ngModel`) | In the component class (`FormGroup`) |
| Validation | HTML attributes | Validator functions |
| Testing | Async, needs DOM | Synchronous |
| Best for | Simple forms | Complex, dynamic forms |

- Reactive building blocks: `FormGroup`, `FormControl`, `FormArray`
- Built-in validators: `Validators.required`, `Validators.email`, `Validators.minLength`

> **Note:** Reactive forms are synchronous; the model is always available in the component. Template-driven forms rely on directives and are asynchronous, requiring `async`/`fakeAsync` in tests.

---

## Pipes

**What it is:** Functions that transform data in templates, applied with the `|` operator.

- Built-in: `date`, `currency`, `percent`, `uppercase`, `json`, `async`, `slice`, `keyvalue`
- **Pure pipe:** re-runs only when the input reference changes (default). Memoized. Efficient.
- **Impure pipe:** re-runs on every change detection cycle (`pure: false`). Use sparingly.
- `async` pipe: subscribes to an Observable/Promise, unwraps the value, auto-unsubscribes on destroy

```typescript
@Pipe({ name: 'truncate' })
export class TruncatePipe implements PipeTransform {
  transform(value: string, limit = 50): string {
    return value.length > limit ? value.slice(0, limit) + '…' : value;
  }
}
```

> **Note:** The `async` pipe is the preferred way to consume Observables in templates. It avoids manual subscribe/unsubscribe and prevents memory leaks automatically.

---

## Change Detection

**What it is:** Angular's mechanism for keeping the view in sync with component state. Runs top-down across the component tree.

- **Default strategy:** checks the entire tree on every event, timer, or HTTP response (powered by Zone.js)
- **OnPush strategy:** only checks the component when an `@Input()` reference changes, an event fires inside it, or an Observable emits via `async` pipe
- `ChangeDetectorRef.markForCheck()` manually schedules an OnPush component for the next check
- `detach()` / `reattach()` give full manual control

> **Note:** `OnPush` combined with immutable data (replace, never mutate) is the primary Angular performance strategy. Always return new object/array references from state updates.

---

## AOT vs JIT Compilation

**What it is:** Angular compiles HTML templates + TypeScript decorators into JavaScript.

- **JIT (Just-in-Time):** compilation in the browser at runtime. Larger bundle, slower startup. Used in development (`ng serve`).
- **AOT (Ahead-of-Time):** compilation at build time. Smaller bundle, faster startup, catches template errors at build time. Default in production (`ng build`).
- AOT removes the Angular compiler from the production bundle entirely

> **Note:** AOT catches template binding errors (referencing a non-existent method or property) at build time rather than runtime, a significant advantage in CI/CD pipelines.

---

## NgRx & State Management

**What it is:** NgRx is a Redux-inspired reactive state library for Angular, built on RxJS Observables.

- **Store:** single immutable state object
- **Actions:** describe events (`createAction('[Auth] Login', props<{ user: User }>())`)
- **Reducers:** pure functions that produce new state from `(state, action)`
- **Effects:** side effects (HTTP calls) triggered by actions, dispatch new actions on completion
- **Selectors:** memoized projections of store slices

```typescript
loadUser$ = createEffect(() =>
  this.actions$.pipe(
    ofType(UserActions.loadUser),
    switchMap(({ id }) => this.userService.getUser(id).pipe(
      map(user => UserActions.loadUserSuccess({ user })),
      catchError(err => of(UserActions.loadUserFailure({ err })))
    ))
  )
);
```

> **Note:** NgRx adds significant boilerplate. For simpler state, prefer Angular services with `BehaviorSubject` or `signal()`-based stores (Angular 16+).

---

## Performance: trackBy & OnPush

**What it is:** Two practical optimizations to prevent unnecessary DOM recreation and re-rendering.

- `*ngFor` without `trackBy` destroys and recreates all DOM nodes whenever the array reference changes
- `trackBy` returns a unique key per item; Angular reuses existing nodes for unchanged items

```typescript
// template
*ngFor="let item of items; trackBy: trackById"

// component
trackById = (_: number, item: Item) => item.id;
```

- Pair with `ChangeDetectionStrategy.OnPush` on the item component to skip change detection for unchanged items

> **Note:** Combine `trackBy` on the list with `OnPush` on the item component. This avoids both DOM churn and change-detection overhead in large lists.

---

*Questions referenced from [devinterview.io](https://devinterview.io). Answers written independently.*
