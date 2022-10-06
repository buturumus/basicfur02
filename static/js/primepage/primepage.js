// primepage/primapage.js


/* On-site controls */

function activateClickables(cont) {
  $(cont).find('.click-for-tab').click(function() {
    loadTab(click_id);
  });
}

$(document).ready(function() {
  activateClickables(document);
});


