---
name: screenshot-review
description: Review screenshots and UI mockups — analyze design, UX, accessibility, and suggest improvements
triggers:
  - "review screenshot"
  - "review ui"
  - "review design"
  - "check screenshot"
  - "/review-ui"
---

# Screenshot & UI Review

When the user provides a screenshot or image path, analyze it as a senior UI/UX designer.

## Review checklist:

### Visual Design

- Color consistency with brand palette (blue #3949F5, green #64bb6a)
- Typography hierarchy — are headings clear? Is body text readable?
- Whitespace — is there enough breathing room?
- Alignment — are elements on a consistent grid?
- Visual weight — is the eye drawn to the right elements?

### UX

- Is the CTA obvious and above the fold?
- Is the information hierarchy logical?
- Are interactive elements clearly clickable?
- Is the navigation intuitive?
- Does the page have a clear purpose?

### Accessibility

- Color contrast (min 4.5:1 for text)
- Text size (min 16px body)
- Touch targets (min 44px for mobile)
- Focus indicators visible?

### Mobile

- Would this work on 375px width?
- Are touch targets large enough?
- Is text readable without zooming?

### Performance hints

- Are there large images that could be optimized?
- Too many elements above the fold?

## Output:

Rate 1-5 stars for each category. List specific issues with fix suggestions.
Use the project's Tailwind classes in recommendations.
