function displayNotification(body, icon, title, link, duration) {
  link = link || null; // Link is optional
  duration = duration || 5000; // Default duration is 5 seconds

  var options = {
    body: body,
    icon: icon
  };

  var n = new Notification(title, options);

  if (link) {
    n.onclick = function () {
      window.open(link);
    };
  }

  setTimeout(n.close.bind(n), duration);
}
