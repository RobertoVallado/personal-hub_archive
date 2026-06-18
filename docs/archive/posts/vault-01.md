---
date:
  created: 2023-07-31
  updated: 2024-12-12
readtime: 3
pin: true
links:
  - Vault Index: archive/index.md
categories:
  - Vault
tags:
  - Vulnerabilities
authors:
  - robertovallado
slug: avoid-idor-bugs-part-ii
---

# Avoid IDOR bugs PART II

>Developer Responsibility and Security Awareness

As developers, we are responsible for the following:

- Write clean, understandable, and maintainable code.  
- Make code that speaks for itself. *(AKA: no comments)*  
- Name things properly: **variables good, vague names bad.**

But we are only human; despite what many might think, we all make mistakes. Those mistakes show up as issues during an application's usage.  
**The dreaded bugs!**  
We can't avoid introducing them sometimes, but we *can* reduce them with good practices.

<!-- more -->

---

## Security-First Mindset

Let’s try to always think like an attacker.

### Parameterized Queries
When interacting with databases or file systems, use **parameterized queries** and **prepared statements**.  
They help prevent injection vulnerabilities, which can indirectly lead to IDOR and similar issues.

### Context-Based Authorization

Consider the **context** of the user’s actions.  
Validate whether the request matches the user's role or privileges.

- Never rely solely on client-side checks.  
- Always enforce authorization on the server side.  
- Take a minute to think: *“What is this user trying to do?”*  

Let’s make this mindset a habit.

### Test and Security Review
Conduct regular:

- Security assessments  
- Code reviews  
- Peer discussions  

Ask questions, take initiative, and bring security concerns to the table.

### Error Handling

Use helpful but **non-revealing** error messages.  
Attackers love detailed errors; keep them general.

Error codes and structured failures are great for debugging and user experience. Just avoid exposing sensitive info.

---

## Bugs Will Always Exist

Bugs will always be there.  
Our job is to **identify and contain them early** in the application lifecycle.

>Take a moment to consider the task at hand.  
>Stay alert and security-focused. It only takes a few minutes.

**Happy bug-hunting!**

---

## References

- Yaworski, P. (2019). *Real-World Bug Hunting: A Field Guide to Web Hacking*. No Starch Press.  
- Kohnfelder, Loren. (2022). *Designing Secure Software: A Guide for Developers*. No Starch Press.


#