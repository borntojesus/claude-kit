# Workspace architecture

## Modules

Keep the content loader independent from the UI framework:

```text
content files
  -> parser and schema validation
  -> inheritance and visibility resolver
  -> typed presentation model
     -> sidebar
     -> deck viewer
     -> slide kitchen
     -> public exporter
```

The deck viewer receives slides through props. It must not import one hard coded presentation. The sidebar receives the resolved research collection. The exporter consumes the same typed model after visibility filtering.

## Navigation

Recommended routes:

```text
/
/p/<project>
/p/<project>/<presentation>
/p/<project>/<presentation>/deck
/p/<project>/<presentation>/r/<research>
/p/<project>/<presentation>/s/<slide>
```

Use stable filename slugs for shared slide links. Do not use the slide number in the permanent route because ordering may change.

## Visibility

Allow `public` and `internal` on every project, presentation, research document, and slide. A child may be stricter than its parent but cannot be more public. Generate internal and public artifacts independently. Do not build internal routes and delete them afterward.

Scan the final public directory for sentinel strings that exist only in internal fixtures. Fail the build if any marker appears in HTML, JSON, JavaScript, route payloads, or search indexes.

## Deck controls

Support Arrow keys, Page Up, Page Down, Space, Backspace, Home, End, `F` for fullscreen, and `B` or `.` for a black screen. Ignore shortcuts while a user types in an input, textarea, select, content editable element, or textbox role.

Do not loop from the last slide to the first. An accidental extra click from a hardware presenter must not reset the talk.

## Responsive behavior

On desktop, use a collapsible sidebar that becomes an icon rail. On mobile, use an off canvas drawer. Keep breadcrumbs and the current presentation title in a sticky top bar. Preserve navigation state in local storage.

## Public artifact

Fullscreen and public output contain only audience facing slide content. The slide kitchen, internal research, private sources, speaker notes, draft objections, and contact history remain internal.
