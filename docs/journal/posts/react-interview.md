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
  - React
  - JavaScript
  - Frontend
authors:
  - robertovallado
slug: react-technical-interview-topics
---

# React Technical Interview Topics

Core React concepts for technical interviews. Compact read-and-recall short form info.

<!-- more -->

---

## What is React & the Virtual DOM

**What it is:** React is a UI library (not a framework) by Meta for building component-based user interfaces. It manages DOM updates efficiently through a virtual DOM diffing algorithm.

- **Virtual DOM:** an in-memory representation of the real DOM. On state change, React computes the diff (reconciliation) and applies only the minimum real DOM mutations
- React is un-opinionated about routing, state management, and HTTP; you choose the libraries
- Renders to the browser DOM via `react-dom`, to native views via React Native, or to strings via `renderToString` (SSR)

> **Note:** The virtual DOM is not inherently faster than direct DOM manipulation; it is a predictability/developer-experience trade-off that happens to be fast enough for most UIs.

---

## JSX

**What it is:** A syntax extension that lets you write HTML-like markup inside JavaScript. Babel/SWC compiles it to `React.createElement()` calls.

- JSX is not HTML: use `className` not `class`, `htmlFor` not `for`, camelCase event names (`onClick`)
- Expressions inside `{}`: `{user.name}`, `{isLoggedIn && <Dashboard />}`, `{items.map(...)}`
- A component must return a single root element; wrap siblings in `<>...</>` (Fragment) to avoid extra DOM nodes
- Self-closing tags are required: `<img />`, `<br />`

```tsx
const Greeting = ({ name }: { name: string }) => (
  <p className="greeting">Hello, {name}!</p>
);
```

> **Note:** `React.createElement` is still what runs at runtime. Understanding JSX as syntactic sugar helps debug cryptic Babel/TypeScript errors.

---

## Class vs Functional Components

**What it is:** Two ways to define React components. Functional components with hooks are the modern standard.

| | Class Component | Functional Component |
|---|---|---|
| State | `this.state` / `setState` | `useState` |
| Lifecycle | `componentDidMount`, etc. | `useEffect` |
| Boilerplate | More (extend, `this`) | Less |
| Performance | Slightly heavier | Lighter |
| Hooks | Not supported | Supported |

- Class components still work; no plans to remove them
- `this` binding issues in class components are a common bug source

> **Note:** Prefer functional components for all new code. Hooks give full access to React features with less ceremony and no `this` confusion.

---

## State & Props

**What it is:** The two data mechanisms in React.

- **Props:** data passed from parent to child. Read-only in the receiving component. Changing a prop requires the parent to update its own state.
- **State:** data local to a component. Changing state triggers a re-render of that component and its children.
- State updates are **asynchronous** and batched. Never read state immediately after `setState`/`useState` setter.

```tsx
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

> **Note:** Use the functional updater form `setCount(c => c + 1)` when new state depends on previous state; avoids stale closure bugs in event handlers.

---

## Hooks: useState & useEffect

**What it is:** Functions that let functional components tap into React features (state, lifecycle, context, etc.).

**useState:**
- Returns `[value, setter]`; setter triggers re-render
- State is preserved across renders; initialized only once

**useEffect:**
- Runs side effects after render (data fetching, subscriptions, DOM mutations)
- `useEffect(fn)`: runs after every render
- `useEffect(fn, [dep])`: runs when `dep` changes
- `useEffect(fn, [])`: runs once, mount equivalent
- Return a cleanup function to cancel subscriptions/timers on unmount

```tsx
useEffect(() => {
  const sub = subscribe(id);
  return () => sub.unsubscribe(); // cleanup
}, [id]);
```

> **Note:** Including all values read inside `useEffect` in the dependency array is required by the `exhaustive-deps` ESLint rule. Missing deps cause stale closures.

---

## Rules of Hooks

**What it is:** Constraints React enforces on hook usage to preserve hook call order across renders.

1. **Only call hooks at the top level**: not inside loops, conditions, or nested functions
2. **Only call hooks from React function components or custom hooks**: not from plain JavaScript functions

- React relies on call order to associate state with the correct hook across re-renders
- Violating rule 1 causes state to be assigned to the wrong hook on conditional renders

> **Note:** The `eslint-plugin-react-hooks` package enforces both rules at build time. Enable it; the rules are easy to violate accidentally.

---

## Props Drilling & Context API

**What it is:** Prop drilling passes data through intermediate components that don't need it. Context avoids this by broadcasting values to any descendant.

- `React.createContext(defaultValue)` creates a context
- `<Context.Provider value={...}>` wraps the tree to provide the value
- `useContext(MyContext)` reads the value in any descendant, no intermediate wiring

```tsx
const ThemeContext = createContext<'light' | 'dark'>('light');

function App() {
  return (
    <ThemeContext.Provider value="dark">
      <DeepChild />
    </ThemeContext.Provider>
  );
}

