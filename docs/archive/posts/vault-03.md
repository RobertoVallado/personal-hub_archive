---
date:
  created: 2023-08-13
  updated: 2024-12-12
readtime: 5
pin: true
links:
  - Vault Index: archive/index.md
categories:
  - Vault
tags:
  - Vulnerabilities
  - XSS
authors:
  - robertovallado
slug: stored-xss
---

# Stored XSS

**Understanding Stored Cross-Site Scripting (Stored XSS)**

Recapping the previous article into the world of XSS basics—covering DOM-based, stored, and reflected XSS—we’re now ready to zoom in on one particular type:

<!-- more -->

**Stored Cross-Site Scripting**, also known as **Persistent XSS**.

Don’t worry if the name sounds daunting—this article breaks it down into simple, developer-friendly ideas. Think of it as a puzzle: we’ll assemble each piece, explain what it means, and walk through a real-life example to make everything clear.

---

##  Definition

**Stored XSS** is a security flaw that occurs when a web application allows malicious code to be injected and stored on the server.  
When another user loads the affected page, the stored malicious code is executed in their browser.

Because the payload lives on the server, **every user who views the compromised content becomes vulnerable**, making this one of the most dangerous forms of XSS.

Common consequences include:

- Account hijacking  
- Redirection to malicious sites  
- Theft of cookies and session tokens  

---

##  How Stored XSS Works

###  Injection Point**
The attacker identifies a vulnerable input field—one that accepts user input **without proper sanitization**.  
These fields often store user-generated content that will be shown to other users.

*In development practices, this is called **“No Bueno.”***

---

###  Payload Injection**
The attacker crafts a malicious payload—typically JavaScript, since it executes natively in browsers.

Before continuing, imagine the attacker asking:

> “What can I inject here that will cause the most harm when another user loads this page?”

As researchers (...and developers), it is essential that we can answer this question, too.

Common malicious outcomes include:

- Website defacement  
- Session theft  
- Cookie extraction  
- Redirection to malicious sites  

White-hat hackers usually keep it simple and harmless, like the classic:

```
  alert(1)
```
as we will see in our example shortly.

## Content Submission
The attacker submits a crafted payload through the vulnerable input field.

Because the payload undergoes no validation, it gets stored on the server and waits to be executed when retrieved. The stored data is often associated with the user who submitted it.

---

## Content Retrieval
When another user (victim) accesses the page containing the stored malicious content, the server retrieves the payload and serves it alongside legitimate data.

---

## Browser Execution
The browser renders the page—including the malicious payload—as part of its normal process. Browsers cannot distinguish malicious code from legitimate code; their job is simply to execute whatever is received.  
This makes the user vulnerable and can compromise their security.

---

## Impact
The attacker may gain control over the victim’s session, allowing them to impersonate the victim, access their account, and perform actions on their behalf.

---


## Example: Stored XSS Case Study

On **January 25, 2019**, a user named **giddsec** submitted a report, which was later disclosed by HackerOne on **April 1** of the same year.  
The vulnerability was identified on **X (formerly Twitter)** and could potentially lead to **data theft in network reports** of users.

---

### Proof of Concept (PoC)

The attacker located the injection point in:

**Company Information → Edit**
#
![screenshot](../images/image-00.png)
#
From there, the attacker submitted the payload directly into the edit field.
#
![screenshot](../images/image-01.png)
#
Once submitted, the information was **safely saved on the server**, and retrieval resulted in automatic execution when rendered by the browser. That is the core behavior of **Stored XSS**.
#
![screenshot](../images/image-02.png)
#
---

### Takeaway

I hope this example and brief proof of concept help clarify the vulnerability.  
It certainly did for me, as it allowed me to better understand and categorize this type of attack more precisely. Still, there’s plenty more to learn as we continue growing.

- As **users**, we should stay aware and practice safe habits online.  
- As **developers**, we must avoid insecure coding practices that enable Stored XSS.  
- As **hackers**, we continue learning and uncovering flaws that help improve security overall.

---

## References

- Yaworski, P. (2019). *Real-World Bug Hunting: A Field Guide to Web Hacking*. No Starch Press.  
- giddsec. (2019, April 1). *Report 485748: Stored XSS*. HackerOne. https://hackerone.com/reports/485748



#