# Budget rules and exceptions

## Why count variants

A small rule set makes relationships easier to perceive and makes the system
easier to maintain. The count is useful because gratuitous variants often hide
weak hierarchy or template-driven design.

## What counts as a layout grammar

Count a layout grammar when content organization changes, not merely when the
number of columns changes responsively.

Examples:

- chronological rows;
- card grid;
- editorial list;
- masonry gallery;
- bento mosaic;
- full-screen slides.

A responsive one-column version of the same project index is not a new grammar.

## Type roles

Count semantic roles, not every font-size token. Typical roles:

- display or page title;
- section heading;
- body;
- metadata or caption;
- code or data;
- control label.

More roles may be justified in a complex application, but near-identical roles
should be merged.

## Color

An accent color is a non-neutral color used for emphasis or identity. Status,
data-series, and validation colors should be inventoried separately because
they carry meaning.

Never reduce a color system by making states indistinguishable.

## Surfaces, radii, and shadows

A surface style is a recurring combination of background, border, elevation,
and treatment. Count functionally equivalent cards as one even when their
content differs.

Merge tiny token differences that have no observable purpose.

## Nested radius coherence

Radius-token count and radius relationships answer different questions. A
system can use one token everywhere and still create awkward nested contours.

Classify each nested rounded pair before judging it:

- `shared-contour`: the child surface visually follows the parent's corner;
- `independent`: the child is a separate control or component whose shape does
  not continue the parent contour;
- `pill-or-circle`: the shape communicates a pill, avatar, dot, or other
  intentionally circular form.

For a shared contour, prefer the next smaller semantic radius token on the
inner surface. Do not import another design system's pixel values as universal
defaults; use the project's declared token order.

When the two curves are intended to be parallel and computed pixel values are
available, check:

```text
expected inner radius = max(0, outer radius - inset)
```

Here `inset` is the measured distance between the compared outer and inner
contours, including relevant padding, gap, and border effects. Use a documented
tolerance for subpixel or rendering differences; the bundled checker defaults
to 1 CSS pixel. Use this concentric-offset rule only for contours intended to
track each other, not for every nested component.

Flag directly observed or measured shared contours when:

- the inner and outer surfaces repeat the same rounded token;
- the inner radius is greater than or equal to a rounded outer radius;
- the declared semantic step is not one level inward;
- a concentric pair exceeds its declared tolerance.

Treat screenshot-only uncertainty as observed or inferred rather than measured.
An unknown nesting scope, inferred mismatch, or documented exception requires
review. Radius awkwardness is not proof of AI authorship and is not a release
hard failure unless it also clips focus, content, targets, or another required
accessibility signal.

## CTA styles

Count visual treatments, not labels. A primary CTA can have many text labels
while remaining one style.

Do not make every link a button. Use native link affordances for navigation.

## Motion patterns

Count distinct motion behaviors such as:

- state fade;
- directional panel transition;
- scale feedback;
- shared-element movement;
- parallax;
- scroll reveal.

Different durations of the same state transition are not necessarily separate
patterns, but inconsistent durations should still be normalized.

## Decorative image families

A family is a repeated visual motif that does not itself provide product,
project, process, person, place, or data evidence.

Examples:

- glowing spheres;
- abstract 3D ribbons;
- generic futuristic dashboards;
- unrelated gradient landscapes.

Authentic project images are not decorative families merely because they are
visually expressive.

## Legitimate exceptions

Possible exceptions include:

- a publication with distinct editorial sections;
- multilingual type requirements;
- a data visualization with categorical color;
- a complex application with many necessary states;
- an established brand system;
- an expressive portfolio where the visual work is the content.

The exception must explain what information or identity would be lost.
