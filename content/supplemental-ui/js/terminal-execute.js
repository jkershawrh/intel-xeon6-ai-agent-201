(function () {
  'use strict'

  function terminalFrame () {
    if (!window.parent || window.parent === window) return null
    return Array.from(window.parent.document.querySelectorAll('iframe')).find(function (frame) {
      return frame.title === 'Terminal' || /\/terminal(?:$|[/?#])/.test(frame.src || '')
    }) || null
  }

  document.addEventListener('click', function (event) {
    const button = event.target.closest('.paste-button')
    if (!button) return

    const code = button.closest('.listingblock')?.querySelector('code')
    const frame = terminalFrame()
    if (!code || !frame || !frame.contentDocument) return

    const textarea = frame.contentDocument.querySelector('.xterm-helper-textarea') ||
      frame.contentDocument.querySelector('textarea')
    if (!textarea) return

    const command = code.innerText.replace(/[\r\n]+$/, '')

    event.preventDefault()
    event.stopImmediatePropagation()
    textarea.focus()
    textarea.value = command
    textarea.dispatchEvent(new InputEvent('input', {
      bubbles: true,
      cancelable: true,
      composed: true,
      data: command,
      inputType: 'insertText'
    }))
    textarea.dispatchEvent(new KeyboardEvent('keydown', {
      bubbles: true,
      cancelable: true,
      composed: true,
      key: 'Enter',
      code: 'Enter',
      keyCode: 13,
      which: 13
    }))
    button.classList.add('clicked')
    window.setTimeout(function () { button.classList.remove('clicked') }, 500)
  }, true)
})()
