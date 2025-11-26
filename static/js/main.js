document.addEventListener("htmx:confirm", function (e) {
  // The event is triggered on every trigger for a request, so we need to check if the element
  // that triggered the request has a confirm question set via the hx-confirm attribute,
  // if not we can return early and let the default behavior happen
  if (!e.detail.question) return

  // This will prevent the request from being issued to later manually issue it
  e.preventDefault()

  Swal.fire({
    title: "Proceed?",
    text: `${e.detail.question}`
  }).then(function (result) {
    if (result.isConfirmed) {
      // If the user confirms, we manually issue the request
      e.detail.issueRequest(true); // true to skip the built-in window.confirm()
    }
  })
})