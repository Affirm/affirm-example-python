// Declar global vars
var _affirm_config = {
  public_api_key:  "{{config['AFFIRM']['PUBLIC_API_KEY']}}",
  script: "{{ config['AFFIRM']['AFFIRM_JS_URL'] }}",
  api_url: "{{ config['AFFIRM']['API_URL'] }}"
};
var page_name = document.title;
var current_page = document.location.origin + document.location.pathname;
var envs = [
  'prod-sandbox',
  'prod-live',
  'br',
  'special-16',
  'stage-int_1_1',
  'stage-int_1_2',
  'stage-int_1_3',
  'stage-int_1_4',
  'stage-int_2_4',
  'stage-int_2_11',
  'stage-sandbox',
  'stage-live',
  'br',
  'dev-special_1',
  'dev-special_2',
  'localhost'];
var pages = [
  'index',
  'br',
  'checkout',
  'checkout-vcn',
  'br',
  'omnichannel',
  'br',
  'promos',
  'promos-legacy',
  'br',
  'prequal'];

var qsParse = function (a) {
  var _qo = {},
    _qa = [];
  if (a) {
    _qa = a.split('&');
    for (var i = _qa.length - 1; i >= 0; i--) {
      var _s = _qa[i].split('='),
        _k = _s[0],
        _v = _s[1] && decodeURIComponent(_s[1]);
      _qo[_k] = _v;
    }
  }
  return {
    'qa': _qa,
    'qo': _qo,
  };
};

var qoParse = function (a) {
  var _qs = '';
  Object.keys(a).forEach(function (key, i) {
    if (a[key] !== '' && a[key] !== undefined) {
      var val = a[key];
      var _a = val.toString();
      if (i > 0) {
        _qs = _qs + '&' + key + '=' + _a;
      }
      else {
        _qs = _qs + key + '=' + _a;
      }
    }
  });
  return _qs;
};

function qsUpdate(url, val, action) {
  _base = '';
  _qs = '';
  if (url.indexOf('?') > -1) {
    _url = url.split('?');
    _base = _url[0].toString();
    _qs = _url[1].toString();
  }
  else {
    _base = url;
    _qs = '';
  }
  var _orig_qs = qsParse(_qs).qo == undefined ? {} : qsParse(_qs).qo,
    _new_qs = '',
    _k = val[0],
    _v = val[1],
    _k_exists = _orig_qs.hasOwnProperty(_k) && _orig_qs[_k].length > 0 ? true : false,
    _v_exists = _k_exists ? _orig_qs[_k].includes(_v) : false;
  switch (action) {
    case 'add':
      if (!_k_exists) {
        _orig_qs[_k] = _v;
      }
      if (_k_exists && !_v_exists) {
        var _a = _orig_qs[_k].split(',');
        _a.push(_v);
        _c = _a.toString();
        _orig_qs[_k] = _c;
      }
      break;
    case 'remove':
      if (_k_exists && _v_exists) {
        var _a = _orig_qs[_k].split(',');
        var _b = _a.indexOf(_v);
        var _d;
        if (_a.indexOf(_v) == 0 && _a.length == 1) {
          _d = '';
        }
        else {
          _a.splice(_b, 1);
          _d = _a.toString();
        }
        _orig_qs[_k] = _d;
      }
      break;
    case 'replace':
      _orig_qs[_k] = _v;
      break;
  }
  _new_qs = qoParse(_orig_qs);

  return {
    url: _base + '?' + _new_qs,
    base: _base,
    qs: _new_qs,
  };
}

// Helper to decode env values
function envParse(a) {
  var _env_query = '?env=' + a;
  var _env_components = {
    name: a,
    query: _env_query,
  };
  return _env_components;
}

// Query vars
var show = [],
  env = '';
var api_key;

var initialQs = location.search.replace('?', '');

if (qsParse(initialQs).qo !== undefined) {
  if (qsParse(initialQs).qo.env) {
    env = qsParse(initialQs).qo.env;
  }
  if (qsParse(initialQs).qo.api_key) {
    api_key = qsParse(initialQs).qo.api_key;
  }
}

