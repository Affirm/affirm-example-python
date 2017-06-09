document.body.insertBefore(top_nav, document.body.firstChild);

// if (to_show) {
//   var _to_show = to_show.split(",");
//   for (var i = _to_show.length - 1; i >= 0; i--) {
//     toggle(_to_show[i]);
//   };
// }
// Initial states
if (qsParse(initialQs).qo !== undefined){
  if (qsParse(initialQs).qo.show !== undefined && qsParse(initialQs).qo.show.length > 0) {
    var _to_show = qsParse(initialQs).qo.show.split(',');
    for (var i = _to_show.length - 1; i >= 0; i--) {
      toggle(_to_show[i]);
    };
  }
}

document.title = page_name + " - " + envParse(env).name;