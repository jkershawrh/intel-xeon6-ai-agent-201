(function () {
  'use strict'

  function terminalFrame () {
    if (!window.parent || window.parent === window) return null
    return Array.from(window.parent.document.querySelectorAll('iframe')).find(function (frame) {
      return frame.title === 'Terminal' || /\/terminal(?:$|[/?#])/.test(frame.src || '')
    }) || null
  }

  function installListener (frame) {
    if (frame.dataset.launchpadExecuteListener === 'true') return

    const script = frame.contentDocument.createElement('script')
    script.textContent = `
      (function () {
        if (window.__launchpadExecuteListener) return;
        window.__launchpadExecuteListener = true;
        window.addEventListener('message', function (event) {
          if (!event.data || event.data.type !== 'execute') return;
          var command = String(event.data.data || '').replace(/[\\r\\n]+$/, '');
          if (window.client && typeof window.client.sendData === 'function') {
            window.client.sendData(command + '\\r');
            return;
          }
          if (window.term && window.term._core && window.term._core._onData) {
            window.term._core._onData.fire(command + '\\r');
          }
        }, false);
      })();`
    frame.contentDocument.body.appendChild(script)
    frame.dataset.launchpadExecuteListener = 'true'
  }

  document.addEventListener('click', function (event) {
    const button = event.target.closest('.paste-button')
    if (!button) return

    const code = button.closest('.listingblock')?.querySelector('code')
    const frame = terminalFrame()
    if (!code || !frame || !frame.contentDocument) return

    event.preventDefault()
    event.stopImmediatePropagation()
    installListener(frame)
    frame.contentWindow.postMessage({ type: 'execute', data: code.innerText + '\r' }, '*')
    button.classList.add('clicked')
    window.setTimeout(function () { button.classList.remove('clicked') }, 500)
  }, true)
})()