function toggle(a) {
  var b = document.getElementById(a);
  b.classList.toggle('hide');
  var c = b.classList.contains('hide');
  var current_location = document.location.href;
  var _new_href = '';
  var z = '';
  if (c) {
    _new_href = qsUpdate(current_location, ['show', a], 'remove');
    var envLinks = document.getElementsByClassName('env_link');
    var pageLinks = document.getElementsByClassName('page_link');
    for (var i = 0; i < pageLinks.length; i++) {
      _orig_href = pageLinks[i].href;
      _new_lnk = qsUpdate(_orig_href, ['show', a], 'remove');
      pageLinks[i].href = _new_lnk.base + _new_lnk.qs;
    }
    ;
    for (var i = 0; i < envLinks.length; i++) {
      _orig_href = envLinks[i].href;
      _new_lnk = qsUpdate(_orig_href, ['show', a], 'remove');
      envLinks[i].href = _new_lnk.base + _new_lnk.qs;
    }
    ;
  }
  else {
    _new_href = qsUpdate(current_location, ['show', a], 'add');
    var envLinks = document.getElementsByClassName('env_link');
    var pageLinks = document.getElementsByClassName('page_link');
    for (var i = 0; i < pageLinks.length; i++) {
      _orig_link = pageLinks[i].href;
      _new_link = qsUpdate(_orig_link, ['show', a], 'add');
      pageLinks[i].href = _new_link.base + '?' + _new_link.qs;
    }
    for (var i = 0; i < envLinks.length; i++) {
      _orig_link = envLinks[i].href;
      _new_link = qsUpdate(_orig_link, ['show', a], 'add');
      envLinks[i].href = _new_link.base + '?' + _new_link.qs;
    }
  }
  z = _new_href.base + '?' + _new_href.qs;
  window.history.pushState({ path: z }, '', z);
}

// Define env api keys
switch (env) {
  case 'prod-live':
    _affirm_config = {
      script: 'https://cdn1.affirm.com/js/v2/affirm.js',
      api_url: 'https://affirm.com/api/v2',
      public_api_key: 'xxxxxxxxx',
    };
    break;
  case 'prod-sandbox':
    _affirm_config = {
      script: 'https://cdn1-sandbox.affirm.com/js/v2/affirm.js',
      api_url: 'https://sandbox.affirm.com/api/v2',
      public_api_key: 'xxxxxxxxxx',
    };
    break;
  case 'dev-special_1':
    _affirm_config = {
      script: 'https://special-1.affirm-dev.com/js/v2/affirm.js',
      api_url: 'https://special-1.affirm-dev.com/api/v2',
      public_api_key: 'QAZKCCUVPDTP7RE2',
    };
    break;
  case 'dev-special_2':
    _affirm_config = {
      script: 'https://special-2.affirm-dev.com/js/v2/affirm.js',
      api_url: 'https://special-2.affirm-dev.com/api/v2',
      public_api_key: 'QAZKCCUVPDTP7RE2',
    };
    break;
  case 'stage-int_1_1':
    _affirm_config = {
      script: 'https://int-1-1.affirm-stage.com/js/v2/affirm.js',
      api_url: 'https://int-1-1.affirm-stage.com/api/v2',
      public_api_key: 'FND06LW8187URGAA',
    };
    break;
  case 'special-16':
    _affirm_config = {
      script: 'https://special-16.affirm-dev.com/js/v2/affirm.js',
      api_url: 'https://special-16.affirm-dev.com/api/v2',
      public_api_key: '8Q9L5CUK3D9NVFBX',
    };
    break;
  case 'stage-int_1_2':
    _affirm_config = {
      script: 'https://int-1-2.affirm-stage.com/js/v2/affirm.js',
      api_url: 'https://int-1-2.affirm-stage.com/api/v2',
      public_api_key: 'FND06LW8187URGAA',
    };
    break;
  case 'stage-int_1_3':
    _affirm_config = {
      script: 'https://int-1-3.affirm-stage.com/js/v2/affirm.js',
      api_url: 'https://int-1-3.affirm-stage.com/api/v2',
      public_api_key: 'FND06LW8187URGAA',
    };
    break;
  case 'stage-int_1_4':
    _affirm_config = {
      script: 'https://int-1-4.affirm-stage.com/js/v2/affirm.js',
      api_url: 'https://int-1-4.affirm-stage.com/api/v2',
      public_api_key: 'FND06LW8187URGAA',
    };
    break;
  case 'stage-int_2_4':
    _affirm_config = {
      script: 'https://int-2-4.affirm-stage.com/js/v2/affirm.js',
      api_url: 'https://int-2-4.affirm-stage.com/api/v2',
      public_api_key: 'W3HRPZ1233KHHKPI',
    };
    break;
  case 'stage-int_2_11':
    _affirm_config = {
      script: 'https://int-2-11.affirm-stage.com/js/v2/affirm.js',
      api_url: 'https://int-2-11.affirm-stage.com/api/v2',
      public_api_key: '15C52NQVJ7J4HV63',
    };
    break;
  case 'stage-sandbox':
    _affirm_config = {
      script: 'https://cdn1-sandbox.affirm-stage.com/js/v2/affirm.js',
      api_url: 'https://sandbox.affirm-stage.com/api/v2',
      public_api_key: 'C2S4ECO7NTD9T5GO',
    };
    break;
  case 'localhost':
    _affirm_config = {
      script: 'http://localhost:3000/v2/affirm.js',
      api_url: 'http://localhost:3000',
      public_api_key: 'xxxxxxxxxxxxxxxx',
    };
    break;
}

