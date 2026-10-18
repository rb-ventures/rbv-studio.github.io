// The screenshot viewer for rbv-studio.com. Any element with `data-gallery` turns the links inside it into a gallery:
// a click opens the picture large, with its caption, "3 of 10", previous and next, a strip of thumbnails, the arrow
// keys, swipes, Escape, a tap beside the picture, and the browser's Back button to close. Without JavaScript the
// links still open the pictures. `data-download` on the gallery adds a Download button (the press kit).
(() => {
  const galleries = [...document.querySelectorAll('[data-gallery]')]
  if (!galleries.length || typeof HTMLDialogElement !== 'function') return

  const icon = (d) => `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="${d}" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>`
  const dlg = document.createElement('dialog')
  dlg.className = 'viewer'
  dlg.setAttribute('aria-label', 'Pictures')
  dlg.innerHTML = `
    <div class="viewer-bar">
      <span class="viewer-count" aria-live="polite"></span>
      <span class="viewer-tools">
        <a class="viewer-download" download>${icon('M12 4v11m-5-5 5 5 5-5M5 20h14')}<span>Download</span></a>
        <button class="viewer-close" type="button" aria-label="Close">${icon('M6 6l12 12M18 6 6 18')}</button>
      </span>
    </div>
    <div class="viewer-stage">
      <button class="viewer-prev" type="button" aria-label="Previous picture">${icon('M15 5l-7 7 7 7')}</button>
      <figure class="viewer-figure"><img class="viewer-img" alt=""><figcaption class="viewer-caption"></figcaption></figure>
      <button class="viewer-next" type="button" aria-label="Next picture">${icon('M9 5l7 7-7 7')}</button>
    </div>
    <div class="viewer-strip" role="group" aria-label="All pictures"></div>`
  document.body.append(dlg)

  const $ = (s) => dlg.querySelector(s)
  const img = $('.viewer-img'), caption = $('.viewer-caption'), count = $('.viewer-count')
  const strip = $('.viewer-strip'), download = $('.viewer-download'), stage = $('.viewer-stage')
  let items = [], index = 0, opener = null, ours = false, token = 0, swiped = 0

  const describe = (a) => {
    const thumb = a.querySelector('img')
    const holder = a.closest('li, figure') || a
    const text = a.dataset.caption || holder.querySelector('figcaption, span')?.textContent || thumb?.alt || ''
    return { full: a.href, thumb: thumb?.currentSrc || thumb?.src || a.href, alt: thumb?.alt || text, caption: text.trim(), link: a }
  }

  function show(i) {
    index = (i + items.length) % items.length
    const item = items[index]
    const mine = ++token
    // the thumbnail is in the cache: show it at once, then the full picture when it has arrived
    img.src = item.thumb
    img.alt = item.alt
    dlg.classList.toggle('loading', item.thumb !== item.full)
    if (item.thumb !== item.full) {
      const full = new Image()
      full.onload = () => { if (mine === token) { img.src = item.full; dlg.classList.remove('loading') } }
      full.onerror = () => { if (mine === token) dlg.classList.remove('loading') }
      full.src = item.full
    }
    caption.textContent = item.caption
    count.textContent = `${index + 1} of ${items.length}`
    download.href = item.full
    strip.querySelectorAll('button').forEach((b, n) => {
      const on = n === index
      b.setAttribute('aria-current', on ? 'true' : 'false')
      if (on) b.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' })
    })
    // the neighbours, so the next swipe is instant
    for (const n of [index + 1, index - 1]) new Image().src = items[(n + items.length) % items.length].full
  }

  function open(gallery, i, link) {
    items = [...gallery.querySelectorAll('a[href]')].map(describe)
    opener = link
    dlg.classList.toggle('single', items.length < 2)
    dlg.classList.toggle('portrait', gallery.hasAttribute('data-portrait'))
    download.hidden = !gallery.hasAttribute('data-download')
    strip.replaceChildren(...items.map((item, n) => {
      const b = document.createElement('button')
      b.type = 'button'
      b.setAttribute('aria-label', `Picture ${n + 1}: ${item.caption}`)
      b.innerHTML = `<img src="${item.thumb}" alt="" loading="lazy">`
      b.addEventListener('click', () => show(n))
      return b
    }))
    document.documentElement.classList.add('viewer-open')
    dlg.showModal()
    show(i)
    $('.viewer-close').focus({ preventScroll: true })
    // the browser's Back button closes the viewer instead of leaving the page
    history.pushState({ viewer: Date.now() }, '')
    ours = true
  }

  function close(fromHistory) {
    if (!dlg.open) return
    dlg.close()
    document.documentElement.classList.remove('viewer-open')
    if (!fromHistory && ours) history.back()
    ours = false
    opener?.focus({ preventScroll: true })
  }

  for (const gallery of galleries) {
    gallery.addEventListener('click', (e) => {
      const link = e.target.closest('a[href]')
      if (!link || !gallery.contains(link) || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return
      e.preventDefault()
      open(gallery, [...gallery.querySelectorAll('a[href]')].indexOf(link), link)
    })
  }

  $('.viewer-prev').addEventListener('click', () => show(index - 1))
  $('.viewer-next').addEventListener('click', () => show(index + 1))
  $('.viewer-close').addEventListener('click', () => close(false))
  dlg.addEventListener('cancel', (e) => { e.preventDefault(); close(false) })
  window.addEventListener('popstate', () => close(true))
  dlg.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') { e.preventDefault(); show(index + 1) }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); show(index - 1) }
    else if (e.key === 'Home') { e.preventDefault(); show(0) }
    else if (e.key === 'End') { e.preventDefault(); show(items.length - 1) }
  })
  // a tap beside the picture (on the dark area) closes it
  dlg.addEventListener('click', (e) => { if (Date.now() - swiped > 400 && (e.target === dlg || e.target === stage)) close(false) })

  // swipe left or right for the next picture, down to close
  let start = null
  stage.addEventListener('pointerdown', (e) => { if (e.pointerType !== 'mouse') start = { x: e.clientX, y: e.clientY } })
  stage.addEventListener('pointerup', (e) => {
    if (!start) return
    const dx = e.clientX - start.x, dy = e.clientY - start.y
    start = null
    if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy)) { swiped = Date.now(); show(index + (dx < 0 ? 1 : -1)) }
    else if (dy > 90 && Math.abs(dy) > Math.abs(dx)) { swiped = Date.now(); close(false) }
  })
  stage.addEventListener('pointercancel', () => { start = null })
})()