function DeepChild() {
  const theme = useContext(ThemeContext);
  return <div className={theme}>...</div>;
}
```

> **Note:** Context re-renders all consumers when the value changes. For high-frequency updates (e.g., mouse position), context is not ideal; consider Zustand or Jotai instead.

---

## Performance: memo, useMemo, useCallback

**What it is:** Tools to skip unnecessary re-renders and expensive recalculations.

- `React.memo(Component)`: wraps a component; skips re-render if props are shallowly equal
- `useMemo(() => compute(), [deps])`: memoizes an expensive computed value
- `useCallback(() => fn, [deps])`: memoizes a function reference (useful when passing callbacks to memoized children)

```tsx
const ExpensiveList = React.memo(({ items }: { items: Item[] }) => (
  <ul>{items.map(i => <li key={i.id}>{i.name}</li>)}</ul>
));

const handleClick = useCallback(() => doSomething(id), [id]);
```

> **Note:** Don't memoize everything by default; `memo` and `useMemo` have a cost too. Profile first. Only memoize when a measured re-render is actually slow.

---

## Reconciliation

**What it is:** The algorithm React uses to diff the previous and next virtual DOM trees and decide the minimum set of real DOM changes.

- React compares trees top-down, element type first; if the type changes, the subtree is torn down and rebuilt
- For lists, React uses the `key` prop to match old and new items
- Stable, unique keys (not array index) prevent unnecessary unmount/remount of list items

> **Note:** Using array index as `key` causes bugs when items reorder; React matches by position, not identity => stale state in reordered items.

---

## Custom Hooks

**What it is:** Functions that start with `use` and encapsulate reusable stateful logic by composing built-in hooks.

- Extract repeated `useState` + `useEffect` patterns into a custom hook
- Return whatever the consumer needs (values, setters, callbacks)
- Each call to a custom hook has its own independent state

```tsx
function useLocalStorage<T>(key: string, initial: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initial;
  });
  useEffect(() => localStorage.setItem(key, JSON.stringify(value)), [key, value]);
  return [value, setValue] as const;
}
```

> **Note:** Custom hooks are the modern replacement for HOCs and render props. They compose cleanly without adding wrapper nodes to the component tree.

---

## Controlled vs Uncontrolled Components

**What it is:** Two ways to handle form input in React.

- **Controlled:** React state is the single source of truth. `value` and `onChange` are both set. Every keystroke updates state.
- **Uncontrolled:** the DOM manages its own state. Access values via `ref` on demand (e.g., on submit).

```tsx
// Controlled
const [name, setName] = useState('');
<input value={name} onChange={e => setName(e.target.value)} />

// Uncontrolled
const ref = useRef<HTMLInputElement>(null);
<input ref={ref} defaultValue="initial" />
// read: ref.current?.value
```

> **Note:** Controlled components are easier to validate and integrate with form libraries. Uncontrolled is simpler for one-off forms where you only need the value at submit time.

---

## Error Boundaries

**What it is:** Class components that catch JavaScript errors anywhere in their child component tree and display a fallback UI instead of crashing.

- Must be class components; no hook equivalent exists yet
- `static getDerivedStateFromError(error)`: update state to show fallback
- `componentDidCatch(error, info)`: log the error
- Does not catch async errors, event handler errors, or SSR errors

```tsx
class ErrorBoundary extends React.Component<{ children: ReactNode }, { hasError: boolean }> {
  state = { hasError: false };
  static getDerivedStateFromError() { return { hasError: true }; }
  render() {
    return this.state.hasError ? <h1>Something went wrong.</h1> : this.props.children;
  }
}
```

> **Note:** Wrap each major section of the UI in its own error boundary so one broken widget doesn't take down the whole page.

---

## SSR & Suspense / Lazy Loading

**What it is:** Techniques for deferring component loading and rendering on the server.

- **`React.lazy`:** dynamically imports a component; must be wrapped in `<Suspense fallback={...}>`
- **Suspense:** shows a fallback while the lazy component (or data) loads; integrates with SSR in React 18+
- **SSR with React:** `renderToString` / `renderToPipeableStream` renders the initial HTML on the server; client hydrates it
- Next.js is the dominant React SSR framework (App Router uses React Server Components)

```tsx
const Chart = React.lazy(() => import('./Chart'));

<Suspense fallback={<Spinner />}>
  <Chart data={data} />
</Suspense>
```

> **Note:** `React.lazy` only works with default exports. For named exports, re-export as default in a wrapper or use a dynamic import expression that selects the named export.

---

## Testing: Jest & React Testing Library

**What it is:** The standard React testing stack: Jest as the test runner, RTL as the rendering/query layer.

- **RTL philosophy:** test behavior, not implementation. Query by accessible roles, labels, and text, not CSS classes or component internals.
- `render(<Component />)`: renders into a test DOM
- `screen.getByRole`, `screen.getByLabelText`, `screen.getByText`: preferred queries
- `userEvent` simulates real user interactions (type, click, tab)
- `waitFor` / `findBy*` for async assertions

```tsx
test('submits form', async () => {
  render(<LoginForm onSubmit={mockFn} />);
  await userEvent.type(screen.getByLabelText('Email'), 'a@b.com');
  await userEvent.click(screen.getByRole('button', { name: /login/i }));
  expect(mockFn).toHaveBeenCalledWith({ email: 'a@b.com' });
});
```

> **Note:** Avoid `getByTestId` when an accessible query exists; tests that rely on `data-testid` are brittle and don't verify accessibility at all.

---

*Questions referenced from [devinterview.io](https://devinterview.io). Answers written independently.*
