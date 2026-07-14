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
