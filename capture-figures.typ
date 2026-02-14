Capture figure/table bodies and replace them with attachment messages.

#let capture-figures(body) = {
  show figure: it => {
    block(breakable: false)[
      #it.caption
      #align(center)[
        Please see attachment
        #it.supplement
        #it.counter.display(it.numbering),
        page #it.counter.get().first(). // one figure per page
      ]
    ]
  }
  body
}

Usage:

#import "capture-figures": *
#show capture-figures

Or copy paste the `show` portion to the top of the file.

To add figures to the end, use this epilogue:

#pagebreak()
#context counter(page).update(1)
#context query(figure).join([#linebreak()])

There are quite some extra work if you want it to be truly automated:

#context metadata(here().page()) <figures-start>

Query that with `typst query --one --field value '<figures-start>'`, and use
the value with `typst compile --pages`.