if (api_key) {
  _affirm_config.public_api_key = api_key;
}

// Top nav
var top_nav = document.createElement('div');
top_nav.id = 'top_nav';

// Page title
var page_title = document.createElement('h1');
page_title.innerText = page_name + ' - ' + envParse(env).name;
// page_title.classList.add('column');

// Build the env list
var env_select = document.createElement('div');
env_select.id = 'env_select';
env_select.classList.add('column');

var env_heading = document.createElement('h3');
env_heading.id = 'env_heading';
env_heading.innerText = 'environment';

var env_list = document.createElement('ul');
env_list.id = 'env_list';
env_list.classList.add('hide');
for (var i = 0; i < envs.length; i++) {
  var _env_item;
  if (envs[i] === 'br') {
    _env_item = document.createElement('br');
  }
  else {
    _env_item = document.createElement('li'),
      _env_link = document.createElement('a');
    _env_link.href = current_page + envParse(envs[i]).query;
    _env_link.classList.add('env_link');
    _env_link.innerText = envParse(envs[i]).name;
    _env_item.appendChild(_env_link);
  }
  env_list.appendChild(_env_item);
}

// Build the index
var page_select = document.createElement('div');
page_select.id = 'page_select';
page_select.classList.add('column');

var page_heading = document.createElement('h3');
page_heading.id = 'page_heading';
page_heading.innerText = 'page';

var page_list = document.createElement('ul');
page_list.id = 'page_list';
page_list.classList.add('hide');
for (var i = 0; i < pages.length; i++) {
  var _page_item;
  if (pages[i] === 'br') {
    _page_item = document.createElement('br');
  }
  else {
    _page_item = document.createElement('li'),
      _page_link = document.createElement('a');
    _page_link.classList.add('page_link');
    _page_link.href = './' + pages[i] + '.html?env=' + env;
    _page_link.innerText = pages[i].charAt(0).toUpperCase() + pages[i].slice(1);
    _page_item.appendChild(_page_link);
  }
  page_list.appendChild(_page_item);
}
;

// build the API input
var api_key_select = document.createElement('div');
var api_key_heading = document.createElement('h3');
var api_key_form = document.createElement('form');
var api_key_entry = document.createElement('input');
var api_key_submit = document.createElement('input');
var merchant_config = document.createElement('div');

api_key_select.id = 'api_key_select';
api_key_select.classList.add('column');
api_key_heading.id = 'api_key_heading';
api_key_heading.innerText = 'api key';
api_key_form.id = 'api_key_form';
api_key_form.classList.add('hide');
api_key_entry.id = 'api_key_entry';
api_key_submit.id = 'api_key_submit';
api_key_submit.type = 'button';
api_key_submit.value = 'Update API key';
merchant_config.id = 'merchant_config';
merchant_config.innerHTML = ' You\'re pointed to ' + _affirm_config.api_url + ' with public API key ' + _affirm_config.public_api_key;

api_key_select.appendChild(api_key_heading);
api_key_select.appendChild(api_key_form);
api_key_form.appendChild(api_key_entry);
api_key_form.appendChild(api_key_submit);
env_select.appendChild(env_heading);
env_select.appendChild(env_list);
page_select.appendChild(page_heading);
page_select.appendChild(page_list);
top_nav.appendChild(page_title);
top_nav.appendChild(env_select);
top_nav.appendChild(page_select);
top_nav.appendChild(api_key_select);
top_nav.appendChild(merchant_config);

env_heading.addEventListener('click', function () { toggle('env_list'); });
page_heading.addEventListener('click', function () { toggle('page_list'); });
api_key_heading.addEventListener('click', function () { toggle('api_key_form'); });
api_key_submit.addEventListener('click', function () {
  var api_key = document.getElementById('api_key_entry').value;
  location.href = qsUpdate(document.location.href, ['api_key', api_key], 'replace').url;
});
window.affirm_config = $.extend({}, _affirm_config);