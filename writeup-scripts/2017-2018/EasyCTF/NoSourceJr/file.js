window.encryptionKey = 'nosource';

function process(a, b) {
  'use strict';
  var len = Math.max(a.length, b.length);
  var out = [];
  for (var i = 0, ca, cb; i < len; i++) {
    ca = a.charCodeAt(i % a.length);
    cb = b.charCodeAt(i % b.length);
    out.push(ca ^ cb);
  }
  return String.fromCharCode.apply(null, out);
}

(function (global) {
  'use strict';
  var formEl = document.getElementById('flag-form');
  var inputEl = document.getElementById('flag');
  var flag = 'Fg4GCRoHCQ4TFh0IBxENAE4qEgwHMBsfDiwJRQImHV8GQAwBDEYvV11BCA==';
  formEl.addEventListener('submit', function (e) {
    e.preventDefault();
    if (btoa(process(inputEl.value, global.encryptionKey)) === flag) {
      alert('Your flag is correct!');
    } else {
      alert('Incorrect, try again.');
    }
  });
})(window);
