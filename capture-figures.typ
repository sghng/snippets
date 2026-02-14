// Capture figure/table bodies and replace them with attachment messages.
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

// Usage:
//
// #import "capture-figures": *
// #show capture-figures
//
// Or copy paste the `show` portion to the top of the file.
